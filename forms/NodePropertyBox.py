# -*- coding: utf-8 -*-

"""
    class implementing NodePropertyBox.
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
from copy import deepcopy
from PyQt5.QtCore import Qt, QSettings, pyqtSlot
from PyQt5.QtGui import QStandardItemModel,  QStandardItem
from PyQt5.QtWidgets import QDialog, QHeaderView, QVBoxLayout, QAbstractItemView, QAbstractScrollArea

from forms.TNodeFormatDlg import TNodeFormatDlg, TNodeFormat
from forms.INodeFormatDlg import INodeFormatDlg, INodeFormat
from forms.Ui_NodePropertyBox import Ui_NodePropertyBox
from forms.DataGridWidget import DataGridWidget

from core.Enums import DataType
from core.helper import Helper, CBDelegate
#from core.neocon import NeoCon
from core.NeoDriver import NeoDriver
from core.NodeTemplateCypher import NodeTemplateCypher
from core.ListPickerDelegate import ListPickerDelegate
from core.NeoEditDelegate import NeoEditDelegate

DEFINITION, CONSTRAINT, DESCRIPTION, FORMATS, DATAGRID = range(5)
LABEL, REQUIRED, NODEKEY = range(3)
# node template property list
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS, UNIQUE, PROPNODEKEY = range(7)
CONTYPE, CONLBL, CONPROPLIST = range(3)
AUTOINDEX, IDXLBL, IDXPROPLIST = range(3)


class NodePropertyBox(QDialog, Ui_NodePropertyBox):
    """
    Provide a modal dialog box that allows the user to edit a Node Template.
    """
    def __init__(self, parent=None, mode=None, objectDict=None, designModel=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(NodePropertyBox, self).__init__(parent)
        self.initUI = True
        self.parent = parent
        self.schemaModel = self.parent.schemaObject 
        self.formatChanged = False
        self.helper = Helper()
        self.setupUi(self)
        self.designModel = designModel
        self.modelData = self.designModel.modelData
        if objectDict is None:
            self.objectDict = self.defaultObjectDict()
        else:
            self.objectDict = objectDict
        self.mode = mode
        self.settings = QSettings()
        self.nodeTemplateCypher = NodeTemplateCypher(templateDict=self.objectDict)
        
        # get neocon object for this project page
        self.neoCon = NeoDriver(name=self.parent.pageItem.neoConName, promptPW=self.parent.pageItem.promptPW)


        # LABEL GRID
        self.gridLabels.setModel(self.createLabelModel())
        
        self.gridLabels.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        
        comboLblList = [""] 
        comboLblList.extend(sorted(set(self.designModel.instanceList("Label") + self.schemaModel.instanceList("Label"))))
#        comboLblList = self.designModel.loadComboBox(topLevel='Label', objectName=None, selectMsg="" )
        self.gridLabels.setItemDelegateForColumn(LABEL, CBDelegate(self, comboLblList, setEditable=True ))        
        self.gridLabels.setColumnWidth(LABEL, 200)
        self.gridLabels.setColumnWidth(REQUIRED, 100)
        self.gridLabels.setColumnWidth(NODEKEY, 100)
        self.gridLabels.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridLabels.setSelectionMode(QAbstractItemView.SingleSelection)
        
        header = self.gridLabels.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(LABEL, QHeaderView.Interactive) 
        header.setSectionResizeMode(REQUIRED, QHeaderView.Fixed)
        header.setSectionResizeMode(NODEKEY, QHeaderView.Fixed)

        # PROPERTY GRID
        self.gridProps.setModel(self.createPropModel())
        comboPropList = [""] 
        comboPropList.extend(sorted(set(self.designModel.instanceList("Property") + self.schemaModel.instanceList("Property"))))
#        comboPropList = self.designModel.loadComboBox(topLevel='Property', objectName=None, selectMsg="" )
        self.gridProps.setItemDelegateForColumn(PROPERTY, CBDelegate(self, comboPropList, setEditable=True ))
        dataTypeList = [dataType.value for dataType in DataType]
        self.gridProps.setItemDelegateForColumn(DATATYPE, CBDelegate(self, dataTypeList, setEditable=False))
        self.gridProps.setItemDelegateForColumn(PROPDEF, NeoEditDelegate(self))
        self.gridProps.setColumnWidth(PROPERTY, 350)
        self.gridProps.setColumnWidth(DATATYPE, 125)
        self.gridProps.setColumnWidth(PROPREQ, 100)
        self.gridProps.setColumnWidth(PROPDEF, 150)
        self.gridProps.setColumnWidth(EXISTS, 100)
        self.gridProps.setColumnWidth(REQUIRED, 100)
        self.gridProps.setColumnWidth(PROPNODEKEY, 100)
        self.gridProps.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridProps.setSelectionMode(QAbstractItemView.SingleSelection)

        header = self.gridProps.horizontalHeader()
        header.setSectionResizeMode(PROPERTY, QHeaderView.Interactive)  
        header.setSectionResizeMode(DATATYPE, QHeaderView.Fixed)  
        header.setSectionResizeMode(PROPREQ, QHeaderView.Fixed) 
        header.setSectionResizeMode(PROPDEF, QHeaderView.Interactive)  
        header.setSectionResizeMode(EXISTS, QHeaderView.Fixed)
        header.setSectionResizeMode(REQUIRED, QHeaderView.Fixed)
        header.setSectionResizeMode(PROPNODEKEY, QHeaderView.Fixed)

        # CONSTRAINT GRID - CONTYPE, CONLBL, CONPROP, CONPROPLIST
        self.gridConstraints.setModel(self.createConstraintsModel())
        conTypeList = ["Node Key", "Property Exists", "Property Unique"]
        self.gridConstraints.setItemDelegateForColumn(CONTYPE, CBDelegate(self, conTypeList, setEditable=False ))         
        self.gridConstraints.selectionModel().selectionChanged.connect(self.constraintGridSelectionChanged)

        self.gridConstraints.setColumnWidth(CONTYPE, 120)
        self.gridConstraints.setColumnWidth(CONLBL, 200)
        self.gridConstraints.setColumnWidth(CONPROPLIST, 428)
        self.gridConstraints.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridConstraints.setSelectionMode(QAbstractItemView.SingleSelection)

        header = self.gridConstraints.horizontalHeader()
        header.setSectionResizeMode(CONTYPE, QHeaderView.Fixed) 
        header.setSectionResizeMode(CONLBL, QHeaderView.Interactive)
        header.setSectionResizeMode(CONPROPLIST, QHeaderView.Interactive)

        # INDEX GRID - AUTOINDEX, IDXLBL, IDXPROPLIST
        self.gridIndex.setModel(self.createIndexModel())
        self.gridIndex.setColumnWidth(AUTOINDEX, 120)
        self.gridIndex.setColumnWidth(IDXLBL, 200)
        self.gridIndex.setColumnWidth(IDXPROPLIST, 428)
        self.gridIndex.selectionModel().selectionChanged.connect(self.indexGridSelectionChanged)
        self.gridIndex.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridIndex.setSelectionMode(QAbstractItemView.SingleSelection)
      
        header = self.gridIndex.horizontalHeader()
        header.setSectionResizeMode(AUTOINDEX, QHeaderView.Fixed) 
        header.setSectionResizeMode(IDXLBL, QHeaderView.Interactive)
        header.setSectionResizeMode(IDXPROPLIST, QHeaderView.Interactive)

        # add the data grid widget.  
        self.nodeGrid = DataGridWidget(self, neoCon=self.neoCon, genCypher=self.nodeTemplateCypher)
        self.nodeGridLayout = QVBoxLayout(self.dataTabFrame)
        self.nodeGridLayout.setObjectName("nodeGridLayout")
        self.nodeGridLayout.addWidget(self.nodeGrid)    
        
        #populate ui data from object
        self.populateUIfromObject()
        # populate combo boxes used on constraint and index grids
        self.updateComboBoxes()
        # sync definition checkboxes with constraints
        self.syncDefCheckBoxes()
        
        if self.mode == "NEW":
            self.editName.setFocus()
        else: 
            # disable name entry and set focus to description
            self.editName.setEnabled(False)
            self.editDescription.setFocus()  
        self.initUI = False

        # position the splitter
        self.show()  # you have to do this to force all the widgets sizes to update 
        third = int((self.height()  / 3)) 
        self.splitter.setSizes([third, third*2])   
        
    def updateComboBoxes(self):
        # populate constraint and index dropdowns from the template definition
        lblList = [""] + [ self.gridLabels.model().item(row,LABEL).data(Qt.EditRole) for row in range(0,self.gridLabels.model().rowCount())]
        self.gridConstraints.setItemDelegateForColumn(CONLBL, CBDelegate(self, lblList, setEditable=True ))        
        self.gridIndex.setItemDelegateForColumn(IDXLBL, CBDelegate(self, lblList, setEditable=True ))        
        propList = [""] + [ self.gridProps.model().item(row,PROPERTY).data(Qt.EditRole) for row in range(0,self.gridProps.model().rowCount())]    
        self.gridConstraints.setItemDelegateForColumn(CONPROPLIST, ListPickerDelegate(self, propList, setEditable=False ))      
        self.gridIndex.setItemDelegateForColumn(IDXPROPLIST, ListPickerDelegate(self, propList, setEditable=False ))      
        
        
    def createIndexModel(self):
        # INDEX GRID - AUTOINDEX, IDXLBL, IDXPROPLIST
        model = QStandardItemModel(0, 3)
        model.setHeaderData(AUTOINDEX, Qt.Horizontal, "Auto Generated")
        model.setHeaderData(IDXLBL, Qt.Horizontal, "LABEL")
        model.setHeaderData(IDXPROPLIST, Qt.Horizontal, "Property List")
        # connect model slots 
#        model.itemChanged.connect(self.indexModelItemChanged)
        return model        
    
    def createConstraintsModel(self):
        # CONSTRAINT GRID - CONTYPE, CONLBL, CONPROP, CONPROPLIST
        model = QStandardItemModel(0, 3)
        model.setHeaderData(CONTYPE, Qt.Horizontal, "Constraint Type")
        model.setHeaderData(CONLBL, Qt.Horizontal, "LABEL")
#        model.setHeaderData(CONPROP, Qt.Horizontal, "Property")
        model.setHeaderData(CONPROPLIST, Qt.Horizontal, "Property List")
        # connect model slots 
        model.itemChanged.connect(self.constraintModelItemChanged)
        return model
        
    def createLabelModel(self):
        # LABEL, REQUIRED, NODEKEY
        model = QStandardItemModel(0, 3)
        model.setHeaderData(LABEL, Qt.Horizontal, "Label")
        model.setHeaderData(REQUIRED, Qt.Horizontal, "Required")
        model.setHeaderData(NODEKEY, Qt.Horizontal, "Node Key")
        # connect model slots 
        model.itemChanged.connect(self.lblModelItemChanged)
        return model
    
    def createPropModel(self):
        # PROPERTY, EXISTS, UNIQUE, PROPNODEKEY
        model = QStandardItemModel(0, 7)
        model.setHeaderData(PROPERTY, Qt.Horizontal, "Property")
        model.setHeaderData(DATATYPE, Qt.Horizontal, "Data Type")
        model.setHeaderData(PROPREQ, Qt.Horizontal, "Required")
        model.setHeaderData(PROPDEF, Qt.Horizontal, "Default Value")
        model.setHeaderData(EXISTS, Qt.Horizontal, "Exists")
        model.setHeaderData(UNIQUE, Qt.Horizontal, "Unique")
        model.setHeaderData(PROPNODEKEY, Qt.Horizontal, "Node Key")
        # connect model slots 
        model.itemChanged.connect(self.propModelItemChanged)
        return model 
        
    def populateUIfromObject(self, ):
        if self.objectDict is not None:
            # get the custom template format if any
            self.templateNodeFormatDict = self.objectDict.get("TNformat", None)
            # get the custom instance format if any
            self.instanceNodeFormatDict = self.objectDict.get("INformat", None)
            
            if self.templateNodeFormatDict == None:
                self.rbTemplateDefaultFormat.setChecked(True)
                self.btnDefineTemplateFormat.setEnabled(False)
            else:
                self.rbTemplateCustomFormat.setChecked(True)
                self.btnDefineTemplateFormat.setEnabled(True)
                
            if self.instanceNodeFormatDict == None:
                self.rbInstanceDefaultFormat.setChecked(True)
                self.btnDefineInstanceFormat.setEnabled(False)
            else:
                self.rbInstanceCustomFormat.setChecked(True)
                self.btnDefineInstanceFormat.setEnabled(True)        
                
            self.editName.insert(str(self.objectDict["name"]))
            self.editDescription.appendPlainText(self.objectDict["desc"])
            
            #load Labels  LABEL, REQUIRED, NODEKEY
            for nodeLbl in self.objectDict["labels"]:
                self.addLabel(self.gridLabels.model(), nodeLbl[LABEL], nodeLbl[REQUIRED], nodeLbl[NODEKEY])
            #load props  PROPERTY, EXISTS, PROPREQ,PROPDEF,UNIQUE, PROPNODEKEY
            for nodeProp in self.objectDict["properties"]:
                dataType = self.designModel.getPropertyDataType(nodeProp[PROPERTY])
#                print("property {} has datatype {}".format(nodeProp[PROPERTY], dataType))
                self.addProp(self.gridProps.model(), nodeProp[PROPERTY], dataType, nodeProp[PROPREQ], nodeProp[PROPDEF], nodeProp[EXISTS], nodeProp[UNIQUE], nodeProp[PROPNODEKEY])
            # get generated description
            self.brwsrGenDescription.setText(self.designModel.getNodeDescription(self.objectDict["name"]))
            # load constraints
            try:
                #CONTYPE, CONLBL, CONPROP, CONPROPLIST
                for nodeCon in self.objectDict["constraints"]:
#                    self.addConstraint(self.gridConstraints.model(), nodeCon[CONTYPE], nodeCon[CONLBL], nodeCon[CONPROP], nodeCon[CONPROPLIST], )
                    self.addConstraint(self.gridConstraints.model(), nodeCon[CONTYPE], nodeCon[CONLBL], nodeCon[CONPROPLIST], )            
            except:
                pass
            # load indexes
            try:
                #AUTOINDEX, IDXLBL, IDXPROPLIST
                for nodeIdx in self.objectDict["indexes"]:
                    self.addIndex(self.gridIndex.model(), nodeIdx[AUTOINDEX], nodeIdx[IDXLBL], nodeIdx[IDXPROPLIST] )
            except:
                pass            
        
        else:
            self.rbTemplateDefaultFormat.setChecked(True)
            self.btnDefineTemplateFormat.setEnabled(False)
            self.rbInstanceDefaultFormat.setChecked(True)
            self.btnDefineInstanceFormat.setEnabled(False)
            self.instanceNodeFormatDict = None
            self.templateNodeFormatDict = None

    def templatePropertyList(self, ):
        propList = []
        model = self.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            propList.append(model.item(row,PROPERTY).data(Qt.EditRole))
        return propList

        
    @pyqtSlot()
    def on_btnLabelUp_clicked(self):
        """
        User clicks on label up button
        """
        self.helper.moveTableViewRowUp(self.gridLabels)
    
    @pyqtSlot()
    def on_btnLabelDown_clicked(self):
        """
        User clicks on label down button
        """
        self.helper.moveTableViewRowDown(self.gridLabels)
    
    @pyqtSlot()
    def on_btnLabelAdd_clicked(self):
        """
        User clicks button to add a new Label
        """
        self.gridLabels.setSortingEnabled(False)    
        self.addLabel(self.gridLabels.model(), "", "N", "N")
        self.helper.adjustGrid(grid=self.gridLabels)
        
#        self.gridLabels.setCurrentIndex(self.gridLabels.model().createIndex(self.gridLabels.model().rowCount(), 0))
#        self.gridLabels.setFocus(Qt.MouseFocusReason)
#        self.gridLabels.resizeColumnsToContents()
#        self.gridLabels.scrollToBottom()   
#        self.gridLabels.repaint()
    
    @pyqtSlot()
    def on_btnLabelRemove_clicked(self):
        """
        User clicks on the remove button in the label grid.
        """
        indexes = self.gridLabels.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            for index in sorted(indexes):
                self.gridLabels.model().removeRows(index.row(),1)
        else:
            self.helper.displayErrMsg("Remove Label", "You must select a row to remove")
    
    @pyqtSlot()
    def on_btnPropUp_clicked(self):
        """
        User clicks on property up button
        """
        self.helper.moveTableViewRowUp(self.gridProps)
    
    @pyqtSlot()
    def on_btnPropDown_clicked(self):
        """
        User clicks on property down button
        """
        self.helper.moveTableViewRowDown(self.gridProps)
    
    @pyqtSlot()
    def on_btnPropAdd_clicked(self):
        """
        User clicks button to add a new property to the property grid
        """
        self.gridProps.setSortingEnabled(False)    
        self.addProp(self.gridProps.model(), "", "Unknown", "N", "Null",  "N",  "N", "N") 
        self.helper.adjustGrid(grid=self.gridProps)
        
    @pyqtSlot()
    def on_btnPropRemove_clicked(self):
        """
        User clicks button to remove a row from the property grid
        """
        indexes = self.gridProps.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            for index in sorted(indexes):
                self.gridProps.model().removeRows(index.row(),1)
        else:
            self.helper.displayErrMsg("Remove Property", "You must select a row to remove")
        
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # force selection change on the datagrid to catch any unprocessed updates
        self.nodeGrid.forceSelectionChange()
        
        if self.validate():
            self.apply()
            QDialog.accept(self)
        
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        User Selects Cancel.
        """
        # force selection change on the datagrid to catch any unprocessed updates
        self.nodeGrid.forceSelectionChange()

        QDialog.reject(self)
        
    def addLabel(self,model,label,required, nodekey):
        # LABEL, REQUIRED, NODEKEY
        
