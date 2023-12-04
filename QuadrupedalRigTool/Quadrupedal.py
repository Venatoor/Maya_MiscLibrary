from RigLibrary.base import control
from RigLibrary.base import module

from . import Quadrupedal_Deformer
from . import Project


from RigLibrary.rigs import tail
from RigLibrary.rigs import SplineSpine
from RigLibrary.rigs import quadrupedalBackLimb

import maya.cmds as mc


sceneScale = Project.sceneScale
projectPath = Project.mainProjectPath

rootJoint = "root"

builderFilePath = r"%s\%s\builder\%s_builder.mb"
modelFilePath =  r"%s\%s\model\%s_model.mb"


def build( creatureName, projectPath = projectPath, sceneScale = sceneScale):
    """
            this is the main function to build the rig
            """

    #  Importing Builder file first

    mc.file(new=True, f=True)

    builderFile = builderFilePath % (projectPath, creatureName, creatureName)

    print(builderFilePath)
    print(builderFile)

    mc.file(builderFile, i=1)

    # Creating the base rig for the bipedal

    baseRig = module.Base(characterName=creatureName, scale=sceneScale)

    # Importing the model file

    modelFile = modelFilePath % (projectPath, creatureName, creatureName)

    mc.file(modelFile, i=1)

    # Parenting the root joint to Joints Grp in Base

    mc.parent(rootJoint, baseRig.jointsGroup)

    # Parenting the model to Model Grp in Base

    modelGrp = "model"
    mc.parent(modelGrp, baseRig.modelGrp)

    # TEMP : we don't delete it for now
    # mc.delete("builder")

    # Humanoid Deform creation

    Quadrupedal_Deformer.build(baseRig=baseRig, creatureName=creatureName)

    # control & modules setup

    makeControlSetup(baseRig)

def makeControlSetup(baseRig):

    #CREATING LEFT REAR LEG

    leftRearLegJoints = ["l_femur","l_fibula","l_metatarsus","l_rear_metacarpus","l_paw"]

    leftRearLeg = quadrupedalBackLimb.build(prefix="leftRearLeg",baseRig = baseRig, scale= sceneScale,
                                                 rootJoint= rootJoint, limbJoints= leftRearLegJoints, isRight= False)

    #CREATING RIGHT REAR LEG

    rightRearLegJoints = ["r_femur", "r_fibula", "r_metatarsus", "r_rear_metacarpus", "r_paw"]

    rightRearLeg = quadrupedalBackLimb.build(prefix="rightRearLeg", baseRig=baseRig, scale=sceneScale,
                                                 rootJoint=rootJoint, limbJoints=rightRearLegJoints, isRight= True)

    #CREATING LEFT FRONT LEG

    leftFrontLegJoints = ["l_humerus","l_radius","l_carpus","l_metacarpus","l_frontpaw"]

    leftFrontLeg = quadrupedalBackLimb.build(prefix="leftFrontLeg", baseRig=baseRig, scale=sceneScale,
                                                 rootJoint=rootJoint, limbJoints=leftFrontLegJoints, isRight= False)

    #CREATING RIGHT FRONT LEG

    rightFrontLegJoints = ["r_humerus", "r_radius", "r_carpus", "r_metacarpus", "r_frontpaw"]

    rightFrontLeg = quadrupedalBackLimb.build(prefix="rightFrontLeg", baseRig=baseRig, scale=sceneScale,
                                             rootJoint=rootJoint, limbJoints=rightFrontLegJoints, isRight= True)

    #CREATING TAIL

    tailJoints = ["tail1","tail2","tail3","tail4","tail5","tail6","tail7"]
    tailCurve = "tail_curve"

    ikTail = tail.build(chainJoints= tailJoints, chainCurve= tailCurve, prefix= "tail", scale= sceneScale,
                        fkParenting= True, baseRig = baseRig)

    #CREATING NECK

    neckJoints = ["neck_base","neck_mid"]
    neckCurve = "neck_curve"

    ikNeck = tail.build(chainJoints = neckJoints, chainCurve = neckCurve, prefix = "neck", scale =sceneScale,
                        fkParenting= True, baseRig= baseRig)

    #CREATING SPINE

    spineJoints= ["spine2","spine3","spine4","spine5"]
    spineCurve = "spine_curve"

    ikSpine = SplineSpine.build(spineJoints = spineJoints, rootJoint= rootJoint, prefix= "spine", rigScale= sceneScale, baseRig= baseRig,
                                spineCurve= spineCurve)


