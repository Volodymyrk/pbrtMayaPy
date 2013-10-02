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
# pbrtTextNode. The node is just a holder of pbrt text API commands with an empty compute method.
#
# ------------------------------------------------------------------------------

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from PBRTNode import PBRTNode
 
 
class pbrtTextNode(OpenMayaMPx.MPxNode,PBRTNode):
    """
    A holder for text representation of the material-related commands
    """
    
    @staticmethod
    def nodeName():
        return "pbrtTextNode"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757802) #borrowing lux id area

    @staticmethod
    def nodeType():
        return  OpenMayaMPx.MPxNode.kDependNode

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
            
            resultColor = OpenMaya.MFloatVector(0.0, 0.0, 1.0)

            # set the output as a flat color
            outColorHandle = block.outputValue( self.outColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter
  
    @classmethod
    def nodeInitializer(cls):
        cls.makeOutColor(cls)
        defaultText = '''TransformBegin
Scale 4 4 4
Texture "%NODE_NAME_Texture" "spectrum" "fbm"
  
MakeNamedMaterial "%NODE_NAME" "string type" ["matte"]
     "texture Kd" "%NODE_NAME_Texture"
TransformEnd
            '''
        cls.makeString(cls,'pbrtText', 'txt',defaultText)
        
        

        
