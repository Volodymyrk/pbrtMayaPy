# ------------------------------------------------------------------------------
# pbrt exporter python script plugin for Maya
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# This script creates a new pbrtSettingsNode and adds dynamic attributes to it.
# While the attributes could be created inside the custom node plugin, it is 
# far easier to upgrade/add new attributes to existing scenes using this approach. 
#
# ------------------------------------------------------------------------------

import os
# AETemplates needs to be explicitly imported, even if they are not used directly
import PBRT.AETemplates.AEpbrtSettingsNodeTemplate

os.altsep = '/'
from maya import OpenMaya
from maya import cmds

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

class pbrt_settings:
    """
    Class to create the pbrt_settings node in the scene
    """
    settingsNodeSelected = False
    
    def selectSettings(self):
        if self.settingsNodeSelected:
            return
        print( 'selecting settings' )
        cmds.select('pbrt_settings') 
        self.settingsNodeSelected = True

    def addString(self, ln, dv=""):
        if cmds.objExists('pbrt_settings.%s'%ln):
            return
        self.selectSettings()
        if not self.firstTimeInit:
            print('adding %s'%ln)
        cmds.addAttr( ln = ln, dt = "string" )
        if not dv: dv = ""
        cmds.setAttr( 'pbrt_settings.%s'%ln, dv, type="string" )
            
        
    def addEnum(self, ln, options, dv = 0):
        if cmds.objExists('pbrt_settings.%s'%ln):
            return
        self.selectSettings()
        if not self.firstTimeInit:
            print('adding %s'%ln)
        cmds.addAttr( ln = ln, at = 'enum', enumName = options, dv = dv )

    def addShort(self, ln, dv = 0):
        if cmds.objExists('pbrt_settings.%s'%ln):
            return
        self.selectSettings()
        if not self.firstTimeInit:
            print('adding %s'%ln)
        cmds.addAttr( ln = ln, at = 'short', dv = dv)

        
    def addLong(self, ln, dv = 0):
        if cmds.objExists('pbrt_settings.%s'%ln):
            return
        self.selectSettings()
        if not self.firstTimeInit:
            print('adding %s'%ln)
        cmds.addAttr( ln = ln, at = 'long', dv = dv)

    def addFloat(self, ln, dv = 0):
        if cmds.objExists('pbrt_settings.%s'%ln):
            return
        self.selectSettings()
        if not self.firstTimeInit:
            print('adding %s'%ln)
        cmds.addAttr( ln = ln, at = 'float', dv = dv)
        
    def addBool(self, ln, dv = 0):
        if cmds.objExists('pbrt_settings.%s'%ln):
            return
        self.selectSettings()
        if not self.firstTimeInit:
            print('adding %s'%ln)
        cmds.addAttr( ln = ln, at = 'bool', dv = dv)


    def __init__(self):
        """
        Class entry point.
        Detect if the node already exists:
            yes, then perform an upgrade, if necessary.
            no, then create a new settings node. 
        """
        self.firstTimeInit = False
        if not cmds.objExists('pbrt_settings'):
            OpenMaya.MGlobal.displayInfo( 'pbrt: No settings node found, creating...' )
            self.createNewSettingsNode()
            self.firstTimeInit = True
        
    def alertIfPbrtNotAccessible(self):
        import pbrtbatch
        pbrtExe = pbrtbatch.getPbrtExe( os.getenv('PBRT_SEARCHPATH') )
        if which(pbrtExe)!=None:
            return True
        cmds.confirmDialog( title='No PBRT found', message='Please set PBRT_SEARCHPATH environment variable or add pbrt folder to your PATH')
                    

    def createNewSettingsNode(self):
        """
        Create a new pbrt_settings node
        """
        
        if 'pbrt_settings' != cmds.createNode( 'pbrtSettingsNode', name = 'pbrt_settings' ):
            OpenMaya.MGlobal.displayError('cannot create settings node with name "pbrt_settings"')
            return
        parentTransform = cmds.listRelatives('pbrt_settings', allParents=True)[0]
        cmds.rename(parentTransform,'PBRT')
        self.alertIfPbrtNotAccessible()
    
        
    def checkAndAddAttributes(self):     
        
        # File paths / scene settings
        self.addString( ln = "pbrt_path", dv=os.getenv('PBRT_SEARCHPATH') )
        self.addString( ln = "scene_path", dv='%spbrt%s' % ( cmds.workspace( q = True, rootDirectory = True), os.altsep ) )
        self.addString( ln = "scene_filename", dv='myScene1' )
        defaultViewer = 'fcheck'
        if os.name == 'nt' : defaultViewer = 'fcheck.exe'
        self.addString( ln = "image_viewer", dv=defaultViewer )
        self.addShort  ( ln = "verbosity", dv = 1 )
        
        #exporter settings
        self.addBool(ln = 'scene_export_meshes' , dv = 1)
        self.addBool(ln = 'scene_export_arealights' , dv = 1)
        self.addBool(ln = 'scene_export_lights' , dv = 1)
        self.addBool(ln = 'scene_export_materials' , dv = 1)
        self.addBool(ln = 'scene_export_defaultLighting' , dv = 1)
        
        
        # Camera settings
        self.addEnum( ln = 'camera_persptype', options = 'Perspective:Environment') #:Realistic' )
        self.addBool(ln = 'camera_infinite_focus' , dv = True)
        self.addFloat( ln = 'camera_exposuretime', dv = 1 )
                
        # Renderer settings

        # Film Settings
        self.addEnum ( ln = 'image_format', options = 'tga:exr:pfm' )        
        # Renderer settings
        
        # Samplers
        # DH-0.6RC 24/03/2009
        self.addEnum ( ln = 'pixel_sampler', options = 'Adaptive:BestCandidate::Halton::LowDiscrepancy:Random:Stratified', dv = 3 )

        #  bestcandidate, lowdiscrepancy, halton, random
        self.addShort( ln = 'pixel_sampler_pixelsamples', dv = 4 )

        #  adaptive
        self.addShort( ln = 'pixel_sampler_minsamples', dv = 4 )
        self.addShort( ln = 'pixel_sampler_maxsamples', dv = 32 )
        self.addEnum ( ln = 'pixel_sampler_method', options = 'contrast:shapeid', dv = 1 )
        
        # stratified
        self.addBool( ln = 'pixel_sampler_jitter', dv = True )
        self.addShort( ln = 'pixel_sampler_xsamples', dv = 2 )
        self.addShort( ln = 'pixel_sampler_ysamples', dv = 2 )
                
        # Filters
        self.addEnum ( ln = 'pixel_filter', options = 'Mitchell:Gaussian:Sinc:Triangle:Box', dv = 1 )
        #  pixel filter settings
        self.addFloat( ln = 'pixel_filter_xwidth', dv = 2 )
        self.addFloat( ln = 'pixel_filter_ywidth', dv = 2 )
        self.addFloat( ln = 'pixel_filter_alpha', dv = 2 )
        self.addFloat( ln = 'pixel_filter_b', dv = 0.333333 )
        self.addFloat( ln = 'pixel_filter_c', dv = 0.333333 )
        self.addFloat( ln = 'pixel_filter_tau', dv = 3 )


        # Renders
        self.addEnum ( ln = 'renderer', options = 'Aggregatetest:CreateProbes:Metropolis:Sampler:SurfacePoints', dv = 3 )
        
        # sampler
        self.addBool( ln = 'visualizeobjectids', dv = False )
        
        # metropolis
        self.addFloat( ln = 'largestepprobability', dv = 0.25 )
        self.addLong( ln = 'samplesperpixel', dv = 100 )
        self.addLong( ln = 'bootstrapsamples', dv = 100000 )
        self.addLong( ln = 'directsamples', dv = 4 )
        self.addBool( ln = 'dodirectseparately', dv = True )
        self.addLong( ln = 'maxconsecutiverejects', dv = 512 )
        self.addShort( ln = 'maxdepth', dv = 7 )
        self.addBool( ln = 'bidirectional', dv = True )
        
        # accelerator
        self.addEnum ( ln = 'accelerator', options = 'BVH:Grid:kdtree' , dv = 0)
        #  BVH
        self.addShort( ln = 'accelerator_maxnodeprims', dv = 7 )
        # Grid
        self.addEnum ( ln = 'accelerator_splitmethod', options = 'sah:middle:equal' , dv = 0)
        self.addBool( ln = 'accelerator_refineimmediately', dv = False )
        # kdtree
        self.addShort( ln = 'accelerator_intersectcost', dv = 80 )
        self.addShort( ln = 'accelerator_traversalcost', dv = 1 )
        self.addFloat( ln = 'accelerator_emptybonus', dv = 0.2 )
        self.addShort( ln = 'accelerator_maxprims', dv = 1 )
        self.addShort( ln = 'accelerator_maxdepth', dv = -1 )
                

        # Integrator
        self.addEnum ( ln = 'surface_integrator', options = 'AmbientOcclusion:Diffuseprt:DipoleSubSurface:DirectLighting:Glossyprt:IGI:IrradianceCache:path:photonmap:useprobes:whitted', dv = 3)

        #  IrradianceCache
        self.addFloat( ln = 'integrator_minweight', dv = 0.5 )
        self.addFloat( ln = 'integrator_minpixelspacing', dv = 2.5 )
        self.addFloat( ln = 'integrator_maxpixelspacing', dv = 15 )
        self.addFloat( ln = 'integrator_maxangledifference', dv = 10 )
        
        self.addShort( ln = 'integrator_maxspeculardepth', dv = 5 )
        self.addShort( ln = 'integrator_maxindirectdepth', dv = 3 )
        self.addShort( ln = 'integrator_ic_nsamples', dv = 4096 )
        
        #  ambientocclusion
        self.addShort( ln = 'integrator_nsamples', dv = 512 )
        self.addFloat( ln = 'integrator_maxdist', dv = 100000 )
        #  igi
        self.addShort( ln = 'integrator_maxdepth', dv = 5 )
        self.addShort( ln = 'integrator_nlights', dv = 64 )
        self.addShort( ln = 'integrator_nsets', dv = 4 )
        self.addFloat( ln = 'integrator_rrthreshold', dv = 0.0001 )
        self.addFloat( ln = 'integrator_glimit', dv = 10 )
        self.addShort( ln = 'integrator_gathersamples', dv = 16 )
        
        
        # Process settings
        self.addBool  ( ln = 'render_launch', dv=True )
        self.addBool  ( ln = 'render_animation' )
        #self.addBool  ( ln = 'render_animation_sequence' )
        
        self.addString( ln = "extra_commands",dv="")
        
        
        
        
        
        
        
        
        
        