from RigLibrary.base import control
from RigLibrary.base import module

from . import Bipedal_Deformer
from . import Project

from RigLibrary.rigs import spine
from RigLibrary.rigs import bipedalLimb
from RigLibrary.rigs import IKFKneck
from RigLibrary.rigs import clavicle
from RigLibrary.rigs import head

import maya.cmds as mc


sceneScale = Project.sceneScale
projectPath = Project.mainProjectPath

rootJoint = "root"

builderFilePath = r"%s\%s\builder\%s_builder.mb"
modelFilePath =  r"%s\%s\model\%s_model.mb"


def build(characterName, projectPath = projectPath, sceneScale = sceneScale):

        """
        this is the main function to build the rig
        """

        #  Importing Builder file first

        mc.file( new = True, f = True)

        builderFile = builderFilePath % ( projectPath, characterName, characterName)

        print(builderFilePath)
        print(builderFile)

        mc.file( builderFile, i=1 )

        # Creating the base rig for the bipedal

        baseRig = module.Base( characterName = characterName, scale = sceneScale )

        # Importing the model file

        modelFile = modelFilePath % ( projectPath, characterName, characterName)

        mc.file( modelFile, i=1 )

        # Parenting the root joint to Joints Grp in Base

        mc.parent( rootJoint, baseRig.jointsGroup )

        # Parenting the model to Model Grp in Base

        modelGrp = "model"
        mc.parent( modelGrp , baseRig.modelGrp )

        # TEMP : we don't delete it for now
        #mc.delete("builder")

        # Humanoid Deform creation

        Bipedal_Deformer.build(baseRig = baseRig, characterName = characterName)

        #control & modules setup

        makeControlSetup(baseRig)


def makeControlSetup( baseRig):

        #CREATING THE BIPEDAL'S JOINTS
        spineJoints = ["pelvis","spine1","spine2","spine3","neck"]
        spineCurve = "spine_IKCurve"


        spineRig = spine

        spine.build( spineJoints= spineJoints,
                                spineCurve= spineCurve,
                                spineRootJoint= rootJoint,
                                prefix= "spine",
                                spineScale= sceneScale,
                                baseRig = baseRig,
                                hipsLocator = "hips_Locator"
                                )

        #CREATING THE LEFT ARM LIMB
        leftArmJoints= ["upperarm_l", "lowerarm_l", "hand_l"]
        leftArmRootLocator = "armRoot_l_Locator"

        leftArmRig = bipedalLimb
        leftArmRig.build(rootJoint = rootJoint,
                                       limbJoints= leftArmJoints,
                                       prefix = "leftArm",
                                       baseRig= baseRig,
                                       mainCtrlLocator = leftArmRootLocator,
                                       scale= sceneScale,
                                       isRight= False,
                                       ikPVlocator= "PV_LeftArm_Locator",
                                       isLeg= False)


        #CREATING THE RIGHT ARM LIMB
        rightArmJoints = ["upperarm_r", "lowerarm_r", "hand_r"]
        rightArmRootLocator = "armRoot_r_Locator"

        rightArmRig = bipedalLimb
        rightArmRig.build(rootJoint=rootJoint,
                                       limbJoints=rightArmJoints,
                                       prefix="rightArm",
                                       baseRig=baseRig,
                                       mainCtrlLocator=rightArmRootLocator,
                                       scale=sceneScale,
                                       isRight= True,
                                       ikPVlocator= "PV_RightArm_Locator",
                                       isLeg= False)



        #CREATING THE LEFT LEG LIMB
        leftLegJoints= ["hips_l","leg_l","foot_l"]
        leftLegRootLocator = "legRoot_l_Locator"


        leftLegRig = bipedalLimb.build(rootJoint=rootJoint,
                                        limbJoints=leftLegJoints,
                                        prefix="leftLeg",
                                        baseRig=baseRig,
                                        mainCtrlLocator=leftLegRootLocator,
                                        scale=sceneScale,
                                        isRight= False,
                                        ikPVlocator= "PV_LeftFoot_Locator",
                                        isLeg = True)



        #CREATING THE RIGHT LEG LIMB
        rightLegJoints = ["hips_r", "leg_r", "foot_r"]
        rightLegRootLocator = "legRoot_r_Locator"

        rightLegRig = bipedalLimb.build(rootJoint=rootJoint,
                                       limbJoints=rightLegJoints,
                                       prefix="rightLeg",
                                       baseRig=baseRig,
                                       mainCtrlLocator=rightLegRootLocator,
                                       scale=sceneScale,
                                       isRight= True,
                                       ikPVlocator= "PV_RightFoot_Locator",
                                       isLeg= True)



        
        #CREATING THE NECK

        neckJoint = ["neck"]

        neckRig = IKFKneck
        IKFKneck.build(neckJoint = neckJoint, rootJoint= rootJoint, prefix= "neck", baseRig= baseRig,
                                 scale= sceneScale, spineModule= spineRig)


        #CREATING THE HEAD

        headJoint = ["head"]
        headRig = head.build(prefix= "head", rootJoint = rootJoint, headJoint = headJoint, baseRig= baseRig,
                             scale= sceneScale, neckModule= neckRig, worldSpaceLocator= "worldspace_locator")
        #CREATING THE EYES
        #CREATING THE FOOT
        #CREATING THE LEFT CLAVICLE

        leftClavicle = "clavicle_l"

        clavicle.build(prefix= leftClavicle, rootJoint= rootJoint, scale = sceneScale, baseRig= baseRig,
                       spineModule= spineRig, armModule= leftArmRig, aimLocator= "clavicle_locator_l",
                       clavicleJoint= leftClavicle)
        #CREATING THE RIGHT CLAVICLE

        rightClavicle = "clavicle_r"

        clavicle.build(prefix=rightClavicle, rootJoint=rootJoint, scale=sceneScale, baseRig=baseRig,
                       spineModule=spineRig, armModule=rightArmRig, aimLocator="clavicle_locator_r",
                       clavicleJoint= rightClavicle)




        #CREATING THE FINGERS




