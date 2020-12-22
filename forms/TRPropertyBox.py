# -*- coding: utf-8 -*-

"""
Module implementing the Relationship Template Editor.  The editor is invoked from the project treeview or from a relationship template shown
on a template diagram.
    Author: John Singer
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
from copy import deepcopy
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QHeaderView, QVBoxLayout, QAbstractItemView

from PyQt5.QtGui import QStandardItemModel,  QStandardItem

from forms.Ui_TRPropertyBox import Ui_TRPropertyBox
from forms.IRelFormatDlg import IRelFormatDlg, IRelFormat
from forms.TRelFormatDlg import TRelFormatDlg, TRelFormat
from forms.DataGridWidget import DataGridWidget

from core.Enums import DataType
from core.helper import Helper, CBDelegate
from core.RelTemplateCypher import RelTemplateCypher
from core.NeoDriver import NeoDriver
from core.NeoEditDelegate import NeoEditDelegate

DEFINITION, CONSTRAINT, DESCRIPTION, FORMAT, DATAGRID = range(5)
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS = range(5)
CONTYPE,  CONPROP = range(2)

class TRPropertyBox(QDialog, Ui_TRPropertyBox):
    """
    This displays and manages the Relationship Template Dialog box
    """
    def __init__(self, parent=None, mode=None, objectDict=None, designModel = None):
        """
        objectDict - Relationship Template object dictionary. For creating a new Relationship Template this will be None
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(TRPropertyBox, self).__init__(parent)
        self.parent = parent
        self.schemaModel = self.parent.schemaObject 
        self.settings = QSettings()
        self.formatChanged = False
        self.helper = Helper()
        self.setupUi(self)
        self.designModel = designModel
        self.modelData = self.designModel.modelData
        if objectDict is None:
            self.objectDict = self.designModel.newRelTemplateDict()
        else:
            self.objectDict = objectDict
        self.mode = mode
        
        # get the class that controls the data grid for relationship templates
        self.RelTemplateCypher = RelTemplateCypher(templateDict=self.objectDict)
        
        # get neocon object for this project page
        self.neoCon = NeoDriver(name=self.parent.pageItem.neoConName, promptPW=self.parent.pageItem.promptPW)
        
        # Properties Grid
        self.gridProps.setModel(self.createPropModel())
        comboPropList = [""] 
        comboPropList.extend(sorted(set(self.designModel.instanceList("Property") + self.schemaModel.instanceList("Property"))))
        
        dataTypeList = [dataType.value for dataType in DataType]
        self.gridProps.setItemDelegateForColumn(DATATYPE, CBDelegate(self, dataTypeList, setEditable=False ))

        self.gridProps.setItemDelegateForColumn(PROPERTY, CBDelegate(self, comboPropList, setEditable=True ))
        self.gridProps.setItemDelegateForColumn(PROPDEF, NeoEditDelegate(self))
        self.gridProps.setColumnWidth(PROPERTY, 350)
        self.gridProps.setColumnWidth(DATATYPE, 125)       
        self.gridProps.setColumnWidth(PROPREQ, 100)
        self.gridProps.setColumnWidth(PROPDEF, 150)
        self.gridProps.setColumnWidth(EXISTS, 100)
        self.gridProps.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridProps.setSelectionMode(QAbstractItemView.SingleSelection)

        header = self.gridProps.horizontalHeader()
        header.setSectionResizeMode(PROPERTY, QHeaderView.Interactive)  
        header.setSectionResizeMode(DATATYPE, QHeaderView.Fixed)  
        header.setSectionResizeMode(PROPREQ, QHeaderView.Fixed) 
        header.setSectionResizeMode(PROPDEF, QHeaderView.Interactive)  
        header.setSectionResizeMode(EXISTS, QHeaderView.Fixed)

        # constraints grid
        self.gridConstraints.setModel(self.createConstraintsModel())
        conTypeList = ["Property Exists"]
        self.gridConstraints.setItemDelegateForColumn(CONTYPE, CBDelegate(self, conTypeList, setEditable=False ))      
        self.gridConstraints.setColumnWidth(CONTYPE, 120)
        self.gridConstraints.setColumnWidth(CONPROP, 350)
        header = self.gridConstraints.horizontalHeader()
         
        header.setSectionResizeMode(CONTYPE, QHeaderView.Fixed) 
        header.setSectionResizeMode(CONPROP, QHeaderView.Interactive)
        
        # populate the rel template dropdowns
        self.loadTemplateDropdowns()
        
        # add the data grid widget.  
        self.relGrid = DataGridWidget(self, neoCon=self.neoCon, genCypher=self.RelTemplateCypher)
        self.relGridLayout = QVBoxLayout(self.dataTabFrame)
        self.relGridLayout.setObjectName("relGridLayout")
        self.relGridLayout.addWidget(self.relGrid)    
        
        #populate ui data from object
        self.populateUIfromObject()
        # populate combo boxes used on constraint and index grids
        self.updateComboBoxes()
        # sync definition checkboxes with constraints
        self.syncDefCheckBoxes()     
        
        if self.mode == "NEW":
            self.txtRelTemplateName.setFocus()               
        else: 
            # disable definition fields
            self.txtRelTemplateName.setEnabled(False)
            self.cboRelName.setEnabled(False)
            # disable from and to nodes if they have been defined
            if self.cmbFromTemplate.currentIndex() > 0:
                self.cmbFromTemplate.setEnabled(False)
            if self.cmbToTemplate.currentIndex() > 0:
                self.cmbToTemplate.setEnabled(False)


    def updateComboBoxes(self):
        propList = [""] + [ self.gridProps.model().item(row,PROPERTY).data(Qt.EditRole) for row in range(0,self.gridProps.model().rowCount())]
        self.gridConstraints.setItemDelegateForColumn(CONPROP, CBDelegate(self, propList, setEditable=True ))        
        
    def loadTemplateDropdowns(self, ):
        # load source node template dropdown
        dropdownList = []
        dropdownList.append("No Template Selected")
        nodeList = dropdownList + self.designModel.instanceList("Node Template")
        self.cmbFromTemplate.addItems(nodeList)
        self.cmbToTemplate.addItems(nodeList)
        
    def createPropModel(self):
        model = QStandardItemModel(0, 5)
        model.setHeaderData(PROPERTY, Qt.Horizontal, "Property")
        model.setHeaderData(DATATYPE, Qt.Horizontal, "Data Type")
        model.setHeaderData(PROPREQ, Qt.Horizontal, "Required")
        model.setHeaderData(PROPDEF, Qt.Horizontal, "Default Value")
        model.setHeaderData(EXISTS, Qt.Horizontal, "Exists")
        # connect model slots 
        model.itemChanged.connect(self.propModelItemChanged)        
        return model   
            
    def createConstraintsModel(self):
        # CONSTRAINT GRID - CONTYPE, CONPROP,
        model = QStandardItemModel(0,2)
        model.setHeaderData(CONTYPE, Qt.Horizontal, "Constraint Type")
        model.setHeaderData(CONPROP, Qt.Horizontal, "Property")
        # connect model slots 
        model.itemChanged.connect(self.constraintModelItemChanged)
        return model
        
    def populateUIfromObject(self, ):
        # default the combo boxes to nothing selected
        self.cmbFromTemplate.setCurrentIndex(0) 
        self.cmbToTemplate.setCurrentIndex(0)              
        
        # get the custom template format if any
        self.TRFormatDict = self.objectDict.get("TRformat", None)
        if self.TRFormatDict == None:
            self.rbTemplateDefaultFormat.setChecked(True)
            self.btnDefineTemplateFormat.setEnabled(False)
        else:
            self.rbTemplateCustomFormat.setChecked(True)
            self.btnDefineTemplateFormat.setEnabled(True)   
            
        # get the custom instance format if any
        self.IRFormatDict = self.objectDict.get("IRformat", None)
        if self.IRFormatDict == None:
            self.rbInstanceDefaultFormat.setChecked(True)
            self.btnDefineInstanceFormat.setEnabled(False)
        else:
            self.rbInstanceCustomFormat.setChecked(True)
            self.btnDefineInstanceFormat.setEnabled(True)               
        
        # name, relname, desc
        self.txtRelTemplateName.insert(str(self.objectDict["name"]))
        self.loadRelationshipNameDropDown()
        self.editDescription.appendPlainText(self.objectDict["desc"])
        
        # from and to node templates
        index = self.cmbFromTemplate.findText(self.objectDict["fromTemplate"])
        if index >= 0:
            self.cmbFromTemplate.setCurrentIndex(index)       
        index = self.cmbToTemplate.findText(self.objectDict["toTemplate"])
        if index >= 0:
            self.cmbToTemplate.setCurrentIndex(index) 
            
        # from and to cardinalities
        index = self.cmbFromCardinality.findText(self.objectDict["fromCardinality"])
        if index >= 0:
            self.cmbFromCardinality.setCurrentIndex(index)       
        index = self.cmbToCardinality.findText(self.objectDict["toCardinality"])
        if index >= 0:
            self.cmbToCardinality.setCurrentIndex(index)     
            
        # cardinality description
        self.editToFromType.setText("Node Type {}".format(self.cmbFromTemplate.currentText()))
        self.editFromToType.setText("Node Type {}".format(self.cmbToTemplate.currentText()))
        
        #properties
        for relProp in self.objectDict["properties"]:
            dataType = self.designModel.getPropertyDataType(relProp[PROPERTY])
            self.addProp(self.gridProps.model(), relProp[PROPERTY], dataType, relProp[PROPREQ], relProp[PROPDEF], relProp[EXISTS])
        # load constraints
        try:
            #CONTYPE, CONLBL, CONPROP, CONPROPLIST
            for nodeCon in self.objectDict["constraints"]:
                self.addConstraint(self.gridConstraints.model(), nodeCon[CONTYPE], nodeCon[CONPROP])
        except:
            pass

    def loadRelationshipNameDropDown(self, ):
        # load relationship name  dropdown
        dropdownList = []
        dropdownList.append("")  # blank option for user to enter a new rel type
        # get relationship types from the project model
        templateRelList = [relDict["relname"] for relDict in self.modelData["Relationship Template"] ]    
        # get relationship types from the schemamodel - this needs to be fixed, need common access to schemamodel from project page and instance diagram
        schemaRelList =  [rel["name"] for rel in self.schemaModel.schemaData["Relationship"] ]
