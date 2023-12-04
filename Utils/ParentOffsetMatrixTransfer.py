import maya.cmds as mc
import maya.api.OpenMaya as om


def parentOffsetTransferWithSelection():
    for node in mc.ls(sl=1):
        parentOffsetTransfer(node)


# To be used in other py files / classes
def parentOffsetTransfer(node):
    ##if mc.nodeType(node) != ["transform", "joint"]:
    ##    raise ValueError('The Node is not a transform node ')

    localMatrix = om.MMatrix(mc.xform(node , q = True, m = True, ws = False))
    parentMatrix = om.MMatrix(mc.getAttr( node + ".offsetParentMatrix"))

    finalMatrix = localMatrix * parentMatrix

    mc.setAttr(node + '.offsetParentMatrix', finalMatrix, type = "matrix")
    resetTransform(node)


def resetTransform(node):
    for attribute in ["translate", "rotate", "scale", "shear"]:
        if attribute == "scale":
            defaultValue = 1
        else:
            defaultValue = 0
        for axis in ["X", "Y", "Z"]:
            if mc.attributeQuery(attribute + axis, node = node,ex=True):
                attributeName = "{}.{}{}".format(node, attribute, axis)
                if not mc.getAttr(attributeName, lock=True):
                    mc.setAttr(attributeName, defaultValue)
