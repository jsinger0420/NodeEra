# -*- coding: utf-8 -*-

"""
Module implementing FormPropertyBox.
"""
from PyQt5.QtCore import pyqtSlot, QSettings, Qt, QModelIndex, QObject
from PyQt5.QtGui import QStandardItemModel,  QStandardItem
from PyQt5.QtWidgets import QWidget, QDialog,  QVBoxLayout, QAbstractItemView, QHeaderView, QTreeWidgetItem, QMenu, QTreeWidgetItemIterator

from core.helper import Helper
from core.FormItem import FormDef, FormRowDef, LabelWidgetDef, ButtonWidgetDef
from .Ui_FormPropertyBox import Ui_FormPropertyBox
from forms.FormMain import FormMain
ATTRNAME, ATTRVALUE = range(2)

class FormPropertyBox(QDialog, Ui_FormPropertyBox):
    """
    Form Definition Editor
    """
    def __init__(self, parent=None, mode=None, objectDict = None, designModel = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FormPropertyBox, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.schemaModel = self.parent.schemaObject 
        self.settings = QSettings()
        self.helper = Helper()
        self.designModel = designModel
        self.modelData = self.designModel.modelData
        if objectDict is None:
            self.objectDict = self.designModel.newFormDict()
        else:
            self.objectDict = objectDict
        self.mode = mode

        # path treeview setup
        self.tvOutline.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tvOutline.customContextMenuRequested.connect(self.openMenu)
        self.tvOutline.setDragDropMode(QAbstractItemView.DragOnly)

        # add preview widget
        self.formPreview = FormMain(self.frmPreview )
        self.formPreviewLayout = QVBoxLayout(self.frmPreview)
        self.formPreviewLayout.setObjectName("MainFormLayout")
        self.formPreviewLayout.addWidget(self.formPreview)    


        self.populatingMetaBox = False
                       

        
        # position the splitter
        self.show()  # you have to do this to force all the widgets sizes to update 
        third = int((self.width()  / 3)) 
        self.vSplitter.setSizes([third*2, third])   
        half = int((self.height()  / 2)) 
        self.hSplitter.setSizes([half, half])   
        
        #populate ui data from object
        self.populateUIfromObject()

    def populateUIfromObject(self):
        self.populateTree()
        self.genForm()

    def genForm(self):
        '''generate the user defined form
        '''
        if self.validate():
            self.apply()
            self.formPreview.generateForm(formDict=self.objectDict)
        
#-----------------------------------------------------------------------------------------------------------------------
#  tree view methods
#-----------------------------------------------------------------------------------------------------------------------        
    def clearTree(self):
        self.tvOutline.clear()
        self.tvOutline.setColumnCount(1)
        self.tvOutline.setHeaderLabels(["Form Outline"])
        self.tvOutline.setItemsExpandable(True)        

    def getMaxTreeOrder(self, ):
        '''scan the tree and find the max itemNum attribute.  This is used to increment and create the next highest item number'''
        max = 0
        # iterate through the treeview
        tvPathIterator = QTreeWidgetItemIterator(self.tvOutline, flags = QTreeWidgetItemIterator.All)
        while tvPathIterator:
            if not tvPathIterator.value() is None:
                formTVItem = tvPathIterator.value()
                formItem = formTVItem.data(0, Qt.UserRole)
                # save the value for order if it's greater
                if formItem.itemDict["idNum"] > max:
                    max = formItem.itemDict["idNum"]
                tvPathIterator.__iadd__(1)
            else:
                break       
        return max
    
        
    def populateTree(self, ):   
        self.clearTree()
#        print("path dict {}".format(self.objectDict))
        # add tree items
        if len(self.objectDict["formOutline"]) > 0:
            for formItemDict in self.objectDict["formOutline"]:
                # create the tree view form item object
                if formItemDict["type"] == "Form":
                    formItem = FormDef(itemDict=formItemDict)
                if formItemDict["type"] == "Row":
                    formItem = FormRowDef(itemDict=formItemDict)
                if formItemDict["type"] == "Widget":
                    if formItemDict["widgetType"] == "Label":
                        formItem = LabelWidgetDef(itemDict=formItemDict)   
                    if formItemDict["widgetType"] == "Button":
                        formItem = ButtonWidgetDef(itemDict=formItemDict)                       
                # get the parent tree view widget
                parent = self.findParentWidget(findID=formItemDict["parentID"])
                # add the treewidgetitem to the tree
                formItem.treeItem = self.addTreeNode(parent=parent, formItem=formItem)
        else:
            # add a new root node
            formItem = FormDef(root=True,  idNum=0, parentID=None, type="Form", itemName=self.objectDict["name"])
            formItem.treeItem = self.addTreeNode(parent=self.tvOutline, formItem=formItem)
            
        self.tvOutline.resizeColumnToContents(0)  
        self.tvOutline.setCurrentItem(self.tvOutline.topLevelItem(0))
     
        
    def addTreeNode(self, parent=None, formItem=None):
#        print("add tree node {}".format(pathItem.displayName))
        item = QTreeWidgetItem(parent, [formItem.displayName])
        item.setData(0, Qt.UserRole, formItem)
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        item.setFlags(  Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled )
        return item

    def findParentWidget(self, findID=None):
        '''scan the tree and find the treeviewwidget with the matching parentOrder'''
        # if the find id is None then this is the root so return the tree view itself
        if findID is None:
            return self.tvOutline
        # find the parent tree view widget
        parentWidget = None
        # iterate through the treeview
        tvOutlineIterator = QTreeWidgetItemIterator(self.tvOutline, flags = QTreeWidgetItemIterator.All)
        while tvOutlineIterator:
            if not tvOutlineIterator.value() is None:
                # get the treeview widget
                tvWidget = tvOutlineIterator.value()
                # get the form item object from the widget
                formItem = tvWidget.data(0, Qt.UserRole)
                # get the idNum of the form item object
                idNum = formItem.itemDict["idNum"]
                # check to see if this is the idNum we're looking for
                if idNum == findID:
                    parentWidget = tvWidget
                    break
                tvOutlineIterator.__iadd__(1)
            else:
                break     
                
        return parentWidget        
        
    def openMenu(self,position):
        selected = self.tvOutline.currentItem()
        if not (selected is None):
            tvFormItem = selected.data(0, Qt.UserRole)
            if (tvFormItem.itemDict["type"] == "Form"):
                menu = QMenu()
                addItemAction = menu.addAction("Add Row")
                addItemAction.triggered.connect(self.addRow)                
                menu.exec_(self.tvOutline.mapToGlobal(position))  
                return
            if (tvFormItem.itemDict["type"] == "Row"):
                menu = QMenu()
                addItemAction = menu.addAction("Add Button Widget")
                addItemAction.triggered.connect(self.addButtonWidget)      
                addItemAction = menu.addAction("Add Label Widget")
                addItemAction.triggered.connect(self.addLabelWidget)      
                addItemAction = menu.addAction("Remove This Row")
                addItemAction.triggered.connect(self.removeRow)
                menu.exec_(self.tvOutline.mapToGlobal(position))  
                return
            if (tvFormItem.itemDict["type"] == "Widget"):
                menu = QMenu()
                addItemAction = menu.addAction("Remove This Widget")
                addItemAction.triggered.connect(self.removeWidget)
                menu.exec_(self.tvOutline.mapToGlobal(position))  
                return


        
    def addRow(self):
        parentTVItem = self.tvOutline.currentItem()
        parentFormItem = parentTVItem.data(0, Qt.UserRole)
        parentID = parentFormItem.itemDict["idNum"]
        nextID = self.getMaxTreeOrder() + 1
        newFormItem = FormRowDef(parentID=parentID, idNum=nextID, type="Row")
        newFormItem.treeItem = self.addTreeNode(parent=parentTVItem, formItem=newFormItem)
        self.tvOutline.setCurrentItem(newFormItem.treeItem)
        
        # update form view
        self.genForm()
        
    def removeRow(self):
        self.removeTVItem()

    def addLabelWidget(self):
        self.addWidget(type="Label")

    def addButtonWidget(self):
        self.addWidget(type="Button")
        
    def addWidget(self, type=None):
        
        parentTVItem = self.tvOutline.currentItem()
        parentFormItem = parentTVItem.data(0, Qt.UserRole)
        parentID = parentFormItem.itemDict["idNum"]
        nextID = self.getMaxTreeOrder() + 1
        if type == "Label":
            newFormItem = LabelWidgetDef(parentID=parentID, idNum=nextID, type="Widget")
        if type == "Button":
            newFormItem = ButtonWidgetDef(parentID=parentID, idNum=nextID, type="Widget")
        if not newFormItem is None:
            newFormItem.treeItem = self.addTreeNode(parent=parentTVItem, formItem=newFormItem)
            self.tvOutline.setCurrentItem(newFormItem.treeItem)
        # update form view
        self.genForm()        
        
    def removeWidget(self):
        self.removeTVItem()
        
    def removeTVItem(self):
        '''remove a form item from the tree and all descedants'''
        currentItem = self.tvOutline.currentItem()
        formDefItem = currentItem.data(0, Qt.UserRole)
        if formDefItem.itemDict["type"] == "Form":
            self.helper.displayErrMsg("Form Editor", "Cannot remove the form definition")
            return
        parentItem = currentItem.parent()
        parentItem.removeChild(currentItem)
        self.tvOutline.takeTopLevelItem(self.tvOutline.indexOfTopLevelItem(currentItem))
        
        # update form view
        self.genForm()        
        
    def validate(self):
        
        return True
        
    def apply(self):
        '''save the object dictionary'''
        formItemList = []
        # iterate through the treeview
        tvOutlineIterator = QTreeWidgetItemIterator(self.tvOutline, flags = QTreeWidgetItemIterator.All)
        while tvOutlineIterator:
            if not tvOutlineIterator.value() is None:
                 # get the treeview widget
                tvWidget = tvOutlineIterator.value()
                # get the form item object from the widget
                formDefItem = tvWidget.data(0, Qt.UserRole)
                if formDefItem.itemDict["type"] == "Form":
                    self.objectDict["name"] = formDefItem.itemDict["itemName"]
                    self.objectDict["description"] = formDefItem.itemDict["description"]
                formItemList.append(formDefItem.dict())
                tvOutlineIterator.__iadd__(1)
            else:
                break
            
        self.objectDict["formOutline"] = formItemList
        self.designModel.setModelDirty()     
        
    @pyqtSlot()
    def on_btnAdd_clicked(self):
        """
        User clicks the add button
        """
        selected = self.tvOutline.currentItem()
        if not (selected is None):
            tvFormItem = selected.data(0, Qt.UserRole)
            if (tvFormItem.type == "Form"):
                self.addRow()
                return
            if (tvFormItem.type == "Row"):
                self.addWidget()
                return
            if (tvFormItem.type == "Widget"):
                self.helper.displayErrMsg("Form Design", "Cannot add anything below a widget")
                return

    
    @pyqtSlot()
    def on_btnRemove_clicked(self):
        """
        User clicks remove button
        """
        self.removeTVItem()
    
    @pyqtSlot()
    def on_btnUp_clicked(self):
        """
        User clicks the up button
        """
        print("move tree item up")
        
    @pyqtSlot()
    def on_btnDown_clicked(self):
        """
        User clicks the down button
        """
        print("move tree item down")
    
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.validate():
            self.apply()
            QDialog.accept(self)
            

    
    @pyqtSlot()
    def on_tvOutline_itemSelectionChanged(self):
        """
        User clicks on an item in the tree view
        """
        print("on_tvOutline_itemSelectionChanged")
        selected = self.tvOutline.currentItem()
        if not (selected is None):
#            parent = self.tvPath.currentItem().parent()
            formDefItem = selected.data(0, Qt.UserRole)
            self.populateMetaBox(formDefItem=formDefItem)

 
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
#        self.lblMetaHeader.setText("Definition")
        # metabox grid setup
#        ATTRNAME, ATTRVALUE  gridMetaBox
        self.gridMetaBox.setModel(None)
        self.metaBoxModel = self.createMetaBoxModel()
        self.gridMetaBox.setModel(self.metaBoxModel)
        self.gridMetaBox.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridMetaBox.setSelectionMode(QAbstractItemView.SingleSelection)
        self.gridMetaBox.setColumnWidth(ATTRNAME, 150)   
        self.gridMetaBox.setColumnWidth(ATTRVALUE, 300)   
        # hide vertical header
        vheader = self.gridMetaBox.verticalHeader()
        vheader.hide()
        # header
        header = self.gridMetaBox.horizontalHeader()
        header.setSectionResizeMode(ATTRNAME, QHeaderView.Fixed) 
        header.setSectionResizeMode(ATTRVALUE, QHeaderView.Stretch) 
        # set editor delegate
#        self.gridMetaBox.setItemDelegateForColumn(ATTRVALUE, MetaBoxDelegate(self))
#        self.gridMetaBox.itemDelegateForColumn(ATTRVALUE).closeEditor.connect(self.metaBoxEditorClosed)
        # connect model slots 
        self.metaBoxModel.itemChanged.connect(self.metaBoxModelItemChanged)
        # connect grid slots
        self.gridMetaBox.selectionModel().selectionChanged.connect(self.metaBoxGridSelectionChanged)    
      
    def addMetaRow(self, attribute=None, dictKey=None, value=None, editable=None ):
        '''
        add a row to the  metabox grid
        '''
#        print("add metarow {}-{}-{}".format(attribute, value, editable))
        self.gridMetaBox.setSortingEnabled(False)
        # attribute
        if attribute is None:
            attribute = ""
        item1 = QStandardItem(attribute)
        # save the dictKey in the attribute name so we can update the itemDict later
        item1.setData(dictKey, Qt.UserRole)
        item1.setEditable(False)
        # value
        if value is None:
            value = ""
        item2 = QStandardItem(str(value))
        # save the attribute name in the value item so the custom editor MetaBoxDelegate can find it
        item2.setData(attribute, Qt.UserRole)
        item2.setEditable(editable)        
        
        self.gridMetaBox.model().appendRow([item1,item2 ])                


    def populateMetaBox(self, formDefItem=None):
        self.populatingMetaBox = True
        if not formDefItem is None:
            self.clearMetaBox()
            for attr in formDefItem.attributes():
                self.addMetaRow(attribute=attr[0], dictKey = attr[1], value=formDefItem.itemDict[attr[1]], editable=attr[2] )       
                
        self.populatingMetaBox = False
        
        
    def metaBoxModelItemChanged(self, item):
        if self.populatingMetaBox == False:
            print("item data changed {} at row:{} col:{}".format(str(item.checkState()), item.index().row(), item.index().column()))
            # a cell changed so see if other changes are needed
            selected = self.tvOutline.currentItem()
            if not (selected is None):
                formDefItem = selected.data(0, Qt.UserRole)  
#                name= self.gridMetaBox.model().item(item.index().row(),ATTRNAME).data(Qt.EditRole)
                # get the dictionary key for this attribute
                name= self.gridMetaBox.model().item(item.index().row(),ATTRNAME).data(Qt.UserRole)
                # get the value entered by the user
                value= self.gridMetaBox.model().item(item.index().row(),ATTRVALUE).data(Qt.EditRole)
                formDefItem.updateAttr(name=name, value=value)
                # update the tree view description
                formDefItem.updateTreeView()

            # force selection of this cell
            self.gridMetaBox.setCurrentIndex(item.index())
        
            # update form view
            self.genForm()

    def metaBoxGridSelectionChanged(self):
        # not used
        print("metabox grid selection changed")
        return
    
