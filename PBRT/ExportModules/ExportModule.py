# ------------------------------------------------------------------------------
# PBRT exporter - python  plugin for Maya 2013
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
# Export module base classes: ExportModule and ShadedObject
#
# ------------------------------------------------------------------------------

import os
import math
os.altsep = '/'
from maya import OpenMaya


class ExportModule:
    """
    The ExportModule base class. This base class holds various vars passed by
    DAG Path, Dependancy Node, and other MObject iterators so that the export
    of various scene elements can be handled in a uniform way.
    The methods of this base class provide I/O (OK, /O) functions to the scene
    file, and helper functions to do various things like find node connections,
    convert Y-Up transforms to Z-Up etc
    """
    
    outputString = ""
    moduleLoaded = False
    
    dagPath = OpenMaya.MDagPath()
    
    dpNode = OpenMaya.MFnDependencyNode()
    
    fShape = OpenMaya.MObject()
    
    plugName = str()
    inputFound = False
    fileHandle = 0
    

    def loadModule(self):
        """
        "Load" this module, ie. start it's main process. Returns the outputString
        if not writing direct to file.
        """
        
        self.getOutput()
        self.moduleLoaded = True
        return self.outputString
    
    def intToBoolString(self, intIn):
        if intIn == 1: return 'true'
        else: return 'false'
    

    def translationMatrix(self, dagPath):
        """
        Convert this class' dagPath inclusive transformation matrix as ConcatTransform
        syntax. Y-Up to Z-Up and scale factor conversion is also performed.
        """
        
        matrix =  dagPath.inclusiveMatrix()
        
        matrix = self.checkUpAxis(matrix)

        strOut  = ( '\tConcatTransform [%f %f %f %f'  % (matrix(0,0), matrix(0,1), matrix(0,2), matrix(0,3)) ) + os.linesep
        strOut += ( '\t                 %f %f %f %f'  % (matrix(1,0), matrix(1,1), matrix(1,2), matrix(1,3)) ) + os.linesep
        strOut += ( '\t                 %f %f %f %f'  % (matrix(2,0), matrix(2,1), matrix(2,2), matrix(2,3)) ) + os.linesep
        strOut += ( '\t                 %f %f %f %f]' % (matrix(3,0), matrix(3,1), matrix(3,2), matrix(3,3)) )
        
        return strOut
    
    
    def checkUpAxis(self, matrix):
        """
        Check the scene's up axis, and convert the given transform matrix if necessary.
        """
        
        if OpenMaya.MGlobal.isYAxisUp():
            tMatrix = OpenMaya.MTransformationMatrix( matrix )
            tMatrix.rotateBy( OpenMaya.MEulerRotation(math.radians(90), 0, 0), OpenMaya.MSpace.kTransform )
            oTrans = tMatrix.getTranslation(OpenMaya.MSpace.kTransform)
            oTrans = OpenMaya.MVector( oTrans[0], -oTrans[2], oTrans[1] )
            tMatrix.setTranslation(oTrans, OpenMaya.MSpace.kTransform)
            return self.checkScale( tMatrix.asMatrix() )
        else:
            return self.checkScale( matrix )    

    def pointCheckUpAxis(self, point):
        """
        Check if the given point needs to be converted to Z-Up from Y-Up and 
        convert if necessary. 
        """
        
        pointTM = OpenMaya.MTransformationMatrix()
        pointTM.setTranslation(OpenMaya.MVector(point.x, point.y, point.z), OpenMaya.MSpace.kWorld)
        pointM = pointTM.asMatrix()
        pointM = self.checkUpAxis(pointM)
        pointTM = OpenMaya.MTransformationMatrix(pointM)
        return pointTM.getTranslation(OpenMaya.MSpace.kWorld)


    def checkScale(self, matrix):
        # Adjust scene scale
        scaleFactor = self.getSceneScaleFactor()
        if scaleFactor==1.0:
            return matrix
            
        scaleMatrix = OpenMaya.MMatrix()    
        OpenMaya.MScriptUtil.createMatrixFromList( (scaleFactor,0,0,0,
                                                    0,scaleFactor,0,0,
                                                    0,0,scaleFactor,0,
                                                    0,0,0,1),
                                                    scaleMatrix )
        matrix = matrix * scaleMatrix
        
        return matrix        

    @staticmethod
    def rgcAndClamp(colorValue):
        "we leave everything as-is"
                    
        return colorValue
    
    def getSceneScaleFactor(self):
        return 1.0    
    
    def addToOutput(self, string):
        """
        Accumulate the given string either to outputString, or direct to
        fileHandle if it exists.
        """
        
        if self.fileHandle==0:
            self.outputString += (string + os.linesep)
        else:
            self.fileHandle.write( string + os.linesep )
    
    
    def exportStr(self):
        return self.outputString
    


class ShadedObject(ExportModule):
    "super class for mesh and other objects with attached shaders"
    def findShadingGroup(self, instanceNum = 0, setNumber = 0):
        if self.fShape.type() == OpenMaya.MFn.kMesh:
            try:
                shadingGroups = OpenMaya.MObjectArray()
                faceIndices = OpenMaya.MIntArray()
                self.fShape.getConnectedShaders(instanceNum, shadingGroups, faceIndices)
                # we return the material connected to the given setNumber
                theShadingGroup = OpenMaya.MFnDependencyNode( shadingGroups[setNumber] )
            except:
                OpenMaya.MGlobal.displayError("Could not find shading group")
                return None
        
        elif self.fShape.type() == OpenMaya.MFn.kNurbsSurface:
            plugs = OpenMaya.MPlugArray()
            self.fShape.getConnections(plugs)
            otherside = OpenMaya.MPlugArray()
            theShadingGroup = OpenMaya.MFnDependencyNode()
            for j in range(0, plugs.length()):
                plugs[j].connectedTo(otherside, False, True)
                for i in range(0, otherside.length()):
                    if otherside[i].node().hasFn(OpenMaya.MFn.kShadingEngine):
                        theShadingGroup = OpenMaya.MFnDependencyNode(otherside[i].node())
                        
        return theShadingGroup
            
    def findSurfaceShader(self, instanceNum = 0, setNumber = 0):
        shadingGroup = self.findShadingGroup(instanceNum, setNumber)
        if shadingGroup==None:
            return None
        
        surfaceShader = shadingGroup.findPlug("surfaceShader")
        materials = OpenMaya.MPlugArray()
        surfaceShader.connectedTo(materials, True, True)
        
        if materials.length() > 0:
            matNode = materials[0].node()
            return OpenMaya.MFnDependencyNode( matNode )
        
        return None
                
    
    def getNamedMaterial(self, shaderNode):
        """
        Return the NamedMaterial syntax with this class' shaderNode.name()
        """
        
        return '\tNamedMaterial "' + shaderNode.name() + '"' #theMaterial.name()
    
    def getAreaLight(self, shaderNode):
        """
        Return AreaLightSource syntax with this class' shaderNode's attributes
        """
                
        gain = shaderNode.findPlug("intensity").asFloat()        
        numSamples = shaderNode.findPlug("samples").asInt()

        colorR = shaderNode.findPlug("colorR").asFloat()
        colorG = shaderNode.findPlug("colorG").asFloat()
        colorB = shaderNode.findPlug("colorB").asFloat()                
        
        outStr = ( '\tAreaLightSource "diffuse"' ) + os.linesep
        outStr += ( '\t\t"integer nsamples" [%i]' % numSamples ) + os.linesep
        outStr += ('\t\t"color L" [%f %f %f]' % (colorR*gain, colorG*gain, colorB*gain)) + os.linesep
        
        
        return outStr        
    