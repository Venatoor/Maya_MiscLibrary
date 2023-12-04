# This is a small tool that generates color ids for pieces in maya for their usage in id maps in Substance Painter
import maya.cmds as mc
import random


storedUsedRGBs = []


def ColorAssignement(objects = []):

    objectsLength = len(objects)

    for object in objects:
        r = random.random()
        g = random.random()
        b = random.random()

        rgb = (r,g,b)
        if rgb not in storedUsedRGBs:
            if (hasShadingEngine(object)):
                shadingEngine = GetShadingEngine(object)
                if shadingEngine:
                    shader = mc.shadingNode("lambert", asShader=True)
                    mc.setAttr(shader + ".color", r, g, b, type="double3")
                    mc.select(object)
                    mc.hyperShade(assign=shader)

                    storedUsedRGBs.append(rgb)

        else:
            ColorAssignement(objects)




def hasShadingEngine(obj = ""):

    shape_node = mc.listRelatives(obj, shapes=True)
    if shape_node:
        shading_engines = mc.listConnections(shape_node[0], type='shadingEngine')
        if shading_engines:
            return True
    return False

def GetShadingEngine(obj = ""):

    shape_node = mc.listRelatives(obj, shapes = True)
    if shape_node:
        shading_engines = mc.listConnections(shape_node[0], type = "shadingEngine")
        return shading_engines[0]
