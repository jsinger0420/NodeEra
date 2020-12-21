# -*- coding: utf-8 -*-

"""
Module implementing PathTemplateTab.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot, Qt, QModelIndex, QObject
from PyQt5.QtWidgets import QWidget,  QVBoxLayout, QAbstractItemView, QHeaderView, QTreeWidgetItem, QMenu, QTreeWidgetItemIterator
from PyQt5.QtGui import QStandardItemModel,  QStandardItem

from core.helper import Helper, CBDelegate
from core.QueryPathNode import QueryPathNode
from core.MetaBoxDelegate import MetaBoxDelegate
from forms.CypherEditGridWidget import CypherEditGridWidget
from .Ui_PathTemplateTab import Ui_PathTemplateTab

MODENEW = 1
MODEEDIT = 2
#enums for metabox stacked widget
NODEBOX=1
RELBOX=2
#enums for metabox grid
ATTRNAME, ATTRVALUE = range(2)
#enums for output grid
SOURCE, SOURCENAME, COLTYPE, COLVAL, COLNAME, DISPLAYIT, SORT, GROUP =  range(8)

# GLOBAL FILE COUNTER
unNamedFileCounter = 0

class PathTemplateTab(QWidget, Ui_PathTemplateTab):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, model=None, name=None, tabType=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(PathTemplateTab, self).__init__(parent)
        self.setupUi(self)
        self.parent=parent
        self.model=model
        self.tabType = tabType
        self.tabName = name
        saveIndex, pathTemplateDict = self.model.getDictByName(topLevel=self.tabType, objectName=name)
        self.pathTemplateDict = pathTemplateDict  
        self.helper = Helper()
        
        self.lastTreeViewWidgetItem = None
        
        # add cypher CypherEditGridWidget
        global unNamedFileCounter
        unNamedFileCounter = unNamedFileCounter + 1
        fileName = "{}".format("Unsaved-0{}".format(unNamedFileCounter))
        self.cypherEditGrid = CypherEditGridWidget(parent=parent, fileName = fileName, fileText = "", mode=MODENEW)
        self.frmDataGridLayout = QVBoxLayout(self.frmDataGrid)
        self.frmDataGridLayout.setObjectName("frmDataGridLayout")
        self.frmDataGridLayout.setContentsMargins(1, 1, 1, 1)
        self.frmDataGridLayout.setSpacing(1)
        self.frmDataGridLayout.addWidget(self.cypherEditGrid)                    
        
        # setup output grid model
        self.gridOutput.setModel(self.createOutputModel())
        self.gridOutput.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridOutput.setSelectionMode(QAbstractItemView.SingleSelection)
#        SOURCE, SOURCENAME, COLTYPE, COLVAL, COLNAME, DISPLAYIT, SORT, GROUP
        self.gridOutput.setColumnWidth(SOURCE, 200)   
        self.gridOutput.setColumnWidth(SOURCENAME, 200)   
        self.gridOutput.setColumnWidth(COLTYPE, 100)   
        self.gridOutput.setColumnWidth(COLVAL, 200)   
        self.gridOutput.setColumnWidth(COLNAME, 200)   
        self.gridOutput.setColumnWidth(DISPLAYIT, 75)   
        self.gridOutput.setColumnWidth(SORT, 75)   
        self.gridOutput.setColumnWidth(GROUP, 75)
        # header
        header = self.gridOutput.horizontalHeader()
        header.setSectionResizeMode(SOURCE, QHeaderView.Interactive) 
        header.setSectionResizeMode(SOURCENAME, QHeaderView.Interactive)
        header.setSectionResizeMode(COLTYPE, QHeaderView.Fixed)      
        header.setSectionResizeMode(COLVAL, QHeaderView.Interactive)
        header.setSectionResizeMode(COLNAME, QHeaderView.Interactive)
        header.setSectionResizeMode(DISPLAYIT, QHeaderView.Fixed)
        header.setSectionResizeMode(SORT, QHeaderView.Fixed)
        header.setSectionResizeMode(GROUP, QHeaderView.Fixed)
        
        # column type
        colTypeList = ["", "Property", "Label", "Function"] 
        self.gridOutput.setItemDelegateForColumn(COLTYPE, CBDelegate(self, colTypeList, setEditable=True ))
        # sort
        sortList = ["No", "Ascending", "Descending"] 
        self.gridOutput.setItemDelegateForColumn(SORT, CBDelegate(self, sortList, setEditable=True ))
        # group
        groupList = ["No", "Yes"] 
        self.gridOutput.setItemDelegateForColumn(GROUP, CBDelegate(self, groupList, setEditable=True ))
        
        # path treeview setup
        self.tvPath.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tvPath.customContextMenuRequested.connect(self.openMenu)
        self.tvPath.setDragDropMode(QAbstractItemView.DragOnly)

        # initiliaze UI from pathTemplateDict
        self.initUI()            
        
    def save(self, ):
#        print("save path {}".format(self.tabName))
        nodeList = []
        # iterate through the treeview
        tvPathIterator = QTreeWidgetItemIterator(self.tvPath, flags = QTreeWidgetItemIterator.All)
        while tvPathIterator:
            if not tvPathIterator.value() is None:
#                print("save node {}".format(tvPathIterator.value().text(0)))
                queryPathNodeItem = tvPathIterator.value()
                queryPathNodeDict = queryPathNodeItem.data(0, Qt.UserRole).dict()
                nodeList.append(queryPathNodeDict)
                # if its the root node then save the description.
                if queryPathNodeDict["type"] == "Path Template":
                    self.pathTemplateDict["description"] = queryPathNodeDict["description"]
                tvPathIterator.__iadd__(1)
            else:
                break
            
        self.pathTemplateDict["queryPath"] = nodeList
        self.model.setModelDirty()     
   

#-----------------------------------------------------------------------------------------------------------------------
#  metabox grid methods
#-----------------------------------------------------------------------------------------------------------------------        
    def createMetaBoxModel(self):
#        ATTRNAME, ATTRVALUE  gridNodeMeta
        model = QStandardItemModel(0, 2)
        model.setHeaderData(ATTRNAME, Qt.Horizontal, "Attribute")
        model.setHeaderData(ATTRVALUE, Qt.Horizontal, "Value")
        return model    
        
    def clearMetaBox(self):
        self.lblMetaHeader.setText("Definition")
        # metabox grid setup
#        ATTRNAME, ATTRVALUE  gridMetaBox
        self.gridMetaBox.setModel(None)
        self.metaBoxModel = self.createMetaBoxModel()
        self.gridMetaBox.setModel(self.metaBoxModel)
        self.gridMetaBox.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridMetaBox.setSelectionMode(QAbstractItemView.SingleSelection)
        self.gridMetaBox.setColumnWidth(ATTRNAME, 200)   
        self.gridMetaBox.setColumnWidth(ATTRVALUE, 300)   
        # header
        header = self.gridMetaBox.horizontalHeader()
        header.setSectionResizeMode(ATTRNAME, QHeaderView.Fixed) 
        header.setSectionResizeMode(ATTRVALUE, QHeaderView.Stretch) 
        # set editor delegate
        self.gridMetaBox.setItemDelegateForColumn(ATTRVALUE, MetaBoxDelegate(self))
#        self.gridMetaBox.itemDelegateForColumn(ATTRVALUE).closeEditor.connect(self.metaBoxEditorClosed)
        # connect model slots 
        self.metaBoxModel.itemChanged.connect(self.metaBoxModelItemChanged)
        # connect grid slots
        self.gridMetaBox.selectionModel().selectionChanged.connect(self.metaBoxGridSelectionChanged)    
      
    def addMetaRow(self, attribute=None, value=None, editable=None ):
        '''
        add a row to the  metabox grid
        '''
#        print("add metarow {}-{}-{}".format(attribute, value, editable))
        self.gridMetaBox.setSortingEnabled(False)
        # attribute
        if attribute is None:
            attribute = ""
        item1 = QStandardItem(attribute)
        item1.setEditable(False)
        # value
        if value is None:
            value = ""
        item2 = QStandardItem(str(value))
        # save the attribute name in the value item so the custom editor MetaBoxDelegate can find it
        item2.setData(attribute, Qt.UserRole)
        item2.setEditable(editable)        
        
        self.gridMetaBox.model().appendRow([item1,item2 ])                


    def populateMetaBox(self, queryPathNode=None):
        if not queryPathNode is None:
            self.clearMetaBox()
            self.lblMetaHeader.setText("{} Definition".format(queryPathNode.type))
            for attr in queryPathNode.attributes():
                self.addMetaRow(attribute=attr[0], value=attr[1], editable=attr[2] )                

    def rePopulateMetaBox(self, queryPathNode=None):
        '''update the displayname'''
        model = self.gridMetaBox.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            name = model.item(row,ATTRNAME).data(Qt.EditRole)
            if name == "Display Name":
                # update displayName in the grid
                model.setData(model.item(row,ATTRVALUE).index(), queryPathNode.displayName, role=Qt.EditRole)
                # update displayName on the tree view
                queryPathNode.treeItem.setData(0, Qt.EditRole, queryPathNode.displayName)

#    def metaBoxEditorClosed(self, ):
#        print("editor closed")
        
    def metaBoxModelItemChanged(self, item):
#        print("item data changed {} at row:{} col:{}".format(str(item.checkState()), item.index().row(), item.index().column()))
        # a cell changed so see if other changes are needed
        # update the queryPathNode object
        selected = self.tvPath.currentItem()
        if not (selected is None):
            queryPathNode = selected.data(0, Qt.UserRole)  
            name= self.gridMetaBox.model().item(item.index().row(),ATTRNAME).data(Qt.EditRole)
            value= self.gridMetaBox.model().item(item.index().row(),ATTRVALUE).data(Qt.EditRole)
            queryPathNode.updateAttr(name=name, value=value)
                
        # update displayName
        self.rePopulateMetaBox(queryPathNode=queryPathNode)
        # force selection of this cell
        self.gridMetaBox.setCurrentIndex(item.index())


    def metaBoxGridSelectionChanged(self):
        # not used
#        print("metabox grid selection changed")
        return
        
    def initUI(self):
        self.populateTree()

#-----------------------------------------------------------------------------------------------------------------------
#  tree view methods
#-----------------------------------------------------------------------------------------------------------------------        
    def clearTree(self):
        self.tvPath.clear()
        self.tvPath.setColumnCount(1)
        self.tvPath.setHeaderLabels(["Query Path"])
        self.tvPath.setItemsExpandable(True)        

    def getMaxTreeOrder(self, ):
        '''scan the tree and find the max order attribute.  This is used to increment and create the next highest order number'''
        max = 0
        # iterate through the treeview
        tvPathIterator = QTreeWidgetItemIterator(self.tvPath, flags = QTreeWidgetItemIterator.All)
        while tvPathIterator:
            if not tvPathIterator.value() is None:
                queryPathNodeItem = tvPathIterator.value()
                queryPathNodeDict = queryPathNodeItem.data(0, Qt.UserRole).dict()
                order = queryPathNodeDict.get("order", 0)
                # save the value for order if it's greater
                if order > max:
                    max = order
                tvPathIterator.__iadd__(1)
            else:
                break       
        return max
    
    def findParentWidget(self, findOrder=None):
        '''scan the tree and find the treeviewwidget with the matching parentOrder'''
        # if the find id is None then this is the root so return the tree view itself
        if findOrder is None:
            return self.tvPath
        # find the parent tree view widget
        parentWidget = None
        # iterate through the treeview
        tvPathIterator = QTreeWidgetItemIterator(self.tvPath, flags = QTreeWidgetItemIterator.All)
        while tvPathIterator:
            if not tvPathIterator.value() is None:
                queryPathNodeItem = tvPathIterator.value()
                queryPathNodeDict = queryPathNodeItem.data(0, Qt.UserRole).dict()
                order = queryPathNodeDict.get("order", 0)
                # save the value for order if it's greater
                if order == findOrder:
                    parentWidget = queryPathNodeItem
                    break
                tvPathIterator.__iadd__(1)
            else:
                break     
                
        return parentWidget        
        
    def populateTree(self, ):   
        self.clearTree()
#        print("path dict {}".format(self.pathTemplateDict))
        # add tree items
        if len(self.pathTemplateDict["queryPath"]) > 0:
            for tvPathDict in self.pathTemplateDict["queryPath"]:
                # create the tree view path item object
                pathItem = QueryPathNode(nodeDict=tvPathDict)
#                print("add path item {}".format(pathItem.displayName))
                # figure out who the parent is
                parent=self.findParentWidget(findOrder=pathItem.parentOrder)
                # add the treewidgetitem to the tree
                pathItem.treeItem = self.addTreeNode(parent=parent, pathItem=pathItem)
        else:
            # add a new root node
            pathItem = QueryPathNode(root=True, parentOrder=None, order=0, type="Path Template")
            pathItem.treeItem = self.addTreeNode(parent=self.tvPath, pathItem=pathItem)
            
        self.tvPath.resizeColumnToContents(0)  
        self.tvPath.setCurrentItem(self.tvPath.topLevelItem(0))
        
    def addTreeNode(self, parent=None, pathItem=None):
#        print("add tree node {}".format(pathItem.displayName))
        item = QTreeWidgetItem(parent, [pathItem.displayName])
        item.setData(0, Qt.UserRole, pathItem)
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        item.setFlags(  Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled )
        return item

            
###########################################################################################
# query path tree view methods
###########################################################################################    

    def openMenu(self,position):
        selected = self.tvPath.currentItem()
        if not (selected is None):
            tvPathNode = selected.data(0, Qt.UserRole)
            if (tvPathNode.type == "Path Template"):
                menu = QMenu()
                addNodeAction = menu.addAction("Add Node")
                addNodeAction.triggered.connect(self.addNodeTreeNode)                
                addNodeAction = menu.addAction("Add Relationship")
                addNodeAction.triggered.connect(self.addRelTreeNode)
                menu.exec_(self.tvPath.mapToGlobal(position))  
                return
            if (tvPathNode.type == "Node"):
                menu = QMenu()
#                addNodeAction = menu.addAction("Add Relationship")
#                addNodeAction.triggered.connect(self.addRelTreeNode)
                subOutMenu = QMenu("Out Bound Relationships", parent=menu)
                # generate outboundrel menu items
                outBoundList = self.parent.model.getOutboundRelTemplates(nodeTemplateName = tvPathNode.templateName)
                for relTemplate in outBoundList:
                    aSubAction = subOutMenu.addAction(relTemplate["name"])
                    aSubAction.setData(relTemplate)
                    aSubAction.triggered.connect(self.addOutboundRel)
                if len(outBoundList) == 0:
                    aSubAction = subOutMenu.addAction("No Outbound Relationship Templates")
                menu.addMenu(subOutMenu)
                
                subInMenu = QMenu("In Bound Relationships", parent=menu)
                # generate outboundrel menu items
                inBoundList = self.parent.model.getInboundRelTemplates(nodeTemplateName = tvPathNode.templateName)
                for relTemplate in inBoundList:
                    aSubAction = subInMenu.addAction(relTemplate["name"])
                    aSubAction.setData(relTemplate)
                    aSubAction.triggered.connect(self.addInboundRel)
                if len(inBoundList) == 0:
                    aSubAction = subInMenu.addAction("No Inbound Relationship Templates")
                menu.addMenu(subInMenu)   
                
                removeNodeAction = menu.addAction("Remove this Node")
                removeNodeAction.triggered.connect(self.removeTreeNode)
                menu.exec_(self.tvPath.mapToGlobal(position))  
                return
            if (tvPathNode.type == "Relationship"):
                menu = QMenu()
                addNodeAction = menu.addAction("Add Node")
                addNodeAction.triggered.connect(self.addNodeTreeNode)
                addNodeAction = menu.addAction("Remove This Relationship")
                addNodeAction.triggered.connect(self.removeTreeNode)
                menu.exec_(self.tvPath.mapToGlobal(position))  
                return


    def addOutboundRel(self):
        # get the action that called this method
        aSubAction = QObject.sender(self)
        relTemplateDict = aSubAction.data()
        if not relTemplateDict is None:
            # add the rel template to the path
            self.addRelTreeNode(templateName=relTemplateDict["name"])
            # add the node template to the path
            self.addNodeTreeNode(templateName=relTemplateDict["toTemplate"])
        
    def addInboundRel(self):
        # get the action that called this method
        aSubAction = QObject.sender(self)
        relTemplateDict = aSubAction.data()
        if not relTemplateDict is None:
            # add the rel template to the path
            self.addRelTreeNode(templateName=relTemplateDict["name"])
            # add the node template to the path
            self.addNodeTreeNode(templateName=relTemplateDict["fromTemplate"])
        
    def addRelTreeNode(self, templateName=None):
        '''add a relationship tree-node into the query path tree'''
        parentItem = self.tvPath.currentItem()
        parentDict = parentItem.data(0, Qt.UserRole).dict()
        parentOrder = parentDict.get("order", 0)
        order = self.getMaxTreeOrder() + 1
#        print("add rel node {}-{}".format(order, parentOrder))
        queryPathNode = QueryPathNode(parentOrder=parentOrder, order=order, type="Relationship", templateName=templateName)
        queryPathNode.treeItem = self.addTreeNode(parent=parentItem, pathItem=queryPathNode)
        self.tvPath.setCurrentItem(queryPathNode.treeItem)


    def addNodeTreeNode(self, templateName=None):
        '''add a node tree-node into the query path tree'''
        # don't know why this happens...
        if type(templateName) is bool:
            templateName = None
        parentItem = self.tvPath.currentItem()
        parentDict = parentItem.data(0, Qt.UserRole).dict()
        parentOrder = parentDict.get("order", 0)
        order = self.getMaxTreeOrder() + 1
#        print("add node node {}-{}".format(order, parentOrder))
        queryPathNode = QueryPathNode(parentOrder=parentOrder, order=order, type="Node", templateName=templateName)
        queryPathNode.treeItem = self.addTreeNode(parent=parentItem, pathItem=queryPathNode)
        self.tvPath.setCurrentItem(queryPathNode.treeItem)

    def removeTreeNode(self):
        '''remove a node from the tree and all descedants'''
#        print("remove item")
        currentItem = self.tvPath.currentItem()
        parentItem = currentItem.parent()
        parentItem.removeChild(currentItem)
        self.tvPath.takeTopLevelItem(self.tvPath.indexOfTopLevelItem(currentItem))

#-----------------------------------------------------------------------------------------------------------------------
#  return grid methods
#-----------------------------------------------------------------------------------------------------------------------
    def createOutputModel(self):
#        SOURCE, SOURCENAME, COLTYPE, COLVAL, COLNAME, DISPLAYIT, SORT, GROUP
        model = QStandardItemModel(0, 8)
        model.setHeaderData(SOURCE, Qt.Horizontal, "Source")
        model.setHeaderData(SOURCENAME, Qt.Horizontal, "Source Name")
        model.setHeaderData(COLTYPE, Qt.Horizontal, "Column Type")
        model.setHeaderData(COLVAL, Qt.Horizontal, "Column Value")
        model.setHeaderData(COLNAME, Qt.Horizontal, "Column Name")
        model.setHeaderData(DISPLAYIT, Qt.Horizontal, "Display ?")
        model.setHeaderData(SORT, Qt.Horizontal, "Sort")
        model.setHeaderData(GROUP, Qt.Horizontal, "Group")
        
        return model   
        
    def addOutputRow(self, source=None, sourceName=None, colType=None, colVal=None, colName=None, displayIt=None, sort=None, group=None ):
        '''
        add a row to the output grid
        SOURCE, SOURCENAME, COLTYPE, COLVAL, COLNAME, DISPLAYIT, SORT, GROUP
        '''
        self.gridOutput.setSortingEnabled(False)
        # SOURCE
        if source is None:
            source = ""
        item1 = QStandardItem(source)
        item1.setEditable(True)
        # SOURCENAME
        if sourceName is None:
            sourceName = ""
        item2 = QStandardItem(sourceName)
        item2.setEditable(True)        
        # COLTYPE
        if colType is None:
            colType = ""
        item3 = QStandardItem(colType)
        item3.setEditable(True)
        # COLVAL
        if colVal is None:
            colVal = ""
        item4 = QStandardItem(colVal)
        item4.setEditable(True)                
        # COLNAME
        if colName is None:
            colName = ""
        item5 = QStandardItem(colName)
        item5.setEditable(True)
        # DISPLAYIT
        if displayIt is None:
            displayIt = Qt.Checked
        item6 = QStandardItem()
        item6.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item6.setText("Display")
        if displayIt in [0, 1, 2]:
            item6.setCheckState(displayIt)  
        else:
            item2.setCheckState(Qt.Unchecked)  
        
        item6.setEditable(True)        
        # SORT
        if sort is None:
            sort = "No"
        item7 = QStandardItem(sort)
        item7.setEditable(True)
        # GROUP
        if group is None:
            group = "No"
        item8 = QStandardItem(group)
        item8.setEditable(True)      
        
        self.gridOutput.model().appendRow([item1,item2,item3,item4,item5,item6,item7,item8 ])        


        
    @pyqtSlot()
    def on_btnSaveAs_clicked(self):
        """
        User clicks button to save the generated query
        """
        return
    
    @pyqtSlot()
    def on_btnAdd_clicked(self):
        """
        User clicks Add Property
        """
        self.addOutputRow()
    
    @pyqtSlot()
    def on_btnRemove_clicked(self):
        """
        User clicks remove row button
        """
        indexes = self.gridOutput.selectionModel().selectedIndexes()
        for index in indexes:
            self.gridOutput.model().removeRows(index.row(),1)
    
    @pyqtSlot()
    def on_btnUp_clicked(self):
        """
        User clicks Up button
        """
        self.helper.moveTableViewRowUp(self.gridOutput)
    
    @pyqtSlot()
    def on_btnDown_clicked(self):
        """
        User clicks Down button
        """
        self.helper.moveTableViewRowDown(self.gridOutput)
    
    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    def on_tvPath_currentItemChanged(self, current, previous):
        """
        Slot documentation goes here.
        
        @param current DESCRIPTION
        @type QTreeWidgetItem
        @param previous DESCRIPTION
        @type QTreeWidgetItem
        """
        return
    
    
    @pyqtSlot(QModelIndex)
    def on_tvPath_clicked(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
#        print("on_tvPath_clicked")
        return
    
    @pyqtSlot(QModelIndex)
    def on_tvPath_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
#        print("on_tvPath_activated")
        return
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tvPath_itemClicked(self, item, column):
        """
        Slot documentation goes here.
        
        @param item DESCRIPTION
        @type QTreeWidgetItem
        @param column DESCRIPTION
        @type int
        """
#        print("on_tvPath_itemClicked")
        return
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tvPath_itemActivated(self, item, column):
        """
        Slot documentation goes here.
        
        @param item DESCRIPTION
        @type QTreeWidgetItem
        @param column DESCRIPTION
        @type int
        """
#        print("on_tvPath_itemActivated")
        return
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tvPath_itemEntered(self, item, column):
        """
        Slot documentation goes here.
        
        @param item DESCRIPTION
        @type QTreeWidgetItem
        @param column DESCRIPTION
        @type int
        """
#        print("on_tvPath_itemEntered")
        return
    
    @pyqtSlot()
    def on_tvPath_itemSelectionChanged(self):
        """
        Slot documentation goes here.
        """
#        print("on_tvPath_itemSelectionChanged")
        selected = self.tvPath.currentItem()
        if not (selected is None):
#            parent = self.tvPath.currentItem().parent()
            queryPathNode = selected.data(0, Qt.UserRole)
            self.populateMetaBox(queryPathNode=queryPathNode)

            
            
        
