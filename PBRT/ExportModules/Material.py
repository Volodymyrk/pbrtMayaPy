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
# material export class.
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import cmds

from ExportModule import ExportModule


class MaterialBase:
    """
    Material type base class.
    """
    
    def __init__(self,fileHandle, shaderNode):
        """
        Set up the node that we're dealing with.
        """
        
        self.dpNode = shaderNode
        self.shaderName = self.dpNode.name()
        self.fileHandle = fileHandle


class Material(ExportModule):
    """
    Material ExportModule. This acts as a factory to return a derived ExportModule
    for the given shader type.
    """
    
    @staticmethod
    def MaterialFactory( fileHandle,dpNode ):
        """
        The material factory.
        """
        
        # global ExportedMaterials
        
        nodeType = dpNode.typeName()
        
        nodeName = dpNode.name()            
        
        if dpNode.classification( nodeType ).find("shader/surface")!=-1 :
            
            if nodeType == "pbrtTextNode":
                # export pbrt material directly
                return PBRTTextNode(fileHandle, dpNode )
            elif nodeType == "lambert":
                # translate lambert -> matte
                return MaterialLambert(fileHandle, dpNode )
            elif nodeType == "blinn":
                # translate blinn -> plastic
                return MaterialBlinn(fileHandle, dpNode )
            elif nodeType == "phong":
                # translate blinn -> plastic
                return MaterialBlinn(fileHandle, dpNode )
            elif nodeType == "phongE":
                # translate blinn -> plastic
                return MaterialBlinn(fileHandle, dpNode )
            elif nodeType == "pbrtAreaLightMaterial":
                # translate blinn -> plastic
                OpenMaya.MGlobal.displayWarning(" %s on %s" % (nodeType,nodeName ))
                return False

            else:
                OpenMaya.MGlobal.displayWarning("Shader type %s not supported" % nodeType )
                return False
        else:
            return False
    
    
class PBRTTextNode(ExportModule, MaterialBase):
    """
    A simple pbrt text node
    """
        
    def getOutput(self):
        text = self.dpNode.findPlug( "pbrtText" ).asString().replace('%NODE_NAME', self.shaderName)
        
        #text =  cmds.getAttr('%s.pbrtText'%self.shaderName).replace('%NODE_NAME', self.shaderName)
        self.addToOutput('#pbrtTextNode %s'%self.shaderName)
        if text:
            self.addToOutput( text)
        self.addToOutput('')


class MaterialLambert(ExportModule, MaterialBase):
    """
    A translatable Maya shader: Lambert
    """
        
    def getOutput(self):
        
        Kd = tuple(cmds.getAttr('%s.color'%self.shaderName)[0])
        self.addToOutput( '# Translated Lambert Material ' + self.shaderName )
        self.addToOutput( 'MakeNamedMaterial "%s" "string type" ["matte"]'%self.shaderName)
        self.addToOutput( '\t "color Kd" [%f %f %f] '%Kd)
        self.addToOutput('')
        

class MaterialBlinn(ExportModule, MaterialBase):
    """
    A translatable Maya shaders: Blinn, Phong, PhongE -> pbrt Plastic. 
    """
            
    def getOutput(self):
        """
        Get the syntax from the phongShader module.
        """
        Kd = tuple(cmds.getAttr('%s.color'%self.shaderName)[0])
        Ks = tuple(cmds.getAttr('%s.specularColor'%self.shaderName)[0])
        roughness = 0.1
        # This is far from precise BRDF conversion. We want let users press "Render" in the existing scene. 
        if cmds.objExists('%s.eccentricity'):
            roughness = cmds.getAttr('%s.eccentricity'%self.shaderName)
        elif cmds.objExists('%s.roughness'):
            roughness = cmds.getAttr('%s.roughness'%self.shaderName)
        elif cmds.objExists('%s.cosinePower'):
            roughness = cmds.getAttr('%s.cosinePower'%self.shaderName)
            roughness = 1.0/roughness
        
        
        self.addToOutput( '# Translated Blinn Material ' + self.dpNode.name() )
        self.addToOutput( 'MakeNamedMaterial "%s" "string type" ["plastic"]'%self.shaderName)
        self.addToOutput( '\t "color Kd" [%f %f %f] '%Kd)
        self.addToOutput( '\t "color Ks" [%f %f %f] '%Ks)
        self.addToOutput( '\t "float roughness" [%f] '%roughness)
        self.addToOutput('')
