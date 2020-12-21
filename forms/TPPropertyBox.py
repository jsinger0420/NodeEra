# -*- coding: utf-8 -*-

"""
Module implementing TPPropertyBox.
"""

from PyQt5.QtCore import pyqtSlot, QSettings, Qt, QModelIndex, QObject
from PyQt5.QtGui import QStandardItemModel,  QStandardItem
from PyQt5.QtWidgets import QWidget, QDialog,  QVBoxLayout, QAbstractItemView, QHeaderView, QTreeWidgetItem, QMenu, QTreeWidgetItemIterator
from core.helper import Helper, CBDelegate
from core.CypherGenPath import CypherGenPath
from core.NeoDriver import NeoDriver
from core.QueryPathNode import QueryPathNode
from core.MetaBoxDelegate import MetaBoxDelegate
from forms.DataGridWidget import DataGridWidget
from .Ui_TPPropertyBox import Ui_TPPropertyBox

MODENEW = 1
MODEEDIT = 2
#enums for metabox stacked widget
NODEBOX=1
RELBOX=2
#enums for metabox grid
ATTRNAME, ATTRVALUE = range(2)
#enums for propbox grid
PROPRETURN, PROPPARM, PROPNAME, COLNAME = range(4)
#enums for main tabs
DEFINITION, DESCRIPTION, DATAGRID = range(3)

