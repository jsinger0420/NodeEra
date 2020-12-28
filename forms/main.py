# -*- coding: utf-8 -*-

''' 
    UC-01 Main Window / Main Menu
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
'''
import sys
import os
import logging
import ntpath

from PyQt5.QtCore import pyqtSlot, QSettings, QSize, QPoint, QFileInfo, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QApplication
from PyQt5.QtGui import QIcon, QPixmap

from core.helper import Helper, PageSetup
from core.pageitem import PageItem
from core.NeoDriver import NeoDriver

from forms.Ui_main import Ui_NodeeraMain
from forms.dlgNeoCon import dlgNeoCons
from forms.tabPageWidget import PageWidget
from forms.cypherPageWidget import CypherPageWidget
from forms.projectPageWidget import ProjectPageWidget
from forms.systemPreferenceBox import SystemPreferenceBox
from forms.INodeFormatDlg import INodeFormat
from forms.IRelFormatDlg import IRelFormat
from forms.TNodeFormatDlg import TNodeFormat
from forms.TRelFormatDlg import TRelFormat
from forms.OnlineHelpDLG import OnlineHelpDLG
from forms.HelpAboutDLG import HelpAboutDLG
from forms.GenerateSchemaDlg import GenerateSchemaDlg
from forms.HelloUserDlg import HelloUserDlg


unNamedFileCounter = 0
MODENEW = 1
MODEEDIT = 2
LABEL, REQUIRED = range(2)
PROPERTY, REQUIRED, PK = range(3)

productName = 'NodeEra' 
currentVersion = '2020.12.01' 


def my_excepthook(type, value, tback):
    '''
    catch any exception not otherwise handled by the application and show it to the user without crashing the program.
    '''    
    msg = "### {}--{}--{} ###".format(type, value, tback.tb_frame)
    clipboard = QApplication.clipboard() 
    clipboard.setText(msg)
    # display error message to the user
    helper = Helper()
    helper.displayErrMsg("Unexpected Error", """
An unexpected error has occured.

Please paste this error message into an email to nodeerainfo@singerlinks.com (it's already in the clipboard)

{}
    """.format(msg))
    # log the error
    if logging:
        logging.info("An unexpected error has occured. \n {}".format(msg))       

'''
call the exception handler if debug mode is off
'''
if not '-d' in sys.argv:
    sys.excepthook = my_excepthook  

