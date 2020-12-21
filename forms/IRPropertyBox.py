# -*- coding: utf-8 -*-

"""
Module implementing IRPropertyBox.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QHeaderView, QApplication, QAbstractItemView

from PyQt5.QtGui import QStandardItemModel,  QStandardItem

from forms.Ui_IRPropertyBox import Ui_IRPropertyBox
from core.helper import Helper, CBDelegate
from core.NodeInstance import NodeInstance
from core.Enums import DataType
from core.NeoEditDelegate import NeoEditDelegate

# ENUM for property grid
PROPERTY, DATATYPE, VALUE = range(3)
# ENUM for tabs
DEFINITION, DESCRIPTION = range(2)
# ENUM for rel template property list
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS = range(5)
'''
ir property box dropdown logic

initial UI setup
load relname dropdown 
- load dropdown with template rel names, if ir relname is in that list, select it, otherwise set cbo text only

loadFromTemplateDropDown
- if a rel template is selected, only load and select the appropriate from node template
- otherwise, load all node templates into from template dropdown

loadToTemplateDropDown
- if a rel template is selected, only load and select the appropriate to node template
- otherwise, load all node templates into to template dropdown

loadDropDownTemplate (rel template dropdown)
- load all rel templates into the dropdown and select the one the IR is currently set to


Ongoing dynamic changes
cborelname changed 
- load rel template dropdown with templates that use the selected relname, if any then select the first one. otherwise, load template dropdown with all templates
- select correct from and to node templates based on selected reltemplate

cboFromTemplate changed
- if no from template is selected then load from node dropdown with all nodes
- if a from template is selected then load from node dropdown with only nodes of the selected template type

cbotoTemplate changed
- if no to template is selected then load to node dropdown with all nodes
- if a to template is selected then load to node dropdown with only nodes of the selected template type

cboTemplate (rel template) changed
- merge template definition into IR definition
- load from template dropdown
- load to template dropdown
'''

class IRPropertyBox(QDialog, Ui_IRPropertyBox):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None,  diagramInstance = None, model = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(IRPropertyBox, self).__init__(parent)
        self.appStartup = True
        self.mergeTemplate = False
        self.parent = parent
        self.schemaModel = self.parent.schemaObject 
        self.helper = Helper()
        # this is the RelationInstance object - called generically diagramInstance. 
        self.diagramInstance = diagramInstance
        self.diagramInstance.reloadDictValues()
        self.model = model
        self.modelData = self.model.modelData
        self.rel = None
        self.setupUi(self)
#        self.appSetToTemplate = False
#        self.appSetFromTemplate = False
        
        self.initUI()

        self.populateUIfromObject()
        
        self.appStartup = False
        self.msg = ""
        
    def initUI(self, ):
        
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

        # load rel name list, select rel name
        self.loadRelationshipNameDropDown()        
        # load from nodes, select the from node and load the from node template if any
        self.loadFromNodeDropdown()
        # load to nodes, select the to node and load the to node template if any
        self.loadToNodeDropdown()
        # load rel template names, select rel template name if any
        self.loadRelTemplateDropDown()

        #NZID
        try:
            self.EditNZID.insert(str(self.diagramInstance.NZID))
        except:
            print("no NZID") # this shouldn't happen
        # neoID
        try:
            self.editNeoID.insert(str(self.diagramInstance.neoID))
        except:
            self.editNeoID.insert("None")

        # disable rel name if already defined
        if self.editNeoID.text() == "None":
            self.cboRelName.setEnabled(True)
        else:
            self.cboRelName.setEnabled(False)
        
        # disable dropdowns if start and end nodes defined 
        if self.cboFromNode.currentIndex() > 0:
            self.cboFromNode.setEnabled(False)
        if self.cboToNode.currentIndex() > 0:
            self.cboToNode.setEnabled(False)

        # load the properties
        for nodeProp in self.diagramInstance.propList:
            self.addProp(self.gridProps.model(), nodeProp[PROPERTY], nodeProp[DATATYPE],  nodeProp[VALUE])

            
    def loadRelationshipNameDropDown(self, ):
        # load relationship name (type)  dropdown
        dropdownList = []
        dropdownList.append("Enter or Select Relationship Type")
        # get relationship types from the project model
        templateRelList = [relDict["name"] for relDict in self.modelData["Relationship"] ]    
#        templateRelList = [relDict["relname"] for relDict in self.modelData["Relationship Template"] ]    
        # get relationship types from the schemamodel - this needs to be fixed, need common access to schemamodel from project page and instance diagram
        schemaRelList =  [rel["name"] for rel in self.schemaModel.schemaData["Relationship"] ]
#        schemaRelList = []
        # merge, dedup, and sort the two lists and put them in the dropdown
        dropdownList.extend(sorted(set(templateRelList + schemaRelList)))
        self.cboRelName.addItems(dropdownList)      
        # if no relationship name has been set then display enabled combo box  
        if (self.diagramInstance.relName is None or self.diagramInstance.relName == "NoRelationshipName"):
            self.cboRelName.setCurrentIndex(0)
        else:
            # if the relationship name has been set then display the rel name
            index = self.cboRelName.findText(self.diagramInstance.relName)
            if index >= 0:
                self.cboRelName.setCurrentIndex(index)
            else:
                # its not a template rel name so just set the text value of the combo box
                self.cboRelName.setEditText(self.diagramInstance.relName)
        
    def loadFromNodeDropdown(self, ):
        # load from node dropdown
        dropdownList = []
        dropdownList.append("No From Node Selected")
        nodeList = self.model.instanceDisplayNameList("Instance Node")
        for node in nodeList:
            dropdownList.append(node)
        self.cboFromNode.addItems(dropdownList)
        if not self.diagramInstance.startNZID is None:
            item, objectDict = self.model.getDictByName("Instance Node",self.diagramInstance.startNZID )
            if  not objectDict is None:
                index = self.cboFromNode.findText(objectDict.get("displayName", ""))
                if index >= 0:
                    self.cboFromNode.setCurrentIndex(index)
                    self.cboFromNode.setEnabled(False)


        
    def loadToNodeDropdown(self, ):
        
        # load from node dropdown
        dropdownList = []
        dropdownList.append("No To Node Selected")
        nodeList = self.model.instanceDisplayNameList("Instance Node")
        for node in nodeList:
            dropdownList.append(node)
        self.cboToNode.addItems(dropdownList)
        if not self.diagramInstance.endNZID is None:
            item, objectDict = self.model.getDictByName("Instance Node",self.diagramInstance.endNZID )
            if  not objectDict is None:
                index = self.cboToNode.findText(objectDict.get("displayName", ""))
                if index >= 0:
                    self.cboToNode.setCurrentIndex(index)
                    self.cboToNode.setEnabled(False)


    def loadRelTemplateDropDown(self, ):
        # load rel template dropdown
        self.cboTemplate.clear()
        startNodeTemplate=self.txtFromTemplate.text() 
        endNodeTemplate=self.txtToTemplate.text() 
#        relName = self.diagramInstance.relName
        relName = self.cboRelName.currentText()
        dropdownList = ["No Template Selected"]
        dropdownList.extend(sorted(self.model.matchAllRelTemplates(startNodeTemplate=startNodeTemplate, endNodeTemplate=endNodeTemplate, relName = relName )))
        self.cboTemplate.addItems(dropdownList)
        if not self.diagramInstance.relTemplate is None:
            index = self.cboTemplate.findText(self.diagramInstance.relTemplate)
            if index >= 0:
                self.cboTemplate.setCurrentIndex(index)  
        

        
    def createPropModel(self):

        model = QStandardItemModel(0, 3)
        model.setHeaderData(PROPERTY, Qt.Horizontal, "Property")
        model.setHeaderData(DATATYPE, Qt.Horizontal, "Data Type")
        model.setHeaderData(VALUE, Qt.Horizontal, "Value")
        # connect model slots 
        model.itemChanged.connect(self.propModelItemChanged)
        
        return model         
       
       
    def getNodeInstance(self, NZID):
        '''
        Using an NZID, create a NodeInstanceObject and return it
        if it doesn't exist, return None
        '''
        index, nodeDict = self.model.getDictByName(topLevel="Instance Node", objectName=NZID)
        nodeInstance = NodeInstance(model=self.model, nodeInstanceDict = nodeDict)
        return nodeInstance
        
    def logMsg(self, msg):
        # add message to the log
        if logging:
            logging.info(msg)        
        
    def validate(self, ):
        if self.helper.gridNoNameError(grid=self.gridProps, col=PROPERTY, txtMsg="You must supply a name for each Property"):
            self.gridProps.setFocus()
            return False
        if self.helper.gridDupEntryError(self.gridProps, col=PROPERTY, txtMsg="has been entered more than once. You can only use a Property once"):
            self.gridProps.setFocus()
            return False
        if self.helper.NoTextValueError(self.cboRelName.currentText(), "You must enter a relationship name."):
            self.cboRelName.setFocus()
            return False
        if self.cboRelName.currentText() == "Enter or Select Relationship Type":
            self.helper.displayErrMsg("Instance Relationship", "You must enter a relationship name.")
            self.cboRelName.setFocus()
            return False            
        if self.cboFromNode.currentIndex() == 0:
            self.helper.displayErrMsg("Instance Relationship", "You must select a from node.")
            self.cboFromNode.setFocus()
            return False
        if self.cboToNode.currentIndex() == 0:
            self.helper.displayErrMsg("Instance Relationship", "You must select a to node.")
            self.cboToNode.setFocus()
            return False
        # property datatype matches property definition
        model = self.gridProps.model()
        for row in range(0, model.rowCount()):
            nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),model.item(row,VALUE).data(Qt.EditRole)]
            if self.model.propertyDataTypeValid(name=nodeProp[PROPERTY], dataType=nodeProp[DATATYPE]) == False:
                self.helper.displayErrMsg("Validate", "You entered datatype {} for  property {} which does not match the property definition. Please enter the correct datatype.".format(nodeProp[DATATYPE], nodeProp[PROPERTY]))
                self.gridProps.setFocus()
                return False     
                
        # template defined required property has a value
        templateName = self.cboTemplate.currentText()
        saveIndex, relTemplateDict = self.model.getDictByName(topLevel="Relationship Template",objectName=templateName)
        if not relTemplateDict is None:
            model = self.gridProps.model()
            numrows = model.rowCount()
            for row in range(0,numrows):
                nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),model.item(row,VALUE).data(Qt.EditRole)]
                if nodeProp[VALUE] == "Null":
                    #  the value is null so see if it is required
                    for templateProp in relTemplateDict["properties"]:
                        if templateProp[PROPERTY] ==  nodeProp[PROPERTY]:
                            if templateProp[PROPREQ] == Qt.Checked:
                                # this property must have a value
                                self.helper.displayErrMsg("Validate", "The property {} is required. Please enter a value.".format(nodeProp[PROPERTY]))
                                return False
        return True
        
    def apply(self, ):
        #update the diagramInstance object with values from the UI.
        self.diagramInstance.relName = self.cboRelName.currentText()
        # if its a new rel type then add it to the model
        self.model.newRelationship(self.diagramInstance.relName)
        # update property list
        self.diagramInstance.propList = []
        model = self.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole), model.item(row,VALUE).data(Qt.EditRole)]
#            print(nodeProp)
            # if its a new property add it to the model
            self.model.newProperty(nodeProp[PROPERTY], nodeProp[DATATYPE] )
            self.diagramInstance.propList.append(nodeProp)
        #save the template
        selectedTemplate = self.cboTemplate.currentText()
        self.diagramInstance.relTemplate = selectedTemplate        
        # save the relationship itself in Neo4j
        rc, msg = self.updateNeo()
        self.msg = msg
        return rc, msg

    def updateNeo(self, ):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if self.modelData["SyncMode"] == "On":
            rc, msg = self.diagramInstance.syncToDB(self.logMsg)
            if rc is True:
                returnmsg = "Update Relationship Succesful"
            else:
                returnmsg = "Update Relationship Failed: {}".format(msg)
                self.helper.displayErrMsg("Update Relationship", returnmsg)
        else:
            rc = True
            returnmsg = "Database Sync is off - Relationship not saved to graph"
        
        QApplication.restoreOverrideCursor()
        return rc, returnmsg
    
    @pyqtSlot()
    def on_btnPropAdd_clicked(self):
        """
        Slot documentation goes here.
        """
        self.addProp(self.gridProps.model(), "","String", "Null")
        # common function to adjust grid after appending a row
        self.helper.adjustGrid(grid=self.gridProps)
#        # scroll to bottom to insure the new row is visible
#        self.gridProps.scrollToBottom()      
    
    @pyqtSlot()
    def on_btnPropRemove_clicked(self):
        """
        Slot documentation goes here.
        """
        indexes = self.gridProps.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            for index in sorted(indexes):
                self.gridProps.model().removeRows(index.row(),1)
        else:
            self.helper.displayErrMsg("Remove Property", "You must select a row to remove")   
            
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
    def on_okButton_clicked(self):
        """
        User clicked on OK button, validate data and sync to graph
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
    
    def addProp(self,model,prop,dataType, value):

        self.gridProps.setSortingEnabled(False)
        item1 = QStandardItem(prop)
        item1.setEditable(True)
        item11 = QStandardItem(dataType)
        item11.setEditable(True)
        item2 = QStandardItem(value)
        item2.setData(dataType, Qt.UserRole + 1)
        item2.setEditable(True)
        model.appendRow([item1, item11, item2])
        
    @pyqtSlot()
    def on_btnCreateTemplate_clicked(self):
        """
        Create a new Relationship Template based on this instance relationship.
        """
        text, ok = QInputDialog.getText(self, 'New Relationship Template', 'Enter the Relationship Template Name:')
        if ok:
            #  make sure they entered something
            if len(text) < 1:
                self.helper.displayErrMsg("Create New Relationship Template Error", "You must enter a name.".format(text))
            #make sure entered name doesn't exist
            index, relDict = self.model.getDictByName("Relationship Template", text)
            if not relDict is None:
                self.helper.displayErrMsg("Create New Relationship Template Error", "The Relationship template {} already exists".format(text))
                return
            # validate the data first, then add the new relationship template
            if self.validate():
                # if its a new rel type then add it to the model
                self.model.newRelationship(self.cboRelName.currentText())
                # save the properties
                propList = []
                model = self.gridProps.model()
                numrows = model.rowCount()
                for row in range(0,numrows):
                    nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole),model.item(row,DATATYPE).data(Qt.EditRole),  Qt.Unchecked, "", Qt.Unchecked]
                    self.model.newProperty(nodeProp[PROPERTY], nodeProp[DATATYPE])
                    propList.append(nodeProp)
                # generate the constraints
                conList = []
                # look at each constraint in the schemaModel and see if it belongs to the rel template
                self.schemaModel.matchConstraintRelTemplate(conList, [prop[0] for prop in propList], relName=self.cboRelName.currentText())
                # get the source/target node template if any
                # can only save a source target if both instance nodes are based on a node template
                try:
                    startNodeInstance = self.getNodeInstance(self.diagramInstance.startNZID)
                    fromTemplate=startNodeInstance.nodeTemplate
                    endNodeInstance = self.getNodeInstance(self.diagramInstance.endNZID)
                    toTemplate=endNodeInstance.nodeTemplate
                    if (not fromTemplate == "No Template Selected" and not toTemplate == "No Template Selected" ):
                        #save it to the model
                        relDict = self.model.newRelTemplateDict(name=text, relname = self.cboRelName.currentText(), propList=propList, 
                                                                                desc="Template generated from Instance Relationship.", 
                                                                                conList=conList, fromTemplate=fromTemplate, toTemplate=toTemplate )
                        self.model.modelData["Relationship Template"].append(relDict)
                        # refresh the treeview
                        self.model.updateTV()
                        # update dropdown  and select the newly created template
                        self.loadRelTemplateDropDown()
                        index = self.cboTemplate.findText(text)
                        if index >= 0:
                            self.cboTemplate.setCurrentIndex(index)
                    else:
                        self.helper.displayErrMsg("Create Template", "Cannot create a relationship template without a from node template and a to node template.")
                except Exception as e:
                    self.helper.displayErrMsg("Create Template","Error creating relationship template: {}".format(str(e)))
            
    def templateChange(self, index):
        if index > 0:
            self.mergeTemplateWithInstanceRel(self.cboTemplate.currentText())

    def mergeTemplateWithInstanceRel(self, templateName):
        '''this merges the properties from the relationship template with the  properties that already exist on the instance relationship
        '''
        # if app is just starting up don't do this
        if self.appStartup:
            return
        # tell the other functions we're merging the template
        self.mergeTemplate = True
        
        saveIndex, relDict = self.model.getDictByName(topLevel="Relationship Template",objectName=templateName)
        if relDict is None:
            self.helper.displayErrMsg("Merge Relationship Template", "Error - Relationship Template {} doesn't exist".format(templateName))
            return         

        # properties
        # what's on the form now
        existingPropList = [self.gridProps.model().item(row,PROPERTY).data(Qt.EditRole) for row in range(0,self.gridProps.model().rowCount()) ]
        existingValueList = [self.gridProps.model().item(row,VALUE).data(Qt.EditRole) for row in range(0,self.gridProps.model().rowCount()) ]
        # property list from the template
        newPropList = [ nodeProp[PROPERTY] for nodeProp in relDict["properties"]]
        newValueList = [ nodeProp[PROPDEF] for nodeProp in relDict["properties"]] # this should get default values some day
        # merge them together
        mergePropList = (list(set(existingPropList + newPropList)))
        mergePropList.sort()
        self.gridProps.model().removeRows( 0, self.gridProps.model().rowCount())
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
        
        self.diagramInstance.relName = relDict["relname"]
        index = self.cboRelName.findText(self.diagramInstance.relName)
        if index >= 0:
            self.cboRelName.setCurrentIndex(index)
        
        # we're done merging
        self.mergeTemplate = False
    
    @pyqtSlot(int)
    def on_cboTemplate_currentIndexChanged(self, index):
        """
        The User has selected a relationship template to use.
        
        @param index DESCRIPTION
        @type int
        """
        # if they selected a rel template then merge it with whatever is on the gui
        if index > 0:
            self.mergeTemplateWithInstanceRel(self.cboTemplate.currentText())

            
    
    @pyqtSlot(int)
    def on_cboFromNode_currentIndexChanged(self, index):
        """
        The user has selected a new from instance node for the relationship
        
        @param index DESCRIPTION
        @type int
        """
        if index > 0:
            # create NodeInstance object
            displayName  = self.cboFromNode.currentText()
            NZID = self.model.lookupNZIDfromDisplayName(displayName=displayName, topLevel="Instance Node")
            if not  NZID is None:
                self.diagramInstance.startNode = self.getNodeInstance(NZID)
                self.diagramInstance.startNZID = NZID
                # if the instance node is based on a node template then set that
                fromTemplate=self.diagramInstance.startNode.nodeTemplate
                self.txtFromTemplate.setText(fromTemplate)   

        else:
            self.txtFromTemplate.setText("")   
        
        
        # force rel template dropdown to refill valid choices
        if self.mergeTemplate == False: 
            self.loadRelTemplateDropDown()            
            
    @pyqtSlot(int)
    def on_cboToNode_currentIndexChanged(self, index):
        """
        The user has selected a new to instance node for the relationship
        
        @param index DESCRIPTION
        @type int
        """
        if index > 0:
            # create NodeInstance object
            displayName  = self.cboToNode.currentText()
            NZID = self.model.lookupNZIDfromDisplayName(displayName=displayName, topLevel="Instance Node")
            if not  NZID is None: 
                self.diagramInstance.endNode = self.getNodeInstance(NZID)
                self.diagramInstance.endNZID = NZID
                # if the instance node is based on a node template then set that
                toTemplate=self.diagramInstance.endNode.nodeTemplate
                self.txtToTemplate.setText(toTemplate)     
        else:
            self.txtToTemplate.setText("")   
            
        # force node template dropdown to refill valid choices
        if self.mergeTemplate == False: 
            self.loadRelTemplateDropDown()            

    @pyqtSlot(int)
    def on_cboRelName_currentIndexChanged(self, index):
        """
        The relationship type was changed
        
        @param index DESCRIPTION
        @type int
        """
        # user changed the relationship type name so reset the template dropdown to new list of valid templates and pick the "none selected" option which forces the user to reselect a template
        if self.mergeTemplate == False: 
            self.loadRelTemplateDropDown() 
            self.cboTemplate.setCurrentIndex(0)
            