class TPPropertyBox(QDialog, Ui_TPPropertyBox):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, mode=None, objectDict=None, designModel = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(TPPropertyBox, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.schemaModel = self.parent.schemaObject 
        self.settings = QSettings()
        self.helper = Helper()
        self.designModel = designModel
        self.modelData = self.designModel.modelData
        if objectDict is None:
            self.objectDict = self.designModel.newPathTemplateDict()
        else:
            self.objectDict = objectDict
        self.mode = mode
        
        # get the class that controls the data grid for relationship templates
        self.CypherGenPath = CypherGenPath(parent=self, templateDict=self.objectDict)
        
        # get neocon object for this project page
        self.neoCon = NeoDriver(name=self.parent.pageItem.neoConName, promptPW=self.parent.pageItem.promptPW)
        
        # path treeview setup
        self.tvPath.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tvPath.customContextMenuRequested.connect(self.openMenu)
        self.tvPath.setDragDropMode(QAbstractItemView.DragOnly)

        # add the data grid widget.  
        self.nodeGrid = DataGridWidget(self, neoCon=self.neoCon, genCypher=self.CypherGenPath)
        self.nodeGridLayout = QVBoxLayout(self.dataTabFrame)
        self.nodeGridLayout.setObjectName("nodeGridLayout")
        self.nodeGridLayout.addWidget(self.nodeGrid)    

        self.populatingMetaBox = False
                       
        #populate ui data from object
        self.populateUIfromObject()

        if self.mode == "NEW":
            self.txtPathTemplateName.setFocus()               
        else: 
            # disable definition fields
            self.txtPathTemplateName.setEnabled(False)
            
        
    def populateUIfromObject(self):
        self.txtPathTemplateName.setText(self.objectDict["name"])        
        self.editDescription.appendPlainText(self.objectDict["description"])
        self.populateTree()
        
    def validate(self):
        if self.objectDict is None:
            self.objectDict = {}
        templateName = self.txtPathTemplateName.text()
        # template name
        if self.helper.NoTextValueError(templateName, "Must enter a Path Template Name"):
            self.txtPathTemplateName.setFocus()
            return False
        # find duplicate cypher variables
        varList = []
        # iterate through the treeview
        tvPathIterator = QTreeWidgetItemIterator(self.tvPath, flags = QTreeWidgetItemIterator.All)
        returnCount = 0
        while tvPathIterator:
            if not tvPathIterator.value() is None:
                queryPathNodeItem = tvPathIterator.value()
                thisQueryPathNode = queryPathNodeItem.data(0, Qt.UserRole)
                if thisQueryPathNode.type in ["Node", "Relationship"]:
                    returnCount = returnCount + thisQueryPathNode.numReturnProps()
                    if returnCount < 1:
                        self.helper.displayErrMsg(thisQueryPathNode.templateName, "Must return at least one property.")
                        return False
                    if self.helper.NoTextValueError(thisQueryPathNode.templateName, "Must supply a template name."):
                        return False
                    if self.helper.NoTextValueError(thisQueryPathNode.cypherVar, "Must supply a cypher variable for {}.".format(thisQueryPathNode.templateName)):
                        return False
                    if thisQueryPathNode.cypherVar in varList:
                        self.helper.displayErrMsg("Validate Path", "Error - duplicate cypher variable {} defined in template: {} ".format(thisQueryPathNode.cypherVar, thisQueryPathNode.templateName))
                        return False
                    if thisQueryPathNode.templateName == "No Template Selected" and thisQueryPathNode.blankTemplate == False:
                        self.helper.displayErrMsg("Validate Path", "Error - must select a template or set blank template to True ")
                        return False
                        
                    varList.append(thisQueryPathNode.cypherVar)
                tvPathIterator.__iadd__(1)  
            else:
                break   
        # passed all edits so return True
        return True
        
    def apply(self, ):
        '''save the object dictionary'''
        self.objectDict["name"] = self.txtPathTemplateName.text()  
        self.objectDict["description"] =  self.editDescription.toPlainText()
        nodeList = []
        # iterate through the treeview
        tvPathIterator = QTreeWidgetItemIterator(self.tvPath, flags = QTreeWidgetItemIterator.All)
        while tvPathIterator:
            if not tvPathIterator.value() is None:
#                print("save node {}".format(tvPathIterator.value().text(0)))
                queryPathNodeItem = tvPathIterator.value()
                queryPathNodeDict = queryPathNodeItem.data(0, Qt.UserRole).dict()
                nodeList.append(queryPathNodeDict)
                tvPathIterator.__iadd__(1)
            else:
                break
            
        self.objectDict["queryPath"] = nodeList
        self.designModel.setModelDirty()     


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
        self.gridMetaBox.setColumnWidth(ATTRNAME, 150)   
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
        self.populatingMetaBox = True
        if not queryPathNode is None:
            self.clearMetaBox()
            self.lblMetaHeader.setText("{} Definition".format(queryPathNode.type))
            for attr in queryPathNode.attributes():
                self.addMetaRow(attribute=attr[0], value=attr[1], editable=attr[2] )                
        self.populatingMetaBox = False
        
        
    def metaBoxModelItemChanged(self, item):
        if self.populatingMetaBox == False:
            print("item data changed {} at row:{} col:{}".format(str(item.checkState()), item.index().row(), item.index().column()))
            # a cell changed so see if other changes are needed
            # update the queryPathNode object
            selected = self.tvPath.currentItem()
            if not (selected is None):
                queryPathNode = selected.data(0, Qt.UserRole)  
                name= self.gridMetaBox.model().item(item.index().row(),ATTRNAME).data(Qt.EditRole)
                value= self.gridMetaBox.model().item(item.index().row(),ATTRVALUE).data(Qt.EditRole)
                queryPathNode.updateAttr(name=name, value=value)
    #            if name == "Blank Template" and value == "True":
    #                # set template name to first entry in list
    #                queryPathNode.updateAttr(name="Node Template", value="No Template Selected")
                # reload the metabox since changing one property can update others
                self.populateMetaBox(queryPathNode=queryPathNode)
                # repopulate return property grid as template may have 
                self.populatePropBox(queryPathNode=queryPathNode)            
                # update the tree view description
                queryPathNode.updateTreeView()
                # refresh cypher view
                self.refreshCypher()

    #        # update displayName
    #        self.rePopulateMetaBox(queryPathNode=queryPathNode)
            # force selection of this cell
            self.gridMetaBox.setCurrentIndex(item.index())


    def metaBoxGridSelectionChanged(self):
        # not used
#        print("metabox grid selection changed")
        return

    def getCurrentCypherVar(self, ):
        # get the queryPathNode object
        selected = self.tvPath.currentItem()
        if not (selected is None):
            queryPathNode = selected.data(0, Qt.UserRole)  
            return queryPathNode.cypherVar
        return None
        
#-----------------------------------------------------------------------------------------------------------------------
#  property box grid methods
#-----------------------------------------------------------------------------------------------------------------------        
    def createPropBoxModel(self):
#       PROPRETURN, PROPPARM, PROPNAME, COLNAME
        model = QStandardItemModel(0, 4)
        model.setHeaderData(PROPRETURN, Qt.Horizontal, "Return")
        model.setHeaderData(PROPPARM, Qt.Horizontal, "Parameter")
        model.setHeaderData(PROPNAME, Qt.Horizontal, "Property/Function")
        model.setHeaderData(COLNAME, Qt.Horizontal, "Column Name")
        return model    
        
    def clearPropBox(self):
        # property box grid setup
#       PROPRETURN, PROPPARM, PROPNAME, COLNAME
        self.gridPropBox.setModel(None)
        self.propBoxModel = self.createPropBoxModel()
        self.gridPropBox.setModel(self.propBoxModel)
        self.gridPropBox.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridPropBox.setSelectionMode(QAbstractItemView.SingleSelection)
        self.gridPropBox.setColumnWidth(PROPRETURN, 100)   
        self.gridPropBox.setColumnWidth(PROPPARM, 100)   
        self.gridPropBox.setColumnWidth(PROPNAME, 400)   
        self.gridPropBox.setColumnWidth(COLNAME, 400)   
        # header
        header = self.gridPropBox.horizontalHeader()
        header.setSectionResizeMode(PROPRETURN, QHeaderView.Fixed) 
        header.setSectionResizeMode(PROPPARM, QHeaderView.Fixed) 
        header.setSectionResizeMode(PROPNAME, QHeaderView.Stretch) 
        header.setSectionResizeMode(COLNAME, QHeaderView.Stretch) 
        # set editor delegate
#        self.gridPropBox.setItemDelegateForColumn(PROPNAME, MetaBoxDelegate(self))
        # connect model slots 
        self.propBoxModel.itemChanged.connect(self.propBoxModelItemChanged)
        # connect grid slots
        self.gridPropBox.selectionModel().selectionChanged.connect(self.propBoxGridSelectionChanged)    
      
#    def addPropRow(self, propName=None, colName=None, propParm=None, propReturn=None ):
    def addPropRow(self, returnProp=None ):
        '''
        add a row to the property box grid
        '''
        #  PROPRETURN, PROPPARM, PROPNAME, COLNAME
        self.gridPropBox.setSortingEnabled(False)
        # checkbox to add property to the return clause
        propReturn = returnProp[PROPRETURN]
        if propReturn is None or propReturn == "":
            propReturn = Qt.Unchecked
        item1 = QStandardItem()
        item1.setEditable(True)   
        item1.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)        
