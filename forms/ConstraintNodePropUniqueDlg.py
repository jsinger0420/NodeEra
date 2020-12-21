# -*- coding: utf-8 -*-

"""
Module implementing ConstraintNodePropUniqueDlg.  
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QApplication
from .Ui_ConstraintNodePropUniqueDlg import Ui_ConstraintNodePropUniqueDlg
from core.helper import Helper

class ConstraintNodePropUniqueDlg(QDialog, Ui_ConstraintNodePropUniqueDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ConstraintNodePropUniqueDlg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.schemaModel = self.parent.schemaModel
        self.helper = Helper()
        self.initUi()
        
    def initUi(self, ):
        aList = sorted(self.schemaModel.instanceList("Label"))
        self.cbLabel.addItem("")
        for indexName in aList:
            self.cbLabel.addItem(indexName)
        
        aList = sorted(self.schemaModel.instanceList("Property"))
        self.cbProperty.addItem("")
        for indexName in aList:
            self.cbProperty.addItem(indexName)
        

    def validate(self, ):

        # must enter or select a label
        if self.helper.NoTextValueError(self.cbLabel.currentText(), "You must enter or select a Label"):
            return False
        # must add at least one property to the list
        if self.helper.NoTextValueError(self.cbProperty.currentText(), "You must enter or select a Property"):
            return False
        
        return True
        
    def apply(self, ):
        """
        Generate and run the create constraint statement
        """
        prop = self.cbProperty.currentText()
        label = self.cbLabel.currentText()
        self.cypherCommand = None
        '''
        CREATE CONSTRAINT ON (p:Person) ASSERT p.name IS UNIQUE
        '''
        self.cypherCommand = "CREATE CONSTRAINT ON (p:{}) ASSERT p.{} IS UNIQUE".format(label, prop)
        
        if self.cypherCommand:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            rc, msg = self.schemaModel.createConstraint(self.cypherCommand)
            QApplication.restoreOverrideCursor()            
            self.helper.displayErrMsg("Create Constraint", msg)
        else:
            self.helper.displayErrMsg("Create Constraint", "Error Generating Constraint Statement.")
            
                
        
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        if self.validate():
            self.apply()
            QDialog.accept(self)
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        QDialog.reject(self)
    
    
