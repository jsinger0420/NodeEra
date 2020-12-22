# -*- coding: utf-8 -*-

"""
Module implementing INPropertyBox.
This provides a model dialog to edit an Instance Node
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QInputDialog, QHeaderView, QApplication, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel,  QStandardItem
from forms.Ui_INPropertyBox import Ui_INPropertyBox
#from forms.NodeFormatTemplate import NodeFormat
from core.helper import Helper, CBDelegate
from core.Enums import DataType
from core.NeoEditDelegate import NeoEditDelegate

# ENUM's for label GRID
LABEL = 0
# ENUM for property grid
PROPERTY, DATATYPE, VALUE = range(3)
# ENUM for property definition in node template
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS, UNIQUE, PROPNODEKEY = range(7)
# ENUM's for the template label grid
LABEL, REQUIRED, NODEKEY = range(3)
# ENUM for tabs
DEFINITION, DESCRIPTION = range(2)


class INPropertyBox(QDialog, Ui_INPropertyBox):
    """
    Provide a modal dialog that allows the user to edit an instance node on an instance diagram.
    """
    treeViewUpdate = pyqtSignal()
    
    def __init__(self, parent=None, diagramInstance = None, model = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(INPropertyBox, self).__init__(parent)
        self.startUp = True
        self.parent = parent
        self.schemaModel = self.parent.schemaObject 
        self.helper = Helper()
        self.diagramInstance = diagramInstance
        # reload the NodeInstance dictionary values in case they've been changed on another diagram
        self.diagramInstance.reloadDictValues()
        
        self.model = model
        self.modelData = self.model.modelData
        self.node = None
#        self.rc = None
        self.msg = None
        self.formatChanged = False
        self.setupUi(self)
        self.initUI()

        self.populateUIfromObject()
        self.loadTemplateDropdown()
        
        self.startUp = False
        
    def initUI(self, ):
        # label grid
        self.gridLabels.setModel(self.createLabelModel())
        comboLblList = [""] 
        comboLblList.extend(sorted(set(self.model.instanceList("Label") + self.schemaModel.instanceList("Label"))))
#        comboLblList = self.model.loadComboBox(topLevel='Label', objectName=None, selectMsg="" )
        self.gridLabels.setItemDelegateForColumn(LABEL, CBDelegate(self, comboLblList, setEditable=True ))        
        self.gridLabels.setColumnWidth(LABEL, 200)
        self.gridLabels.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridLabels.setSelectionMode(QAbstractItemView.SingleSelection)
        
        header = self.gridLabels.horizontalHeader()
        header.setSectionResizeMode(LABEL, QHeaderView.Interactive)   
        
        # property grid
        self.gridProps.setSortingEnabled(False)
        self.gridProps.setModel(self.createPropModel())
        self.gridProps.setSortingEnabled(False)
        comboPropList = [""] 
        comboPropList.extend(sorted(set(self.model.instanceList("Property") + self.schemaModel.instanceList("Property"))))
        dataTypeList = [dataType.value for dataType in DataType]
        self.gridProps.setItemDelegate(NeoEditDelegate(self))
        self.gridProps.setItemDelegateForColumn(DATATYPE, CBDelegate(self, dataTypeList, setEditable=False))
        self.gridProps.setItemDelegateForColumn(PROPERTY, CBDelegate(self, comboPropList, setEditable=True ))
        self.gridProps.setColumnWidth(PROPERTY, 200)
        self.gridProps.setColumnWidth(DATATYPE, 125)
        self.gridProps.setColumnWidth(VALUE, 300)
        self.gridProps.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridProps.setSelectionMode(QAbstractItemView.SingleSelection)
        header = self.gridProps.horizontalHeader()
        header.setSectionResizeMode(PROPERTY, QHeaderView.Interactive)
        header.setSectionResizeMode(DATATYPE, QHeaderView.Fixed)
        header.setSectionResizeMode(VALUE, QHeaderView.Stretch)
        
        
    def populateUIfromObject(self, ):
        try:
#            print("NZID: {}".format(self.diagramInstance.NZID))
            self.editNZID.insert(str(self.diagramInstance.NZID))
        except:
            self.editNZID.insert("No NZID")
#            print("no NZID")        
        try:
#            print("NeoID: {}".format(self.diagramInstance.neoID))
            self.editNeoID.insert(str(self.diagramInstance.neoID))
        except:
            self.editNeoID.insert("No NeoID")
#            print("no neoID")        
 
        #load Label grid
        for nodeLbl in self.diagramInstance.labelList:
            self.addLabel(self.gridLabels.model(), nodeLbl[LABEL])
        #load Property grid    
        for nodeProp in self.diagramInstance.propList:
            self.addProp(self.gridProps.model(), nodeProp[PROPERTY], nodeProp[DATATYPE], nodeProp[VALUE])

    def loadTemplateDropdown(self, ):
        # load node template dropdown
        dropdownList = ["No Template Selected"]
        dropdownList.extend(sorted(self.model.instanceList("Node Template")))
        self.cboTemplate.addItems(dropdownList)
        if not self.diagramInstance.nodeTemplate is None:
            index = self.cboTemplate.findText(self.diagramInstance.nodeTemplate)
            if index >= 0:
                self.cboTemplate.setCurrentIndex(index)
            
    def logMsg(self, msg):
        # add message to the log
        if logging:
            logging.info(msg)        
        
    def createLabelModel(self):
        model = QStandardItemModel(0, 1)
        model.setHeaderData(LABEL, Qt.Horizontal, "Label")
        return model
    
    def createPropModel(self):

        model = QStandardItemModel(0, 3)
        model.setHeaderData(PROPERTY, Qt.Horizontal, "Property")
        model.setHeaderData(DATATYPE, Qt.Horizontal, "Data Type")
        model.setHeaderData(VALUE, Qt.Horizontal, "Value")
        # connect model slots 
        model.itemChanged.connect(self.propModelItemChanged)
        
        return model  
            

    def mergeTemplateWithInstanceNode(self, templateName):
        # don't merge template if we're just starting up the UI
        if self.startUp:
            return
            
        saveIndex, nodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=templateName)
        if nodeTemplateDict is None:
            self.logMsg("Merge Template Error - no node template dictionary for {}".format(templateName))
            return 

        # append any labels from the template not already on the instance node to the end of the label grid
        existingLabelList = [self.gridLabels.model().item(row,LABEL).data(Qt.EditRole) for row in range(0,self.gridLabels.model().rowCount()) ]
        templateLabelList = [ nodeLbl[LABEL] for nodeLbl in nodeTemplateDict["labels"]]
        newLabelList = list(set(templateLabelList) - set(existingLabelList))
        for lbl in newLabelList:
            self.addLabel(self.gridLabels.model(), lbl)
        
        # properties
        # what's on the form now
        existingPropList = [self.gridProps.model().item(row,PROPERTY).data(Qt.EditRole) for row in range(0,self.gridProps.model().rowCount()) ]
        existingValueList = [self.gridProps.model().item(row,VALUE).data(Qt.EditRole) for row in range(0,self.gridProps.model().rowCount()) ]
        # property list from the template
        newPropList = [ nodeProp[PROPERTY] for nodeProp in nodeTemplateDict["properties"]]
        newValueList = [ nodeProp[PROPDEF] for nodeProp in nodeTemplateDict["properties"]] # this should get default values some day
        # add new properties to the end of the list
        mergePropList = (list(set(newPropList) - set(existingPropList)))
        for prop in mergePropList:
            val = ""
            # get default value from template first 
            if prop in newPropList:
                val = newValueList[newPropList.index(prop)] 
            # override with existing value for same property if it exists
            if prop in existingPropList:
                val = existingValueList[existingPropList.index(prop)]
            # set Null so editor delegates will work
            if val == "" or val is None:
                val = "Null"
            dataType = self.model.getPropertyDataType(prop)
            self.addProp(self.gridProps.model(), prop, dataType, val)            

        
    def validate(self, ):
        # label grid checks
        if self.helper.gridNoNameError(grid=self.gridLabels, col=LABEL, txtMsg="You must supply a name for each Label"):
            self.gridLabels.setFocus()
            return False
        if self.helper.gridDupEntryError(self.gridLabels, col=LABEL, txtMsg="has been entered more than once. You can only use a Label once"):
            self.gridLabels.setFocus()
            return False
        # property grid checks
        if self.helper.gridNoNameError(grid=self.gridProps, col=PROPERTY, txtMsg="You must supply a name for each Property"):
            self.gridProps.setFocus()
            return False
        if self.helper.gridDupEntryError(self.gridProps, col=PROPERTY, txtMsg="has been entered more than once. You can only use a Property once"):
            self.gridProps.setFocus()
            return False
        
        model = self.gridProps.model()
        for row in range(0, model.rowCount()):
            nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),model.item(row,VALUE).data(Qt.EditRole)]
            # property datatype matches property definition
            if self.model.propertyDataTypeValid(name=nodeProp[PROPERTY], dataType=nodeProp[DATATYPE]) == False:
                self.helper.displayErrMsg("Validate", "You entered datatype {} for  property {} which does not match the property definition. Please enter the correct datatype.".format(nodeProp[DATATYPE], nodeProp[PROPERTY]))
                self.gridProps.setFocus()
                return False                
            # can't add/update a value for an Unknown datatype property
            if nodeProp[DATATYPE] == "Unknown" and nodeProp[VALUE] != "Null":
                self.helper.displayErrMsg("Validate", "Property {} has Unknown datatype.  You can't add/update a value for this property.  Set the value to Null".format(nodeProp[PROPERTY]))
                self.gridProps.setFocus()
                return False                
                
        
        # template defined required property has a value
        templateName = self.cboTemplate.currentText()
        saveIndex, nodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=templateName)
        if not nodeTemplateDict is None:
            model = self.gridProps.model()
            numrows = model.rowCount()
            for row in range(0,numrows):
                nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),model.item(row,VALUE).data(Qt.EditRole)]
                if nodeProp[VALUE] == "Null":
                    #  the value is null so see if it is required
                    for templateProp in nodeTemplateDict["properties"]:
                        if templateProp[PROPERTY] ==  nodeProp[PROPERTY]:
                            if templateProp[PROPREQ] == Qt.Checked:
                                # this property must have a value
                                self.helper.displayErrMsg("Validate", "The property {} is required. Please enter a value.".format(nodeProp[PROPERTY]))
                                return False
            
        return True
        
    def apply(self, ):
        # update the diagramInstance object with values from the UI.
        # save the labels
        self.diagramInstance.labelList = []
        model = self.gridLabels.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            nodeLbl = [model.item(row,LABEL).data(Qt.EditRole)]
            self.model.newLabel(nodeLbl[LABEL])   # check to see if this is a new Label and create a Label object in the dictionary
            self.diagramInstance.labelList.append(nodeLbl)
#        #save the attributes
        self.diagramInstance.propList = []
        model = self.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),model.item(row,VALUE).data(Qt.EditRole)]
#            print("save prop {}".format(nodeProp))
            self.model.newProperty(nodeProp[PROPERTY], nodeProp[DATATYPE])
            self.diagramInstance.propList.append(nodeProp)
        #save the template
        selectedTemplate = self.cboTemplate.currentText()
        self.diagramInstance.nodeTemplate = selectedTemplate
        # save the node itself in Neo4j
        rc, msg = self.updateNeo()
        
        return rc, msg
            
        
    def updateNeo(self, ):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if self.modelData["SyncMode"] == "On":
            rc, msg = self.diagramInstance.syncToDB(self.logMsg)
            if rc is True:
                returnmsg = "Update Node Succesful"
            else:
                returnmsg = "Update Node Failed: {}".format(msg)
                self.helper.displayErrMsg("Update Node", returnmsg)
        else:
            rc = True
            returnmsg = "Database Sync is off - Node not saved to graph"
            
        QApplication.restoreOverrideCursor() 
        
        return rc, returnmsg
        
    @pyqtSlot()
    def on_btnCreateTemplate_clicked(self):
        """
        Create a new Node Template based on the labels and properties entered into this Instance Node.
        This is the same logic as in the reverse engineering dialog
        """
        text, ok = QInputDialog.getText(self, 'New Node Template', 'Enter the Node Template Name:')
        if ok:
            #  make sure they entered something
            if len(text) < 1:
                self.helper.displayErrMsg("Create New Node Template Error", "You must enter a name.".format(text))
            #make sure entered name doesn't existing
            index, nodeDict = self.model.getDictByName("Node Template", text)
            #create a node template dictionary
            if not nodeDict is None:
                self.helper.displayErrMsg("Create New Node Template Error", "The node template {} already exists".format(text))
                return
            
            labelList = []
            model = self.gridLabels.model()
            numrows = model.rowCount()
            for row in range(0,numrows):
                nodeLbl = [model.item(row,LABEL).data(Qt.EditRole), Qt.Checked, Qt.Unchecked]
                self.model.newLabel(nodeLbl[LABEL])   # check to see if this is a new Label and create a Label object in the dictionary
                labelList.append(nodeLbl)
            propList = []
            model = self.gridProps.model()
            numrows = model.rowCount()
            for row in range(0,numrows):
                nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),Qt.Unchecked, "",Qt.Unchecked, Qt.Unchecked, Qt.Unchecked]
                self.model.newProperty(nodeProp[PROPERTY], nodeProp[DATATYPE])
                propList.append(nodeProp)
            # check for constraints that match label/prop
            # generate the constraints and indexes
            conList = []
            # look at each constraint in the schemaModel and see if it belongs to the node template
            self.schemaModel.matchConstraintNodeTemplate(conList, [lbl[0] for lbl in labelList], [prop[0] for prop in propList])
            # look at each index in the schemaModel and see if it belongs to the node template
            idxList = []
            self.schemaModel.matchIndexNodeTemplate(idxList, [lbl[0] for lbl in labelList], [prop[0] for prop in propList])            
            #save it to the model
            nodeDict = self.model.newNodeTemplate(name=text, labelList=labelList, propList=propList, 
                                                                    conList=conList, idxList = idxList, 
                                                                    desc="Template generated from Instance Node.")
            self.model.modelData["Node Template"].append(nodeDict)
            # refresh the treeview
            self.model.updateTV()
            # set combo box
            self.loadTemplateDropdown()
            if not (self.cboTemplate.findText(text) is None):
                self.cboTemplate.setCurrentIndex(self.cboTemplate.findText(text))
    
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
        Slot documentation goes here.
        """
        self.addLabel(self.gridLabels.model(), "")
        # common function to adjust grid after appending a row
        self.helper.adjustGrid(grid=self.gridLabels)
