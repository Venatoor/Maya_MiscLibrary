import maya.cmds as mc

# general algorithms not linked to maya in particular but CS and DSA notions

def RemoveSuffix( name ) :

    edits = name.split("_")
    if len(edits) < 2 :
        return name

    suffix = "_" + edits[-1]
    nameWithoutSuffix = name[:-len(suffix)]

    return nameWithoutSuffix

def equidistantSpacing( width, lines) :

    return width / lines


def CollisionDetection(object1, object2):

    bb1 = mc.xform(object1, query = True, boundingBox = True, worldSpace= True)
    bb2 = mc.xform(object2 , query= True, boundingBox = True, worldSpace = True)

    if bb1[3] > bb2[0] and bb1[0] < bb2[3] and bb1[4] > bb2[1] and bb1[1] < bb2[4] and bb1[5] > bb2[2] and bb1[2] < bb2[5]:
        return 1
    else:
        return 0
