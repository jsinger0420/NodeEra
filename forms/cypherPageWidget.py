# -*- coding: utf-8 -*-

"""
    UC-04 Schema/Cypher Page
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
import ntpath
import logging
from operator import itemgetter

from PyQt5.QtCore import pyqtSlot, QFileInfo, Qt, pyqtSignal, QModelIndex, QSettings
from PyQt5.QtWidgets import QWidget, QFileDialog, QFileSystemModel, QMenu, QTreeWidgetItem, QInputDialog, QApplication
from PyQt5.Qsci import QsciScintilla

from .Ui_cypherPageWidget import Ui_CypherPageWidget
from .CypherEditGridWidget import CypherEditGridWidget
#from core.neocon import NeoCon
from core.NeoDriver import NeoDriver
from core.SchemaModel import SchemaModel
from core.helper import Helper
from forms.CreateIndexDlg import CreateIndexDlg
from forms.ConstraintNodeKeyDlg import ConstraintNodeKeyDlg
from forms.ConstraintNodePropExistsDlg import ConstraintNodePropExistsDlg
from forms.ConstraintNodePropUniqueDlg import ConstraintNodePropUniqueDlg
from forms.ConstraintRelPropExistsDlg import ConstraintRelPropExistsDlg
from forms.EditUserDlg import EditUserDlg
from forms.EditRoleDlg import EditRoleDlg
from forms.GenerateSchemaDlg import GenerateSchemaDlg
from forms.ChangeUserPW import ChangeUserPW

from forms.DropObjectDlg import DropObjectDlg

unNamedFileCounter = 0
MODENEW = 1
MODEEDIT = 2

class CypherPageWidget(QWidget, Ui_CypherPageWidget):
    """
    Implements a tab on the main UI that provides the schema editor, cypher editor, and file explorer.
    """
    treeViewUpdate = pyqtSignal()
    def __init__(self, parent=None, pageItem=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(CypherPageWidget, self).__init__(parent)
        self.pageType = "CYPHER"
        self.settings = QSettings()
        self.parent=parent
        self.pageItem=pageItem
        
        self.setupUi(self)
        self.initUI()
        self.helper = Helper()
        self.treeViewUpdate.connect(self.populateTree)
        
        ########################################################################
        # Schema editor setup
        ########################################################################
        self.schemaNeoDriver = NeoDriver(name=self.pageItem.neoConName, promptPW=self.pageItem.promptPW)
       
        self.schemaModel = SchemaModel(self, neoDriver = self.schemaNeoDriver)
        self.refreshSchemaModel()
        self.schemaModel.setUpdateTreeViewMethod(method=self.on_btnRefresh_clicked)
        self.tvSchema.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tvSchema.customContextMenuRequested.connect(self.openMenu)
        self.clearTree()
        self.populateTree()
        
        # display a default cypher tab
        self.on_btnNew_clicked()
        

        # display an error message if the schema connection doesn't work
        rc, msg = self.schemaModel.testSchemaConnection()
        if  rc == False:
            self.helper.displayErrMsg("Connect Schema", "The Connection Failed: {}".format(msg)) 
           
    def logMsg(self, msg):
        '''
        If logging is active, then log the message
        '''
        if logging:
            logging.info(msg)        
        
##############################################################################
#   UI setups not generated
##############################################################################
    def initUI(self):
        
        try:
            self.defaultProjPath = self.settings.value("Default/ProjPath")
            if self.defaultProjPath is None:
                self.defaultProjPath = '//'
        except:
            self.defaultProjPath = '//'     

        self.currentProjPath = self.defaultProjPath
        self.setUpFileExplorer(self.defaultProjPath)

       
#########################################################################################
# schema tree view methods
#########################################################################################
    def clearTree(self, ):
        self.editNeo4j.clear()
        self.tvSchema.clear()
        self.tvSchema.setColumnCount(1)
        self.tvSchema.setHeaderLabels(["Schema Items"])
        self.tvSchema.setItemsExpandable(True)

    def populateTree(self, addObject=None):
        # put neocon url in text box above the tree view
        self.editNeo4j.setText("{} - {}".format( self.schemaNeoDriver.name, self.schemaNeoDriver.neoDict["URL"]))
        #selected = None
        self.tvSchema.clear()
        self.tvSchema.setColumnCount(1)
        self.tvSchema.setHeaderLabels(["Schema Items"])
        self.tvSchema.setItemsExpandable(True)
        nodeTypes = {}
        parent = self.tvSchema.invisibleRootItem()
        # add tree items
        for item in self.schemaModel.schemaData["TopLevel"]:
            topItem = self.addParent(parent, 0, item, "data")
            nodeTypes[item]=topItem
            for object in sorted(self.schemaModel.schemaData[item], key=itemgetter('name')) :
#                childItem = self.addChild(topItem, 0, object["name"], "data")          
                self.addChild(topItem, 0, object["name"], "data")    
                
        self.tvSchema.resizeColumnToContents(0)
        
    def addParent(self, parent, column, title, data):
        item = QTreeWidgetItem(parent, [title])
        item.setData(column, Qt.UserRole, data)
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        return item

    def addChild(self, parent, column, title, data):
        item = QTreeWidgetItem(parent, [title, ])
        item.setData(column, Qt.UserRole, data)
        return item
        
#####################################################################################
# Context menus for schema tree view
#####################################################################################
    def openMenu(self,position):
        selected = self.tvSchema.currentItem()
        if not (selected is None):
            parent = self.tvSchema.currentItem().parent()
            # top level object menus
            if (parent is None):
                menu = QMenu()
                if (selected.data(0,0) == "User"):
                    self.addMenu(menu=menu, text="New...", method=self.newUser)
                    self.addMenu(menu=menu, text="Generate Create(s)...", method=self.genCreates)
                    self.addMenu(menu=menu, text="Generate Drop(s)...", method=self.genDrops)
                if (selected.data(0,0) == "Role"):
                    self.addMenu(menu=menu, text="New...", method=self.newRole)
                    self.addMenu(menu=menu, text="Generate Create(s)...", method=self.genCreates)
                    self.addMenu(menu=menu, text="Generate Drop(s)...", method=self.genDrops)
                if (selected.data(0,0) == "Index"):
                    self.addMenu(menu=menu, text="New...", method=self.newIndex)
                    self.addMenu(menu=menu, text="Generate Create(s)...", method=self.genCreates)
                    self.addMenu(menu=menu, text="Generate Drop(s)...", method=self.genDrops)
                if (selected.data(0,0) == "Relationship Property Exists"):
                    self.addMenu(menu=menu, text="New...", method=self.newConstraintRelPropExists)
                    self.addMenu(menu=menu, text="Generate Create(s)...", method=self.genCreates)
                    self.addMenu(menu=menu, text="Generate Drop(s)...", method=self.genDrops)
                if (selected.data(0,0) == "Node Key"):
                    self.addMenu(menu=menu, text="New...", method=self.newConstraintNodeKey)
                    self.addMenu(menu=menu, text="Generate Create(s)...", method=self.genCreates)
                    self.addMenu(menu=menu, text="Generate Drop(s)...", method=self.genDrops)
                if (selected.data(0,0) == "Node Property Unique"):
                    self.addMenu(menu=menu, text="New...", method=self.newConstraintNodePropUnique)
                    self.addMenu(menu=menu, text="Generate Create(s)...", method=self.genCreates)
                    self.addMenu(menu=menu, text="Generate Drop(s)...", method=self.genDrops)
                if (selected.data(0,0) == "Node Property Exists"):
                    self.addMenu(menu=menu, text="New...", method=self.newConstraintNodePropExists)
                    self.addMenu(menu=menu, text="Generate Create(s)...", method=self.genCreates)
                    self.addMenu(menu=menu, text="Generate Drop(s)...", method=self.genDrops)
                # pop up the menu
                menu.exec_(self.tvSchema.mapToGlobal(position))  
            
            # object instance pop up menus
            if not(parent is None):
                menu = QMenu()
                if parent.data(0,0) == "Label":
                    self.addMenu(menu=menu, text="Generate Match...", method=self.matchSchemaObject)
                if parent.data(0,0) == "Property":
                    self.addMenu(menu=menu, text="Generate Match...", method=self.matchSchemaObject)
                if parent.data(0,0) == "Relationship":
                    self.addMenu(menu=menu, text="Generate Match...", method=self.matchSchemaObject)
                if parent.data(0,0) == "User":
                    self.addMenu(menu=menu, text="Edit...", method=self.editUser)
                    self.addMenu(menu=menu, text="Drop...", method=self.dropSchemaObject)
                if parent.data(0,0) == "Role":
                    self.addMenu(menu=menu, text="Edit...", method=self.editRole)
                    self.addMenu(menu=menu, text="Drop...", method=self.dropSchemaObject)
                if parent.data(0,0) == "Index":
                    self.addMenu(menu=menu, text="Drop...", method=self.dropSchemaObject)
                    self.addMenu(menu=menu, text="Generate Match...", method=self.matchSchemaObject)
                if parent.data(0,0) in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists"]:
                    self.addMenu(menu=menu, text="Drop...", method=self.dropSchemaObject)
                    self.addMenu(menu=menu, text="Generate Match...", method=self.matchSchemaObject)
                # pop up the menu
                menu.exec_(self.tvSchema.mapToGlobal(position))  
                
    def addMenu(self, menu=None, text=None, method=None):
        menuAction = menu.addAction(text)
        menuAction.triggered.connect(method)
        
##############################################################################
#   schema menu options
##############################################################################
    def resetPassword(self, ):
        """
        User requests the change user password from main menu
        """
        d = ChangeUserPW(parent=self)
        if d.exec_():
            pass
            
    def newUser(self, ):
        '''
        prompt for the new user name and bring up the user editor dialog box
        '''
        text, ok = QInputDialog.getText(self, 'Create New User', 'Enter the User Name:')
        if ok:
            # make sure they entered a valid user name
            # see if the user name already exists
            if text in [object["name"] for object in self.schemaModel.schemaData["User"]]:
                self.helper.displayErrMsg("Create New User", "The user {} already exists. Cannot create new user.".format(text)) 
            else:
                # create the user with requires password change on first login.
                QApplication.setOverrideCursor(Qt.WaitCursor)
                rc, msg = self.schemaModel.createUser(text)
                if rc:
                    self.schemaModel.updateTV()
                    QApplication.restoreOverrideCursor() 
                    #show the edit user dialog box 
                    d = EditUserDlg(self,  userName=text, mode="NEW")
                    if d.exec_():
                        self.on_btnRefresh_clicked()
                
                else:
                    self.helper.displayErrMsg("Create User Error", msg)
                    QApplication.restoreOverrideCursor()                
                
                
                

                    
    def editUser(self, ):
        '''
        edit an existing user
        '''
        d = EditUserDlg(self,  userName=self.tvSchema.currentItem().data(0,0), mode="EDIT")
        if d.exec_():
            self.on_btnRefresh_clicked()         
            
    def newRole(self, ):
        '''
        prompt for the new user name and bring up the user editor dialog box
        '''
        text, ok = QInputDialog.getText(self, 'Create New Role', 'Enter the Role Name:')
        if ok:
            # make sure they entered a valid Role Name
            
            # see if the user name already exists
            if text in [object["name"] for object in self.schemaModel.schemaData["Role"]]:
                self.helper.displayErrMsg("Create New Role", "The role {} already exists. Cannot create new role.".format(text)) 
            else:
                # create the role if needed
                QApplication.setOverrideCursor(Qt.WaitCursor)
                rc, msg = self.schemaModel.createRole(text)
                if rc:
                    self.schemaModel.updateTV()
                    QApplication.restoreOverrideCursor()    
                    d = EditRoleDlg(self, roleName=text, mode="NEW")
                    if d.exec_():
                        self.on_btnRefresh_clicked()                    
                else:
                    self.helper.displayErrMsg("Create Role Error", msg)
                    QApplication.restoreOverrideCursor()    
                


    def editRole(self, ):
        '''
        edit an existing role
        '''
        d = EditRoleDlg(self, roleName=self.tvSchema.currentItem().data(0,0), mode="EDIT")
        if d.exec_():
            self.on_btnRefresh_clicked()

        return
        
    def newIndex(self, ):
        d = CreateIndexDlg(self)
        if d.exec_():
            self.on_btnRefresh_clicked()

    def newConstraintNodeKey(self, ):
        d = ConstraintNodeKeyDlg(self)
        if d.exec_():
            self.on_btnRefresh_clicked()
            
    def newConstraintNodePropExists(self, ):
        d = ConstraintNodePropExistsDlg(self)
        if d.exec_():
            self.on_btnRefresh_clicked()
            
    def newConstraintNodePropUnique(self, ):
        d = ConstraintNodePropUniqueDlg(self)
        if d.exec_():
            self.on_btnRefresh_clicked()
            
    def newConstraintRelPropExists(self, ):
        d = ConstraintRelPropExistsDlg(self)
        if d.exec_():
            self.on_btnRefresh_clicked()

    def dropSchemaObject(self, type ):
        objectName = self.tvSchema.currentItem().data(0,0)
        objectType = self.tvSchema.currentItem().parent().data(0,0)
        d = DropObjectDlg(self, objectType=objectType, objectName=objectName)
        if d.exec_():
            self.on_btnRefresh_clicked()        
        return
        
    def matchSchemaObject(self, ):
        objectName = self.tvSchema.currentItem().data(0,0)
        objectType = self.tvSchema.currentItem().parent().data(0,0)
        cypher = self.schemaModel.genMatchFromConstraint(objectName=objectName, objectType=objectType)
        # add the comment
        editCypher = "// Generated by NodeEra from schema connection: {} \n// Match {} schema object: {} \n{}".format(self.pageItem.neoConName, objectType, objectName, cypher)
        self.addCypherEditorTab(fileName=None, fileText = editCypher, mode=MODENEW)      
        
        
    def genCreates(self, ):
        '''
        display the generate schema dialog with the object selected, and the generate create only option selected
        '''
        objectName = self.tvSchema.currentItem().data(0,0)   
        d = GenerateSchemaDlg(self.parent, objectType=objectName, genOption="CreateOnly")
        if d.exec_():
            pass

    def genDrops(self, ):
        '''
        display the generate schema dialog with the object selected, and the generate drop only option selected
        '''
        objectName = self.tvSchema.currentItem().data(0,0)   
        d = GenerateSchemaDlg(self.parent, objectType=objectName, genOption="DropOnly")
        if d.exec_():
            pass        
            
##############################################################################
#   signal slots
##############################################################################
    @pyqtSlot(int)
    def on_tabCypher_tabCloseRequested(self, index):
        """
        Process request to close a schema tab
        
        @param index DESCRIPTION
        @type int
        """
#        print("cypher tab index {} request close".format(str(index)))
        if self.tabCypher.widget(index).tabType == "CYPHER":
            self.tabCypher.widget(index).close() 
            self.tabCypher.removeTab(index)
        
##############################################################################
#   main buttons
##############################################################################
    @pyqtSlot()
    def on_btnUndo_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.tabCypher.count() > 0:
            if self.tabCypher.currentWidget().tabType == "CYPHER":
                self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_UNDO)
    
    @pyqtSlot()
    def on_btnRedo_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.tabCypher.count() > 0:
            if self.tabCypher.currentWidget().tabType == "CYPHER":
                self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_REDO)
        
        
    @pyqtSlot()
    def on_btnComment_clicked(self):
        """
        comment the selected lines.
        if no lines are selected, then comment the line where the cursor is.
        adds a single line comment "//" to the very beginning of each selected line.
        """
        if self.tabCypher.count() > 0:
            if self.tabCypher.currentWidget().tabType == "CYPHER":
                
                startPosition =  self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GETSELECTIONSTART)
                endPosition = self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GETSELECTIONEND)
                startLine = self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, startPosition)
                endLine  = self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, endPosition )
                if startPosition != endPosition:
                    # if there is a selection, then comment every line in the selection
                    for line in range(startLine, endLine+1):
                        self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GOTOLINE, line)
                        self.tabCypher.currentWidget().editor.insert("//")
                else:
                    # there is no selection, so comment the line where the cursor is
                    self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GOTOLINE, startLine)
                    self.tabCypher.currentWidget().editor.insert("//")
            
    @pyqtSlot()
    def on_btnUnComment_clicked(self):
        """
        uncomment the selected lines, if they have a comment. 
        only supports removing a single line comment "//" at the very beginning of the line.
        """
        if self.tabCypher.count() > 0:
            if self.tabCypher.currentWidget().tabType == "CYPHER":
                startPosition =  self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GETSELECTIONSTART)
                endPosition = self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GETSELECTIONEND)
                startLine = self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, startPosition)
                endLine  = self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, endPosition )
                if startPosition != endPosition:
                    # if there is a selection, then comment every line in the selection
                    for line in range(startLine, endLine+1):
                        self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GOTOLINE, line)
                        currentPos = self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
                        self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_SETSELECTIONSTART, currentPos)
                        self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_SETSELECTIONEND, currentPos+2)
                        # see if its a //
                        if self.tabCypher.currentWidget().editor.selectedText() == "//":
                            self.tabCypher.currentWidget().editor.removeSelectedText() 
                        else:
                            # this will remove the selection
                            self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GOTOLINE, startLine)
                else:
                    # there is no selection, so comment the line where the cursor is
                    self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GOTOLINE, startLine)
                    currentPos = self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
                    self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_SETSELECTIONSTART, currentPos)
                    self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_SETSELECTIONEND, currentPos+2)
                    # see if its a //
                    if self.tabCypher.currentWidget().editor.selectedText() == "//":
                        self.tabCypher.currentWidget().editor.removeSelectedText() 
                    else:
                        # this will remove the selection
                        self.tabCypher.currentWidget().editor.SendScintilla(QsciScintilla.SCI_GOTOLINE, startLine)

    @pyqtSlot()
    def on_btnRefresh_clicked(self):
        """
        This refreshes the schema treeview
        """
        self.refreshSchemaModel()

    @pyqtSlot()
    def refreshSchemaModel(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        rc, msg = self.schemaModel.refreshModel()
        if rc == False:
            self.helper.displayErrMsg("Refresh Schema", msg)

        self.populateTree()     
        QApplication.restoreOverrideCursor()        
        
        
    @pyqtSlot()
    def on_btnOpen_clicked(self):
        """
        Slot documentation goes here.
        """
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setNameFilters(["Cypher Query (*.cyp *.cypher)","Cypher Query (*.cyp)","Cypher Query (*.cypher)","all files (*.*)"])
        dlg.setDirectory(self.settings.value("Default/ProjPath"))
        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            if fileNames:
                fileName = fileNames[0]
                self.addCypherEditorTab(fileName=fileName, mode=MODEEDIT)

    
    @pyqtSlot()
    def on_btnNew_clicked(self):
        """
        Add a new CypherEditnGrid tab
        """
        # update unnamed file counter
        global unNamedFileCounter
        unNamedFileCounter = unNamedFileCounter + 1
        # Add a new tab with a CypherEditnGrid widget
        newCypherEditnGrid = CypherEditGridWidget(parent=self, mode=MODENEW)
        index = self.tabCypher.addTab(newCypherEditnGrid, "{}".format("Unsaved-0{}".format(unNamedFileCounter)))
        newCypherEditnGrid.tabIndex = index
        self.tabCypher.setCurrentIndex(index)

    @pyqtSlot()
    def on_btnSave_clicked(self):
        """
        Slot documentation goes here.
        bool QsciScintilla::isModified	(		)	const
        Returns true if the text has been modified.
        """
        #get current tab
#        print ("current tab is {}-{}".format(self.tabCypher.currentWidget().tabType, self.tabCypher.currentWidget().tabName))
        if self.tabCypher.count() > 0:
            if self.tabCypher.currentWidget().tabType == "CYPHER":
                self.tabCypher.currentWidget().save()

    
    @pyqtSlot()
    def on_btnSaveAs_clicked(self):
        """
        Slot documentation goes here.
        """
#        print ("current tab is {}-{}".format(self.tabCypher.currentWidget().tabType, self.tabCypher.currentWidget().tabName))
        if self.tabCypher.count() > 0:
            if self.tabCypher.currentWidget().tabType == "CYPHER":
                self.tabCypher.currentWidget().saveAs()

    
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        Slot documentation goes here.
        """