#        # scroll to bottom to insure the new row is visible
#        self.gridLabels.scrollToBottom()              
    
    @pyqtSlot()
    def on_btnLabelRemove_clicked(self):
        """
        Slot documentation goes here.
        """
        indexes = self.gridLabels.selectionModel().selectedIndexes()
        for index in sorted(indexes):
#            print('Row %d is selected' % index.row())
            self.gridLabels.model().removeRows(index.row(),1)
    
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
        User clicks Add Property
        """
        self.addProp(self.gridProps.model(), "", "String", "Null")
        # common function to adjust grid after appending a row
        self.helper.adjustGrid(grid=self.gridProps)
#        # scroll to bottom to insure the new row is visible
#        self.gridProps.scrollToBottom()    
        
    @pyqtSlot()
    def on_btnMakeNull_clicked(self):
        """
        User requests to set a property value to Null
        """
        # grid only allows single selection
        indexes = self.gridProps.selectionModel().selectedIndexes()
        for index in indexes:
            valueIndex = self.gridProps.model().index(index.row(), VALUE)
            self.gridProps.model().setData(valueIndex, "Null", Qt.DisplayRole)
        
    @pyqtSlot()
    def on_btnPropRemove_clicked(self):
        """
        Slot documentation goes here.
        """
        # grid only allows single selection
        indexes = self.gridProps.selectionModel().selectedIndexes()
        for index in indexes:
            self.gridProps.model().removeRows(index.row(),1)
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        User clicked OK button, validate the data then sync to graph
        """
        if self.validate():
            rc, msg = self.apply()
            if rc == True:
                QDialog.accept(self)
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        QDialog.reject(self)

    def addLabel(self,model,label):
        self.gridLabels.setSortingEnabled(False)
        item1 = QStandardItem(label)
        item1.setEditable(True)
        model.appendRow([item1,])