#        # save the attribute name in the value item so the custom editor MetaBoxDelegate can find it
#        item1.setData(propReturn, Qt.UserRole)
        if propReturn in [0, 1, 2]:
            item1.setCheckState(propReturn)  
        else:
            item1.setCheckState(Qt.Unchecked)  
        item1.setText("")
        
        # checkbox to indicate property is a parameter
        propParm = returnProp[PROPPARM]
        if propParm is None or propParm == "":
            propParm = Qt.Unchecked
        item2 = QStandardItem()
        item2.setEditable(True)   
        item2.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)        
#        # save the attribute name in the value item so the custom editor MetaBoxDelegate can find it
#        item2.setData(propParm, Qt.UserRole)
        if propParm in [0, 1, 2]:
            item2.setCheckState(propParm)  
        else:
            item2.setCheckState(Qt.Unchecked)  
        item2.setText("")
        
        # property name
        if returnProp[PROPNAME] is None:
            returnProp[PROPNAME] = ""
        item3 = QStandardItem(returnProp[PROPNAME])
        item3.setEditable(False)

        # column name
        if returnProp[COLNAME] is None or returnProp[COLNAME] == "":
            colName = "{}_{}".format(str(self.getCurrentCypherVar()), returnProp[PROPNAME])
        else:
            colName = returnProp[COLNAME]
        item4 = QStandardItem(colName)
        item4.setEditable(True)
        
        
        # add it to the grid
        self.gridPropBox.model().appendRow([item1,item2, item3, item4 ])                

    def populatePropBox(self, queryPathNode=None):