#        model.beginInsertRows(model.createIndex(model.rowCount(), 0), model.rowCount(), model.rowCount())
        
        item1 = QStandardItem(label)
        item1.setEditable(True)
        item2 = QStandardItem()
        item2.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item2.setText("Required")
        if required in [0, 1, 2]:
            item2.setCheckState(required)  
        else:
            item2.setCheckState(Qt.Unchecked)  
        
        item3 = QStandardItem()
        item3.setFlags(Qt.ItemIsEnabled)
        item3.setText("Node Key")
        if nodekey in [0, 1, 2]:
            item3.setCheckState(nodekey)
            # if nodekey is checked then force required to be checked and disable it.
            if item3.checkState() == Qt.Checked:
                item2.setCheckState(Qt.Checked)
                item2.setEnabled(False)
        else:
            item3.setCheckState(Qt.Unchecked)  
            
        model.appendRow([item1,item2,item3])
        
#        model.insertRow(0, [item1,item2,item3])
    
        
#        model.endInsertRows()
#        model.layoutChanged.emit()
    
    def addProp(self,model,prop,datatype, propreq, propdef, exists, unique, propnodekey):
        #PROPERTY, EXISTS, UNIQUE, PROPNODEKEY
        item1 = QStandardItem(prop)
        item1.setEditable(True)
        item11 = QStandardItem(datatype)
        if self.designModel.objectExists(topLevel="Property",objectName=prop ) == True:
            item11.setEditable(False)
        else:
            item11.setEditable(True)
        item12 = QStandardItem(propreq)
        item12.setEditable(True)
        item12.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item12.setText("Required")        
        item13 = QStandardItem(propdef)
        # store the datatype in role + 1                
        item13.setData(datatype, Qt.UserRole+1)
        item13.setEditable(True)        
        item2 = QStandardItem()
        item2.setFlags(Qt.ItemIsEnabled)
        item2.setText("Exists")
        item3 = QStandardItem()
        item3.setFlags(Qt.ItemIsEnabled)
        item3.setText("Unique")
        item4 = QStandardItem()
        item4.setFlags(Qt.ItemIsEnabled)
        item4.setText("Node Key") 
        
        if propreq in [0, 1, 2]:
            item12.setCheckState(propreq)  
        else:
            item12.setCheckState(Qt.Unchecked)  
            
        if exists in [0, 1, 2]:
            item2.setCheckState(exists)  
        else:
            item2.setCheckState(Qt.Unchecked)  
        
        if unique in [0, 1, 2]:
            item3.setCheckState(unique) 
        else:
            item3.setCheckState(Qt.Unchecked) 
        
        if propnodekey in [0, 1, 2]:
            item4.setCheckState(propnodekey) 
            if item4.checkState() == Qt.Checked:
                item2.setCheckState(Qt.Checked)
                item2.setEnabled(False)
                item3.setCheckState(Qt.Checked)
                item3.setEnabled(False)                
        else:
            item4.setCheckState(Qt.Unchecked)             
        
        model.appendRow([item1,item11, item12,item13, item2, item3, item4])  
        
        
    def addConstraint(self,model, conType,lbl,  propList):
        # CONTYPE, CONLBL, CONPROP, CONPROPLIST
        item1 = QStandardItem(conType)
        item1.setEditable(True)
        item2 = QStandardItem(lbl)
        item2.setEditable(True)
