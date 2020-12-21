# -*- coding: utf-8 -*-

"""
Module implementing GenerateSchemaDlg.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from core.helper import Helper
from .Ui_GenerateSchemaDlg import Ui_GenerateSchemaDlg

MODENEW = 1
MODEEDIT = 2

class GenerateSchemaDlg(QDialog, Ui_GenerateSchemaDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, objectType=None, genOption=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(GenerateSchemaDlg, self).__init__(parent)
        self.setupUi(self)
        
        self.parent = parent
        self.objectType = objectType
        self.genOption = genOption
        self.helper = Helper()
#        self.schemaTab = self.parent.pageDict[self.parent.curPage].pageWidget.tabPage.currentWidget()
        self.schemaTab = self.parent.getSchemaTab()
        # the generated cypher text
        self.cypherGen = ""
        # create a list of all the checkboxes
        self.cbList = [self.cbNodeKey, 
                     self.cbNodePropertyExists, 
                     self.cbNodePropertyUnique, 
                     self.cbRelPropertyExists, 
                     self.cbIndex, 
                     self.cbUser, 
                     self.cbRole]

        if self.objectType is None:
            # check all the check boxes                     
            for checkBox in self.cbList:
                checkBox.setChecked(True)
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
            if objectType == "Index":
                self.cbIndex.setChecked(True)
            if objectType == "User":
                self.cbUser.setChecked(True)
            if objectType == "Role":
                self.cbRole.setChecked(True)
        
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
        if self.parent.curPage:
            if self.parent.curPage in self.parent.pageDict:
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
                if self.cbUser.isChecked():
                    self.listTypes.append("User")
                if self.cbRole.isChecked():
                    self.listTypes.append("Role") 
                    
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

                editCypher = "// Schema objects generated by NodeEra \n" + self.cypherGen
                self.schemaTab.addCypherEditorTab(fileName=None, fileText = editCypher, mode=MODENEW)


                
        return
        
#        self.schemaData["TopLevel"] = ["Node Key","Node Property Unique",
#                                                     "Node Property Exists","Relationship Property Exists",
#                                                     "Index",
#                                                     "User", 
#                                                     "Role", 
#                                                     "Label", "Property", "Relationship"]
    def genDropFirst(self):
        # create an empty list of generated cypher statements
        lineList = []
        # generate drops
        for objectType in self.listTypes:
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                for x in self.schemaTab.schemaModel.instanceList(objectType):
                    # this logic is needed to resolve neo4j error, when retrieving nodekeys if it only has one property the retrieved nodekey text has a syntax error
                    if (not "ASSERT (" in x and objectType == "Node Key"):
                        x = x.replace("ASSERT ", "ASSERT (")
                        x = x.replace(" IS", ") IS")
                    lineList.extend( ["Drop {} ;\n".format(x) ])                        

#        for objectType in self.listTypes:
#            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
#                lineList.extend( ["// Generated {} Drop Statements \n".format(objectType)])
#                lineList.extend( ["Drop {} ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)])


        for objectType in self.listTypes:
            if objectType in ["User"]:
                lineList.extend( ["// Generated {} Delete Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.deleteUser('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType) if x != "neo4j"] )
        for objectType in self.listTypes:
            if objectType in ["Role"]:
                lineList.extend( ["// Generated {} Delete Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.deleteRole('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType) if not x in ["editor", "reader", "architect", "admin", "publisher"]])
                
        # generate creates
        for objectType in self.listTypes:
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                for x in self.schemaTab.schemaModel.instanceList(objectType):
                    # this logic is needed to resolve neo4j error, when retrieving nodekeys if it only has one property the retrieved nodekey text has a syntax error
                    if (not "ASSERT (" in x and objectType == "Node Key"):
                        x = x.replace("ASSERT ", "ASSERT (")
                        x = x.replace(" IS", ") IS")
                    lineList.extend( ["Create {} ;\n".format(x) ])                
        
        
        
        
#        for objectType in self.listTypes:
#            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
#                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
#                lineList.extend( ["Create {} ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)])
        
        
        
        for objectType in self.listTypes:
            if objectType in ["Role"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.createRole('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)   if not x in ["editor", "reader", "architect", "admin", "publisher"]])
        for objectType in self.listTypes:
            if objectType in ["User"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.createUser('{}','changeonfirstlogon',TRUE) ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)  if x != "neo4j" ])
###  need to add creates for assigning roles to users

        self.cypherGen = ''.join(line for line in lineList)
        
    def genCreateFirst(self):
        # create an empty list of generated cypher statements
        lineList = []
        # generate creates
        for objectType in self.listTypes:
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                for x in self.schemaTab.schemaModel.instanceList(objectType):
                    # this logic is needed to resolve neo4j error, when retrieving nodekeys if it only has one property the retrieved nodekey text has a syntax error
                    if (not "ASSERT (" in x and objectType == "Node Key"):
                        x = x.replace("ASSERT ", "ASSERT (")
                        x = x.replace(" IS", ") IS")
                    lineList.extend( ["Create {} ;\n".format(x) ])        
        
#        for objectType in self.listTypes:
#            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
#                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
#                lineList.extend( ["Create {} ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)])
        
        for objectType in self.listTypes:
            if objectType in ["Role"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.createRole('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)  if not x in ["editor", "reader", "architect", "admin", "publisher"]])
        for objectType in self.listTypes:
            if objectType in ["User"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.createUser('{}','changeonfirstlogon',TRUE) ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)  if x != "neo4j"])
###  need to add creates for assigning roles to users
        
        # generate drops
        for objectType in self.listTypes:
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                for x in self.schemaTab.schemaModel.instanceList(objectType):
                    # this logic is needed to resolve neo4j error, when retrieving nodekeys if it only has one property the retrieved nodekey text has a syntax error
                    if (not "ASSERT (" in x and objectType == "Node Key"):
                        x = x.replace("ASSERT ", "ASSERT (")
                        x = x.replace(" IS", ") IS")
                    lineList.extend( ["Drop {} ;\n".format(x) ])                        

#        
#        for objectType in self.listTypes:
#            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
#                lineList.extend( ["// Generated {} Drop Statements \n".format(objectType)])
#                lineList.extend( ["Drop {} ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)])




        for objectType in self.listTypes:
            if objectType in ["User"]:
                lineList.extend( ["// Generated {} Delete Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.deleteUser('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)   if x != "neo4j"])
        for objectType in self.listTypes:
            if objectType in ["Role"]:
                lineList.extend( ["// Generated {} Delete Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.deleteRole('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)   if not x in ["editor", "reader", "architect", "admin", "publisher"]])
                
        self.cypherGen = ''.join(line for line in lineList)
        
    def genDropCreate(self):
        # create an empty list of generated cypher statements
        lineList = []
        # generate drops then creates
        for objectType in self.listTypes:
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                for x in self.schemaTab.schemaModel.instanceList(objectType):
                    # this logic is needed to resolve neo4j error, when retrieving nodekeys if it only has one property the retrieved nodekey text has a syntax error
                    if (not "ASSERT (" in x and objectType == "Node Key"):
                        x = x.replace("ASSERT ", "ASSERT (")
                        x = x.replace(" IS", ") IS")
                    lineList.extend( ["Drop {} ;\n".format(x)] )
                    lineList.extend( ["Create {} ;\n".format(x) ])
        
#        for objectType in self.listTypes:
#            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
#                lineList.extend( ["// Generated {} Drop/Create Statements \n".format(objectType)])
#                for x in self.schemaTab.schemaModel.instanceList(objectType):
#                    lineList.append( "Drop {} ;\n".format(x) )
#                    lineList.append( "Create {} ;\n".format(x) )

        for objectType in self.listTypes:
            if objectType in ["User"]:
                lineList.extend( ["// Generated {} Delete/Create Statements \n".format(objectType) ])
                lineList.extend( ["CALL dbms.security.deleteUser('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)   if x != "neo4j"])
                lineList.extend( ["CALL dbms.security.createUser('{}','changeonfirstlogon',TRUE) ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)  if x != "neo4j"])
        
        for objectType in self.listTypes:
            if objectType in ["Role"]:
                lineList.extend( ["// Generated {} Delete/Create Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.deleteRole('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)   if not x in ["editor", "reader", "architect", "admin", "publisher"]])
                lineList.extend( ["CALL dbms.security.createRole('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)   if not x in ["editor", "reader", "architect", "admin", "publisher"]])

        self.cypherGen = ''.join(line for line in lineList)

    def genCreateOnly(self):
        # create an empty list of generated cypher statements
        lineList = []
        # generate creates
        for objectType in self.listTypes:
          
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                for x in self.schemaTab.schemaModel.instanceList(objectType):
                    # this logic is needed to resolve neo4j error, when retrieving nodekeys if it only has one property the retrieved nodekey text has a syntax error
                    if (not "ASSERT (" in x and objectType == "Node Key"):
                        x = x.replace("ASSERT ", "ASSERT (")
                        x = x.replace(" IS", ") IS")
                    
                    lineList.extend( ["Create {} ;\n".format(x) ])
                    
        for objectType in self.listTypes:
            if objectType in ["Role"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.createRole('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)    if not x in ["editor", "reader", "architect", "admin", "publisher"]])
        for objectType in self.listTypes:
            if objectType in ["User"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.createUser('{}','changeonfirstlogon',TRUE) ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)   if x != "neo4j"])
###  need to add creates for assigning roles to users

        self.cypherGen = ''.join(line for line in lineList)

    def genDropOnly(self):
        # create an empty list of generated cypher statements
        lineList = []
        # generate drops
        for objectType in self.listTypes:
            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
                lineList.extend( ["// Generated {} Create Statements \n".format(objectType)])
                for x in self.schemaTab.schemaModel.instanceList(objectType):
                    # this logic is needed to resolve neo4j error, when retrieving nodekeys if it only has one property the retrieved nodekey text has a syntax error
                    if (not "ASSERT (" in x and objectType == "Node Key"):
                        x = x.replace("ASSERT ", "ASSERT (")
                        x = x.replace(" IS", ") IS")
                    lineList.extend( ["Drop {} ;\n".format(x) ])                        
        
#        for objectType in self.listTypes:
#            if objectType in ["Node Key","Node Property Unique","Node Property Exists","Relationship Property Exists","Index"]:
#                lineList.extend( ["// Generated {} Drop Statements \n".format(objectType)])
#                lineList.extend( ["Drop {} ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)])
        
        
        for objectType in self.listTypes:
            if objectType in ["User"]:
                lineList.extend( ["// Generated {} Delete Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.deleteUser('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)   if x != "neo4j"])
        for objectType in self.listTypes:
            if objectType in ["Role"]:
                lineList.extend( ["// Generated {} Delete Statements \n".format(objectType)])
                lineList.extend( ["CALL dbms.security.deleteRole('{}') ;\n".format(x) for x in self.schemaTab.schemaModel.instanceList(objectType)  if not x in ["editor", "reader", "architect", "admin", "publisher"]])

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
