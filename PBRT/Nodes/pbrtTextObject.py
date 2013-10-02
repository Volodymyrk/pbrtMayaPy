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
# pbrtTextObject. The DAG object is just a holder of pbrt text API commands with custom GL draw method.
#
# ------------------------------------------------------------------------------


import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from PBRTNode import PBRTNode
import maya.OpenMayaRender as OpenMayaRender
import maya.OpenMayaUI as OpenMayaUI
 
glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

 
class pbrtTextObject(OpenMayaMPx.MPxLocatorNode,PBRTNode):
    """
    A holder for text representation of the material-related commands
    """
    
    @staticmethod
    def nodeName():
        return "pbrtTextObject"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757804) #borrowing lux id area

    @staticmethod
    def nodeType():
        return  OpenMayaMPx.MPxNode.kLocatorNode

    @staticmethod
    def nodeClassify():
        return 0

    def __init__(self):
        OpenMayaMPx.MPxLocatorNode.__init__(self)


    @classmethod
    def nodeCreator(cls):
        return OpenMayaMPx.asMPxPtr(cls())


    def drawBoundingLines(self,view,status):
        glFT.glBegin( OpenMayaRender.MGL_LINES );
        
        if status == OpenMayaUI.M3dView.kDormant:
            glFT.glColor3f(0.0, 0.25, 0.05)
            
        corners = {}
        corners['farTopRight']  = [1,1,-1]
        corners['farTopLeft']   = [-1,1,-1]
        corners['farLowLeft']   = [-1,-1,-1]
        corners['farLowRight']  = [1,-1,-1]
        
        corners['nearTopRight'] = [1,1,1]   
        corners['nearTopLeft']  = [-1,1,1]  
        corners['nearLowLeft']  = [-1,-1,1] 
        corners['nearLowRight'] = [1,-1,1]  
    
        #draw far frame
        glFT.glVertex3f( *corners['farTopRight'] )
        glFT.glVertex3f( *corners['farTopLeft'] )
        
        glFT.glVertex3f( *corners['farTopLeft'] )
        glFT.glVertex3f( *corners['farLowLeft'] )
         
        glFT.glVertex3f( *corners['farLowLeft'] )
        glFT.glVertex3f( *corners['farLowRight'] )
         
        glFT.glVertex3f( *corners['farLowRight'] )
        glFT.glVertex3f( *corners['farTopRight'] )
         
        #draw edges from far to near
        glFT.glVertex3f( *corners['farTopRight'] )
        glFT.glVertex3f( *corners['nearTopRight'] )
 
        glFT.glVertex3f( *corners['farTopLeft'] )
        glFT.glVertex3f( *corners['nearTopLeft'] )
 
        glFT.glVertex3f( *corners['farLowLeft'] )
        glFT.glVertex3f( *corners['nearLowLeft'] )
 
        glFT.glVertex3f( *corners['farLowRight'] )
        glFT.glVertex3f( *corners['nearLowRight'] )      
           
        #draw near frame
        glFT.glVertex3f( *corners['nearTopRight'] )
        glFT.glVertex3f( *corners['nearTopLeft'] )
         
        glFT.glVertex3f( *corners['nearTopLeft'] )
        glFT.glVertex3f( *corners['nearLowLeft'] )
         
        glFT.glVertex3f( *corners['nearLowLeft'] )
        glFT.glVertex3f( *corners['nearLowRight'] )
         
        glFT.glVertex3f( *corners['nearLowRight'] )
        glFT.glVertex3f( *corners['nearTopRight'] )
        #draw diagonals
        glFT.glVertex3f( *corners['farTopRight'] )
        glFT.glVertex3f( *corners['nearLowLeft'] )
        
        glFT.glVertex3f( *corners['farLowLeft'] )
        glFT.glVertex3f( *corners['nearTopRight'] ) 

        glFT.glVertex3f( *corners['farLowRight'] )
        glFT.glVertex3f( *corners['nearTopLeft'] )

        glFT.glVertex3f( *corners['farTopLeft'] )
        glFT.glVertex3f( *corners['nearLowRight'] )
      
        glFT.glEnd();
          
    def draw(self, view, path, style, status):
        "This is the main draw method called by Maya's viewport renderer"
        glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
        
        view.beginGL()
        self.drawBoundingLines(view,status)
        glFT.glPopAttrib()
        view.endGL()
  
    @classmethod
    def nodeInitializer(cls):
        defaultText = '''Shape "sphere" "float radius" [1.0]'''
        cls.makeString(cls,'pbrtText', 'txt',defaultText)
        
        

        