#        item3 = QStandardItem(prop)
#        item3.setEditable(True)
        item4 = QStandardItem(propList)
        item4.setEditable(True)
#        model.appendRow([item1,item2,item3, item4])    
        model.appendRow([item1,item2, item4])

    def addIndex(self, model, autoIndex, idxLbl, idxPropList):
        # INDEX GRID - AUTOINDEX, IDXLBL, IDXPROPLIST        
        item1 = QStandardItem(autoIndex)
        item1.setEditable(True)
        item2 = QStandardItem(idxLbl)
        item2.setEditable(True)
        item3 = QStandardItem(idxPropList)
        item3.setEditable(True)
        model.appendRow([item1,item2,item3])
        
    def validate(self):
        # DEFINITION, CONSTRAINT, DESCRIPTION, DATAGRID
        if self.objectDict is None:
            self.objectDict = {}
        name = self.editName.text()
        if self.helper.NoTextValueError(name, "Must enter a Node Template Name"):
            self.tabNodeTemplate.setCurrentIndex(DEFINITION)
            self.editName.setFocus()
            return False
        if self.mode == 'NEW':
            if self.helper.DupObjectError(designModel = self.designModel, objName=name, topLevel = "Node Template", txtMsg = "A Node Template named {} already exists".format(name)):
                self.tabNodeTemplate.setCurrentIndex(DEFINITION)
                self.editName.setFocus()
                return False
                
        # label edits
        if self.helper.gridNoEntryError(grid=self.gridLabels, txtMsg="Warning - A node template with no Labels represents all Nodes in the graph."):