#        print ("current tab is {}-{}".format(self.tabCypher.currentWidget().tabType, self.tabCypher.currentWidget().tabName))
        if self.tabCypher.count() > 0:
            if self.tabCypher.currentWidget().tabType == "CYPHER":
                self.on_tabCypher_tabCloseRequested(self.tabCypher.currentIndex())

    

    @pyqtSlot()
    def on_btnZoomIn_clicked(self):
        """
        iterate thru all the tab widgets and tell them to zoom in
        """
        for index in range(self.tabCypher.count()):
            self.tabCypher.widget(index).zoomIn()
            
    @pyqtSlot()
    def on_btnZoomOut_clicked(self):
        """
        iterate thru all the tab widgets and tell them to zoom out
        """
        for index in range(self.tabCypher.count()):
            self.tabCypher.widget(index).zoomOut()
            
##############################################################################
#   support functions
##############################################################################
    def addCypherEditorTab(self, fileName=None, fileText = None,mode=None):

        if fileName is None:
            # update unnamed file counter
            global unNamedFileCounter
            unNamedFileCounter = unNamedFileCounter + 1
            fileName = "{}".format("Unsaved-0{}".format(unNamedFileCounter))
        tab = CypherEditGridWidget(parent=self, fileName = fileName, fileText = fileText, mode=mode)
        head, tail = ntpath.split(QFileInfo(fileName).fileName())
        self.tabCypher.addTab(tab,"{}".format(tail))
        self.tabCypher.setCurrentWidget(tab)

    def save(self, ):
        '''the parent calls this method to tell the cypherPageWidget to save all it's open cyphereditngrid tabs
        '''
        for tabIndex in range(0, self.tabCypher.count()):
            tab = self.tabCypher.widget(tabIndex)
            # switch focus to the tab
            self.tabCypher.setCurrentIndex(tabIndex)
            # tell the tab to close
            tab.close()

