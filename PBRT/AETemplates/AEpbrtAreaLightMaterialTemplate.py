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
# AE Template for PBRT AreaLight. Create in hypershade and assign to any object 
#
# ------------------------------------------------------------------------------


import pymel.core.uitypes as pymelUI 

class AEpbrtAreaLightMaterialTemplate(pymelUI.AETemplate):
    _nodeType = 'pbrtAreaLightMaterial' 
    def __init__(self, nodeName):
        self.beginScrollLayout()

        self.beginLayout("Area Light",collapse=0)
        self.addControl("intensity")
        self.addControl("color")
        self.addControl("samples")
        self.endLayout()
    
        self.addExtraControls()
        self.endScrollLayout()


        
        
        
    
        