#            self.gridLabels.setFocus()
            # this is just a warning
            pass
        if self.helper.gridAtLeastOneRequired(grid=self.gridLabels, col=REQUIRED, txtMsg="You must supply at least one required Label"):
            self.gridLabels.setFocus()
            return False
            
        if self.helper.gridNoNameError(grid=self.gridLabels, col=LABEL, txtMsg="You must supply a name for each Label"):
            self.tabNodeTemplate.setCurrentIndex(DEFINITION)
            self.gridLabels.setFocus()
            return False
        if self.helper.gridDupEntryError(self.gridLabels, col=LABEL, txtMsg="has been entered more than once. You can only use a Label once"):
            self.tabNodeTemplate.setCurrentIndex(DEFINITION)
            self.gridLabels.setFocus()
            return False
        
        # property edits
        if self.helper.gridNoNameError(grid=self.gridProps, col=PROPERTY, txtMsg="You must supply a name for each Property"):
            self.tabNodeTemplate.setCurrentIndex(DEFINITION)
            self.gridProps.setFocus()
            return False
        if self.helper.gridDupEntryError(self.gridProps, col=PROPERTY, txtMsg="has been entered more than once. You can only use a Property once"):
            self.tabNodeTemplate.setCurrentIndex(DEFINITION)
            self.gridProps.setFocus()
            return False
        # don't allow changes to data types.  they must be changed in the property definition
        model = self.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole),
                             model.item(row,DATATYPE).data(Qt.EditRole), 
                             model.item(row,PROPREQ).checkState(), 
                             model.item(row,PROPDEF).data(Qt.EditRole), 
                             model.item(row,EXISTS).checkState(),  
                             model.item(row,UNIQUE).checkState(),  
                             model.item(row,PROPNODEKEY).checkState()]