#        schemaRelList = []
        # merge, dedup, and sort the two lists and put them in the dropdown
        dropdownList.extend(sorted(set(templateRelList + schemaRelList)))
        self.cboRelName.addItems(dropdownList)      
        # if no relationship name has been set then display enabled combo box  
        if str(self.objectDict["relname"]) is None: 
            self.cboRelName.setCurrentIndex(0)
        elif (str(self.objectDict["relname"]) == "NoRelationshipName" or len(self.objectDict["relname"]) < 1):
            self.cboRelName.setCurrentIndex(0)
        else:
            # if the relationship name has been set then display the rel name
            index = self.cboRelName.findText(str(self.objectDict["relname"]))
            if index >= 0:
                self.cboRelName.setCurrentIndex(index)
            else:
                # its not an existing name so just set the text in the combo box
                self.cboRelName.setEditText(str(self.objectDict["relname"]))
                
    #
    # PROPERTY GRID BUTTONS
    #
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
        Slot documentation goes here.
        """
        self.gridProps.setSortingEnabled(False)    
        self.addProp(self.gridProps.model(), "","Unknown","N","Null","N")
        # generic function to adjust grid after adding a row
        self.helper.adjustGrid(grid=self.gridProps)
#        # scroll to bottom to insure the new row is visible
#        self.gridProps.scrollToBottom()      
        
    @pyqtSlot()
    def on_btnPropRemove_clicked(self):
        """
        Slot documentation goes here.
        """
#        indexes = self.gridProps.selectionModel().selectedIndexes()
#        for index in sorted(indexes):
#            print('Row %d is selected' % index.row())
#            self.gridProps.model().removeRows(index.row(),1)
            
        indexes = self.gridProps.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            for index in sorted(indexes):
                self.gridProps.model().removeRows(index.row(),1)
        else:
            self.helper.displayErrMsg("Remove Property", "You must select a row to remove")         
            
    def addProp(self,model,prop,dataType, propreq, propdef, exists):
        item1 = QStandardItem(prop)
        item1.setEditable(True)
        item11 = QStandardItem(dataType)
        item11.setEditable(False)
        item12 = QStandardItem(propreq)
        item12.setEditable(True)
        item12.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item12.setText("Required")        
        item13 = QStandardItem(propdef)
        # store the datatype in role + 1                
        item13.setData(dataType, Qt.UserRole+1)
        item13.setEditable(True)        
        item2 = QStandardItem()
        item2.setFlags(Qt.ItemIsEnabled)
        item2.setText("Exists")
        
        if exists in [0, 1, 2]:
            item2.setCheckState(exists)  
        else:
            item2.setCheckState(Qt.Unchecked)  
            
        if propreq in [0, 1, 2]:
            item12.setCheckState(propreq)  
        else:
            item12.setCheckState(Qt.Unchecked)    
            
        model.appendRow([item1, item11, item12,item13, item2])

    def handleItemClicked(self, item):
        return


    def addConstraint(self,model, conType, prop):
        # CONTYPE, CONPROP
        item1 = QStandardItem(conType)
        item1.setEditable(True)

        item3 = QStandardItem(prop)
        item3.setEditable(True)
            
        model.appendRow([item1, item3])
        
    def syncDefCheckBoxes(self):    
        # clear all checkboxes on the definition tab
        self.clearCheckBoxes()
        # loop through the constraints grid
        model=self.gridConstraints.model()
        numrows = model.rowCount()
        for row in range(0, numrows):
            relCon = [model.item(row,CONTYPE).data(Qt.EditRole), model.item(row,CONPROP).data(Qt.EditRole)]
            # process Property Exists
            if relCon[CONTYPE] == "Property Exists":
                self.setPropCheckBox(prop=relCon[CONPROP], chkBox=EXISTS )
                self.setPropCheckBox(prop=relCon[CONPROP], chkBox=PROPREQ )

    def setPropCheckBox(self, prop=None, chkBox=None):
        try:
            model = self.gridProps.model()
            numrows = model.rowCount()
            if not prop is None:
                for row in range(0,numrows):
                    if prop == model.item(row,PROPERTY).data(Qt.EditRole):
                        model.item(row,chkBox).setCheckState(Qt.Checked)        
        except:
            pass       
            
    def clearCheckBoxes(self):

        model = self.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            model.item(row,EXISTS).setCheckState(0) 

            
#################################################################################        
# DIALOG BUTTONS
#################################################################################    
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

    def validate(self):
        if self.objectDict is None:
            self.objectDict = {}
        templateName = self.txtRelTemplateName.text()
        # template name
        if self.helper.NoTextValueError(templateName, "Must enter a Relationship Template Name"):
            self.txtRelTemplateName.setFocus()
            return False
        # relationship name            
#        name = self.txtRelName.text() 
        name = self.cboRelName.currentText()    
        if self.helper.NoTextValueError(name, "Must enter a Relationship Name"):
#            self.txtRelName.setFocus()
            self.cboRelName.setFocus()
            return False
        # dup check
        if self.mode == 'NEW':
            if self.helper.DupObjectError(designModel = self.designModel, objName=templateName, topLevel = "Relationship Template", txtMsg = "A Relationship Template named {} already exists".format(name)):
                self.txtRelTemplateName.setFocus()
                return False
        # must have a From Node Template
        if self.helper.NoComboBoxSelectionError(self.cmbFromTemplate, "Must enter a From Node Template"):
            self.cmbFromTemplate.setFocus()
            return False                
        # must have a To Node Template
        if self.helper.NoComboBoxSelectionError(self.cmbToTemplate, "Must enter a To Node Template"):
            self.cmbToTemplate.setFocus()
            return False
        # property name must exist
        if self.helper.gridNoNameError(grid=self.gridProps, col=PROPERTY, txtMsg="You must supply a name for each Property"):
            self.gridProps.setFocus()
            return False
        # dup property
        if self.helper.gridDupEntryError(self.gridProps, col=PROPERTY, txtMsg="has been entered more than once. You can only use a Property once"):
            self.gridProps.setFocus()
            return False
#        # required property  must have a default value
#        model = self.gridProps.model()
#        numrows = model.rowCount()
#        for row in range(0,numrows):
#            nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole),
#                             model.item(row,DATATYPE).data(Qt.EditRole), 
#                             model.item(row,PROPREQ).checkState(), 
#                             model.item(row,PROPDEF).data(Qt.EditRole), 
#                             model.item(row,EXISTS).checkState()]
#            if nodeProp[PROPREQ] == Qt.Checked and nodeProp[PROPDEF] == "":
#                self.helper.displayErrMsg("Validate", "Required property {} must have a default value.".format(nodeProp[PROPERTY]))
#                self.gridProps.setFocus()
#                return False
        # constraint type exists
        if self.helper.gridNoNameError(grid=self.gridConstraints, col=CONTYPE, txtMsg="You must select a constraint type"):
            self.tabRelTemplate.setCurrentIndex(CONSTRAINT)
            self.gridConstraints.setFocus()
            return False        
        model =self.gridConstraints.model()
        numrows = model.rowCount()
        for row in range(0, numrows):
            nodeCon = [model.item(row,CONTYPE).data(Qt.EditRole), model.item(row,CONPROP).data(Qt.EditRole)]
            if nodeCon[CONTYPE]  in ["Property Exists", "Property Unique"]:
                if self.helper.NoTextValueError(nodeCon[CONPROP], "Row {} - You must select a property".format(row+1)):
                    self.tabRelTemplate.setCurrentIndex(CONSTRAINT)
                    self.gridConstraints.setFocus()
                    return False
        # passed all edits so return True
        return True
        
    def apply(self, ):
        
        self.objectDict["TRformat"] = self.TRFormatDict
        self.objectDict["IRformat"] = self.IRFormatDict
        self.objectDict["name"] = self.txtRelTemplateName.text()
#        self.objectDict["relname"] = self.txtRelName.text()
        self.objectDict["relname"] = self.cboRelName.currentText()
        # if its a new rel type then add it to the model
        self.designModel.newRelationship(self.objectDict["relname"])
        if self.cmbFromTemplate.currentIndex() > 0:
            self.objectDict["fromTemplate"] = self.cmbFromTemplate.currentText()
        else:
            self.objectDict["fromTemplate"] = ''
        if self.cmbToTemplate.currentIndex() > 0:    
            self.objectDict["toTemplate"]  = self.cmbToTemplate.currentText()
        else:
            self.objectDict["toTemplate"] = ''
        self.objectDict["fromCardinality"] = self.cmbFromCardinality.currentText()
        self.objectDict["toCardinality"] = self.cmbToCardinality.currentText()
        desc = self.editDescription.toPlainText()
        if desc is not None:
            self.objectDict["desc"] = desc
        #save the properties
        self.objectDict["properties"] = []
        model = self.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            relProp = [model.item(row,PROPERTY).data(Qt.EditRole),
                            model.item(row,DATATYPE).data(Qt.EditRole), 
                             model.item(row,PROPREQ).checkState(), 
                             model.item(row,PROPDEF).data(Qt.EditRole),                             
                            model.item(row,EXISTS).checkState()]
            self.designModel.newProperty(relProp[PROPERTY], relProp[DATATYPE])   # check to see if this is a new Property and create a Property object in the dictionary
            self.objectDict["properties"].append(relProp)
        # save the constraints
        # CONTYPE, CONPROP
        self.objectDict["constraints"] = []
        model =self.gridConstraints.model()
        numrows = model.rowCount()
        for row in range(0, numrows):
            relCon = [model.item(row,CONTYPE).data(Qt.EditRole), model.item(row,CONPROP).data(Qt.EditRole)]
            self.objectDict["constraints"].append(relCon)
    
    @pyqtSlot()
    def on_rbDefaultFormat_clicked(self):
        """
        Slot documentation goes here.
        """
        self.btnDefineFormat.setEnabled(False)
    
    @pyqtSlot()
    def on_rbCustomFormat_clicked(self):
        """
        Slot documentation goes here.
        """
        self.btnDefineFormat.setEnabled(True)
    
    @pyqtSlot()
    def on_btnDefineFormat_clicked(self):
        """
        Slot documentation goes here.
        """
        d = IRelFormatDlg(self, modelData = None, relFormat = IRelFormat(formatDict=self.TRFormatDict))
        if d.exec_():
            self.TRFormatDict = IRelFormat(formatDict=d.relFormat.formatDict).formatDict
            # tell diagrams to redraw
            self.formatChanged = True
            
    def constraintModelItemChanged(self, item):
        self.syncDefCheckBoxes()    
        
    @pyqtSlot()
    def on_btnAddConstraint_clicked(self):
        """
        Slot documentation goes here.
        """
        self.gridConstraints.setSortingEnabled(False)    
        self.addConstraint(self.gridConstraints.model(), "", "")
        # generic function to adjust grid after adding a row
        self.helper.adjustGrid(grid=self.gridConstraints)
#        # scroll to bottom to insure the new row is visible
#        self.gridConstraints.scrollToBottom()        
        
    @pyqtSlot()
    def on_btnRemoveConstraint_clicked(self):
        """
        User clicked the remove row button
        """
        indexes = self.gridConstraints.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            for index in sorted(indexes):
                self.gridConstraints.model().removeRows(index.row(),1)
            self.syncDefCheckBoxes()    
        else:
            self.helper.displayErrMsg("Remove Constraint", "You must select a row to remove")         
            
#        indexes = self.gridConstraints.selectionModel().selectedRows()
#        for index in sorted(indexes):
#            self.gridConstraints.model().removeRows(index.row(),1)
            
            
    def propModelItemChanged(self, item):
        
#        print("item data changed {} at {} {}".format(str(item.checkState()), item.index().row(), item.index().column()))

        # this fires when checkbox is selected or deselected. 
        columnIndex = item.index().column()
        propName = self.gridProps.model().item(item.index().row(),PROPERTY).data(Qt.EditRole)
        dataType = self.designModel.getPropertyDataType(propName)
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
            
    @pyqtSlot(int)
    def on_tabRelTemplate_currentChanged(self, index):
        """
        If the user has switched to the data tab then update the object dictionary
        
        @param index DESCRIPTION
        @type int
        """
        # user switched to the description tab.  must regenerate description
        if index == DESCRIPTION:
            self.apply()
            self.brwsrGeneratedDesc.setText(self.designModel.getRelationshipDescription(self.objectDict))

        # user switched to the definition tab.  must resync checkboxes with the current values on the constraints tab
        if index == DEFINITION:
            self.syncDefCheckBoxes()
        if index == DATAGRID:
            if self.validate():
                self.apply()
                self.relGrid.refreshGrid()
            else:
                self.tabRelTemplate.setCurrentIndex(0)
        # user switched to the constraint tab so update the combo boxes to get latest values from def
        if index == CONSTRAINT:
            self.updateComboBoxes()     
    
    @pyqtSlot()
    def on_btnDefineTemplateFormat_clicked(self):
        """
        Display the Node Template Format Editor
        """
        myTemplateRelFormatDict = self.TRFormatDict
        # if the template doesn't have a specific instance node format then get the project default
        if myTemplateRelFormatDict is None:
            myTemplateRelFormatDict = deepcopy(self.modelData["TRformat"])
        d = TRelFormatDlg(self, modelData = None, relFormat = TRelFormat(formatDict=myTemplateRelFormatDict))
        if d.exec_():
#            self.TRFormatDict = TRelFormat(formatDict=d.relFormat.formatDict).formatDict
            self.TRFormatDict = d.relFormat.formatDict
            self.formatChanged = True
    
    @pyqtSlot()
    def on_btnDefineInstanceFormat_clicked(self):
        """
        Display the Instance Node Format Editor
        """
        myInstanceRelFormatDict = self.IRFormatDict
        # if the template doesn't have a specific instance rel format then get the project default
        if myInstanceRelFormatDict is None:
            myInstanceRelFormatDict = deepcopy(self.modelData["IRformat"])
        d = IRelFormatDlg(self, modelData = None, relFormat = IRelFormat(formatDict=myInstanceRelFormatDict))
        if d.exec_():
#            self.IRFormatDict = IRelFormat(formatDict=d.relFormat.formatDict).formatDict
            self.IRFormatDict = d.relFormat.formatDict
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

    @pyqtSlot(int)
    def on_cmbToTemplate_currentIndexChanged(self, index):
        """
        The to template changed
        
        @param index DESCRIPTION
        @type int
        """
        self.editFromToType.setText("Node Type {}".format(self.cmbToTemplate.currentText()))
#        print(self.editFromToType.text())
        
    @pyqtSlot(int)
    def on_cmbFromTemplate_currentIndexChanged(self, index):
        """
        The from template changed
        
        @param index DESCRIPTION
        @type int
        """
        self.editToFromType.setText("Node Type {}".format(self.cmbFromTemplate.currentText()))
#        print(self.editToFromType.text())
        
    @pyqtSlot(int)
    def on_cmbFromCardinality_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        self.editFromToType.setText("Node Type {}".format(self.cmbToTemplate.currentText()))
#        print(self.editFromToType.text())
        
