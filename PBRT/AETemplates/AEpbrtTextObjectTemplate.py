# ------------------------------------------------------------------------------
# PBRT exporter for Maya
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# AE Template for pbrt text DAG object. This object can be created and placed in the scene.
# Can be used to define custom light sources, unsupported geometric primitives, etc.
#
# ------------------------------------------------------------------------------

import pymel.core.uitypes as pymelUI 
import maya.cmds as cmds
 

class AEpbrtTextObjectTemplate(pymelUI.AETemplate):
    _nodeType = 'pbrtTextObject' 
    def __init__(self, nodeName):
        self.beginScrollLayout()
        
        self.beginLayout("PBRT Text",collapse=0)
        self.callCustom(self.customTextCreate, self.customTextUpdate, "pbrtText")
        self.endLayout()

        self.addExtraControls()        
        self.endScrollLayout()
        
    def changeText(self,*args):
        textValue = self.textField.getText()
        cmds.setAttr( self.textAttribute, textValue, type="string" )

    def customTextCreate(self,attr):
        self.textField = pymelUI.ScrollField(h=300,nl=25,cc=self.changeText)
        self.customTextUpdate(attr)
            
    def customTextUpdate(self, attr):
        self.textAttribute = attr
        existingText = cmds.getAttr( attr )
        if existingText:
            self.textField.setText(existingText)    

        
        
        
    
        