#            if nodeProp[PROPREQ] == Qt.Checked and nodeProp[PROPDEF] == "":
#                self.helper.displayErrMsg("Validate", "Required property {} must have a default value.".format(nodeProp[PROPERTY]))
#                self.gridProps.setFocus()
#                return False
            dataType = self.designModel.getPropertyDataType(nodeProp[PROPERTY])
            # if the property has a datatype defined then don't let them change it.
            if dataType != "Unknown":   
                if nodeProp[DATATYPE] != dataType:
                    self.helper.displayErrMsg("Validate", "Property {} is defined with datatype {}. You can't change it.".format(nodeProp[PROPERTY], dataType))
                    self.gridProps.setFocus()
                    return False
            
            
        # Constraint tab edits
        # Constraint grid edits # CONTYPE, CONLBL, CONPROPLIST 
        if self.helper.gridNoNameError(grid=self.gridConstraints, col=CONTYPE, txtMsg="You must select a constraint type"):
            self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
            self.gridConstraints.setFocus()
            return False
        if self.helper.gridNoNameError(grid=self.gridConstraints, col=CONLBL, txtMsg="You must select a Label"):
            self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
            self.gridConstraints.setFocus()
            return False            
        if self.helper.gridNoNameError(grid=self.gridConstraints, col=CONPROPLIST, txtMsg="You must enter a property list"):
            self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
            self.gridConstraints.setFocus()
            return False                                  

        model =self.gridConstraints.model()
        numrows = model.rowCount()
        for row in range(0, numrows):
            nodeCon = [model.item(row,CONTYPE).data(Qt.EditRole), model.item(row,CONLBL).data(Qt.EditRole), model.item(row,CONPROPLIST).data(Qt.EditRole)]
#            if self.helper.NoTextValueError(nodeCon[CONLBL], "Row {} - You must select a Label".format(row+1)):
#                self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
#                self.gridConstraints.setFocus()
#                return False
#            if nodeCon[CONTYPE] in ["Node Key","Property Exists", "Property Unique"]:
#                if self.helper.NoTextValueError(nodeCon[CONPROPLIST], "Row {} - You must enter a property list".format(row+1)):
#                    self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
#                    self.gridConstraints.setFocus()
#                    return False
            if not set(nodeCon[CONPROPLIST].split(", ")).issubset(set(self.templatePropertyList())):
                self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
                self.helper.displayErrMsg("Check Property List", "Row {} has a property that isn't in the node template".format(row+1))
                self.gridConstraints.setFocus()
                return False            
            if nodeCon[CONTYPE]  in ["Property Exists", "Property Unique"]:
                if self.helper.csvNumItemsError(value=nodeCon[CONPROPLIST], min=1, max=1, msg="Row {} - Enter at most 1 Property".format(row+1)):
                    self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
                    self.gridConstraints.setFocus()
                    return False
                    
        # Index grid edits # AUTOINDEX, IDXLBL, IDXPROPLIST 
        if self.helper.gridNoNameError(grid=self.gridIndex, col=AUTOINDEX, txtMsg="Auto Generate must be Yes or No"):
            self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
            self.gridIndex.setFocus()
            return False
        if self.helper.gridNoNameError(grid=self.gridIndex, col=IDXLBL, txtMsg="You must select a Label"):
            self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
            self.gridIndex.setFocus()
            return False                    
        if self.helper.gridNoNameError(grid=self.gridIndex, col=IDXPROPLIST, txtMsg="You must enter a property list"):
            self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
            self.gridIndex.setFocus()
            return False                                  
        # make sure the property list doesn't have a property that isn't defined in the template.
        model =self.gridIndex.model()
        numrows = model.rowCount()
        for row in range(0, numrows):
            propList = model.item(row,IDXPROPLIST).data(Qt.EditRole)
            if not set(propList.split(", ")).issubset(set(self.templatePropertyList())):
                self.tabNodeTemplate.setCurrentIndex(CONSTRAINT)
                self.helper.displayErrMsg("Check Property List", "Row {} has a property that isn't in the node template".format(row+1))
                self.gridIndex.setFocus()
                return False            

        # passed all edits
        return True

    def defaultObjectDict(self, ):
        objectDict = {}
        objectDict["TNformat"] = None
        objectDict["INformat"] = None 
        objectDict["name"] = ""
        objectDict["desc"] = ""
        objectDict["labels"] = []
        objectDict["properties"] = []
        objectDict["constraints"] = []
        objectDict["indexes"] = []
        return objectDict
        
    def apply(self, ):
        '''
            update the object dictionary for the node template based on what the user has entered.
            you should call validate first to make sure there aren't any errrors.
        '''
        # see if they defined a custom template format
        if self.rbTemplateCustomFormat.isChecked():
            self.objectDict["TNformat"] = self.templateNodeFormatDict
        else:
            self.objectDict["TNformat"] = None
        # see if they defined a custom instance format
        if self.rbInstanceCustomFormat.isChecked():
            self.objectDict["INformat"] = self.instanceNodeFormatDict
        else:
            self.objectDict["INformat"] = None 
            
        self.objectDict["name"] = self.editName.text()
        
        desc = self.editDescription.toPlainText()
        if desc is not None:
            self.objectDict["desc"] = desc
        #save the labels
        # LABEL, REQUIRED, NODEKEY
        self.objectDict["labels"] = []
        model = self.gridLabels.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            nodeLbl = [model.item(row,LABEL).data(Qt.EditRole), model.item(row,REQUIRED).checkState(), model.item(row,NODEKEY).checkState()]
            self.designModel.newLabel(nodeLbl[LABEL])   # check to see if this is a new Label and create a Label object in the dictionary
            self.objectDict["labels"].append(nodeLbl)
        #save the properties
        #PROPERTY, DATATYPE,PROPREQ,PROPDEF,EXISTS, UNIQUE, PROPNODEKEY
        self.objectDict["properties"] = []
        model = self.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole),
                             model.item(row,DATATYPE).data(Qt.EditRole), 
                             model.item(row,PROPREQ).checkState(), 
                             model.item(row,PROPDEF).data(Qt.EditRole), 
                             model.item(row,EXISTS).checkState(),  
                             model.item(row,UNIQUE).checkState(),  
                             model.item(row,PROPNODEKEY).checkState()]
            # check to see if this is a new Property and create a Property object in the dictionary
            self.designModel.newProperty(nodeProp[PROPERTY], nodeProp[DATATYPE])   
            self.objectDict["properties"].append(nodeProp)
            
        # save the constraints
        # CONTYPE, CONLBL, CONPROP, CONPROPLIST 
        self.objectDict["constraints"] = []
        model =self.gridConstraints.model()
        numrows = model.rowCount()
        for row in range(0, numrows):
            nodeCon = [model.item(row,CONTYPE).data(Qt.EditRole), model.item(row,CONLBL).data(Qt.EditRole), model.item(row,CONPROPLIST).data(Qt.EditRole)]
            self.objectDict["constraints"].append(nodeCon)

        # save the indexes
        # AUTOINDEX, IDXLBL, IDXPROPLIST 
        self.objectDict["indexes"] = []
        model =self.gridIndex.model()
        numrows = model.rowCount()
        for row in range(0, numrows):
            nodeIdx = [model.item(row,AUTOINDEX).data(Qt.EditRole), model.item(row,IDXLBL).data(Qt.EditRole), model.item(row,IDXPROPLIST).data(Qt.EditRole)]
            self.objectDict["indexes"].append(nodeIdx)   
        