#        if index > 0:
##            relName = self.cboRelName.currentText()
#            # reload rel template dropdown to reflect newly selected rel type
##            relTemplate = self.cboTemplate.currentText()
#            self.loadRelTemplateDropDown()
#            self.cboTemplate.setCurrentIndex(0)
##            relList = ["select a relationship template"] + [relDict["name"] for relDict in self.modelData["Relationship Template"] if relDict["relname"] == relName]
##            self.cboTemplate.clear()
##            self.cboTemplate.addItems(relList)
#            # set to no rel template selected.
##            self.cboTemplate.setCurrentIndex(0)
#        else:
#            # user switched back to no rel name selected so relaod all rel templates
#            self.loadRelTemplateDropDown()
#            self.cboTemplate.setCurrentIndex(0)  
            

        
    def propModelItemChanged(self, item):
        
#        print("item data changed {} at {} {}".format(str(item.checkState()), item.index().row(), item.index().column()))

        # this checks to see if property name changed and updates the data type accordingly
        columnIndex = item.index().column()
        if columnIndex == PROPERTY:
            # if property has changed then change the datatype
            propName = self.gridProps.model().item(item.index().row(),PROPERTY).data(Qt.EditRole)
            dataType = self.model.getPropertyDataType(propName)
            self.gridProps.model().item(item.index().row(), DATATYPE).setText(dataType)
        if columnIndex == DATATYPE:
            # if datatype has changed then change value to "Null" 
            self.gridProps.model().item(item.index().row(), VALUE).setText("Null")
            dataType = self.gridProps.model().item(item.index().row(),DATATYPE).data(Qt.EditRole)
            self.gridProps.model().item(item.index().row(), VALUE).setData(dataType, Qt.UserRole+1)
    
    @pyqtSlot()
    def on_btnSetNull_clicked(self):
        """
        User clicks button to set a property value to Null
        """
        indexes = self.gridProps.selectionModel().selectedIndexes()
        for index in indexes:
            valueIndex = self.gridProps.model().index(index.row(), VALUE)
            self.gridProps.model().setData(valueIndex, "Null", Qt.DisplayRole)
    
    @pyqtSlot(int)
    def on_tabRelInspector_currentChanged(self, index):
        """
        User has switched to another tab
        
        @param index DESCRIPTION
        @type int
        """
        # user switched to the description tab.  must regenerate description if there is a node template selected
        if index == DESCRIPTION:
            if self.cboTemplate.currentIndex() > 0:
                saveIndex, objectDict = self.model.getDictByName(topLevel="Relationship Template",objectName=self.cboTemplate.currentText())
                if not objectDict is None:
                    self.brwsrGeneratedDesc.setText(self.model.getRelationshipDescription(objectDict))
                else:
                    self.helper.displayErrMsg("Get Description", "Error - could not find node template: {}".format(self.cboTemplate.currentText))
    
#    @pyqtSlot(int)
#    def on_cboTemplate_activated(self, index):
#        """
#        Slot documentation goes here.
#        
#        @param index DESCRIPTION
#        @type int
#        """
#        print("cboTemplateActivated:{}".format(str(index)))
