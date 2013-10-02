# ------------------------------------------------------------------------------
# PBRT exporter for Maya 2013
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# GUI builder command
#
# ------------------------------------------------------------------------------

from maya import cmds
from maya import mel


class mMenu:
    """
    GUI helper class to construct window menus.
    """
    
    mName = str()
    def __init__(self, label, helpMenu = False, parent = False, tearOff = False ):
        """
        Start a new menu with the gIven options.
        """
        
        if parent == False:
            self.mName = cmds.menu( label = label, helpMenu = helpMenu, tearOff = tearOff )
        else:
            self.mName = cmds.menu( label = label, helpMenu = helpMenu, tearOff = tearOff, parent = parent )
    
    def getName(self):
        """
        Return the name of the created menu object
        """
        
        return self.mName
        
    def addItem(self, label, command, subMenu = False, divider = False, parent = False):
        """
        Add an item (or submenu) to this menu object.
        """
        
        if parent == False:
            return cmds.menuItem( label = label, command = command, parent = self.mName, divider = divider, subMenu = subMenu)
        else:
            return cmds.menuItem( label = label, command = command, divider = divider, subMenu = subMenu, parent = parent)
        
    def end(self):
        """
        End this menu object. No more items can be added.
        """
        
        cmds.setParent( '..', menu = True)


class mainMenu:
    def exportAndRender(self,*args):
        mel.eval('pbrt_export()')

    def makeRenderSettings(self,*args):
        import pbrt_settings
        if not cmds.objExists('pbrt_settings'):
            settings = pbrt_settings.pbrt_settings()   
            settings.checkAndAddAttributes()
        cmds.select('pbrt_settings')       
        

    def createNewTextObject(self,*args):
        textObject = cmds.createNode('pbrtTextObject')
        parentTransform = cmds.listRelatives(textObject, allParents=True)[0]
        cmds.rename(parentTransform,textObject.replace('Object','Transform'))


    def make(self):
        """
        Make the main pbrt menu which resides in the Rendering menuSet
        """
        
        gMainWindow = mel.eval('$tmpVar=$gMainWindow')
        
        pbrtMenu = mMenu(label = 'PBRT', parent = gMainWindow, tearOff = True )
        pbrtMenu.addItem( label = "Export and Render" , command =self.exportAndRender  )
        pbrtMenu.addItem( label = "Render Globals" , command = self.makeRenderSettings )
        pbrtMenu.addItem( label = "Create Text Object" , command = self.createNewTextObject )

        pbrtMenu.end()
        
        renderMS = mel.eval('findMenuSetFromLabel("Rendering")')
        cmds.menuSet( currentMenuSet = renderMS )
        menuIndex  = cmds.menuSet( query = True, numberOfMenus = True)
        cmds.menuSet( insertMenu = (pbrtMenu.getName(), menuIndex) )
        pbrtMenu.end()
