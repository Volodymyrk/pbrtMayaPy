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
# AE Template for pbrt_settings. This acts as a main RenderGlobals for PBRT 
#
# ------------------------------------------------------------------------------

import pymel.core.uitypes as pymelUI 
import maya.cmds as cmds
 

class AEpbrtSettingsNodeTemplate(pymelUI.AETemplate):
    _nodeType = 'pbrtSettingsNode' 
    
    def addNiceCtrl(self, attribute, label=None):
        label = label
        if attribute.find('_')!=-1:
            parts = attribute.split('_')
            label = parts[-1]
        self.addControl(attribute, label=label)
        
    def __init__(self, nodeName):
        print "building", nodeName
        self.beginScrollLayout()
        
        self.beginLayout("Paths",collapse=0)
        self.addControl("scene_path")
        self.addControl("scene_filename")

        self.addControl("image_format")
        self.addControl("pbrt_path")
        self.addControl("image_viewer")
        self.addControl("verbosity")
        self.endLayout()

        self.beginLayout("Export Settings",collapse=1)
        self.addControl("scene_export_meshes")
        self.addControl("scene_export_arealights")
        self.addControl("scene_export_lights")
        self.addControl("scene_export_materials")
        self.addControl("scene_export_defaultLighting")
        
        
        self.endLayout()

        self.beginLayout("Camera",collapse=1)
        self.addControl("camera_persptype")
        self.addControl("camera_infinite_focus")
        self.addControl("camera_exposuretime")
        self.endLayout()
        
        self.beginLayout("Sampling",collapse=1)
        self.addControl("pixel_sampler")
        self.addControl("pixel_sampler_pixelsamples")
        self.addControl("pixel_sampler_minsamples")
        self.addControl("pixel_sampler_maxsamples")
        self.addControl("pixel_sampler_method")
        self.addControl("pixel_sampler_jitter")
        self.addControl("pixel_sampler_xsamples")
        self.addControl("pixel_sampler_ysamples")
        self.endLayout()

        self.beginLayout("Filtering",collapse=1)
        self.addControl("pixel_filter")
        self.addControl("pixel_filter_xwidth")
        self.addControl("pixel_filter_ywidth")
        self.addControl("pixel_filter_alpha")
        self.addControl("pixel_filter_b")
        self.addControl("pixel_filter_c")
        self.addControl("pixel_filter_tau")
        self.endLayout()

        self.beginLayout("Renderer",collapse=1)
        self.addControl("renderer")
        self.beginLayout("Sampler",collapse=1)
        self.addControl("visualizeobjectids")
        self.endLayout()
        self.beginLayout("Metropolis",collapse=1)
        self.addControl("largestepprobability")
        self.addControl("samplesperpixel")
        self.addControl("bootstrapsamples")
        self.addControl("directsamples")
        self.addControl("dodirectseparately")
        self.addControl("maxconsecutiverejects")
        self.addControl("maxdepth")
        self.addControl("bidirectional")
        self.endLayout()
        self.endLayout()


        self.beginLayout("Integrator",collapse=1)
        self.addNiceCtrl("surface_integrator")
        
        self.beginLayout("IrradianceCache",collapse=1)
        self.addNiceCtrl("integrator_minweight")
        self.addNiceCtrl("integrator_minpixelspacing")
        self.addNiceCtrl("integrator_maxpixelspacing")
        self.addNiceCtrl("integrator_maxangledifference")
        
        self.addNiceCtrl("integrator_maxspeculardepth")
        self.addNiceCtrl("integrator_maxindirectdepth")
        self.addNiceCtrl("integrator_ic_nsamples")
        self.endLayout()
                
        
        self.beginLayout("ambientocclusion",collapse=1)
        self.addNiceCtrl("integrator_nsamples")
        self.addNiceCtrl("integrator_maxdist")
        self.endLayout()
        self.beginLayout("IGI",collapse=1)
        self.addNiceCtrl("integrator_maxdepth")
        self.addNiceCtrl("integrator_nlights")
        self.addNiceCtrl("integrator_nsets")
        self.addNiceCtrl("integrator_rrthreshold")
        self.addNiceCtrl("integrator_glimit")
        self.addNiceCtrl("integrator_gathersamples")
        self.endLayout()
        self.endLayout()


        self.beginLayout("Accelerator",collapse=1)
        self.addControl("accelerator")
        self.beginLayout("BVH",collapse=1)
        self.addControl("accelerator_maxnodeprims")
        self.endLayout()
        self.beginLayout("Grid",collapse=1)
        self.addControl("accelerator_splitmethod")
        self.addControl("accelerator_refineimmediately")
        self.endLayout()
        self.beginLayout("KDtree",collapse=1)
        self.addControl("accelerator_intersectcost")
        self.addControl("accelerator_traversalcost")
        self.addControl("accelerator_emptybonus")
        self.addControl("accelerator_maxprims")
        self.addControl("accelerator_maxdepth")
        self.endLayout()
        self.endLayout()

        self.beginLayout("Text Box",collapse=1)
        self.callCustom(self.textCustom1, self.textCustom2, "extra_commands")
        self.endLayout()

        self.beginLayout("Process",collapse=1)
        self.addControl("render_launch")
        self.addControl("render_animation")
        self.endLayout()
    
        # --------------- extra stuff --------
        self.beginLayout("Ignored",collapse=1)
        self.addExtraControls()
        
        self.endLayout()
        self.endScrollLayout()
        
    def changeText(self,*args):
        textValue = self.textField.getText()
        cmds.setAttr( 'pbrt_settings.extra_commands', textValue, type="string" )

    def textCustom1(self,attr):
        self.textField = pymelUI.ScrollField(h=100,nl=25,cc=self.changeText)
        existingText = cmds.getAttr( 'pbrt_settings.extra_commands')
        if existingText!="":
            self.textField.setText(existingText)
            
    def textCustom2(self, attr):
        pass
        
    
        