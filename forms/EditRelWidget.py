# -*- coding: utf-8 -*-

"""
Module implementing EditRelWidget.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
import logging

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QApplication
from PyQt5.QtGui import QStandardItemModel,  QStandardItem

from .Ui_EditRelWidget import Ui_EditRelWidget
from core.helper import Helper
from core.NeoEditDelegate import NeoEditDelegate
from core.NodeTemplateCypher import NodeTemplateCypher

# rel template property list
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS = range(5)
# ENUM for property grid
PROPERTY, DATATYPE, VALUE = range(3)

class EditRelWidget(QWidget, Ui_EditRelWidget):
    """
    This widget provides a generic UI to enter a relationship
    """
    def __init__(self, parent=None, templateDict=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(EditRelWidget, self).__init__(parent)
        self.setupUi(self)
        self.helper = Helper()
        self.parent = parent
        self.neoCon = self.parent.neoCon
        self.designModel = self.parent.designModel
        self.templateDict = templateDict
        # rel type
        self.lblRelationship.setText("Relationship Type: {}".format(self.templateDict["relname"]))
        # from Node
        self.lblFromNode.setText("From Node - Node Template: {}".format(self.templateDict["fromTemplate"]))
        index, nodeTemplateDict = self.designModel.getDictByName(topLevel="Node Template",objectName=self.templateDict["fromTemplate"])        
        fromNodeTemplateCypher = NodeTemplateCypher(templateDict=nodeTemplateDict)
        getNodesCypher, x = fromNodeTemplateCypher.genMatchReturnNodeOnly()
#        print(getNodesCypher)
        rc, msg = self.runCypher(requestType="Get From Nodes based on Node Template: {}".format(self.templateDict["fromTemplate"]), cypher=getNodesCypher)
        if rc == True:
            self.loadNodeDropDown(dropDown=self.cmbFromNode)
        else:
            self.helper.displayErrMsg("Load From Nodes", "Error loading From Nodes - {}".format(msg))
        
        # to Node
        self.lblToNode.setText("To Node - Node Template: {}".format(self.templateDict["toTemplate"]))        
        index, nodeTemplateDict = self.designModel.getDictByName(topLevel="Node Template",objectName=self.templateDict["toTemplate"])        
        fromNodeTemplateCypher = NodeTemplateCypher(templateDict=nodeTemplateDict)
        getNodesCypher, x = fromNodeTemplateCypher.genMatchReturnNodeOnly()
#        print(getNodesCypher)
        rc, msg = self.runCypher(requestType="Get From Nodes based on Node Template: {}".format(self.templateDict["toTemplate"]), cypher=getNodesCypher)
        if rc == True:
            self.loadNodeDropDown(dropDown=self.cmbToNode)
        else:
            self.helper.displayErrMsg("Load To Nodes", "Error loading From Nodes - {}".format(msg))      
            
        # property grid
        self.gridProps.setSortingEnabled(False)
        self.gridProps.setModel(self.createPropModel())
        self.gridProps.setItemDelegate(NeoEditDelegate(self))
        self.gridProps.setColumnWidth(PROPERTY, 200)
        self.gridProps.setColumnWidth(DATATYPE, 125)
        self.gridProps.setColumnWidth(VALUE, 300)
        self.gridProps.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridProps.setSelectionMode(QAbstractItemView.SingleSelection)
        header = self.gridProps.horizontalHeader()
        header.setSectionResizeMode(PROPERTY, QHeaderView.Interactive)
        header.setSectionResizeMode(DATATYPE, QHeaderView.Fixed)
        header.setSectionResizeMode(VALUE, QHeaderView.Stretch)

        self.populateUIfromObject()    
        
    def logMsg(self, msg):
        # add message to the log
        if logging:
            logging.info(msg)        
            
    def createPropModel(self):

        model = QStandardItemModel(0, 3)
        model.setHeaderData(PROPERTY, Qt.Horizontal, "Property")
        model.setHeaderData(DATATYPE, Qt.Horizontal, "Data Type")
        model.setHeaderData(VALUE, Qt.Horizontal, "Value")
        
        return model  
        
    def populateUIfromObject(self, ):
        if self.templateDict is not None:
            #load props  PROPERTY, EXISTS, PROPREQ,PROPDEF,UNIQUE, PROPNODEKEY
            for nodeProp in self.templateDict["properties"]:
                self.addProp(self.gridProps.model(), nodeProp[PROPERTY], nodeProp[DATATYPE], nodeProp[PROPREQ], nodeProp[PROPDEF] )

    def loadNodeDropDown(self, dropDown=None):
#        print(self.neoCon.resultSet)
        dropdownList = []
        nodeList = ["[{}]-".format(str(result["nodeID"])) + str(result["Node"]) for result in self.neoCon.resultSet]
        dropdownList.extend(nodeList)
        dropDown.addItems(dropdownList)      
        
    def addProp(self,model,prop, dataType, required, default):
        '''
        add a row to the property grid
        '''
        self.gridProps.setSortingEnabled(False)
        if required == Qt.Checked:
            item1 = QStandardItem("{}".format(prop))
        else:
            item1 = QStandardItem("{}".format(prop))
        item1.setEditable(False)
        item2 = QStandardItem(dataType)
        item2.setEditable(False)
        
        if default is None or default == "":
            item3 = QStandardItem("Null")
        else:
            item3 = QStandardItem(default)
            
        item3.setData(dataType, Qt.UserRole + 1)
        item3.setEditable(True)
        model.appendRow([item1, item2, item3])

    def runCypher(self, requestType, cypher):
        '''
        Run a Cypher query and return the entire result set
        '''
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.logMsg("User requests {}".format(requestType))
        try:
            rc = False 
            self.logMsg(cypher)
            #run the query
            rc1, msg1 = self.neoCon.runCypherAuto(cypher)
            if rc1:
                self.logMsg("{} Relationship {}".format(requestType, msg1))
                rc = True
                msg = "{} Relationship complete".format(requestType)
            else:
                rc = False
                msg = "{} Relationship Error {}".format(requestType,  msg1)
        except BaseException as e:
            msg = "{} - {} failed.".format(requestType, repr(e))
        finally: 
            QApplication.restoreOverrideCursor()
            if rc == False:
                self.helper.displayErrMsg("Process Query",  msg)
            self.logMsg(msg)   
        
        return rc, msg
        
    @pyqtSlot()
    def on_btnSetNull_clicked(self):
        """
        User requests to set a property value to Null
        """
        # grid only allows single selection
        indexes = self.gridProps.selectionModel().selectedIndexes()
        for index in indexes:
            valueIndex = self.gridProps.model().index(index.row(), VALUE)
            self.gridProps.model().setData(valueIndex, "Null", Qt.DisplayRole)
    
    @pyqtSlot()
    def on_btnAddNew_clicked(self):
        """
        User clicks button to add new relationship
        """
        # the add logic is in the parent dialog
        self.parent.on_btnAddNew_clicked()
