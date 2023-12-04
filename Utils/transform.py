import maya.cmds as mc
from . import algorithms

# Various functions that concern the transform nodes

def freezeTransformWithSelection( translate = True, rotation = True, scale = True, jointOrient =True) :

        selections  = mc.ls(sl = 1)
        for selectedObject in selections :
            mc.makeIdentity( t = translate,s = scale, r = rotation, jo = jointOrient)

def freezeTransform( node = "" ,translate = True, rotation = True, scale = True, jointOrient = True):

    mc.makeIdentity( node,t = translate, r = rotation, s = scale, jo = jointOrient)

def matchTransform( sourceObject, targetObject ) :


    sourceTranslation = mc.getAttr(sourceObject + ".translate")[0]
    sourceRotation = mc.getAttr(sourceObject + ".rotate")[0]
    sourceShear = mc.getAttr(sourceObject + ".shear")[0]

    mc.setAttr(targetObject + ".translate", sourceTranslation[0], sourceTranslation[1], sourceTranslation[2],
               type="double3")
    mc.setAttr(targetObject + ".rotate", sourceRotation[0], sourceRotation[1], sourceRotation[2], type="double3")
    mc.setAttr(targetObject + ".shear", sourceShear[0], sourceShear[1], sourceShear[2], type="double3")

def matchTransformSelection():

    nodes = mc.ls(sl = 1)
    targetNode = nodes[-1]
    nodesToMatch = nodes[0:len(nodes)]

    ##need to define general purpose matchTransform


def deleteHistorySelection() :
    pass
def makeOffsetGroup() :
    pass

def centerPivot():
    pass


def linkParentOffset( sourceNode, targetNode):

    pass




def setVisibility(node, visibility = True ):

    mc.setAttr( node + ".visibility", 1)



# IN CONTROLS TRY TO MERGE THESE FUNCTIONS TOGETHER
#