#        print("objectDict {}".format(self.objectDict))
#        print("nodetemplate {}".format(self.nodeTemplateCypher.templateDict))
        
    def generateAutoIndexEntries(self):
        '''
        go thru constraints and create matching index entries for node key and property unique
        '''
        # clear all existing auto generate index entries
        model =self.gridIndex.model()
        numrows = model.rowCount()
        for row in range(numrows-1, -1, -1):
            if model.item(row,AUTOINDEX).data(Qt.EditRole) == "Yes":
                self.gridIndex.model().removeRows(row,1)
        # add auto index entries
        model = self.gridConstraints.model()
        numrows = model.rowCount()
        for row in range(0, numrows):
            nodeCon = [model.item(row,CONTYPE).data(Qt.EditRole), model.item(row,CONLBL).data(Qt.EditRole), model.item(row,CONPROPLIST).data(Qt.EditRole)]
            if nodeCon[CONTYPE] == "Node Key":
                if (len(nodeCon[CONLBL]) > 0 and len(nodeCon[CONPROPLIST]) > 0):
                    self.addIndex(self.gridIndex.model(), "Yes", nodeCon[CONLBL], nodeCon[CONPROPLIST] )
            if nodeCon[CONTYPE] == "Property Unique":
                if (len(nodeCon[CONLBL]) > 0 and len(nodeCon[CONPROPLIST]) > 0):
                    self.addIndex(self.gridIndex.model(), "Yes", nodeCon[CONLBL], nodeCon[CONPROPLIST] )


        
    def syncDefCheckBoxes(self):    
        # clear all checkboxes on the definition tab
        # LABEL, REQUIRED, NODEKEY 
        # PROPERTY, EXISTS, UNIQUE, PROPNODEKEY 
        self.clearCheckBoxes()
        # loop through the constraints grid
        model=self.gridConstraints.model()
        numrows = model.rowCount()
        for row in range(0, numrows):
            nodeCon = [model.item(row,CONTYPE).data(Qt.EditRole), model.item(row,CONLBL).data(Qt.EditRole), model.item(row,CONPROPLIST).data(Qt.EditRole)]
            # process Nodekey
            if nodeCon[CONTYPE] == "Node Key":
                self.setLblCheckBox(lbl=nodeCon[CONLBL], chkBox=NODEKEY)
                self.setPropCheckBox(propList=nodeCon[CONPROPLIST], chkBox=PROPNODEKEY )
                self.setPropCheckBox(propList=nodeCon[CONPROPLIST], chkBox=PROPREQ )
            # process Property Exists
            if nodeCon[CONTYPE] == "Property Exists":
                self.setLblCheckBox(lbl=nodeCon[CONLBL], chkBox=REQUIRED)
                self.setPropCheckBox(propList=nodeCon[CONPROPLIST], chkBox=EXISTS )
                self.setPropCheckBox(propList=nodeCon[CONPROPLIST], chkBox=PROPREQ )
            # process Property Unique
            if nodeCon[CONTYPE] == "Property Unique":
                self.setLblCheckBox(lbl=nodeCon[CONLBL], chkBox=REQUIRED)
                self.setPropCheckBox(propList=nodeCon[CONPROPLIST], chkBox=UNIQUE )
                
        # enable/disable the PROPREQ checkbox depending on the EXISTS and NODEKEY checkboxes
        model = self.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole),
                             model.item(row,DATATYPE).data(Qt.EditRole), 
                             model.item(row,PROPREQ).checkState(), 
                             model.item(row,PROPDEF).data(Qt.EditRole), 
                             model.item(row,EXISTS).checkState(),  
                             model.item(row,UNIQUE).checkState(),  
                             model.item(row,PROPNODEKEY).checkState()]
            if nodeProp[PROPNODEKEY] == Qt.Checked or nodeProp[EXISTS] == Qt.Checked:
                model.item(row,PROPREQ).setFlags(Qt.ItemIsEnabled)
            else:
                model.item(row,PROPREQ).setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                
    def setLblCheckBox(self, lbl=None, chkBox=None):
        try:
            model = self.gridLabels.model()
            numrows = model.rowCount()
            for row in range(0,numrows):
                if lbl == model.item(row,LABEL).data(Qt.EditRole):
                    model.item(row,chkBox).setCheckState(Qt.Checked)             
        except:
            pass

    def setPropCheckBox(self, prop=None, propList=None, chkBox=None):
        try:
            model = self.gridProps.model()
            numrows = model.rowCount()
            if not prop is None:
                for row in range(0,numrows):
                    if prop == model.item(row,PROPERTY).data(Qt.EditRole):
                        model.item(row,chkBox).setCheckState(Qt.Checked)
            else:
                if not propList is None:
                    props = propList.split(",")
                    for prop in props:
                        for row in range(0,numrows):
                            if prop.strip() == model.item(row,PROPERTY).data(Qt.EditRole):
                                model.item(row,chkBox).setCheckState(Qt.Checked)       

        except:
            pass

            
    def clearCheckBoxes(self):
        model = self.gridLabels.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            model.item(row,NODEKEY).setCheckState(0) 
