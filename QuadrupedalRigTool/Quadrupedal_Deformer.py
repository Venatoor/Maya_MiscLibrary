import maya.cmds as mc

import os

from Utils import algorithms
from . import Project

from SkinSaverTool import bSkinSaver


skinDirWeights =  "weights"
swExt = ".swt"

scale = 2

def build(baseRig , creatureName):

    modelGrp = "model"


    geoList = _getModelGeoList(modelGrp)
    #_applyDeltaMush(geoList)
    loadSkinWeights(creatureName, geoList)

def _applyDeltaMush( geo ):
    deltaMushDf = mc.deltaMush(geo, smoothingIterations=50)[0]

def _getModelGeoList( model ):
    geoList = [ mc.listRelatives( i, p = 1)[0] for i in mc.listRelatives(model, ad = 1, type = "mesh")]
    return geoList

def saveSkinWeights(creatureName, geoList=None):

    for obj in geoList:

        wtFile = os.path.join(Project.mainProjectPath, creatureName, skinDirWeights, obj + swExt)
        print(wtFile)

        mc.select(obj)

        bSkinSaver.bSaveSkinValues(wtFile)
        print("success ?")

def loadSkinWeights(creatureName, geoList=None):

    if geoList is None:
        geoList = []
    wtDir = os.path.join(Project.mainProjectPath, creatureName, skinDirWeights)
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