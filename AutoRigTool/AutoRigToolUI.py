from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

from AutoRigTool import AutoRigToolLogic

import maya.cmds as mc
import maya.OpenMayaUI as omui
import os

from BipedalRigTool import Bipedal
from QuadrupedalRigTool import Quadrupedal


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class AutoRigDialog(QtWidgets.QDialog):

    def __init__(self, parent = maya_main_window()):
        super(AutoRigDialog, self).__init__(parent)

        self.setWindowTitle("Auto Rig Tool")
        self.setMinimumWidth(369)
        self.setMinimumHeight(447)

        self.autoRig = AutoRigToolLogic.AutoRigLogic()

        self.init_ui()
        self.create_layout()
        self.create_connections()

        self.path = ""
        self.rigType = "Bipedal"
        self.sceneScale = ""
        self.ctrlsSize = ""

        self.pattern = ""
        self.names = []

        self.chainPath = ""



    def init_ui(self):
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load("D:\Animations\Qt\AutoRigTool.ui", parentWidget=None)


    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.ui)

    def create_connections(self):
        self.ui.RigTypeCB.activated.connect(self.on_rig_type_selected)
        #self.ui.ChainRigTypeCB.activated.connect(self.on_chain_rig_selected)
        self.ui.specificNamePB.clicked.connect(self.add_name)
        self.ui.rigPB.clicked.connect(self.on_single_rig)
        self.ui.chainRigPB.clicked.connect(self.on_chain_rig_selected)

    def on_rig_type_selected(self, index):
        self.rigType = self.ui.RigTypeCB.currentText()

    def add_name(self):

        if len(str(self.ui.specificNameLE.text())) == 0:
            print( "Please enter a name ! ")
            return
        self.names.append(self.ui.specificNameLE.text())
        print(str(self.ui.specificNameLE.text()))

        #TODO
        # showing name in selection list

    def remove_name(self):
        pass

    def on_chain_rig_selected(self, index):

        if self.ui.tabWidget.currentIndex() == 0:
            pass
        elif self.ui.tabWidget.currentIndex() == 1:
            # verify path
            if int(self.ui.sceneScaleLE.text()) == 0:
                print("Please enter a scene Scale Value")
                return
            self.sceneScale = int(self.ui.sceneScaleLE.text())
            if int(self.ui.ctrlsSizeLE.text()) == 0:
                print("Please enter a ctrls Size Value")
                return
            self.ctrlsSize = int(self.ui.ctrlsSizeLE.text())
            if os.path.exists(self.ui.PathLE.text()) and len(self.names) != 0 :
                for name in self.names:
                    characterName = name
                    fullPath = os.path.join(self.ui.PathLE.text(), characterName)
                    print(fullPath)
                    builder_path = os.path.join(fullPath, 'builder')
                    if os.path.exists(builder_path) and os.path.isdir(builder_path):
                        model_path = os.path.join(fullPath, 'model')
                        if os.path.exists(model_path) and os.path.isdir(model_path):
                            # Verifying existence of model and file obj
                            model_file = characterName + "_model"
                            builder_file = characterName + "_builder"
                            full_model_path = os.path.join(model_path, model_file)
                            full_builder_path = os.path.join(builder_path, builder_file)

                            if self.rigType == "Bipedal":
                                Bipedal.build(characterName=characterName, projectPath=self.ui.PathLE.text(),
                                          sceneScale=self.sceneScale)


                            elif self.rigType == "Quadrupedal":
                                Quadrupedal.build(creatureName=characterName, projectPath=self.ui.PathLE.text(),
                                              sceneScale=self.sceneScale)


                            # Check if the scene is already saved; if not, perform a "Save As" operation
                            conservationFile = os.path.join(fullPath, characterName + "ConservationFile.ma")
                            mc.file(rename=conservationFile)  # Set the file name to the specified file path
                            mc.file(save=True, type='mayaAscii')
                            print(f"File saved to {fullPath}")

    def on_single_rig(self):

        if  int(self.ui.sceneScaleLE.text()) == 0 :
            print("Please enter a scene Scale Value")
            return
        self.sceneScale = int(self.ui.sceneScaleLE.text())
        if int(self.ui.ctrlsSizeLE.text()) == 0:
            print("Please enter a ctrls Size Value")
            return
        self.ctrlsSize = int(self.ui.ctrlsSizeLE.text())
        if os.path.exists(self.ui.PathLE.text()) and self.ui.characterLE.text() != 0:
            characterName = self.ui.characterLE.text()
            fullPath = os.path.join(self.ui.PathLE.text(), characterName)
            builder_path = os.path.join(fullPath, 'builder')
            if os.path.exists(builder_path) and os.path.isdir(builder_path):
                model_path = os.path.join(fullPath, 'model')
                if os.path.exists(model_path) and os.path.isdir(model_path):
                    #Verifying existence of model and file obj
                    model_file = characterName + "_model"
                    builder_file = characterName +"_builder"
                    full_model_path = os.path.join(model_path, model_file)
                    full_builder_path = os.path.join(builder_path, builder_file)

                    print(self.rigType)
                    if self.rigType == "Bipedal":
                        Bipedal.build(characterName= characterName, projectPath= self.ui.PathLE.text(), sceneScale= self.sceneScale)

                    elif self.rigType == "Quadrupedal":
                        Quadrupedal.build(creatureName = characterName, projectPath= self.ui.PathLE.text(), sceneScale= self.sceneScale)
            else:
                print("Builder and Model infound or invalid")
        else:
            print("Path or character invalid")



    #Multiple Chain Rig Code Below

    #Initialize project
    def On_Initialize_Project(self):
        pass




if __name__ == "__main__":

    autoRigUI = AutoRigDialog()
    autoRigUI.show()
