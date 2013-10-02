# ------------------------------------------------------------------------------
# PBRT exporter - python  plugin for Maya by Vladimir (Volodymyr) Kazantsev
# 2013
#
#
# This file is licensed under the GPL (the original exporter uses that license)
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# pbrtAreaLightMaterial. The node is just a holder of data with an empty compute method.
#
# ------------------------------------------------------------------------------

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from PBRTNode import PBRTNode
 
 
class pbrtAreaLightMaterial(OpenMayaMPx.MPxNode,PBRTNode):
    """
    Assign this material to any poly object in maya, to turn the object into an area light
    """
    
    @staticmethod
    def nodeName():
        return "pbrtAreaLightMaterial"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757803) #borrowing lux id area

    @staticmethod
    def nodeType():
        return  OpenMayaMPx.MPxNode.kDependNode
        #return  OpenMayaMPx.MPxNode.kHwShaderNode

    @staticmethod
    def nodeClassify():
        return "shader/surface"

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)


    @classmethod
    def nodeCreator(cls):
        return OpenMayaMPx.asMPxPtr(cls())
  
    def compute(self, plug, block):
        if plug == self.outColor or plug.parent() == self.outColor:
            # THIS IS A VERY SIMPLE FLAT COLOUR SHADER.
            # I CAN'T GET THE LAMBERTIAN BIT TO WORK
            
            resultColor = OpenMaya.MFloatVector(0.5, 0.0, 0.0)
            

            # set the output as a flat color
            outColorHandle = block.outputValue( self.outColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter
  
    @classmethod
    def nodeInitializer(cls):
        cls.makeOutColor(cls)
        cls.makeFloat(cls,'intensity','in',1.0)
        cls.makeColor(cls,'color','cl')
        cls.makeInteger(cls,'samples','sa',1)
        

        