#        EXISTS, UNIQUE, PROPNODEKEY    
        model = self.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            model.item(row,EXISTS).setCheckState(0) 
            model.item(row,UNIQUE).setCheckState(0) 
            model.item(row,PROPNODEKEY).setCheckState(0) 


    
    @pyqtSlot(int)
    def on_tabNodeTemplate_currentChanged(self, index):
        """
        The user has switched to a different tab
        DEFINITION, CONSTRAINT, DESCRIPTION, DATAGRID
        @param index DESCRIPTION
        @type int
        """
        # user switched to the description tab.  regenerate the description
        if index == DESCRIPTION:
            if self.validate():
                self.apply()
                # get generated description
                self.brwsrGenDescription.setText(self.designModel.getNodeDescription(self.objectDict["name"]))

        # user switched to the definition tab.  must resync checkboxes with the current values on the constraints tab
        if index == DEFINITION:
            self.syncDefCheckBoxes()
        # user switched to the data grid then update object dictionary so query will generate with latest values
        if index == DATAGRID:
            if self.validate():
                self.apply()
                self.nodeGrid.refreshGrid()
            else:
                self.tabNodeTemplate.setCurrentIndex(0)
        # user switched to the constraint tab so update the combo boxes to get latest values from def
        if index == CONSTRAINT:
            self.updateComboBoxes()
            self.generateAutoIndexEntries()
            
    def propModelItemChanged(self, item):
        
#        print("item data changed {} at {} {}".format(str(item.checkState()), item.index().row(), item.index().column()))

        columnIndex = item.index().column()
        if columnIndex == PROPERTY:
            # if property has changed then change the datatype
            propName = self.gridProps.model().item(item.index().row(),PROPERTY).data(Qt.EditRole)
            # get the defined datatype for the property
            dataType = self.designModel.getPropertyDataType(propName)
            self.gridProps.model().item(item.index().row(), DATATYPE).setText(dataType)
            # store the datatype in role + 1 for the default value
            self.gridProps.model().item(item.index().row(), PROPDEF).setData(dataType, Qt.UserRole+1)
            # set default value to a null string
            self.gridProps.model().item(item.index().row(), PROPDEF).setText("")
            # if the property doesn't exist yet then allow the datatype to be changed
            if self.designModel.objectExists(topLevel="Property",objectName=propName ) == False:
                self.gridProps.model().item(item.index().row(), DATATYPE).setEditable(True)
            else:
                self.gridProps.model().item(item.index().row(), DATATYPE).setEditable(False)
                
        if columnIndex == DATATYPE:
            # datatype changed so reset default value and store new datatype   
            dataType = self.gridProps.model().item(item.index().row(),DATATYPE).data(Qt.EditRole)
            # store the datatype in role + 1    
            self.gridProps.model().item(item.index().row(), PROPDEF).setData(dataType, Qt.UserRole+1)
            self.gridProps.model().item(item.index().row(), PROPDEF).setText("")

        if columnIndex == PROPNODEKEY:
            # force selection of this cell
            self.gridProps.setCurrentIndex(item.index())
            if item.checkState() == Qt.Checked:
#                self.gridProps.model().item(item.index().row(), UNIQUE).setCheckState(Qt.Checked)
                self.gridProps.model().item(item.index().row(), EXISTS).setCheckState(Qt.Checked)
#                self.gridProps.model().item(item.index().row(), UNIQUE).setEnabled(False)
#                self.gridProps.model().item(item.index().row(), EXISTS).setEnabled(False)
#                self.gridProps.model().item(item.index().row(), UNIQUE).setEditable(False)
                self.gridProps.model().item(item.index().row(), EXISTS).setEditable(False)                
            else:
                self.gridProps.model().item(item.index().row(), UNIQUE).setCheckState(Qt.Unchecked)
                self.gridProps.model().item(item.index().row(), EXISTS).setCheckState(Qt.Unchecked)
                self.gridProps.model().item(item.index().row(), UNIQUE).setEnabled(True)
                self.gridProps.model().item(item.index().row(), EXISTS).setEnabled(True)
                self.gridProps.model().item(item.index().row(), UNIQUE).setEditable(True)
                self.gridProps.model().item(item.index().row(), EXISTS).setEditable(True)
                
    def lblModelItemChanged(self, item):

        # this fires when checkbox is selected or deselected. 
        columnIndex = item.index().column()
        if columnIndex == NODEKEY:
            # force selection of this cell
            self.gridLabels.setCurrentIndex(item.index())
            # if the label is used on a nodekey, then also check the required checkbox and disable it
            if item.checkState() == Qt.Checked:
                self.gridLabels.model().item(item.index().row(), REQUIRED).setCheckState(Qt.Checked)
                self.gridLabels.model().item(item.index().row(), REQUIRED).setEnabled(False)
            else:
                # if the nodekey checkbox is unchecked, then enable the required checkbox but don't uncheck it, the user can do that manually.
                self.gridLabels.model().item(item.index().row(), REQUIRED).setEnabled(True)

    def constraintModelItemChanged(self, item):