class NodeeraMain(QMainWindow, Ui_NodeeraMain):

    displayWelcomeMsg = pyqtSignal(str)
    closeWelcomeMsg = pyqtSignal()
    
    """
    Create Ui_NodeeraMain and display it.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(NodeeraMain, self).__init__(parent)
        self.setupUi(self)
        self.parent=parent
        
        # object data
        self.pageDict = {}
        self.curPage = None
        self.helper = Helper()        
        
        # get startup settings
        self.initSettings()     
        
        # launch the welcome wagon
        self.welcomeDlg = HelloUserDlg(self)
        self.welcomeDlg.show()
        QApplication.processEvents()
        self.displayWelcomeMsg.emit("Starting NodeEra...")
        
        # setup stuff not covered by generated code
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/RUN and DATA TAB/Disconnected.png"), QIcon.Normal, QIcon.Off)
        self.actionOpen_Connection.setIcon(icon)
        
        # main window
        self.setTitle("No Connection")   
        self.resize(self.winSize)
        self.move(self.position)

        # display welcome message
        self.displayWelcomeMsg.emit("Welcome To NodeEra")
        
        # auto open last used connection
        try:
            lastNeoConName = self.settings.value("NeoCon/LastUsed") 
            if not lastNeoConName  is None:
                neoDict=self.settings.value("NeoCon/connection/{}".format(lastNeoConName))
                self.openConnection(neoConName=lastNeoConName,  neoConDict=neoDict)  
                self.displayWelcomeMsg.emit("Opened most recent connection: {}".format(lastNeoConName))
                
            self.setTitle(lastNeoConName)
            
        except:
            self.logMsg("Unable to open last connection: {}".format(lastNeoConName))
            self.displayWelcomeMsg.emit("Unable to open last connection: {}".format(lastNeoConName))
        # auto close the welcome dialog box
        self.closeWelcomeMsg.emit()
            
    def logMsg(self, msg):
        if logging:
            logging.info(msg)            
    
    def initSettings(self, ):
        '''
        get the system settings needed to start NodeEra.
        If a system setting doesn't exist then create it with default value - this happens on initial startup
        '''
        self.settings = QSettings()
        try:
            self.expirationDate = self.helper.getText(self.settings.value("License/expirationDate"))
            if self.expirationDate is None:
                self.expirationDate = 'No expiration date set'
                self.settings.setValue("License/expirationDate",self.helper.putText(self.expirationDate))
        except:
            self.expirationDate = 'No expiration date set'
            self.settings.setValue("License/expirationDate",self.helper.putText(self.expirationDate))
            
        try:
            self.currentVersion = self.settings.value("License/currentVersion")
            if self.currentVersion is None:
                self.currentVersion = currentVersion
                self.settings.setValue("License/currentVersion",self.currentVersion)
            elif self.currentVersion != currentVersion:
                self.currentVersion = currentVersion
                self.settings.setValue("License/currentVersion",self.currentVersion)                
        except:
            self.currentVersion = currentVersion
            self.settings.setValue("License/currentVersion",self.currentVersion)
            
        try:
            self.winSize = self.settings.value("MainWindow/Size")
            if self.winSize is None:
                self.winSize = QSize(800, 500)
        except:
            self.winSize = QSize(800, 500)  
                    
        try:
            self.position = self.settings.value("MainWindow/Position")
            if self.position is None:
                self.position = QPoint(0, 0)
        except:
            self.position = QPoint(0, 0)

        try:
            self.recentList = self.settings.value("Default/RecentList")
            if self.recentList is None:
                self.recentList = []
                self.settings.setValue("Default/RecentList",self.recentList) 
        except:
            self.recentList = []
            self.settings.setValue("Default/RecentList",self.recentList) 

        try:
            self.defaultLoggingPath = self.settings.value("Default/LoggingPath")
            if self.defaultLoggingPath is None:
                self.logDir = os.getcwd()
                self.logDir = os.path.realpath(os.path.abspath(self.logDir))
                self.settings.setValue("Default/LoggingPath",self.logDir)            
        except:
            self.logDir = os.getcwd()
            self.logDir = os.path.realpath(os.path.abspath(self.logDir))
            self.settings.setValue("Default/LoggingPath",self.logDir)            
            
        try:
            self.defaultProjPath = self.settings.value("Default/ProjPath")
            if self.defaultProjPath is None:
                self.defaultProjPath = os.getcwd()
                self.defaultProjPath = os.path.realpath(os.path.abspath(self.defaultProjPath))
                self.settings.setValue("Default/ProjectPath",self.defaultProjPath)                            
        except:
            self.defaultProjPath = os.getcwd()
            self.defaultProjPath = os.path.realpath(os.path.abspath(self.defaultProjPath))
            self.settings.setValue("Default/ProjectPath",self.defaultProjPath)          
            
        # default custom formats for diagram objects
        # Display Format - Instance Node
        try:
            test = self.settings.value("Default/Format/InstanceNode")
            if test is None:
                self.settings.setValue("Default/Format/InstanceNode",INodeFormat().formatDict)
        except:
            self.settings.setValue("Default/Format/InstanceNode",INodeFormat().formatDict)
        
        # Display Format - Instance Relationship 
        try:
            test = self.settings.value("Default/Format/InstanceRelation")
            if test is None:
                self.settings.setValue("Default/Format/InstanceRelation",IRelFormat().formatDict)
        except:
            self.settings.setValue("Default/Format/InstanceRelation",IRelFormat().formatDict)
        
        # Display Format - Template Node
        try:
            test = self.settings.value("Default/Format/TemplateNode")
            if test is None:
                self.settings.setValue("Default/Format/TemplateNode",TNodeFormat().formatDict)
        except:
            self.settings.setValue("Default/Format/TemplateNode",TNodeFormat().formatDict)
        
        # Display Format - Template Relationship 
        try:
            test = self.settings.value("Default/Format/TemplateRelation")
            if test is None:
                self.settings.setValue("Default/Format/TemplateRelation",TRelFormat().formatDict)
        except:
            self.settings.setValue("Default/Format/TemplateRelation",TRelFormat().formatDict)        
        
        # page setup
        try:
            test = self.settings.value("Default/PageSetup")
            if test is None:
                self.settings.setValue("Default/PageSetup",PageSetup().objectDict)
        except:
            self.settings.setValue("Default/PageSetup",PageSetup().objectDict)      
        
        # default project neocon
        try:
            defaultNeoConName = self.settings.value("NeoCon/Default") 
            if defaultNeoConName is None:
                self.settings.setValue("NeoCon/Default", "LOCAL")
        except:
            self.settings.setValue("NeoCon/Default", "LOCAL")

        # LOCAL neocon definition
        try:
            self.localNeoCon = self.settings.value("NeoCon/connection/LOCAL")
            if self.localNeoCon is None:
                self.settings.setValue("NeoCon/connection/LOCAL", NeoDriver().localNeoConDict())
        except:
            self.settings.setValue("NeoCon/connection/LOCAL", NeoDriver().localNeoConDict())
            
        # default lexer font size
        try:
            defaultLexerFontSize = self.settings.value("Lexer/FontSize") 
            if defaultLexerFontSize is None:
                self.settings.setValue("Lexer/FontSize", "10")
        except:
            self.settings.setValue("Lexer/FontSize", "10")        

        # validate all neocons have the prompt dictionary key which was added in 1.04
        self.settings.beginGroup("NeoCon/connection")
        neoKeys = self.settings.childKeys()
        for key in neoKeys:
            neoDict=self.settings.value(key)
            promptVal = neoDict.get("prompt", None)
            if promptVal is None:
                neoDict["prompt"] = "False"
                self.settings.setValue(key,neoDict)
                
        self.settings.endGroup()
        

    def setTitle(self, filename):
        self.setWindowTitle("{} - {}".format(productName, filename))

    def setMenuAccess(self, ):
        '''
        determine what connection tab is currently selected and enable/disable menu items as needed
        '''
        # turn on all Settings menu items
        for action in self.menuSettings.actions():
            if type(action) == QAction and not action.isSeparator():
                action.setEnabled(True)

        try:
            # get tab widget (schema or project) that is currently active - if there isn't one this will cause an exception
            currentTab = self.stackedPageItems.currentWidget().tabPage.currentWidget()
            # enable all the schema actions
            for action in self.menuNeo.actions():
                if type(action) == QAction and not action.isSeparator():
                    action.setEnabled(True)
            for action in self.menuProject.actions():
                # enable project actions
                if type(action) == QAction and not action.isSeparator():
                    if currentTab.pageType == "PROJECT":
                        action.setEnabled(True)
                    else:
                        if action.text() in ["New", "Open...", "Recent Projects"]:
                            action.setEnabled(True)
                        else:
                            action.setEnabled(False)
                    
        except:
                # no connection tabs are open
                # disable all project menu actions
                for action in self.menuProject.actions():
                    if type(action) == QAction and not action.isSeparator():
                        action.setEnabled(False)                        
                for action in self.menuNeo.actions():
                    if type(action) == QAction and not action.isSeparator():
                        if action.text() in ["Close Connection", "Generate Schema..."]:
                            action.setEnabled(False)
                        else:
                            action.setEnabled(True) 
                            
                        
    ########################################################################
    #     NEO CONNECTION Dropdown Menu Actions
    ########################################################################
    @pyqtSlot()
    def on_actionOpen_Connection_triggered(self):
        """
        This slot provides functionality for the open connection button
        """
        d = dlgNeoCons(parent=self)
        if d.exec_():
            if d.selectedNeoConName:
                # make sure it isn't already opened
                if d.selectedNeoConName not in self.pageDict:
                    self.openConnection(neoConName=d.selectedNeoConName, neoConDict=d.selectedNeoConDict)
                else:
                    self.helper.displayErrMsg("NodeEra - Open Connection","Connection {} is already open.".format(d.selectedNeoConName) )
                    # switch to the page they tried to open
                    self.pageDict[d.selectedNeoConName].actionButton.trigger()

    def openConnection(self, neoConName=None,  neoConDict=None):
        '''
        User selects a connection to open so create the schema page and display it
        '''
        # set the last used neocon in system settings
        self.settings.setValue("NeoCon/LastUsed", neoConName )
        # create a new toolbar button and add it to the toolbar
        newConAction = QAction(self)
        newConAction.setObjectName("newConnection") 
        newConAction.setText("Neo4j - {}".format(neoConName)) 
        newConAction.setData(neoConName)
        
        newConAction.setToolTip(neoConDict["URL"])
        newConAction.setCheckable(True)
        newConAction.setChecked(True)
        newConAction.triggered.connect(self.connectionClicked) 
        self.tbConnection.addAction(newConAction)

        # add a tabPage widget to the stacked widget
        newPageWidget = PageWidget(parent=self)
        newPageWidget.pageType = "Schema"
        widgetIndex = self.stackedPageItems.addWidget(newPageWidget)
        # save new pageItem
        newPageItem = PageItem(neoConName=neoConName, actionButton=newConAction, pageWidget=newPageWidget, pageWidgetIndex=widgetIndex)
        self.pageDict[neoConName] = newPageItem
        # add the schema tab
        cypherTab = CypherPageWidget(parent=self, pageItem=newPageItem)
        newPageWidget.tabPage.addTab(cypherTab, "Schema - {}".format(neoConName))     

        # click the new action to force selection logic
        newConAction.trigger()
        self.logMsg("Open Connection: {}".format(neoConName))

        
    @pyqtSlot()
    def connectionClicked(self):
        '''
        User clicks on a connection in the menu bar so switch to that stacked widget
        '''
        self.logMsg("connection clicked {}".format(self.sender().text()))
        # uncheck all the page action buttons
        for pageName in self.pageDict:
            self.pageDict[pageName].actionButton.setChecked(False)
        # check the one just clicked
        self.sender().setChecked(True)
        # save the current page name 
        self.curPage = self.sender().data()
        # switch the stacked page widget to the one just clicked      
        self.stackedPageItems.setCurrentIndex(self.pageDict[self.curPage].pageWidgetIndex)
        # update the main window title
        self.setTitle(self.curPage)
        # adjust the menu items
        self.setMenuAccess()
        
    @pyqtSlot()
    def on_actionClose_Connection_triggered(self):
        """
        Close the active connection and remove the page from the UI
        """
        if self.curPage:
            if self.curPage in self.pageDict:
                # must find the schema tab and tell it to close, it will tell all other tabs to close.  schema tab is always the first one (index=0)
                self.pageDict[self.curPage].pageWidget.closeSchemaTab()
                self.removeConnection()

    def removeConnection(self, ):
        '''if the tab page widget is responding to the close request it only needs this logic to remove the connection
        '''
        curPage = self.pageDict.get(self.curPage, None)
        if not curPage is None:
            # remove the pageWidget from the stacked widget
            self.stackedPageItems.removeWidget(self.pageDict[self.curPage].pageWidget)
            del self.pageDict[self.curPage].pageWidget
            # remove the action from menu's and toolbars
            self.tbConnection.removeAction(self.pageDict[self.curPage].actionButton)
            # take the page out of the dictionary
            del self.pageDict[self.curPage]
            # if any pages left select the first one
            if len(self.pageDict) > 0:
                for pageName in self.pageDict:
                    self.pageDict[pageName].actionButton.trigger()
                    break
            else:
                # there are no open connections and the home page is closed
                self.setTitle("No Connection")   
                    
    @pyqtSlot()
    def on_actionNeo4j_Connection_Manager_triggered(self):
        """
        Display the Connection Manager
        """
        d = dlgNeoCons(parent=self)
        if d.exec_():
            pass
            
    @pyqtSlot()
    def on_actionExit_triggered(self):
        """
        User selected the File / Exit menu item.  Tell all the open connections to close
        """
        self.closeOpenStuff()
        # close the app
        self.close()
        
    def closeEvent(self, event):
        # close open connections
        self.closeOpenStuff()
        #save the window state
        self.settings.setValue("MainWindow/Size", self.size())
        self.settings.setValue("MainWindow/Position", self.pos())

        event.accept()

    def closeOpenStuff(self):
        # get a list of all the keys in the pageDict dictionary
        keys = list(self.pageDict.keys())
        # iterate thru the list of dictionary keys.  this is required as the dictionary will be changing size, i.e. you can't simply iterate thru the dictionary
        for key in keys:
            pageItem = self.pageDict[key]
            actionButton = pageItem.actionButton
            actionButton.trigger()
            # must find the schema tab and tell it to close, it will tell all other tabs to close.  schema tab is always the first one (index=0)
            pageItem.pageWidget.closeSchemaTab()
            self.removeConnection()                
            
#####################################################################
# SETTINGS DROPDOWNS
#####################################################################
    @pyqtSlot()
    def on_actionSystem_Preferences_triggered(self):
        """
        User selects the System Preferences menu item.  Display the system preferences dialog box.
        """
        self.editSystemPreferences()
        
    def editSystemPreferences(self, ):
        """
        User selects the System Preferences menu item.  Display the system preferences dialog box.
        """
        if not (self.settings is None):
            d = SystemPreferenceBox(self, settings = self.settings)
            if d.exec_():
                self.settings.sync()

#####################################################################
# PROJECT METHODS
#####################################################################


    @pyqtSlot()
    def on_actionNewProject_triggered(self):
        """
        Open new project
        """
        self.loadProject(fileName = None)
    
    @pyqtSlot()
    def on_actionOpenProject_triggered(self):
        """
        Open an existing project file
        """
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setNameFilters(["NodeEra Project (*.mdl)","all files (*.*)"])
        dlg.setDirectory(self.settings.value("Default/ProjPath"))
        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            if fileNames:
                fileName = fileNames[0]
                self.loadProject(fileName = fileName)
    
    
    @pyqtSlot()
    def on_actionSaveProject_triggered(self):
        """
        Save the open project
        """
        curPageWidget = self.stackedPageItems.currentWidget()
        if not curPageWidget is None:
            if curPageWidget.tabPage.currentWidget().pageType == "PROJECT":
                newName = curPageWidget.tabPage.currentWidget().saveProject()
                # if this was an unsaved project then it was really a save as so the tab name has to be updated
                if newName is not None:
                    curPageWidget.tabPage.setTabText(curPageWidget.tabPage.currentIndex(),"Project: {} - {}".format(newName, self.pageDict[self.curPage].neoConName))
            
    @pyqtSlot()
    def on_actionSaveProjectAs_triggered(self):
        """
        Save Project As
        """
        curPageWidget = self.stackedPageItems.currentWidget()
        if not curPageWidget is None:
            if curPageWidget.tabPage.currentWidget().pageType == "PROJECT":
                newName = curPageWidget.tabPage.currentWidget().saveProjectAs()
                if newName is not None:
                    curPageWidget.tabPage.setTabText(curPageWidget.tabPage.currentIndex(),"Project: {} - {}".format(newName, self.pageDict[self.curPage].neoConName))
            
    @pyqtSlot()
    def on_actionReverse_Engineer_triggered(self):
        """
        User selects the Reverse Engineer menu item.  Display the Reverse Engineer dialog box.
        """
        curPageWidget = self.stackedPageItems.currentWidget()
        if not curPageWidget is None:
            if curPageWidget.tabPage.currentWidget().pageType == "PROJECT":
                curPageWidget.tabPage.currentWidget().reverseEngineerGraph()
            else:
                self.helper.displayErrMsg("Reverse Engineer","{} not a project".format(curPageWidget.tabPage.currentWidget().pageType))
            
    @pyqtSlot()
    def on_actionProjectProperties_triggered(self):
        """
        User selects the project properties menu item. Display the project properties dialog box.
        """
        curPageWidget = self.stackedPageItems.currentWidget()
        if not curPageWidget is None:
            if curPageWidget.tabPage.currentWidget().pageType == "PROJECT":
                curPageWidget.tabPage.currentWidget().editProjectProperties()
            else:
                self.helper.displayErrMsg("Project Properties","{} not a project".format(curPageWidget.tabPage.currentWidget().pageType))

    def getSchemaObject(self, ):
        curPageWidget = self.stackedPageItems.currentWidget()
        for ctr in range(0, curPageWidget.tabPage.count()):
            tab = curPageWidget.tabPage.widget(ctr)
            if tab.pageType == "CYPHER":
                return tab.schemaModel
        return None
    
    def getSchemaTab(self, ):
        curPageWidget = self.stackedPageItems.currentWidget()
        for ctr in range(0, curPageWidget.tabPage.count()):
            tab = curPageWidget.tabPage.widget(ctr)
            if tab.pageType == "CYPHER":
                return tab
        return None
                
    def loadProject(self, fileName=None):
        '''
        Load the project file with name fileName.  If fileName is None, create a new empty project.
        '''

        # create a temporary file name if its a new project
        if fileName is None:
            # update unnamed file counter
            global unNamedFileCounter
            unNamedFileCounter = unNamedFileCounter + 1
            shortName = "{}".format("New Project-0{}".format(unNamedFileCounter))
        else:
            head, shortName = ntpath.split(QFileInfo(fileName).fileName())
        
        # make sure the project isn't already loaded
        curPageWidget = self.stackedPageItems.currentWidget()
        for ctr in range(0, curPageWidget.tabPage.count()):
            tab = curPageWidget.tabPage.widget(ctr)
            if tab.pageType == "PROJECT":  
                if (not fileName is None) and (tab.fileName == fileName):
                    self.helper.displayErrMsg("Open Project", "The project file: {} is already open.  It can only be open once.".format(fileName))
                    return
            
        # create the project widget
        projectTab = ProjectPageWidget(parent=self, settings=self.settings, pageItem=self.pageDict[self.curPage], fileName = fileName)

        curPageWidget = self.stackedPageItems.currentWidget()
        
        # add the project widget as a tab on the current page widget     
        x = curPageWidget.tabPage.addTab(projectTab, "Project: {} - {}".format(shortName, self.pageDict[self.curPage].neoConName)) 
        curPageWidget.tabPage.setCurrentIndex(x)
        
    @pyqtSlot()
    def on_actionOnline_Help_triggered(self):
        """
        User selects the Online Help menu item.  Dislay Online Help menu.
        """
        d = OnlineHelpDLG(self)
        if d.exec_():
            pass
        
    @pyqtSlot()
    def on_actionAbout_triggered(self):
        """
        User selects Help / About menu item.  Display the about dialog box
        """
        d = HelpAboutDLG(self)
        if d.exec_():
            pass
    
    @pyqtSlot()
    def on_actionGenerate_Schema_triggered(self):
        """
        User requests the generate schema dialog box from main menu
        """
        d = GenerateSchemaDlg(self)
        if d.exec_():
            pass
    
    @pyqtSlot()
    def on_actionForward_Engineer_triggered(self):
        """
        User requests to perform forward engineering from the open project from main menu
        """
        curPageWidget = self.stackedPageItems.currentWidget()
        if not curPageWidget is None:
            if curPageWidget.tabPage.currentWidget().pageType == "PROJECT":
                curPageWidget.tabPage.currentWidget().forwardEngineerGraph()
            else:
                self.logMsg("User requested to forward engineer but current tab is not a Project")
    
    @pyqtSlot()
    def on_actionGenerate_Reports_triggered(self):
        """
        User selects the Generate Project Reports menu item.  Display the Generate Reports dialog box.
        """
        curPageWidget = self.stackedPageItems.currentWidget()
        if not curPageWidget is None:
            if curPageWidget.tabPage.currentWidget().pageType == "PROJECT":
                curPageWidget.tabPage.currentWidget().generateProjectReports()
    
    @pyqtSlot()
    def on_actionReset_User_Password_triggered(self):
        """
        User requests the change user password from main menu
        """
        curPageWidget = self.stackedPageItems.currentWidget()
        if not curPageWidget is None:
            if curPageWidget.tabPage.currentWidget().pageType == "CYPHER":
                curPageWidget.tabPage.currentWidget().resetPassword()
    
    @pyqtSlot(QAction)
    def on_menuRecent_Projects_triggered(self, action):
        """
        User clicked on a recent file menu item
        
        @param action DESCRIPTION
        @type QAction
        """
        self.loadProject(fileName = action.data())
    
    @pyqtSlot()
    def on_menuRecent_Projects_aboutToShow(self):
        """
        user hovering on recent projects menu item
        """
        recentList = self.settings.value("Default/RecentList")
        if len(recentList) == 0:
            return
        else:
            # remove any existing actions
            self.menuRecent_Projects.clear()
            for projectFile in recentList:
                # create actions for the recent files
                aSubAction = self.menuRecent_Projects.addAction(projectFile)
                aSubAction.setData(projectFile)
       
