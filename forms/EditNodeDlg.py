# -*- coding: utf-8 -*-

"""
Module implementing EditNodeDlg.
"""
import logging

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication

from .Ui_EditNodeDlg import Ui_EditNodeDlg
from core.helper import Helper
from forms.EditNodeWidget import EditNodeWidget

# labels in node template
LABEL, REQUIRED, NODEKEY = range(3)
# node template property list
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS, UNIQUE, PROPNODEKEY = range(7)
# ENUM for property grid
PROPERTY, DATATYPE, VALUE = range(3)


class EditNodeDlg(QDialog, Ui_EditNodeDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, ):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(EditNodeDlg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.templateDict = self.parent.templateDict
        self.neoCon = self.parent.neoCon
        self.helper = Helper()
        self.node = None
        self.neoID = None
        # add edit node widet
        self.editNode = EditNodeWidget(self, templateDict=self.templateDict )
        self.editNodeLayout = QVBoxLayout(self.frameBody)
        self.editNodeLayout.setObjectName("editNodeLayout")
        self.editNodeLayout.addWidget(self.editNode)    
        # finish UI setup
        self.txtTitle.setText("Add New Node")
        
        self.lastAddNeoID = None

    def logMsg(self, msg):
        # add message to the log
        if logging:
            logging.info(msg)        
    
    @pyqtSlot()
    def on_btnAddNew_clicked(self):
        """
        User clicks the add new button so add a new node
        """
        # validate the data entry
        if self.validate():
            # add the node to the graph
            QApplication.setOverrideCursor(Qt.WaitCursor)
            try:
                #  add or update this node in the db'            
                rc, msg = self.createBlankNode()
                if rc is True:
                    # now update the node in the neo4j instance
                    updateCypher = self.helper.genUpdateCypher(neoID = self.neoID, nodeInstanceDict = self.getObjectDict(),  node = self.node)
#                    print(updateCypher)
                    rc, msg = self.neoCon.runCypherAuto(updateCypher)
                    QApplication.restoreOverrideCursor() 
                    if not rc == True:
                        self.helper.displayErrMsg("Create New Node", msg)
                    else:
                        self.helper.displayErrMsg("Create New Node", "New Node Created.")
                else:
                    self.helper.displayErrMsg("Create New Node", msg)
            except BaseException as e:
                self.helper.displayErrMsg("Create New Node","Error creating Node - {}".format(repr(e)))
            finally:
                QApplication.restoreOverrideCursor() 
            
    def getObjectDict(self, ):
        '''
        This function returns a dictionary with all the data entered on the UI
        '''
        objectDict = {}
        objectDict["neoID"] = self.neoID
        # save the labels
        labelList = []
        model = self.editNode.gridLabels.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            # only include labels that have been checked
#            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            
            nodeLbl = [model.item(row,LABEL).data(Qt.EditRole)]
            labelList.append(nodeLbl)
        #save the attributes
        propList = []
        model = self.editNode.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),model.item(row,VALUE).data(Qt.EditRole)]
            # only include properties that aren't null
            propList.append(nodeProp)
        objectDict["labels"] = labelList
        objectDict["properties"] = propList
        
        return objectDict
        
    def createBlankNode(self, ):
        # create a new blank node
        cypher = "create (n) return id(n), n"
        rc, msg = self.neoCon.runCypherExplicit(cypher)
        if rc is True:
            firstRec = self.neoCon.resultSet[0]
            if not firstRec is None:
                self.neoID =  firstRec["id(n)"]
                self.node = firstRec["n"]
            else:
                self.logMsg(msg)
            
        return rc, msg

    def validate(self, ):
        # make sure all properties have valid datatypes
#        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # make sure all required properties have a value
        if not self.templateDict is None:
            model = self.editNode.gridProps.model()
            numrows = model.rowCount()
            for row in range(0,numrows):
                nodeProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),model.item(row,VALUE).data(Qt.EditRole)]
                if nodeProp[VALUE] == "Null":
                    #  the value is null so see if it is required
                    for templateProp in self.templateDict["properties"]:
                        if templateProp[PROPERTY] ==  nodeProp[PROPERTY]:
                            if templateProp[PROPREQ] == Qt.Checked:
                                # this property must have a value
                                self.helper.displayErrMsg("Validate", "The property {} is required. Please enter a value.".format(nodeProp[PROPERTY]))
                                return False
        return True
        
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        User Clicks the close button so close the dialog
        """
        QDialog.accept(self)
