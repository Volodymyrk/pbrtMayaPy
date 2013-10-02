# ------------------------------------------------------------------------------
# PBRT exporter python script plugin for Maya
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# pbrtbatch: a command to launch the Exporter (one frame or sequence) 
# and start the rendering job. Actual scene graph iterator is in Exporter module.
#
# ------------------------------------------------------------------------------

import os
os.altsep = '/'

from maya import cmds
from maya import OpenMaya
from maya import OpenMayaMPx
from maya import OpenMayaUI

import subprocess
import pbrt_settings
reload(pbrt_settings)
import Exporter
reload(Exporter)

def getPbrtExe(pbrtSearchPathVar):
    'Utility proc that builds up a path to pbrt executable'
    pbrtSearchPath =  pbrtSearchPathVar
    if not pbrtSearchPath:
        'empty string if None'
        pbrtSearchPath=''
    else:
        pbrtSearchPath = pbrtSearchPath.strip()
    if pbrtSearchPath and pbrtSearchPath[-1] not in ('/','\\'):
        pbrtSearchPath += os.altsep
    pbrtExe = 'pbrt'
    if os.name=='nt':
        pbrtExe = 'pbrt.exe'
    return pbrtSearchPath+pbrtExe
    

class pbrtbatch(OpenMayaMPx.MPxCommand):
    """
    Class to handle an export processs, but not the actual export.
    It calls Exporter in exportFile method
    """

    @staticmethod
    def commandName():
        return "pbrt_export"

    @staticmethod
    def commandCreator():
        return OpenMayaMPx.asMPxPtr( pbrtbatch() )

    def doIt(self, args = OpenMaya.MArgList() ):
        """
        Class entry point.
        1. Detect if pbrt_settings exists
        2. Detect if exporting an animation
        3. Determine start and end frame to export, and pass control to startBatch()
        """


        OpenMaya.MGlobal.displayInfo( 'PBRT Batch Export start 2' )

        if not cmds.objExists('pbrt_settings'):
            OpenMaya.MGlobal.displayWarning('No PBRT settings found for this scene, creating a new settings node first')

        render_settings = pbrt_settings.pbrt_settings()
        render_settings.checkAndAddAttributes()

        # here we go
        doAnimation  = cmds.getAttr( 'pbrt_settings.render_animation' )

        self.startFrame = round( cmds.currentTime( query = True ) )
        self.unix = (os.name != 'nt')

        if doAnimation:
            self.startFrame  = round( cmds.getAttr( 'defaultRenderGlobals.startFrame'  ) )
            self.endFrame    = round( cmds.getAttr( 'defaultRenderGlobals.endFrame'    ) )
            self.stepFrame   = round( cmds.getAttr( 'defaultRenderGlobals.byFrameStep' ) )
        else:
            self.endFrame = self.startFrame

        self.initProgressWindow()

        self.startBatch()

    def initProgressWindow(self):

        from Exporter import consoleProgress

        self.MayaGUIMode = OpenMaya.MGlobal.mayaState() == OpenMaya.MGlobal.kInteractive

        if self.MayaGUIMode:
            self.mProgress = OpenMayaUI.MProgressWindow()
        else:
            self.mProgress = consoleProgress()

    def showProgressWindow(self):
        if self.MayaGUIMode:
            self.mProgress.reserve()
            self.mProgress.setInterruptable(True)
            self.mProgress.setProgressRange(0, int(self.endFrame-self.startFrame)+1)
            self.mProgress.setProgress(0)
            self.mProgress.startProgress()
        else:
            self.mProgress.tProgress = int(self.endFrame-self.startFrame)+1


    def startBatch(self):
        """
        Start the batch export process.
        1. For each frame to export, export it
        2. Append exported scene filename to fileList
        3. pass fileList to makeBatchFile()
        """


        fileList = []

        self.showProgressWindow()

        if self.startFrame == self.endFrame:
            # single frame export
            fileList.append( self.exportFile(self.startFrame) )
            self.mProgress.advanceProgress(1)
        else:
            # frame range export
            ct = cmds.currentTime( query = True )
            import time
            for f in range(int(self.startFrame), int(self.endFrame)+1, int(self.stepFrame)):
                self.mProgress.setTitle( 'Frames %i - %i: %i' % (int(self.startFrame), int(self.endFrame), f) )
                cmds.currentTime( f )
                time.sleep(.1)
                fileList.append( self.exportFile(f) )
                self.mProgress.advanceProgress(1)
                if self.mProgress.isCancelled(): break

            cmds.currentTime( ct )

        self.makeBatchFile(fileList)
        doRender  = cmds.getAttr( 'pbrt_settings.render_launch' )
        if  doRender:
            self.runProcess()
        OpenMaya.MGlobal.displayInfo( 'PBRT Export Successful' )
        self.mProgress.endProgress()

    def exportFile(self, frameNumber = 1, tempExportPath = False):
        """
        Export a single frame, and return the name of the created scene file
        """
        reload(Exporter)

        renderCameraName = ''

        for cam in cmds.listCameras():
            renderable = cmds.getAttr( '%s.renderable' % cam )
            if renderable == 1:
                renderCameraName = cam
                break

        if renderCameraName == '':
            OpenMaya.MGlobal.displayError('No renderable camera in scene')

        saveFolder = cmds.getAttr( 'pbrt_settings.scene_path' )
        if not os.path.exists(saveFolder):
            os.mkdir( saveFolder )

        sceneFileBaseName = cmds.getAttr( 'pbrt_settings.scene_filename' ) + ('.%04i' % frameNumber)

        renderFolder = saveFolder + os.altsep + "renders" + os.altsep
        if not os.path.exists(renderFolder):
            os.mkdir(renderFolder)

        imageSaveName = renderFolder + sceneFileBaseName +'.'+ cmds.getAttr( 'pbrt_settings.image_format', asString = True )
        self.imageSaveName = imageSaveName

        if tempExportPath:
            saveFolder += ('tmp') + os.altsep
            if not os.path.exists(saveFolder):
                os.mkdir( saveFolder )
            else:
                for file_val in os.listdir(saveFolder):
                    os.remove(saveFolder+file_val)
                os.rmdir( saveFolder )
                os.mkdir( saveFolder )
        else:
            saveFolder += ('%04i' % frameNumber) + os.altsep
            if not os.path.exists(saveFolder):
                os.mkdir( saveFolder )

        sceneFileName = str(saveFolder + sceneFileBaseName + '.pbrt')

        renderWidth = cmds.getAttr( 'defaultResolution.width' )
        renderHeight = cmds.getAttr( 'defaultResolution.height' )
        verbosity = cmds.getAttr( 'pbrt_settings.verbosity' )

        # launch export proc here !
        pe = Exporter.Exporter(sceneFileName, imageSaveName, renderWidth, renderHeight, renderCameraName, verbosity )
        try:
            pe.doIt( )
        except:
            self.mProgress.endProgress()
            raise

        return sceneFileName

    def makeBatchFile(self, fileList):
        renderFolder = cmds.getAttr( 'pbrt_settings.scene_path' )
        imageViewer = cmds.getAttr( 'pbrt_settings.image_viewer' )

        ext = 'sh'
        if not self.unix: ext = 'bat'
        self.batchFileName = renderFolder+"batchRender."+ ext

        pbrtPath = getPbrtExe( cmds.getAttr( 'pbrt_settings.pbrt_path') )

        batchFile = open(self.batchFileName,'w')
        if len(fileList)==1:
            batchFile.write('%s %s'%(pbrtPath,fileList[0] ))
            batchFile.write(os.linesep)
            batchFile.write('%s %s'%(imageViewer, self.imageSaveName))
            batchFile.write(os.linesep)
        else:
            for f in fileList:
                batchFile.write('%s %s'%(pbrtPath, f))
                batchFile.write(os.linesep)

        if not self.unix:
            batchFile.write('pause')
            
        batchFile.close()
        OpenMaya.MGlobal.displayInfo( '%s batch file create'%self.batchFileName )

        return batchFile

    def runProcess(self):

        if self.batchFileName!='':

            if self.unix:
                'Linux or Mac. bash should be available on those systems by default'
                cmds = ['bash',self.batchFileName]
            else:
                'windows. Execute the bat file directly'
                cmds = [self.batchFileName]

            try:
                process = subprocess.Popen(cmds )
            except:

                print "cannot execute %s"%(cmds[-1])

        else:
            OpenMaya.MGlobal.displayError('No batch file to execute')