#        PROPRETURN, PARAMETER, PROPNAME, COLNAME
        if not queryPathNode is None:
            self.clearPropBox()
            for returnProp in queryPathNode.returnProps:
                self.addPropRow(returnProp)                

        
    def propBoxModelItemChanged(self, item):
        # a cell changed so see if other changes are needed
        # update the queryPathNode object
        # print("item data changed {} {} at row:{} col:{}".format(str(item.checkState()), propName, item.index().row(), item.index().column()))            
        selected = self.tvPath.currentItem()
        if not (selected is None):
            queryPathNode = selected.data(0, Qt.UserRole)  
            propName= self.gridPropBox.model().item(item.index().row(),PROPNAME).data(Qt.EditRole)
            colName= self.gridPropBox.model().item(item.index().row(),COLNAME).data(Qt.EditRole)
            propReturn= self.gridPropBox.model().item(item.index().row(),PROPRETURN).checkState()
            propParm= self.gridPropBox.model().item(item.index().row(),PROPPARM).checkState()
            queryPathNode.updateProp([propReturn, propParm, propName, colName])
            self.refreshCypher()   
        
        # force selection of this cell
        self.gridPropBox.setCurrentIndex(item.index())


    def propBoxGridSelectionChanged(self):
        # not used
#        print("propbox grid selection changed")
        return

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
#        print("path dict {}".format(self.objectDict))
        # add tree items
        if len(self.objectDict["queryPath"]) > 0:
            for tvPathDict in self.objectDict["queryPath"]:
                # create the tree view path item object
                pathItem = QueryPathNode(designModel = self.designModel, nodeDict=tvPathDict)
#                print("add path item {}".format(pathItem.displayName))
                # figure out who the parent is
                parent=self.findParentWidget(findOrder=pathItem.parentOrder)
                # add the treewidgetitem to the tree
                pathItem.treeItem = self.addTreeNode(parent=parent, pathItem=pathItem)
        else:
            # add a new root node
            pathItem = QueryPathNode(designModel = self.designModel, root=True, parentOrder=None, order=0, type="Path Template")
            pathItem.treeItem = self.addTreeNode(parent=self.tvPath, pathItem=pathItem)
            
        self.tvPath.resizeColumnToContents(0)  
        self.tvPath.setCurrentItem(self.tvPath.topLevelItem(0))
        # update cypher
        self.refreshCypher()        
        
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
#                    print("outboundlist {}".format(relTemplate))
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
#                    print("inboundlist {}".format(relTemplate))
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
        queryPathNode = QueryPathNode(designModel = self.designModel, parentOrder=parentOrder, order=order, type="Relationship", templateName=templateName)
        # set a ypher variable name for the relationship
        queryPathNode.cypherVar = "r{}".format(str(queryPathNode.order).lower())
#        queryPathNode.reltype = self.designModel.getRelType(templateName)
        queryPathNode.treeItem = self.addTreeNode(parent=parentItem, pathItem=queryPathNode)
        self.tvPath.setCurrentItem(queryPathNode.treeItem)
        # update cypher
        self.refreshCypher()


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
        queryPathNode = QueryPathNode(designModel = self.designModel, parentOrder=parentOrder, order=order, type="Node", templateName=templateName)
        # set a cypher variable name for the Node
        queryPathNode.cypherVar = "{}".format(queryPathNode.templateName[0].lower())
        queryPathNode.treeItem = self.addTreeNode(parent=parentItem, pathItem=queryPathNode)
        self.tvPath.setCurrentItem(queryPathNode.treeItem)
        # update cypher
        self.refreshCypher()

    def removeTreeNode(self):
        '''remove a node from the tree and all descedants'''