#        column = item.index().column()
#        row = item.index().row()
#        print("item changed {}-{}".format(row, column))
        # must regenerate all auto indexes if anything changed
        self.generateAutoIndexEntries()
        self.syncDefCheckBoxes()

        
    @pyqtSlot()
    def on_btnAddConstraint_clicked(self):
        """
        Slot documentation goes here.
        """
        self.gridConstraints.setSortingEnabled(False)    
        self.addConstraint(self.gridConstraints.model(), "", "", "")
        self.helper.adjustGrid(grid=self.gridConstraints)

        
    @pyqtSlot()
    def on_btnRemoveConstraint_clicked(self):
        """
        User clicked the remove row button
        """
        indexes = self.gridConstraints.selectionModel().selectedIndexes()
        for index in sorted(indexes):
#            print('Row %d is selected' % index.row())
            self.gridConstraints.model().removeRows(index.row(),1)
            self.generateAutoIndexEntries()
            self.syncDefCheckBoxes()
    
    @pyqtSlot()
    def on_btnAddIndex_clicked(self):
        """
        Slot documentation goes here.
        """
        self.gridIndex.setSortingEnabled(False)    
        self.addIndex(self.gridIndex.model(), "No", "", "")
        self.helper.adjustGrid(grid=self.gridIndex)
        
    @pyqtSlot()
    def on_btnRemoveIndex_clicked(self):
        """
        User clicked the remove row button
        """
        indexes = self.gridIndex.selectionModel().selectedIndexes()
        for index in sorted(indexes):
#            print('Row %d is selected' % index.row())
            # not sure why this if is needed, doesn't seem needed in other remove row buttons
            if not self.gridIndex.model().item(index.row(), AUTOINDEX) is None:
                if self.gridIndex.model().item(index.row(), AUTOINDEX).data(Qt.EditRole) == "Yes":
                    self.helper.displayErrMsg("Remove Row", "Can't remove Auto Generate Yes index")
                else:
                    self.gridIndex.model().removeRows(index.row(),1)
    
    @pyqtSlot()
    def on_btnDefineTemplateFormat_clicked(self):
        """
        Display the Node Template Format Editor
        """
        myTemplateNodeFormatDict = self.templateNodeFormatDict
        # if the template doesn't have a specific instance node format then get the project default
        if myTemplateNodeFormatDict is None:
            # create a copy of the project default
            myTemplateNodeFormatDict = deepcopy(self.modelData["TNformat"])

        d = TNodeFormatDlg(self, modelData = None, nodeFormat = TNodeFormat(formatDict=myTemplateNodeFormatDict))
        if d.exec_():
#            self.templateNodeFormatDict = TNodeFormat(formatDict=d.nodeFormat.formatDict).formatDict
            self.templateNodeFormatDict = d.nodeFormat.formatDict
            self.formatChanged = True
    
    @pyqtSlot()
    def on_btnDefineInstanceFormat_clicked(self):
        """
        Display the Instance Node Format Editor
        """
        myInstanceNodeFormatDict = self.instanceNodeFormatDict
        # if the template doesn't have a specific instance node format then get the project default
        if myInstanceNodeFormatDict is None:
            # create a copy of the project default
            myInstanceNodeFormatDict = deepcopy(self.modelData["INformat"])
        d = INodeFormatDlg(self, modelData = None, nodeFormat = INodeFormat(formatDict=myInstanceNodeFormatDict))
        if d.exec_():
#            self.instanceNodeFormatDict = INodeFormat(formatDict=d.nodeFormat.formatDict).formatDict
            self.instanceNodeFormatDict = d.nodeFormat.formatDict
            self.formatChanged = True
    
    @pyqtSlot()
    def on_rbTemplateDefaultFormat_clicked(self):
        """
        If default radio button selected, then disable the define format button
        """
        self.btnDefineTemplateFormat.setEnabled(False)
    
    @pyqtSlot()
    def on_rbTemplateCustomFormat_clicked(self):
        """
        If custom radio button selected, then enable the define format button
        """
        self.btnDefineTemplateFormat.setEnabled(True)

    
    @pyqtSlot()
    def on_rbInstanceDefaultFormat_clicked(self):
        """
        If default radio button selected, then disable the define format button
        """
        self.btnDefineInstanceFormat.setEnabled(False)
   
    @pyqtSlot()
    def on_rbInstanceCustomFormat_clicked(self):
        """
        If custom radio button selected, then enable the define format button
        """
        self.btnDefineInstanceFormat.setEnabled(True)
    
    def indexGridSelectionChanged(self, selected, deselected):
        # see if a property list cell was deselected
        if len(deselected.indexes()) > 0:
            self.prevIndex = deselected.indexes()[0]
            columnIndex = self.prevIndex.column()
            if columnIndex == CONPROPLIST:
                self.gridIndex.setRowHeight(self.prevIndex.row(), 30)    
                
    def constraintGridSelectionChanged(self, selected, deselected):
        # see if a property list cell was deselected
        if len(deselected.indexes()) > 0:
            self.prevIndex = deselected.indexes()[0]
            columnIndex = self.prevIndex.column()
            if columnIndex == CONPROPLIST:
                self.gridConstraints.setRowHeight(self.prevIndex.row(), 30)

                
#            print ("deselected: row - {}, col - {}, data - {}".format(self.prevIndex.row(), self.prevIndex.column(), self.prevIndex.data(role = Qt.DisplayRole)))
    
    @pyqtSlot()
    def on_btnSetDefaultNull_clicked(self):
        """
        User requests to set a property default to Null
        """
        # grid only allows single selection
        indexes = self.gridProps.selectionModel().selectedIndexes()
        for index in indexes:
            valueIndex = self.gridProps.model().index(index.row(), PROPDEF)
            self.gridProps.model().setData(valueIndex, "Null", Qt.DisplayRole)
        
