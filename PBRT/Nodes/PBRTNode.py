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
# Maya PBRT node base class.
#
# ------------------------------------------------------------------------------

import os
os.altsep = '/'
from maya import OpenMaya

from PBRT.ExportModules.ExportModule import ExportModule

class PBRTNode:
    """
    Custom PBRT node base class
    """
    
    attributes = {}    
    outputString = str()
    
    def addToOutput(self, string):
        if not string == '': 
            self.outputString += ( string + os.linesep )
            
    def prependToOutput(self, string):
        if not string == '':
            self.outputString = string + os.linesep + self.outputString 

    # node attribute setup helper functions
    @staticmethod
    def makeInput(attr):
        attr.setKeyable(1)
        attr.setStorable(1)
        attr.setReadable(1)
        attr.setWritable(1)

    @staticmethod
    def makeOrdinary(attr):
        attr.setKeyable(1)
        attr.setStorable(1)
        attr.setReadable(0)
        attr.setWritable(1)

    @staticmethod
    def makeColor(cls,longName, shortName, defaultR = 1.0, defaultG = 1.0, defaultB = 1.0):
        nAttr = OpenMaya.MFnNumericAttribute()
        attrOut = nAttr.createColor(longName, shortName)
        PBRTNode.makeInput( nAttr )
        nAttr.setUsedAsColor(1)
        nAttr.setDefault(defaultR, defaultG, defaultB)
        cls.addAttribute(attrOut)
        #return attrOut

    @staticmethod
    def makeFloat(cls,longName, shortName, default = 0.0, input = True):
        nAttr = OpenMaya.MFnNumericAttribute()
        attrOut = nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kFloat)
        if input:
            PBRTNode.makeInput( nAttr )
        else:
            PBRTNode.makeOrdinary( nAttr )
        nAttr.setDefault( default )
        #return attrOut
        cls.addAttribute(attrOut)
    
    @staticmethod
    def makeInteger(cls,longName, shortName, default = 0, input = True):
        nAttr = OpenMaya.MFnNumericAttribute()
        attrOut = nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kInt)
        if input:
            PBRTNode.makeInput( nAttr )
        else:
            PBRTNode.makeOrdinary( nAttr )
        nAttr.setDefault( default )
        cls.addAttribute(attrOut)
    
    @staticmethod
    def makeBoolean(cls,longName, shortName, default = False, input = True):
        nAttr = OpenMaya.MFnNumericAttribute()
        attrOut = nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kBoolean)
        if input:
            PBRTNode.makeInput( nAttr )
        else:
            PBRTNode.makeOrdinary( nAttr )
        # nAttr.setDefault( default )
        cls.addAttribute(attrOut)
    

    @staticmethod
    def makeString(cls,longName, shortName, default = "default", input = True):
        tAttr = OpenMaya.MFnTypedAttribute()
        attrOut = tAttr.create(longName, shortName, OpenMaya.MFnData.kString)
        if input:
            PBRTNode.makeInput( tAttr )
        else:
            PBRTNode.makeOrdinary( tAttr )
        tAttr.setDefault( OpenMaya.MFnStringData().create(default) )
        cls.addAttribute(attrOut)
        
    @staticmethod
    def makeOutColor(cls):
        # a special color attribute for shading purposes
        nAttr        = OpenMaya.MFnNumericAttribute()
        cls.outColor = nAttr.createColor("outColor", "oc")
        nAttr.setKeyable(0)
        nAttr.setStorable(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)
        cls.addAttribute(cls.outColor)


