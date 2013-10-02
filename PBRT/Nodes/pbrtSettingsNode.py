'''
Created on Jul 9, 2013

@author: volodymyrkazantsev
'''

# import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
# import maya.OpenMayaRender as OpenMayaRender
# import maya.OpenMayaUI as OpenMayaUI
 
 
class pbrtSettingsNode(OpenMayaMPx.MPxLocatorNode):
    """
    A locator node that draws camera frustum using Maya OpenGL
    """
    
    @staticmethod
    def nodeName():
        return "pbrtSettingsNode"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757801) #borrowing lux id area


    @staticmethod
    def nodeType():
        return OpenMayaMPx.MPxNode.kLocatorNode 

    @staticmethod
    def nodeClassify():
        return 0

    def __init__(self):
        OpenMayaMPx.MPxLocatorNode.__init__(self)

    @classmethod
    def nodeCreator(cls):
        return OpenMayaMPx.asMPxPtr(cls())
  
    @classmethod
    def nodeInitializer(cls):
        "Adding all node attributes here"
        #unitAttr = OpenMaya.MFnUnitAttribute()
        #typedAttr = OpenMaya.MFnTypedAttribute()

        
