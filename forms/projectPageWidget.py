# -*- coding: utf-8 -*-

"""
    UC-05 Project Page
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
import logging
import sys
from operator import itemgetter

from PyQt5.QtCore import pyqtSlot, Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem,  QMenu, QInputDialog, QFileDialog, QAbstractItemView

from core.NeoDriver import NeoDriver
from core.DesignModel import ProjectModel
from core.helper import Helper
from core.NodeInstance import NodeInstance
from core.RelationInstance import RelationInstance
from core.NodeTemplateCypher import NodeTemplateCypher
from core.RelTemplateCypher import RelTemplateCypher
from core.helper import PageSetup

from .Ui_projectPageWidget import Ui_ProjectPageWidget

from forms.InstanceDiagramTab import InstanceDiagramTab
from forms.NodePropertyBox import NodePropertyBox
from forms.TRPropertyBox import TRPropertyBox
from forms.LabelPropertyBox import LabelPropertyBox
from forms.RelationshipPropertyBox import RelationshipPropertyBox
from forms.PropPropertyBox import PropPropertyBox
from forms.ProjectPropertyBox import ProjectPropertyBox
from forms.ObjectRenameDlg import ObjectRenameDlg
from forms.SyncToDBDlg import SyncToDBDlg
from forms.ReverseEngineerDlg import dlgReverseEngineer
from forms.ForwardEngineerSchemaDlg import ForwardEngineerSchemaDlg
from forms.ProjectHTMLDlg import ProjectHTMLDlg
from forms.INPropertyBox import INPropertyBox
from forms.IRPropertyBox import IRPropertyBox
from forms.TPPropertyBox import TPPropertyBox
from forms.FormPropertyBox import FormPropertyBox

MODENEW = 1
MODEEDIT = 2

class ProjectPageWidget(QWidget, Ui_ProjectPageWidget):
    """
    Implements a tab on the main UI that manages a NodeEra Project.  
    The project tab contains a project explorer and a tabbed area for diagrams
    """
    def __init__(self, parent=None, settings=None, pageItem=None, fileName = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ProjectPageWidget, self).__init__(parent)
        self.parent = parent
        self.schemaTab = self.parent.getSchemaTab()
        self.schemaObject = self.parent.getSchemaObject()
        self.pageType = "PROJECT"
        self.settings = settings
        self.helper = Helper()
        self.pageItem=pageItem
        self.fileName = fileName
        self.setupUi(self)
        
        # create the neocon for the project.
        self.projectNeoCon = NeoDriver(name=self.pageItem.neoConName,  promptPW=self.pageItem.promptPW)

        # create an empty project model
        self.model = ProjectModel(neoCon=self.projectNeoCon)        


        
#        self.strategyList = "Match and Merge Node", "Match and Merge Relationship", "Create Node", "Create Relationship", "Match and Delete Node", "Match and Delete Relationship"
        
        # project treeview setup
        self.tvProject.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tvProject.customContextMenuRequested.connect(self.openMenu)
        self.tvProject.setDragDropMode(QAbstractItemView.DragOnly)
        self.clearTree()


        
        # load it from disk if a filename was given

        if self.fileName is not None:
            rc, msg = self.model.readFile(filename=fileName)
            if rc:
                # apply any needed iupgrades if it's an older project file
                self.model.upgradeModel()

            else:
                # display error message
                self.helper.displayErrMsg("Read Project File Error", msg + "/n/n A blank project will be opened.")
                # reset file name and create a blank project
                self.fileName = None

            self.logMsg(msg)    
        else:
                # initialize a blank model
                self.model.initModel()
                self.logMsg("Open new project model.")
                

        # tell the project model how to update the treeview
        self.model.setUpdateTreeViewMethod(self.populateTree)

        # initiliaze UI from project model
        self.initUI()    
        
        # put the model data into the treeview
        self.populateTree()

        # position the splitter
        self.show()  # you have to do this to force all the widgets sizes to update 
        quarter = int((self.width()  / 4)) 
        self.splitter.setSizes([quarter, quarter*3])   
        
        
    def initUI(self, ):
        # put neocon url in text box above the tree view
        self.editNeo4j.setText("{} - {}".format( self.projectNeoCon.name, self.projectNeoCon.neoDict["URL"]))
        # set the sync mode checkbox
        if self.model.modelData.get("SyncMode", "On") == "On":
            self.cbSyncMode.setChecked(True)
            self.syncMode = "On"
        else:
            self.cbSyncMode.setChecked(False)
            self.syncMode = "Off"

    def logMsg(self, msg):
        if logging:
            logging.info(msg)                     
###########################################################################################
# project tree view methods
###########################################################################################    

    def openMenu(self,position):
        selected = self.tvProject.currentItem()
        if not (selected is None):
            parent = self.tvProject.currentItem().parent()
            if (parent is None):
                if (selected.data(0,0) == "Path Template"):
                    menu = QMenu()
                    addNodeAction = menu.addAction("Add Path Template")
                    addNodeAction.triggered.connect(self.newPath)
                    menu.exec_(self.tvProject.mapToGlobal(position))  
                    return
                if (selected.data(0,0) == "Form"):
                    menu = QMenu()
                    addNodeAction = menu.addAction("Add Form")
                    addNodeAction.triggered.connect(self.newForm)
                    menu.exec_(self.tvProject.mapToGlobal(position))  
                    return
                if (selected.data(0,0) == "Node Template"):
                    menu = QMenu()
                    addNodeAction = menu.addAction("Add Node Template")
                    addNodeAction.triggered.connect(self.newNode)
                    menu.exec_(self.tvProject.mapToGlobal(position))  
                    return
                if (selected.data(0,0) == "Relationship"):
                    menu = QMenu()
                    addlabelAction = menu.addAction("Add Relationship Type")
                    addlabelAction.triggered.connect(self.newRelationshipType)
                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return
                if (selected.data(0,0) == "Label"):
                    menu = QMenu()
                    addlabelAction = menu.addAction("Add Label")
                    addlabelAction.triggered.connect(self.newLabel)
                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return
                if (selected.data(0,0) == "Property"):
                    menu = QMenu()
                    addattrAction = menu.addAction("Add Property")
                    addattrAction.triggered.connect(self.newProp)
                    menu.exec_(self.tvProject.mapToGlobal(position))   
                    return
                if (selected.data(0,0) == "Relationship Template"):
                    menu = QMenu()
                    addrelAction = menu.addAction("Add Relationship Template")
                    addrelAction.triggered.connect(self.newRel)
                    menu.exec_(self.tvProject.mapToGlobal(position))     
                    return
                if (selected.data(0,0) == "Template Diagram"):
                    menu = QMenu()
                    addrelAction = menu.addAction("Add Diagram")
                    addrelAction.triggered.connect(self.newTemplateDiagram)
                    menu.exec_(self.tvProject.mapToGlobal(position))     
                    return                    
                if (selected.data(0,0) == "Instance Diagram"):
                    menu = QMenu()
                    addrelAction = menu.addAction("Add Diagram")
                    addrelAction.triggered.connect(self.newInstanceDiagram)
                    menu.exec_(self.tvProject.mapToGlobal(position))     
                    return
                if (selected.data(0,0) == "Instance Node"):
                    menu = QMenu()
                    addrelAction = menu.addAction("Add Instance Node")
                    addrelAction.triggered.connect(self.newInstanceNode)
                    menu.exec_(self.tvProject.mapToGlobal(position))     
                    return
                if (selected.data(0,0) == "Instance Relationship"):
                    menu = QMenu()
                    addrelAction = menu.addAction("Add Instance Relationship")
                    addrelAction.triggered.connect(self.newInstanceRelationship)
                    menu.exec_(self.tvProject.mapToGlobal(position))     
                    return
                    
            if not(parent is None):
                if parent.data(0,0) == "Node Template":
                    menu = QMenu()
                    propNodeAction = menu.addAction("Properties...")
                    propNodeAction.triggered.connect(self.propNode)
                    renameNodeAction = menu.addAction("Rename...")
                    renameNodeAction.triggered.connect(self.renameObject)
                    delNodeAction = menu.addAction("Delete...")
                    delNodeAction.triggered.connect(self.delObject)
                    wuNodeAction = menu.addAction("Where Used...")
                    wuNodeAction.triggered.connect(self.whereUsed)                    
                    genNodeAction1 = menu.addAction("Generate Cypher Match")
                    genNodeAction1.triggered.connect(self.genMatchNode)
                    menu.exec_(self.tvProject.mapToGlobal(position))    
                    return
                if parent.data(0,0) == "Relationship":
                    menu = QMenu()
                    propLblAction = menu.addAction("Properties...")
                    propLblAction.triggered.connect(self.propRelationshipType)
                    renameLblAction = menu.addAction("Rename...")
                    renameLblAction.triggered.connect(self.renameObject)
                    delLblAction = menu.addAction("Delete...")
                    delLblAction.triggered.connect(self.delObject)
                    wuNodeAction = menu.addAction("Where Used...")
                    wuNodeAction.triggered.connect(self.whereUsed)    
                    genNodeAction1 = menu.addAction("Generate Cypher Match")
                    genNodeAction1.triggered.connect(self.genMatchRel)
                    menu.exec_(self.tvProject.mapToGlobal(position))  
                    return
                if parent.data(0,0) == "Label":
                    menu = QMenu()
                    propLblAction = menu.addAction("Properties...")
                    propLblAction.triggered.connect(self.propLabel)
                    renameLblAction = menu.addAction("Rename...")
                    renameLblAction.triggered.connect(self.renameObject)
                    delLblAction = menu.addAction("Delete...")
                    delLblAction.triggered.connect(self.delObject)
                    wuNodeAction = menu.addAction("Where Used...")
                    wuNodeAction.triggered.connect(self.whereUsed)    
                    genNodeAction1 = menu.addAction("Generate Cypher Match")
                    genNodeAction1.triggered.connect(self.genMatchLabel)
                    menu.exec_(self.tvProject.mapToGlobal(position))  
                    return
                if parent.data(0,0) == "Property":
                    menu = QMenu()
                    propAttrAction = menu.addAction("Properties...")
                    propAttrAction.triggered.connect(self.propProp)
                    renamepropAction = menu.addAction("Rename...")
                    renamepropAction.triggered.connect(self.renameObject)
                    delAttrAction = menu.addAction("Delete...")
                    delAttrAction.triggered.connect(self.delObject)
                    wuNodeAction = menu.addAction("Where Used...")
                    wuNodeAction.triggered.connect(self.whereUsed)    
                    genNodeAction1 = menu.addAction("Generate Cypher Match")
                    genNodeAction1.triggered.connect(self.genMatchProperty)
                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return
                if parent.data(0,0) == "Relationship Template":
                    menu = QMenu()
                    propRelAction = menu.addAction("Properties...")
                    propRelAction.triggered.connect(self.propRel)
                    renameRelAction = menu.addAction("Rename...")
                    renameRelAction.triggered.connect(self.renameObject)
                    delRelAction = menu.addAction("Delete...")
                    delRelAction.triggered.connect(self.delObject)
                    wuNodeAction = menu.addAction("Where Used...")
                    wuNodeAction.triggered.connect(self.whereUsed)    
                    genNodeAction1 = menu.addAction("Generate Cypher Match")
                    genNodeAction1.triggered.connect(self.genMatchRelationship)
                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return
                    
                if parent.data(0,0) == "Path Template":
                    menu = QMenu()
                    propRelAction = menu.addAction("Properties...")
                    propRelAction.triggered.connect(self.propPath)
                    renameRelAction = menu.addAction("Rename...")
                    renameRelAction.triggered.connect(self.renameObject)
                    delRelAction = menu.addAction("Delete...")
                    delRelAction.triggered.connect(self.delObject)
                    wuNodeAction = menu.addAction("Where Used...")
                    wuNodeAction.triggered.connect(self.whereUsed)    
                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return  
                    
                if parent.data(0,0) == "Form":
                    menu = QMenu()
                    propRelAction = menu.addAction("Properties...")
                    propRelAction.triggered.connect(self.propForm)
                    renameRelAction = menu.addAction("Rename...")
                    renameRelAction.triggered.connect(self.renameObject)
                    delRelAction = menu.addAction("Delete...")
                    delRelAction.triggered.connect(self.delObject)
                    wuNodeAction = menu.addAction("Where Used...")
                    wuNodeAction.triggered.connect(self.whereUsed)    
                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return  
                    
                if parent.data(0,0) == "Template Diagram":
                    menu = QMenu()
                    isOpen, tabIndex = self.currentIsOpen()
                    if not isOpen:
                        editDiagramAction = menu.addAction("Open Diagram")
                        editDiagramAction.triggered.connect(self.openTemplateDiagram)  
                        renameDiagramAction = menu.addAction("Rename...")
                        renameDiagramAction.triggered.connect(self.renameObject)
                        delDiagramAction = menu.addAction("Delete...")
                        delDiagramAction.triggered.connect(self.delObject)

                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return             
                    
                if parent.data(0,0) == "Instance Diagram":
                    menu = QMenu()
                    isOpen, tabIndex = self.currentIsOpen()
                    if not isOpen:
                        editDiagramAction = menu.addAction("Open Diagram")
                        editDiagramAction.triggered.connect(self.openInstanceDiagram)  
                        renameDiagramAction = menu.addAction("Rename...")
                        renameDiagramAction.triggered.connect(self.renameObject)
                        delDiagramAction = menu.addAction("Delete...")
                        delDiagramAction.triggered.connect(self.delObject)
                    if isOpen:
                        delDiagramAction = menu.addAction("Sync To DB...")
                        delDiagramAction.triggered.connect(self.syncToDB)

                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return
                if parent.data(0,0) == "Instance Node":
                    menu = QMenu()
                    propNodeAction = menu.addAction("Properties...")
                    propNodeAction.triggered.connect(self.propINode)
                    delNodeAction = menu.addAction("Delete...")
                    delNodeAction.triggered.connect(self.delObject)
                    wuNodeAction = menu.addAction("Where Used...")
                    wuNodeAction.triggered.connect(self.whereUsed) 
                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return
                if parent.data(0,0) == "Instance Relationship":
                    menu = QMenu()
                    propNodeAction = menu.addAction("Properties...")
                    propNodeAction.triggered.connect(self.propIRelationship)
                    delNodeAction = menu.addAction("Delete...")
                    delNodeAction.triggered.connect(self.delObject)
                    wuNodeAction = menu.addAction("Where Used...")
                    wuNodeAction.triggered.connect(self.whereUsed) 
                    menu.exec_(self.tvProject.mapToGlobal(position)) 
                    return                    

    
    def clearTree(self, ):
        self.editNeo4j.clear()
        self.tvProject.clear()
        self.tvProject.setColumnCount(1)
        self.tvProject.setHeaderLabels(["Project Items"])
        self.tvProject.setItemsExpandable(True)


        
    def populateTree(self, addObject=None):        
#        print(sys.argv)
        self.tvProject.clear()
        self.tvProject.setColumnCount(1)
        self.tvProject.setHeaderLabels(["Project Items"])
        self.tvProject.setItemsExpandable(True)
        nodeTypes = {}
        parent = self.tvProject.invisibleRootItem()
        # add tree items
        for item in self.model.modelData["TopLevel"]:
            if (item in ["Path Template", "Form"] and not '-b' in sys.argv):
#            if item == "":
                pass
            else:
                topItem = self.addParent(parent, 0, item, "data")
                nodeTypes[item]=topItem
                for object in sorted(self.model.modelData[item], key=itemgetter('name')):
                    name = object.get("name", "missing name")
                    # instance node and instance relationship have a different display name, everthing else uses name for displayname on the treeview
                    displayName = object.get("displayName", "")
                    if displayName == "":
                        displayName = object.get("name", "missing name")
                    self.addChild(parentItem = topItem, childDisplayName=displayName, childName = name, parentName=item )    
        self.tvProject.resizeColumnToContents(0)
        
    def addParent(self, parent, column, title, data):
        item = QTreeWidgetItem(parent, [title])
        item.setData(column, Qt.UserRole, data)
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        item.setFlags(  Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled )
        return item

    def addChild(self, parentItem=None, childDisplayName=None, childName = None, parentName=None ):
        item = QTreeWidgetItem(parentItem, [childDisplayName, ])
        item.setData(0, Qt.UserRole, parentName)
        item.setData(0, Qt.UserRole+1, childName)
        # make certain items dragable
        if parentItem.data(0,Qt.DisplayRole) in ["Instance Node", "Instance Relationship", "Node Template", "Relationship Template"]:
            item.setFlags(  Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)
        else:
            item.setFlags(  Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled )
        
        return item

    def notYet(self, ):
        return

    def createCypherTab(self, cypher=None, title=None, objectName=None):
            editCypher = "// Generated by NodeEra from project: {} \n// {}: {} \n{}".format(self.fileName, title, objectName, cypher)
            self.schemaTab.addCypherEditorTab(fileName=None, fileText = editCypher, mode=MODENEW)
            # switch to the schema tab
            self.pageItem.pageWidget.tabPage.setCurrentIndex(self.pageItem.pageWidget.tabPage.indexOf(self.schemaTab))

########################################
# GENERIC METHODS FOR ALL PROJECT TABS
########################################      
    def isOpen(self, tabType=None, tabName=None):
        for tabIndex in range(0, self.tabProject.count()):
            tab = self.tabProject.widget(tabIndex)
            if tab.tabType == tabType:
                if tab.tabName == tabName:
                    return True
        return False

    def currentIsOpen(self,):
        tabType = self.tvProject.currentItem().parent().data(0,0)
        tabName = self.tvProject.currentItem().data(0,0)
        # not all items in the treeview are tab types but who cares, this will still work.
        for tabIndex in range(0, self.tabProject.count()):
            tab = self.tabProject.widget(tabIndex)
            if tab.tabType == tabType:
                if tab.tabName == tabName:
                    return True, tabIndex
        return False, None 
    
        
########################################
# GENERIC METHODS FOR ALL TOP LEVEL OBJECTS
########################################  
    def whereUsed(self):
#        objectName=self.tvProject.currentItem().data(0,0)
        objectName=self.tvProject.currentItem().data(0,Qt.UserRole+1)
        objectType = self.tvProject.currentItem().parent().data(0,0)
        d = ObjectRenameDlg(self, mode="VIEW", objectType = objectType, objectName = objectName, designModel = self.model)
        d.exec_()

    def delObject(self):
#        objectName=self.tvProject.currentItem().data(0,0)
        objectName=self.tvProject.currentItem().data(0,Qt.UserRole+1)
        objectType = self.tvProject.currentItem().parent().data(0,0)
        d = ObjectRenameDlg(self, mode="DELETE", objectType = objectType, objectName = objectName, designModel = self.model)
        if d.exec_():
            if d.instanceObjectChanged == True:
                self.model.setModelDirty()
                # tell all open diagrams to redraw
                self.redrawInstanceDiagrams()            
                self.redrawTemplateDiagrams()
        self.populateTree()


    def renameObject(self, ):
#        objectName=self.tvProject.currentItem().data(0,0)
        objectName=self.tvProject.currentItem().data(0,Qt.UserRole+1)
        objectType = self.tvProject.currentItem().parent().data(0,0)
        d = ObjectRenameDlg(self, mode="RENAME", objectType = objectType, objectName = objectName, designModel = self.model)
        if d.exec_():
            if d.instanceObjectChanged == True:
                self.model.setModelDirty()
                # tell all open diagrams to redraw
                self.redrawInstanceDiagrams()            
                self.redrawTemplateDiagrams()
        self.populateTree()
        return    

###########################
# INSTANCE NODE METHODS
###########################      
    def newInstanceNode(self):
        self.editINode(nodeKey=None)
    
    def propINode(self):
        # get the nodeKey from userData
        self.editINode(nodeKey=self.tvProject.currentItem().data(0,Qt.UserRole+1))

    def editINode(self, nodeKey=None):
#        if nodeKey:
        saveIndex, nodeDict = self.model.getDictByName(topLevel="Instance Node",objectName=nodeKey)
        nodeInstance = NodeInstance(model=self.model, nodeInstanceDict=nodeDict)

        d = INPropertyBox(self, diagramInstance=nodeInstance,  model = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.diagramInstance is not None:
                if saveIndex is None:
                    self.model.modelData["Instance Node"].append(d.diagramInstance.getObjectDict())
                    self.populateTree()
                else:
                    self.model.modelData["Instance Node"][saveIndex]=d.diagramInstance.getObjectDict()
                    self.populateTree()
            
            # tell all open diagrams to redraw
            self.redrawInstanceDiagrams()
                
###########################
# INSTANCE RELATIONSHIP METHODS
###########################      
    def newInstanceRelationship(self):
        self.editIRelationship(nodeKey=None)
    
    def propIRelationship(self):
        # get the nodeKey from userData
        self.editIRelationship(nodeKey=self.tvProject.currentItem().data(0,Qt.UserRole+1))

    def editIRelationship(self, nodeKey=None):
        # see if relationship dictionary exists otherwise you get None
        saveIndex, relDict = self.model.getDictByName(topLevel="Instance Relationship",objectName=nodeKey)
        relationInstance = RelationInstance(parent=self, model = self.model, relationInstanceDict=relDict)
        d = IRPropertyBox(self, diagramInstance=relationInstance,  model = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.diagramInstance is not None:
                if saveIndex is None:
                    self.model.modelData["Instance Relationship"].append(d.diagramInstance.getObjectDict())
                    self.populateTree()
                else:
                    self.model.modelData["Instance Relationship"][saveIndex]=d.diagramInstance.getObjectDict()
                    self.populateTree()

            # tell all open diagrams to redraw
            self.redrawInstanceDiagrams()   
            
###########################
# NODE TEMPLATE METHODS
###########################
    def newNode(self):
        self.editNode(mode="NEW")
    
    def propNode(self):
        self.editNode(nodeName=self.tvProject.currentItem().data(0,0), mode="UPDATE")
    
    def genMatchNode(self):
        self.matchNode(nodeName=self.tvProject.currentItem().data(0,0))
 
    def editNode(self, nodeName=None, mode=None):
        saveIndex, nodeDict = self.model.getDictByName(topLevel="Node Template",objectName=nodeName)
        d = NodePropertyBox(self, mode=mode, objectDict = nodeDict, designModel = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.objectDict is not None:
                if saveIndex is None:
                    self.model.modelData["Node Template"].append(d.objectDict)
                    self.populateTree()
                else:
                    self.model.modelData["Node Template"][saveIndex]=d.objectDict
                    self.populateTree()

            # tell all open diagrams to redraw
            self.redrawInstanceDiagrams()
            self.redrawTemplateDiagrams()

    def matchNode(self, nodeName=None):
        saveIndex, nodeDict = self.model.getDictByName(topLevel="Node Template",objectName=nodeName)
        if not nodeDict is None:
            nodeTemplateCypher = NodeTemplateCypher(templateDict=nodeDict)
            cypher, editParmDict = nodeTemplateCypher.genMatch()
            # add comment and create cypher tab
            self.createCypherTab(cypher=cypher, title="Match Node Template", objectName=nodeName)
        
###########################
# RELATIONSHIP TEMPLATE METHODS
###########################
    def newRel(self):
        self.editRel(mode="NEW")

    def propRel(self):
        self.editRel(relName=self.tvProject.currentItem().data(0,0), mode="UPDATE")
        
    def editRel(self, relName=None, mode=None):
        saveIndex, relDict = self.model.getDictByName(topLevel="Relationship Template",objectName=relName)
        d = TRPropertyBox(self, mode=mode, objectDict = relDict, designModel = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.objectDict is not None:
                if saveIndex is None:
                    self.model.modelData["Relationship Template"].append(d.objectDict)
                    self.populateTree()
                else:
                    self.model.modelData["Relationship Template"][saveIndex]=d.objectDict
                    self.populateTree()
            # tell all open diagrams to redraw        
            self.redrawTemplateDiagrams()
                
    def genMatchRelationship(self):
        self.matchRelationship(relName=self.tvProject.currentItem().data(0,0))    
        
    def matchRelationship(self, relName=None):
        saveIndex, relDict = self.model.getDictByName(topLevel="Relationship Template",objectName=relName)
        if not relDict is None:
            relTemplateCypher = RelTemplateCypher(templateDict=relDict)
            cypher, editParmDict = relTemplateCypher.genMatch()
            # add comment and create cypher tab
            self.createCypherTab(cypher=cypher, title="Match Relationship Template", objectName=relName)

###########################
# PATH TEMPLATE METHODS
###########################
    def newPath(self):
        self.editPath(mode="NEW")
    
    def propPath(self):
        self.editPath(pathName=self.tvProject.currentItem().data(0,0), mode="UPDATE")
    
    def genMatchPath(self):
        self.matchPath(pathName=self.tvProject.currentItem().data(0,0))
 
    def editPath(self, pathName=None, mode=None):
        saveIndex, pathDict = self.model.getDictByName(topLevel="Path Template",objectName=pathName)
        d = TPPropertyBox(self, mode=mode, objectDict = pathDict, designModel = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.objectDict is not None:
                if saveIndex is None:
                    self.model.modelData["Path Template"].append(d.objectDict)
                    self.populateTree()
                else:
                    self.model.modelData["Path Template"][saveIndex]=d.objectDict
                    self.populateTree()

###########################
# FORM METHODS
###########################
    def newForm(self):
        text, ok = QInputDialog.getText(self, 'New Form', 'Enter the Form Name:')
        if ok:
            if self.helper.DupObjectError(designModel = self.model, objName=text, topLevel = "Form", txtMsg = "Error, The Form - {} - already exists.".format(text)):
                return
            else:
                self.editForm(mode="NEW", formName=text)
    
    def propForm(self):
        self.editForm(formName=self.tvProject.currentItem().data(0,0), mode="UPDATE")
 
    def editForm(self, formName=None, mode=None):
        saveIndex, formDict = self.model.getDictByName(topLevel="Form",objectName=formName)
        if formDict is None:
            formDict = self.model.newFormDict(name=formName)        
        d = FormPropertyBox(self, mode=mode, objectDict = formDict, designModel = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.objectDict is not None:
                if saveIndex is None:
                    self.model.modelData["Form"].append(d.objectDict)
                    self.populateTree()
                else:
                    self.model.modelData["Form"][saveIndex]=d.objectDict
                    self.populateTree()
             
 
###########################
# LABEL METHODS
###########################
    def genMatchLabel(self):
        p1 = self.tvProject.currentItem().data(0,0)  
        p3 = "n:{} as {},\n".format(p1, p1)
        cypher = '''MATCH (n:{}) \nRETURN id(n) as NodeID, \n{}n as Node  '''.format(p1, p3)  
        self.createCypherTab(cypher=cypher, title="Match Label", objectName=p1)
            
    def newLabel(self):
        self.editLabel(mode="NEW")

    def propLabel(self):
        self.editLabel(labelName=self.tvProject.currentItem().data(0,0), mode="UPDATE")
    
    def editLabel(self, labelName=None, mode=None):

        saveIndex, labelDict = self.model.getDictByName(topLevel="Label",objectName=labelName)
        d = LabelPropertyBox(self, mode=mode, objectDict = labelDict, designModel = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.objectDict is not None:
                if saveIndex is None:
                    self.model.modelData["Label"].append(d.objectDict)
                    self.populateTree()
                else:
                    self.model.modelData["Label"][saveIndex]=d.objectDict
                    
###########################
# RELATIONSHIP METHODS
###########################
    def genMatchRel(self):
        p1 = self.tvProject.currentItem().data(0,0)
        cypher = '''MATCH (f)-[r:{}]->(t) \nRETURN id(r) as RelID,\ntype(r) as RelName,\nr as Relationship,\nf as FromNode,\nt as ToNode  '''.format(p1)
        self.createCypherTab(cypher=cypher, title="Match Relationship Type", objectName=p1)
                
    def newRelationshipType(self):
        self.editRelationshipType(mode="NEW")

    def propRelationshipType(self):
        self.editRelationshipType(relName=self.tvProject.currentItem().data(0,0), mode="UPDATE")
    
    def editRelationshipType(self, relName=None, mode=None):

        saveIndex, relTypeDict = self.model.getDictByName(topLevel="Relationship",objectName=relName)
        d = RelationshipPropertyBox(self, mode=mode, objectDict = relTypeDict, designModel = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.objectDict is not None:
                if saveIndex is None:
                    self.model.modelData["Relationship"].append(d.objectDict)
                    self.populateTree()
                else:
                    self.model.modelData["Relationship"][saveIndex]=d.objectDict          
                    
###########################
# PROPERTY METHODS
###########################
    
    def genMatchProperty(self):
        propertyName=self.tvProject.currentItem().data(0,0)
        p1 = "exists(n.{})\n".format(propertyName)
        p2 = "n.{} as {},\n".format(propertyName, propertyName)
        cypher = '''MATCH (n) \nWHERE {}RETURN id(n) as NodeID, \n{}n as Node  '''.format(p1, p2)        
        self.createCypherTab(cypher=cypher, title="Match Property", objectName=propertyName)
        
    def newProp(self):
        self.editProp(mode="NEW")
        
    def propProp(self):
        self.editProp(propName=self.tvProject.currentItem().data(0,0), mode="UPDATE")
        
    def editProp(self, propName=None, mode=None):

        saveIndex, propDict = self.model.getDictByName(topLevel="Property",objectName=propName)
        d = PropPropertyBox(self, mode=mode, objectDict = propDict, designModel = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.objectDict is not None:
                if saveIndex is None:
                    self.model.modelData["Property"].append(d.objectDict)
                    self.populateTree()
                else:
                    self.model.modelData["Property"][saveIndex]=d.objectDict
        
###########################################################################################
# Project Methods
###########################################################################################

    def editProjectProperties(self, ):
        if not (self.model is None):
            d = ProjectPropertyBox(self, model = self.model, settings=self.settings)
            if d.exec_():
                self.model.setModelDirty()
                if d.formatChanged == True:
                # tell all open diagrams to redraw
                    self.redrawInstanceDiagrams()
                    self.redrawTemplateDiagrams()
                self.model.setModelDirty()
                
    def reverseEngineerGraph(self, ):
        if not (self.model is None):
            schemaModel = self.parent.getSchemaObject()
            d = dlgReverseEngineer(self, schemaModel = schemaModel, model = self.model, settings=self.settings)
            if d.exec_():
                self.model.setModelDirty()
                
    def generateProjectReports(self, ):
        if not (self.model is None):
            schemaModel = self.parent.getSchemaObject()
            d = ProjectHTMLDlg(self, schemaModel = schemaModel, model = self.model)
            if d.exec_():
                self.model.setModelDirty()     
                
    def forwardEngineerGraph(self, ):
        if not (self.model is None):
            d = ForwardEngineerSchemaDlg(self,  )
            if d.exec_():
                self.model.setModelDirty()    
                
    def save(self, ):
        'This is called by the parent when closing'
#        print("project page widget save {}".format(self.fileName))
        if self.model.dirty:        
            # prompt if they want to save
            if self.fileName is not None:
                displayName = self.fileName
            else:
                displayName = "New Project File"
            if self.helper.saveChangedObject("Project File", displayName): 
                self.saveProject()
            
    def saveProject(self, ):
        
        newName = None
        
        # need to tell all open project related tabs to save their current state to the project model
        for tabIndex in range(0, self.tabProject.count()):
            tab = self.tabProject.widget(tabIndex)
            tab.save()

        # if no file name then this is really a save as...
        if self.model.modelFileName is None:
            newName = self.saveProjectAs()
        else:
            self.saveModel()      
            
        return newName
        
    def saveProjectAs(self, ):
        # get filename to save as 
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setDefaultSuffix("mdl")
        dlg.setNameFilters(["NodeEra project (*.mdl)","all files (*.*)"])
        dlg.setDirectory(self.settings.value("Default/ProjPath"))
        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            if fileNames:
                self.fileName = fileNames[0]
                # save the file
                self.model.modelFileName = self.fileName
                self.model.setModelDirty()
                self.saveModel()
                x = self.parent.stackedPageItems.currentWidget().tabPage.currentIndex()
                self.parent.stackedPageItems.currentWidget().tabPage.setTabText(x, "Project: {} - {}".format(self.model.shortName(), self.pageItem.neoConName))

        
    def saveModel(self):
        '''write the model file to disk if the dirty flag is true
        '''
        if self.model.dirty:
            rc, msg = self.model.writeFile()
            self.logMsg(msg)
            if rc == False:
                self.helper.displayErrMsg("Write Project File Error", msg)
            self.model.setModelClean()
            # save it in the recent list
            self.addRecentFile()
        else:
            self.logMsg("project file: {} not saved.".format(self.fileName))


    def addRecentFile(self):
        '''add the current model filename to the recent list if it isn't there
          move the current model filename to the top of the list if its already in the list
          '''
        try:
            if not self.model.modelFileName is None:
                recentList = self.settings.value("Default/RecentList")
                if not self.model.modelFileName in recentList:
                    # add it as the first item in the list
                    recentList.insert(0, self.model.modelFileName)
                else:
                    # remove it from whereever it is in the list and add it as the first item in the list
                    recentList.remove(self.model.modelFileName)
                    recentList.insert(0, self.model.modelFileName)
                # check if the list is longer than 5 and trim it down to only 5
                if len(recentList) > 5:
                    del recentList[5:]
                self.settings.setValue("Default/RecentList", recentList)
        except:
            self.logMsg("Error adding project file: {} to the recents list.".format(self.model.modelFileName))
            
            
        
###########################
# Diagram METHODS
###########################
    def newTemplateDiagram(self, ):
        text, ok = QInputDialog.getText(self, 'New Template Diagram', 'Enter the Template Diagram Name:')
        if ok:
            if self.helper.DupObjectError(designModel = self.model, objName=text, topLevel = "Template Diagram", txtMsg = "Error, The Template Diagram - {} - already exists.".format(text)):
                return
            else:
                templateDiagram = {}
                templateDiagram["name"] = text
                templateDiagram["pageSetup"] = self.model.modelData["pageSetup"]
                templateDiagram["items"] = []
                self.model.modelData["Template Diagram"].append(templateDiagram)
                self.populateTree()
                self.addTemplateDiagramTab(name=text)
                self.model.setModelDirty()        
                
    def newInstanceDiagram(self, ):
        text, ok = QInputDialog.getText(self, 'New Instance Diagram', 'Enter the Instance Diagram Name:')
        if ok:
            if self.helper.DupObjectError(designModel = self.model, objName=text, topLevel = "Instance Diagram", txtMsg = "Error, The Instance Diagram - {} - already exists.".format(text)):
                return
            else:
                instanceDiagram = {}
                instanceDiagram["name"] = text
                # get the page setup data from the project defaults
                pageSetup = PageSetup(self.model.modelData["pageSetup"])
                instanceDiagram["pageSetup"] = pageSetup.objectDict
                
                instanceDiagram["items"] = []
                self.model.modelData["Instance Diagram"].append(instanceDiagram)
                self.populateTree()
                self.addInstanceDiagramTab(name=text)
                self.model.setModelDirty()

    def addInstanceDiagramTab(self, name=None):
        if self.isOpen(tabType="Instance Diagram", tabName=name):
            self.helper.displayErrMsg("Open Diagram", "Error - This diagram is already open")
        else:
            tab = InstanceDiagramTab(parent=self, model=self.model, name=name, tabType="Instance Diagram")
            self.tabProject.addTab(tab,"Instance Diagram - {}".format(str(name)))
            self.tabProject.setCurrentWidget(tab)
    
    def addTemplateDiagramTab(self, name=None):
        if self.isOpen(tabType="Template Diagram", tabName=name):
            self.helper.displayErrMsg("Open Diagram", "Error - This diagram is already open")
        else:
            tab = InstanceDiagramTab(parent=self, model=self.model, name=name,  tabType="Template Diagram")
            self.tabProject.addTab(tab,"Template Diagram - {}".format(str(name)))
            self.tabProject.setCurrentWidget(tab)

    def openInstanceDiagram(self,  ): 
        self.addInstanceDiagramTab(name=self.tvProject.currentItem().data(0,0))
        self.model.setModelDirty()
    
    def openTemplateDiagram(self,  ): 
        self.addTemplateDiagramTab(name=self.tvProject.currentItem().data(0,0))    
        self.model.setModelDirty()    
    
    def closeDiagramTab(self, currentIndex):
#        print("close diagram tab index:{}".format(currentIndex))
        if self.tabProject.currentWidget():
            self.tabProject.currentWidget().save()
            self.model.setModelDirty()
            currentIndex = self.tabProject.currentIndex()
            self.tabProject.removeTab(currentIndex)
            
                            
    def redrawInstanceDiagrams(self, ):
        '''
        loop through all open instance diagrams and tell them to redraw
        '''
        for diagramIndex in range(0, self.tabProject.count()):
            tab = self.tabProject.widget(diagramIndex)
            if tab.tabType == "Instance Diagram":
                tab.reDrawDiagram()

    def redrawTemplateDiagrams(self, ):
        '''
        loop through all open template diagrams and tell them to redraw
        '''
        for diagramIndex in range(0, self.tabProject.count()):
            tab = self.tabProject.widget(diagramIndex)
            if tab.tabType == "Template Diagram":
                tab.reDrawDiagram()
                
    def syncToDB(self, ):
        
        if self.model.modelData["SyncMode"] == "On":
            d = SyncToDBDlg(self, )
            d.exec_()
            self.model.setModelDirty()
        else:
            self.helper.displayErrMsg("Sync DB Error", "You must turn Sync Mode On before you can synchronize to the Neo4j Instance")

  
    @pyqtSlot(int)
    def on_tabProject_tabCloseRequested(self, index):
        """
        When the tab in the project closes, see if the tab data should be saved.
        The tabs are instance or template diagrams.
        
        @param index DESCRIPTION
        @type int
        """
#        print("tabProject tabCloseRequested index:{}".format(index))
        
        if self.tabProject.currentWidget():
            self.tabProject.currentWidget().save()
            self.tabProject.removeTab(index)
    
    @pyqtSlot()
    def on_btnSave_clicked(self):
        """
        Slot documentation goes here.
        """
        self.saveProject()
    
    @pyqtSlot()
    def on_btnSaveAs_clicked(self):
        """
        Save Project As
        """
        self.saveProjectAs()

   
    @pyqtSlot()
    def on_cbSyncMode_clicked(self):
        """
        User clicks the sync mode checkbox to change it's value
        """
#        print("sync clicked {}".format(self.cbSyncMode.isChecked()))
        if self.cbSyncMode.isChecked():
            self.model.modelData["SyncMode"] = "On"
        else:
            self.model.modelData["SyncMode"] = "Off"
        
        self.model.setModelDirty()
    
    @pyqtSlot()
    def on_btnCloseProject_clicked(self):
        """
        Slot documentation goes here.
        """
#        print("closeProject button clicked")
        self.save()
    
    @pyqtSlot(QModelIndex)
    def on_tvProject_doubleClicked(self, index):
        """
        User double clicks on the project tree view
        - if a model object is clicked on open the editor for that object
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        selected = self.tvProject.currentItem()
        if not (selected is None):
            parent = self.tvProject.currentItem().parent()
            if not(parent is None):
                if parent.data(0,0) == "Node Template":
                    self.propNode()
                    return
                if parent.data(0,0) == "Relationship":
                    self.propRelationshipType()
                    return
                if parent.data(0,0) == "Label":
                    self.propLabel()
                    return
                if parent.data(0,0) == "Property":
                   self.propProp()
                   return
                if parent.data(0,0) == "Relationship Template":
                    self.propRel()
                    return
                if parent.data(0,0) == "Template Diagram":
                    isOpen, tabIndex = self.currentIsOpen()
                    if not isOpen:
                        self.openTemplateDiagram()
                    else:
                        # switch to the tab
                        self.tabProject.setCurrentIndex(tabIndex)
                    return
                if parent.data(0,0) == "Instance Diagram":
                    isOpen, tabIndex = self.currentIsOpen()
                    if not isOpen:
                        self.openInstanceDiagram()
                    else:
                        # switch to the tab
                        self.tabProject.setCurrentIndex(tabIndex)
                    return
                if parent.data(0,0) == "Path Template":
                    self.propPath()
                    return
                if parent.data(0,0) == "Form":
                    self.propForm()
                    return
                if parent.data(0,0) == "Instance Node":
                    self.propINode()
                    return
                if parent.data(0,0) == "Instance Relationship":
                    self.propIRelationship()
                    return

                
