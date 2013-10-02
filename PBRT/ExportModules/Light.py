# ------------------------------------------------------------------------------
# PBRT exporter - python  plugin for Maya by Vladimir (Volodymyr) Kazantsev
# 2013
#
# Based on a Python LuxMaya translation by Doug Hammond, in turn base on translation of the c++ luxmaya exporter, 
# in turn based on original maya-pbrt c++ exporter by Mark Colbert
#
# This file is licensed under the GPL (the original exporter uses that license)
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# lights export module
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya

# uncomment for interactive development
# import ExportModule
# reload(ExportModule)
from ExportModule import ExportModule


class Light(ExportModule):
    """
    Light ExportModule base class. This is primarily a factory for returning
    various light types.
    """
    
    @staticmethod
    def LightFactory( fileHandle, dagPath ):
        """
        Detect the given light type and return a corresponding light object
        """
        
        nodeType = dagPath.node().apiType()
        
        if nodeType == OpenMaya.MFn.kSpotLight:
            #this is a spotlight
            return SpotLight( fileHandle, dagPath )
        elif nodeType == OpenMaya.MFn.kPointLight:
            #this is a pointlight
            return PointLight( fileHandle, dagPath )
        elif nodeType == OpenMaya.MFn.kDirectionalLight:
            #this is a pointlight
            return DistantLight( fileHandle, dagPath )

        else:
            OpenMaya.MGlobal.displayWarning("Light type %i not supported" % nodeType)
            return False
    
    @staticmethod
    def defaultLighting():
        return """
        AttributeBegin
        CoordSysTransform "camera"
        LightSource "distant" "color I" [ .7 .7 .5 ] "point from" [0 0 0] "point to" [1.0 -1.0 1.0]
        LightSource "distant" "color I" [ .2 .2 .35 ] "point from" [0 0 0] "point to" [0.0 0.0 1.0]
        AttributeEnd

        """
    
    def getOutput(self):
        """
        Nothing to do here, child classes output light type specific syntax.
        """
        pass
    

class DistantLight(Light):
    """
    Distant light type.
    """

    light = OpenMaya.MFnDirectionalLight()
    
    def __init__( self, fileHandle, dagPath ):
        """
        Constructor. Sets up this object's data.
        """
        
        self.fileHandle = fileHandle
        self.dagPath = dagPath
        self.light = OpenMaya.MFnDirectionalLight( dagPath )
        
    def getOutput(self):
        """
        Return LightSource "distant" from the given directional node.
        """
        
        color = self.light.color()
        intensity = self.light.intensity()
        
        colorR = self.rgcAndClamp( color.r * intensity )
        colorG = self.rgcAndClamp( color.g * intensity )
        colorB = self.rgcAndClamp( color.b * intensity )
    
        self.addToOutput( '# Directional Light ' + self.dagPath.fullPathName() )
        self.addToOutput( 'TransformBegin' )
        self.addToOutput( self.translationMatrix( self.dagPath ) )
        self.addToOutput( '\tLightSource "distant"' )
        self.addToOutput( '\t\t"color L" [%f %f %f]' % (colorR, colorG, colorB) )
        self.addToOutput( '\t\t"point from" [0 0 0]')
        self.addToOutput( '\t\t"point to" [0 0 -1]' )
        self.addToOutput( 'TransformEnd' )
        self.addToOutput( '' )
        
        self.fileHandle.flush()
        

class SpotLight(Light):
    """
    Spot light type.
    """

    light = OpenMaya.MFnSpotLight()
    
    def __init__( self, fileHandle, dagPath ):
        """
        Constructor. Sets up this object's data.
        """
        
        self.fileHandle = fileHandle
        self.dagPath = dagPath
        self.light = OpenMaya.MFnSpotLight( dagPath )
        
    def getOutput(self):
        """
        Return PBRT LightSource "spot" from the given spotlight node.
        """
        
        color = self.light.color()
        intensity = self.light.intensity()
        
        colorR = self.rgcAndClamp( color.r * intensity )
        colorG = self.rgcAndClamp( color.g * intensity )
        colorB = self.rgcAndClamp( color.b * intensity )
    
        self.addToOutput( '# Spot Light ' + self.dagPath.fullPathName() )
        self.addToOutput( 'TransformBegin' )
        self.addToOutput( self.translationMatrix( self.dagPath ) )
        self.addToOutput( '\tLightSource "spot"' )
        self.addToOutput( '\t\t"color I" [%f %f %f]' % (colorR, colorG, colorB) )
        self.addToOutput( '\t\t"point from" [0 0 0]')
        self.addToOutput( '\t\t"point to" [0 0 -1]' )
        self.addToOutput( '\t\t"float coneangle" [%f]' % ( self.light.coneAngle()*180/math.pi ) )
        self.addToOutput( '\t\t"float conedeltaangle" [%f]' % ( self.light.dropOff()*180/math.pi ) )
        self.addToOutput( 'TransformEnd' )
        self.addToOutput( '' )
        
        self.fileHandle.flush()


class PointLight(Light):
    """
    Point light type.
    """
    
    light = OpenMaya.MFnPointLight()

    def __init__( self, fileHandle, dagPath ):
        """
        Constructor. Sets up this object's data.
        """
        
        self.fileHandle = fileHandle
        self.dagPath = dagPath
        self.light = OpenMaya.MFnPointLight( dagPath )

    def getOutput(self):
        """
        Export Maya Point Light as pbrt's LightSource "point" 
        """
        
        color = self.light.color()
        intensity = self.light.intensity()
        
        colorR = self.rgcAndClamp( color.r * intensity )
        colorG = self.rgcAndClamp( color.g * intensity )
        colorB = self.rgcAndClamp( color.b * intensity )
        
        self.addToOutput( '# Point Light ' + self.dagPath.fullPathName() )
        self.addToOutput( 'TransformBegin' )
        self.addToOutput( self.translationMatrix( self.dagPath ) )
        self.addToOutput( '\tLightSource "point"' )
        self.addToOutput( '\t\t"color I" [%f %f %f]' % (colorR, colorG, colorB) )
        self.addToOutput( 'TransformEnd' )
        self.addToOutput( '' )