#        print("remove item")
        currentItem = self.tvPath.currentItem()
        parentItem = currentItem.parent()
        parentItem.removeChild(currentItem)
        self.tvPath.takeTopLevelItem(self.tvPath.indexOfTopLevelItem(currentItem))
        # update cypher
        self.refreshCypher()

  
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.validate():
            self.apply()
            QDialog.accept(self)
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        User Selects the Cancel button
        """
        QDialog.reject(self)

    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    def on_tvPath_currentItemChanged(self, current, previous):
        """
        Not Used
        
        @param current DESCRIPTION
        @type QTreeWidgetItem
        @param previous DESCRIPTION
        @type QTreeWidgetItem
        """
        print("on tvpath current item changed")
        return
    
    
    @pyqtSlot(QModelIndex)
    def on_tvPath_clicked(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        print("on_tvPath_clicked")
    
    @pyqtSlot(QModelIndex)
    def on_tvPath_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        print("on_tvPath_activated")
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tvPath_itemClicked(self, item, column):
        """
        Slot documentation goes here.
        
        @param item DESCRIPTION
        @type QTreeWidgetItem
        @param column DESCRIPTION
        @type int
        """
        print("on_tvPath_itemClicked")
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tvPath_itemActivated(self, item, column):
        """
        Slot documentation goes here.
        
        @param item DESCRIPTION
        @type QTreeWidgetItem
        @param column DESCRIPTION
        @type int
        """
        print("on_tvPath_itemActivated")
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tvPath_itemEntered(self, item, column):
        """
        Slot documentation goes here.
        
        @param item DESCRIPTION
        @type QTreeWidgetItem
        @param column DESCRIPTION
        @type int
        """
        print("on_tvPath_itemEntered")
    
    @pyqtSlot()
    def on_tvPath_itemSelectionChanged(self):
        """
        User clicks on an item in the tree view
        """
        print("on_tvPath_itemSelectionChanged")
        selected = self.tvPath.currentItem()
        if not (selected is None):
#            parent = self.tvPath.currentItem().parent()
            queryPathNode = selected.data(0, Qt.UserRole)
            self.populateMetaBox(queryPathNode=queryPathNode)
            self.populatePropBox(queryPathNode=queryPathNode)
    
    @pyqtSlot(int)
    def on_tabPathTemplate_currentChanged(self, index):
        """
        The user has switched to a different tab
        DEFINITION, DESCRIPTION, DATAGRID
        @param index DESCRIPTION
        @type int
        """
        # user switched to the description tab.  regenerate the description
#        if index == DESCRIPTION:
#            if self.validate():
#                self.apply()
#                # get generated description
#                self.brwsrGenDescription.setText(self.designModel.getNodeDescription(self.objectDict["name"]))

        # user switched to the definition tab.  
#        if index == DEFINITION:
#            self.syncDefCheckBoxes()
        # user switched to the data grid then update object dictionary so query will generate with latest values
        if index == DATAGRID:
            if self.validate():
                self.apply()
                self.nodeGrid.refreshGrid()
            else:
                self.tabPathTemplate.setCurrentIndex(0)

    def refreshCypher(self):
            if self.validate():
                self.apply()        
                self.cypher, self.editParmDict = self.nodeGrid.genCypher.genMatch()
#                print("cypher:{}".format(self.cypher))
                self.txtCypher.clear()
                self.txtCypher.appendPlainText(self.cypher)
    
    @pyqtSlot()
    def on_btnAddNode_clicked(self):
        """
        user clicks on add node button
        """
        '''add a node tree-node into the query path tree'''
        parentItem = self.tvPath.currentItem()
        parentDict = parentItem.data(0, Qt.UserRole).dict()
        parentOrder = parentDict.get("order", 0)
        order = self.getMaxTreeOrder() + 1
        queryPathNode = QueryPathNode(designModel = self.designModel, parentOrder=parentOrder, order=order, type="Node", templateName="Anonymous Node")
        # set a cypher variable name for the Node
        queryPathNode.cypherVar = "n{}".format(str(queryPathNode.order).lower())
        queryPathNode.treeItem = self.addTreeNode(parent=parentItem, pathItem=queryPathNode)
        self.tvPath.setCurrentItem(queryPathNode.treeItem)
        # update cypher
        self.refreshCypher()
        
    @pyqtSlot()
    def on_btnAddRel_clicked(self):
        """
        user clicks on add relationship button
        """
        parentItem = self.tvPath.currentItem()
        parentDict = parentItem.data(0, Qt.UserRole).dict()
        parentOrder = parentDict.get("order", 0)
        order = self.getMaxTreeOrder() + 1
        queryPathNode = QueryPathNode(designModel = self.designModel, parentOrder=parentOrder, order=order, type="Relationship", templateName="Anonymous Relationship")
        # set a ypher variable name for the relationship
        queryPathNode.cypherVar = "r{}".format(str(queryPathNode.order).lower())
        queryPathNode.treeItem = self.addTreeNode(parent=parentItem, pathItem=queryPathNode)
        self.tvPath.setCurrentItem(queryPathNode.treeItem)
        # update cypher
        self.refreshCypher()
    
    @pyqtSlot()
    def on_btnRemove_clicked(self):
        """
        User clicks on remove button
        """
        return
    
    @pyqtSlot()
    def on_btnAdd_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_btnRemove_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
