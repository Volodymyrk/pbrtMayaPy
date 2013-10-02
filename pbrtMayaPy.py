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
# This script loads the various commands and nodes to allow PBRT integration into Maya.
# This file is purely a loader, all the real classes are in the PBRT package. 
#
# ------------------------------------------------------------------------------



import sys, os.path
from maya import OpenMaya
from maya import OpenMayaMPx

#GUI/Commands
from PBRT.Commands.pbrtbatch import pbrtbatch
from PBRT.Commands.gui import mainMenu

import pkgutil
import PBRT.Nodes


# ------------------------------------------------------------------------------

# Global list of commands that we want to register with Maya.
pbrtCommands = [
    pbrtbatch
]

# We build the list of nodes by scanning the Nodes directory
nodesPath = os.path.dirname(PBRT.Nodes.__file__)
pbrtNodes = [name for _, name, _ in pkgutil.iter_modules([nodesPath])]

pbrtRegisteredNode = []

# initialize the script plug-ins
def initializePlugin(mobject):
    """
    Start the plugin by registering all commands and nodes etc that this plugin provides
    """
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Vlad Volodymyr Kazantsev", "0.1", "Any")
    
    # there are multiple reload() calls in various places in code
    # Those are used to load updated code without restarting Maya
    #reload(PBRT.Commands.pbrtbatch)

    try:

        # Register commands
        for command in pbrtCommands:
            mplugin.registerCommand( command.commandName(), command.commandCreator )

        #Register nodes
        for nodeName in pbrtNodes:
            node = None
            try:
                __import__('PBRT.Nodes', fromlist=[nodeName])
                module = sys.modules['PBRT.Nodes.'+nodeName]
                reload(module)
                node = module.__dict__[nodeName]
            except ImportError:
                OpenMaya.MGlobal.displayError( "Failed to load "+nodeName )
            
            # abstract node classes should return None in nodeName() method
            isNode = getattr(node, 'nodeName', None)  
            if isNode is None:
                continue
                        
            pbrtRegisteredNode.append(node)
            mplugin.registerNode(
                node.nodeName(),
                node.nodeId(),
                node.nodeCreator,
                node.nodeInitializer,
                node.nodeType(),
                node.nodeClassify()
                
            )
            
            AETemplateName = "AE"+nodeName+"Template"
            try:
                __import__('PBRT.AETemplates', fromlist=[AETemplateName])
                module = sys.modules['PBRT.AETemplates.'+AETemplateName]
                reload(module)
            except ImportError:
                OpenMaya.MGlobal.displayError( "Failed to load "+AETemplateName )

        if OpenMaya.MGlobal.mayaState() == OpenMaya.MGlobal.kInteractive:
            # Create Top menu
            mainMenu().make()
            
        
        OpenMaya.MGlobal.displayInfo('PBRTMayaPy: Plugin loaded')

    except:
        OpenMaya.MGlobal.displayError( "Failed to register PBRT Plugin" )
        raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    """
    Unregister all commands and nodes etc that the initializePlugin() method registered with Maya
    """
     
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        # deregister commands
        for command in pbrtCommands:
            mplugin.deregisterCommand ( command.commandName() )
    
        # deregister nodes
        for node in pbrtRegisteredNode:
            mplugin.deregisterNode( node.nodeId() )

        # OpenMaya.MGlobal.displayInfo("Plugin Removed OK.")
    except:
        OpenMaya.MGlobal.displayError( "Failed to deregister plugin" )
        raise