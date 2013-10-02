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
# AE Template for pbrt text DG node. This node can be created in hypershade and assigned to any object.
# User can place custom material description, as well as other code.
#
# ------------------------------------------------------------------------------


import pymel.core.uitypes as pymelUI 
import maya.cmds as cmds


class AEpbrtTextNodeTemplate(pymelUI.AETemplate):
    _nodeType = 'pbrtTextNode' 
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

        
        
        
    
        