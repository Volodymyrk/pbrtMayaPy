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
# Locator export module. Currently exports only pbrtTextObject
#
# ------------------------------------------------------------------------------


from maya import OpenMaya

# uncomment for interactive development
# import ExportModule
# reload(ExportModule)
from ExportModule import ExportModule


class Locator(ExportModule):
    """
    Locator ExportModule base class. This is primarily a factory for returning
    various types. Only textObject locator is currently supported
    """
    
    @staticmethod
    def Factory( fileHandle, dagPath ):
        """
        Detect the given light type and return a corresponding light object
        """
        
        dpNode = OpenMaya.MFnDependencyNode( dagPath.node() )
        nodeType = dpNode.typeName()
        
        if nodeType == 'pbrtTextObject':
            #this is a spotlight
            return TextObject( fileHandle, dagPath )
        else:
            #OpenMaya.MGlobal.displayWarning("Locator type %s not supported" % nodeType)
            return False
    
    
    def getOutput(self):
        """
        Nothing to do here, child classes output light type specific syntax.
        """
        pass
    

class TextObject(Locator):
    
    def __init__( self, fileHandle, dagPath ):
        """
        Constructor. Sets up this object's data.
        """
        
        self.fileHandle = fileHandle
        self.dagPath = dagPath
        self.dpNode = OpenMaya.MFnDependencyNode( dagPath.node() )
    
        
    def getOutput(self):
        """
        Return LightSource "distant" from the given directional node.
        """
        
        textBox = self.dpNode.findPlug("pbrtText").asString()
    
        self.addToOutput( '# Text Box  ' + self.dagPath.fullPathName() )
        self.addToOutput( 'TransformBegin' )
        self.addToOutput( self.translationMatrix( self.dagPath ) )
        self.addToOutput( textBox )
        self.addToOutput( 'TransformEnd' )
        self.addToOutput( '' )
        
        self.fileHandle.flush()
        