#####################################################################################################
## file system explorer related methods
#####################################################################################################
    def setUpFileExplorer(self, folder):
        tvFileModel = QFileSystemModel()
        tvFileModel.setRootPath(folder)
        self.tvFileSystem.setModel(tvFileModel)
        self.tvFileSystem.setRootIndex(tvFileModel.index(folder))
        self.tvFileSystem.hideColumn(1)
        self.tvFileSystem.hideColumn(2)
        self.tvFileSystem.hideColumn(3)
        self.tvFileSystem.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tvFileSystem.customContextMenuRequested.connect(self.fileSystemMenu)
#        self.tvFileSystem.doubleClicked.connect(self.tvFileSystem_doubleClicked)

        self.setPathDisplay(folder)
    
    def setPathDisplay(self, pathName):
        self.editPath.clear()
        self.editPath.setText(pathName)
        self.editPath.setToolTip(pathName)
        
    @pyqtSlot()
    def on_btnPickPath_clicked(self):
        """
        The user selects a new folder as the top level of the file system explorer
        """
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.currentProjPath))
        if folder:
            self.setUpFileExplorer(folder)
            self.currentProjPath = folder
    
        
##########################################################################################
## file system tree view methods
##########################################################################################
    def fileSystemMenu(self, position):
        #get a qmodelindex
        index = self.tvFileSystem.selectedIndexes()[0]
        if not (index is None):
