# -*- coding: utf-8 -*-

"""
Module implementing EditRelDlg.
"""
import logging

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication

from .Ui_EditRelDlg import Ui_EditRelDlg
from core.helper import Helper
from forms.EditRelWidget import EditRelWidget

# rel template property list
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS = range(5)
# ENUM for property grid
PROPERTY, DATATYPE, VALUE = range(3)

class EditRelDlg(QDialog, Ui_EditRelDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(EditRelDlg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.designModel = self.parent.designModel
        self.templateDict = self.parent.templateDict
        self.neoCon = self.parent.neoCon
        self.helper = Helper()
        self.rel = None
        self.neoID = None
        # add edit relationship widet
        self.editRel = EditRelWidget(self, templateDict=self.templateDict )
        self.editRelLayout = QVBoxLayout(self.frameBody)
        self.editRelLayout.setObjectName("editRelLayout")
        self.editRelLayout.addWidget(self.editRel)    
        # finish UI setup
        self.txtTitle.setText("Add New Relationship")
        
        self.lastAddNeoID = None
        
    def logMsg(self, msg):
        # add message to the log
        if logging:
            logging.info(msg)     
    
        
    @pyqtSlot()
    def on_btnAddNew_clicked(self):
        """
        User clicks the add new button so add a new relationship
        """
        # validate the data entry
        if self.validate():
            QApplication.setOverrideCursor(Qt.WaitCursor)
            try:
                #  create a new relationship
                selectedFromNode = self.editRel.cmbFromNode.currentText()
                endIndex = selectedFromNode.find("]")
                fromNeoID = selectedFromNode[1:endIndex]
                selectedToNode = self.editRel.cmbToNode.currentText()
                endIndex = selectedToNode.find("]")
                toNeoID = selectedToNode[1:endIndex]
                createCypher =  self.helper.genCreateRelCypher(relInstanceDict = self.getObjectDict(), fromNeoID = fromNeoID, toNeoID=toNeoID)
                rc, msg = self.neoCon.runCypherExplicit(createCypher)
                QApplication.restoreOverrideCursor() 
                if not rc == True:
                    self.helper.displayErrMsg("Create New Relationship", msg)
                else:
                    firstRec = self.neoCon.resultSet[0]
                    if not firstRec is None:
                        self.neoID =  firstRec["id(r)"]
                        self.rel = firstRec["r"]
                    self.helper.displayErrMsg("Create New Relationship", "New Relationship Created.")
            except BaseException as e:
                self.helper.displayErrMsg("Create New Relationship","Error creating Relationship - {}".format(repr(e)))
            finally:
                QApplication.restoreOverrideCursor() 

    def getObjectDict(self, ):
        '''
        This function returns a dictionary with all the data entered on the UI
        '''
        objectDict = {}
        objectDict["neoID"] = self.neoID
        objectDict["relName"] = self.templateDict["relname"]   
        #save the attributes
        propList = []
        model = self.editRel.gridProps.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            relProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),model.item(row,VALUE).data(Qt.EditRole)]
            # only include properties that aren't null
            propList.append(relProp)
        objectDict["properties"] = propList
        
        return objectDict

    def validate(self, ):
        # make sure all properties have valid datatypes
#        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # make sure all required properties have a value
        if not self.templateDict is None:
            model = self.editRel.gridProps.model()
            numrows = model.rowCount()
            for row in range(0,numrows):
                relProp = [model.item(row,PROPERTY).data(Qt.EditRole), model.item(row,DATATYPE).data(Qt.EditRole),model.item(row,VALUE).data(Qt.EditRole)]
                if relProp[VALUE] == "Null":
                    #  the value is null so see if it is required
                    for templateProp in self.templateDict["properties"]:
                        if templateProp[PROPERTY] ==  relProp[PROPERTY]:
                            if templateProp[PROPREQ] == Qt.Checked:
                                # this property must have a value
                                self.helper.displayErrMsg("Validate", "The property {} is required. Please enter a value.".format(relProp[PROPERTY]))
                                return False
        return True
    
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        User Clicks the close button so close the dialog
        """
        QDialog.accept(self)
