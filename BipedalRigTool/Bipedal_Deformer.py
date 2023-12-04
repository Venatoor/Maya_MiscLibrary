import maya.cmds as mc

import os

from Utils import algorithms
from . import Project

from SkinSaverTool import bSkinSaver


skinDirWeights =  "weights"
swExt = ".swt"

scale = 2



def build( baseRig, characterName) :

    modelGrp = "model"

    geoList = _getModelGeoList(modelGrp)
    loadSkinWeights(characterName, geoList )

    _applyDeltaMush(geoList)

    JointsToDuplicate = ["upperarm_l","upperarm_r","hand_r","hand_l","foot_l","foot_r"]
    JointsToConstraint = ["upperarm_l","upperarm_r","lowerarm_l","lowerarm_r", "hips_r", "leg_r", "hips_l", "leg_l"]

    buildTwistJoints(baseRig , JointsToConstraint = JointsToConstraint, JointsToDuplicate = JointsToDuplicate )


# these are private functions

def _applyDeltaMush( geo ):

    deltaMushDf = mc.deltaMush( geo, smoothingIterations = 50)[0]

def _getModelGeoList( model ):

    geoList = [ mc.listRelatives( i, p = 1)[0] for i in mc.listRelatives(model, ad = 1, type = "mesh")]
    return geoList

# Private functions end

def saveSkinWeights(characterName, geoList = []):

    for obj in geoList:

        wtFile = os.path.join(Project.mainProjectPath, characterName, skinDirWeights, obj + swExt)
        print(wtFile)

        mc.select(obj)

        bSkinSaver.bSaveSkinValues(wtFile)
        print("success ?")

def loadSkinWeights(characterName, geoList=None):

    if geoList is None:
        geoList = []
    wtDir = os.path.join(Project.mainProjectPath, characterName, skinDirWeights)
    wtFiles = os.listdir(wtDir)

    for  file in wtFiles:

        extRes = os.path.splitext(file)

        if not extRes[1] == swExt:
            continue

        if geoList and not extRes[0] in geoList:
            continue

        if not mc.objExists(extRes[0]):
            continue

        fullPathWtDir = os.path.join(wtDir, file)
        print(fullPathWtDir)
        bSkinSaver.bLoadSkinValues(inputFile= fullPathWtDir, loadOnSelection = False)







def buildTwistJoints( baseRig, JointsToConstraint, JointsToDuplicate ):

    # For joints to duplicate :

    twistGroup = mc.group( name = "twist_joint_grp", p = baseRig.jointsGroup ,em = 1)

    for joint in JointsToDuplicate:
        prefix = algorithms.RemoveSuffix(joint)
        jointName = prefix[:-1]

        jointChild = mc.duplicate( joint, n = jointName + "Twist0_Jnt", parentOnly = True)[0]

        origJntScale = mc.getAttr(jointChild + ".radius")
        mc.setAttr(jointChild +".radius", origJntScale * 3)
        mc.parent(jointChild, joint)




    # Duplicating joints

    # Parenting children to jointsToDuplicate

    # For Joints to Constraint :

    for parentJoint in JointsToConstraint:
        prefix = algorithms.RemoveSuffix(parentJoint)
        jointName = prefix[:]

        jointChild = mc.listRelatives( parentJoint, c = 1, type = "joint" )[0]

        twistJoint = mc.duplicate( parentJoint , n = jointName + "Twist1_Jnt", parentOnly = True)[0]
        ##if mc.objExists(twistJoint):
        ##       for i in mc.listRelatives(twistJoint, children = True, type = "transform"):
        ##            mc.delete(i)

        #Adjust the twist joint radius

        origJntScale = mc.getAttr(twistJoint + ".radius")
        mc.setAttr(twistJoint + ".radius", origJntScale * 3)

        mc.delete(mc.pointConstraint(parentJoint, jointChild, twistJoint))

        mc.parent(twistJoint, parentJoint)

        ##mc.parentConstraint(twistJoint, parentJoint)





