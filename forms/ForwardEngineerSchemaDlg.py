# -*- coding: utf-8 -*-

"""
Module implementing GenerateSchemaDlg.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from core.helper import Helper
from .Ui_ForwardEngineerSchemaDlg import Ui_ForwardEngineerSchemaDlg

MODENEW = 1
MODEEDIT = 2

class ForwardEngineerSchemaDlg(QDialog, Ui_ForwardEngineerSchemaDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, objectType=None, genOption=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ForwardEngineerSchemaDlg, self).__init__(parent)
        self.setupUi(self)
        
        self.parent = parent
        self.objectType = objectType
        self.genOption = genOption
        self.helper = Helper()
        self.schemaTab = self.parent.parent.getSchemaTab()
#        self.schemaModel = self.schemaTab.schemaModel
        self.projectModel = self.parent.model
        # the generated cypher text
        self.cypherGen = ""
        # create a list of all the checkboxes
        self.cbList = [self.cbNodeKey, 
                     self.cbNodePropertyExists, 
                     self.cbNodePropertyUnique, 
                     self.cbRelPropertyExists, 
                     self.cbIndex
                     ]

        if self.objectType is None:
            # check all the check boxes                     
            for checkBox in self.cbList:
                checkBox.setChecked(True)
            self.rbIndexNoConstraint.setChecked(True)
        else:
            # uncheck all the check boxes                     
            for checkBox in self.cbList:
                checkBox.setChecked(False)
            # check the appropriate check box
            if objectType == "Node Key":
                self.cbNodeKey.setChecked(True)
            if objectType == "Node Property Exists":
                self.cbNodePropertyExists.setChecked(True)
            if objectType == "Node Property Unique":
                self.cbNodePropertyUnique.setChecked(True)
            if objectType == "Relationship Property Exists":
                self.cbRelPropertyExists.setChecked(True)
            if objectType == "Index All":
                self.cbIndex.setChecked(True)
                self.rbIndexAll.setChecked(True)
            if objectType == "Index Non-Constraint":
                self.cbIndex.setChecked(True)
                self.rbIndexNonConstraint.setChecked(True)
                
        if self.genOption is None:
#            self.rbDropFirst.setChecked(False)
#            self.rbCreateFirst.setChecked(False)
#            self.rbDropCreate.setChecked(False)
            self.rbCreateOnly.setChecked(True)
#            self.rbDropOnly.setChecked(False)
        else:
            if self.genOption == "DropFirst":
                self.rbDropFirst.setChecked(True)
            if self.genOption == "CreateFirst":
                self.rbCreateFirst.setChecked(True)    
            if self.genOption == "DropCreate":
                self.rbDropCreate.setChecked(True)
            if self.genOption == "CreateOnly":
                self.rbCreateOnly.setChecked(True)
            if self.genOption == "DropOnly":
                self.rbDropOnly.setChecked(True)
                
    def validate(self, ):    
        # make sure at least one schema object is checked
        foundOne = False
        for checkBox in self.cbList:
            if checkBox.isChecked():
                foundOne = True
        if foundOne == False:
            return False
        # 
        return True

    def generateCypher(self, ):

        self.cypherGen = ""
        self.listTypes = []
        # create a list of the checked object types
        if self.cbNodeKey.isChecked():
            self.listTypes.append("Node Key")
        if self.cbNodePropertyExists.isChecked():
            self.listTypes.append("Node Property Exists")
        if self.cbNodePropertyUnique.isChecked():
            self.listTypes.append("Node Property Unique")
        if self.cbRelPropertyExists.isChecked():
            self.listTypes.append("Relationship Property Exists")
        if self.cbIndex.isChecked():
            self.listTypes.append("Index")
            
        # generate the cypher commands
        if  self.rbDropFirst.isChecked():
            self.genDropFirst()
        elif self.rbCreateFirst.isChecked():
            self.genCreateFirst()
        elif self.rbDropCreate.isChecked():
            self.genDropCreate()
        elif self.rbCreateOnly.isChecked():
            self.genCreateOnly()
        elif self.rbDropOnly.isChecked():
            self.genDropOnly()

        editCypher = "// Generated by NodeEra from project: {} \n// by forward engineering \n".format(self.parent.fileName) + self.cypherGen
        self.schemaTab.addCypherEditorTab(fileName=None, fileText = editCypher, mode=MODENEW)
        # switch to the schema tab
        self.parent.pageItem.pageWidget.tabPage.setCurrentIndex(self.parent.pageItem.pageWidget.tabPage.indexOf(self.schemaTab))
        
    def genDropFirst(self):
        self.genDropOnly()
        self.saveDrop = self.cypherGen        
        self.genCreateOnly()
        self.saveCreate = self.cypherGen

        self.cypherGen =self.saveDrop + self.saveCreate 
        
    def genCreateFirst(self):
        self.genCreateOnly()
        self.saveCreate = self.cypherGen
        self.genDropOnly()
        self.saveDrop = self.cypherGen
        self.cypherGen = self.saveCreate + self.saveDrop

        
    def genDropCreate(self):
        # create an empty list of generated cypher statements
        lineList = []
        # generate drops then creates
        for objectType in self.listTypes:
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Drop then Create Statements \n".format(objectType)])
                if objectType == "Node Key":
                    conList = self.projectModel.genNodeKeyConstraints()
                if objectType == "Node Property Unique":
                    conList = self.projectModel.genNodePropUniqueConstraints()
                if objectType == "Node Property Exists":
                    conList = self.projectModel.genNodePropExistsConstraints()
                if objectType == "Relationship Property Exists":
                    conList = self.projectModel.genRelPropExistsConstraints()                       
                if objectType == "Index":
                    if self.rbIndexAll.isChecked():
                        conList = self.projectModel.genIndexes(indexType="all")
                    else:
                        conList = self.projectModel.genIndexes(indexType="nonconstraint")
                if len(conList) > 0:    
                    for con in conList:
                        lineList.extend( "DROP {} ;\n".format(con))
                        lineList.extend( "CREATE {} ;\n".format(con))

        self.cypherGen = ''.join(line for line in lineList)

    def genCreateOnly(self):
        # create an empty list of generated cypher statements
        lineList = []
        createList = []
        # generate creates
        for objectType in self.listTypes:
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                if objectType == "Node Key":
                    createList = self.projectModel.genNodeKeyConstraints()
                if objectType == "Node Property Unique":
                    createList = self.projectModel.genNodePropUniqueConstraints()
                if objectType == "Node Property Exists":
                    createList = self.projectModel.genNodePropExistsConstraints()   
                if objectType == "Relationship Property Exists":
                    createList = self.projectModel.genRelPropExistsConstraints()   

                if objectType == "Index":
                    if self.rbIndexAll.isChecked():
                        createList = self.projectModel.genIndexes(indexType="all")
                    else:
                        createList = self.projectModel.genIndexes(indexType="nonconstraint")
                if len(createList) > 0:    
                    for create in createList:
                        lineList.extend( "CREATE {} ;\n".format(create))

        self.cypherGen = ''.join(line for line in lineList)

    def genDropOnly(self):
        # create an empty list of generated cypher statements
        lineList = []
        # generate drops
        for objectType in self.listTypes:
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Drop Statements \n".format(objectType)])
                if objectType == "Node Key":                
                    dropList = self.projectModel.genNodeKeyConstraints()
                if objectType == "Node Property Unique":
                    dropList = self.projectModel.genNodePropUniqueConstraints()
                if objectType == "Node Property Exists":
                    dropList = self.projectModel.genNodePropExistsConstraints()
                if objectType == "Relationship Property Exists":
                    dropList = self.projectModel.genRelPropExistsConstraints()                       
                if objectType == "Index":
                    if self.rbIndexAll.isChecked():
                        dropList = self.projectModel.genIndexes(indexType="all")
                    else:
                        dropList = self.projectModel.genIndexes(indexType="nonconstraint")     
                if len(dropList) > 0:    
                    for drop in dropList:
                        lineList.extend( "DROP {} ;\n".format(drop))        

        self.cypherGen = ''.join(line for line in lineList)

    @pyqtSlot()
    def on_btnGenerate_clicked(self):
        """
        User requests to generate cypher code
        """
        if self.validate():
            self.generateCypher()
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        User clicks on the Close button
        """
        QDialog.accept(self)
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        User clicks on something to cancel out of the dialog
        """
        QDialog.reject(self)
    
    @pyqtSlot(bool)
    def on_cbIndex_clicked(self, checked):
        """
        user checked or unchecked the index checkbox
        enable or disable index radio buttons as appropriate
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked:
            self.rbIndexNoConstraint.setEnabled(True)
            self.rbIndexAll.setEnabled(True)
        else:
            self.rbIndexNoConstraint.setEnabled(False)
            self.rbIndexAll.setEnabled(False)
            