#            print("{}-{}".format(index.row(), index.column()))
            # get a QFileInfo
            fileInfo = index.model().fileInfo(index)
            if fileInfo.isFile():
                if fileInfo.suffix().upper() == "MDL":
#                    print ("{}-{}-{}".format(fileInfo.path(), fileInfo.suffix(), fileInfo.fileName()))
                    menu = QMenu()
                    editCypherAction = menu.addAction("Open Model")
                    editCypherAction.triggered.connect(self.openFileSystemModel)
                    menu.exec_(self.tvFileSystem.mapToGlobal(position))    
                    return                
                if fileInfo.suffix().upper() == "CYP":
#                    print ("{}-{}-{}".format(fileInfo.path(), fileInfo.suffix(), fileInfo.fileName()))
                    menu = QMenu()
                    editCypherAction = menu.addAction("Edit Cypher")
                    editCypherAction.triggered.connect(self.openFileSystemCypher)
                    menu.exec_(self.tvFileSystem.mapToGlobal(position))    
                    return      

    def openFileSystemCypher(self, ):
        index = self.tvFileSystem.selectedIndexes()[0]
        if not (index is None):
            # get a QFileInfo
            fileInfo = index.model().fileInfo(index)        
            fileName = fileInfo.absoluteFilePath()
            self.logMsg("Open Cypher File: {}".format(fileName))
            self.addCypherEditorTab(fileName=fileName, mode=MODEEDIT)
    
    def openFileSystemModel(self, ):
        index = self.tvFileSystem.selectedIndexes()[0]
        if not (index is None):
            # get a QFileInfo
            fileInfo = index.model().fileInfo(index)        
            fileName = fileInfo.absoluteFilePath()
            self.logMsg("Open Project File: {}".format(fileName))
            self.parent.loadProject(fileName=fileName)
    

    
    @pyqtSlot(QModelIndex)
    def on_tvFileSystem_doubleClicked(self, index):
        """
        User doubleclicks on the file system tree view
        - if it is a .cyp file then load it into a cypher tab
        - if is is a .mdl file then load it into a project tab
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        index = self.tvFileSystem.selectedIndexes()[0]
#        print("{}-{}".format(index.row(), index.column()))
        fileInfo = index.model().fileInfo(index)
        if fileInfo.isFile():
            if fileInfo.suffix().upper() == "MDL":
#                print ("{}-{}-{}".format(fileInfo.path(), fileInfo.suffix(), fileInfo.fileName()))
                self.openFileSystemModel()
            if fileInfo.suffix().upper() == "CYP":
                self.openFileSystemCypher()
    
    @pyqtSlot(QModelIndex)
    def on_tvSchema_doubleClicked(self, index):
        """
        User doubleclicks on the schema tree view
        - if it is a user then show user editor
        - if is is a role then show role editor
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        index = self.tvSchema.selectedIndexes()[0]
#        print("{}-{}".format(index.row(), index.column()))
        
        selected = self.tvSchema.currentItem()
        if not (selected is None):
            parent = self.tvSchema.currentItem().parent()
            if not(parent is None):
#                print(parent.data(0, 0))
#                print(self.tvSchema.currentItem().data(0,0))
                if parent.data(0, 0) == "User":
                    self.editUser()
                if parent.data(0, 0) == "Role":
                    self.editRole()
    