#        self.gridLabels.resizeColumnsToContents()
#        self.gridLabels.setSortingEnabled(True)
    
    def addProp(self,model,prop, dataType, value):
        '''
        add a row to the property grid
        '''
        self.gridProps.setSortingEnabled(False)
        item1 = QStandardItem(prop)
        item1.setEditable(True)
        item11 = QStandardItem(dataType)
        item11.setEditable(True)
        item2 = QStandardItem(value)
        item2.setData(dataType, Qt.UserRole + 1)
        item2.setEditable(True)
        model.appendRow([item1, item11, item2])

    
    @pyqtSlot(int)
    def on_cboTemplate_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
#        print("template changed {}".format(str(index)))
        # the new node template might have a custom format so set this to true which will force
        # a diagram redraw when the dialog closes.
        self.formatChanged = True
        if index > 0:
            self.mergeTemplateWithInstanceNode(self.cboTemplate.currentText())

    def propModelItemChanged(self, item):
        
#        print("item data changed {} at {} {}".format(str(item.checkState()), item.index().row(), item.index().column()))
        templateName = self.cboTemplate.currentText()
        columnNum = item.index().column()
        if columnNum == PROPERTY:
            # if property has changed then change the datatype
            propName = self.gridProps.model().item(item.index().row(),PROPERTY).data(Qt.EditRole)
            dataType = self.model.getPropertyDataType(propName)
            self.gridProps.model().item(item.index().row(), DATATYPE).setText(dataType)
            # see if this property has a default value defined in the template
            defaultVal = self.model.getTemplatePropDefVal(templateName=templateName, propName=propName)
            if not defaultVal is None:
                self.gridProps.model().item(item.index().row(), VALUE).setText(defaultVal)
                
        if columnNum == DATATYPE:
            # if datatype has changed then change value to "Null" 
            self.gridProps.model().item(item.index().row(), VALUE).setText("Null")
            dataType = self.gridProps.model().item(item.index().row(),DATATYPE).data(Qt.EditRole)
            self.gridProps.model().item(item.index().row(), VALUE).setData(dataType, Qt.UserRole+1)
    
    @pyqtSlot(int)
    def on_tabNodeInspector_currentChanged(self, index):
        """
        User has switched to another tab
        
        @param index DESCRIPTION
        @type int
        """
        # user switched to the description tab.  must regenerate description if there is a node template selected
        if index == DESCRIPTION:
            if self.cboTemplate.currentIndex() > 0:
                saveIndex, objectDict = self.model.getDictByName(topLevel="Node Template",objectName=self.cboTemplate.currentText())
                if not objectDict is None:
                    self.brwsrGeneratedDesc.setText(self.model.getNodeDescription(self.cboTemplate.currentText()))
                else:
                    self.helper.displayErrMsg("Get Description", "Error - could not find node template: {}".format(self.cboTemplate.currentText()))

