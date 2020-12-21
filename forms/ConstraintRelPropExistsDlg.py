# -*- coding: utf-8 -*-

"""
Module implementing ConstraintRelPropExistsDlg.  
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QApplication
from .Ui_ConstraintRelPropExistsDlg import Ui_ConstraintRelPropExistsDlg
from core.helper import Helper

class ConstraintRelPropExistsDlg(QDialog, Ui_ConstraintRelPropExistsDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ConstraintRelPropExistsDlg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.schemaModel = self.parent.schemaModel
        self.helper = Helper()
        self.initUi()
        
    def initUi(self, ):
        aList = sorted(self.schemaModel.instanceList("Property"))
        self.cbProperty.addItem("")
        for indexName in aList:
            self.cbProperty.addItem(indexName)
        
        aList = sorted(self.schemaModel.instanceList("Relationship"))
        self.cbRelationships.addItem("")
        for indexName in aList:
            self.cbRelationships.addItem(indexName)
        return

    def validate(self, ):

        # must enter or select a relationship
        if self.helper.NoTextValueError(self.cbRelationships.currentText(), "You must enter or select a Relationship"):
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
        relationship  = self.cbRelationships.currentText()
        self.cypherCommand = None
            
        '''
        CREATE CONSTRAINT ON ()-[r:RelID]-() ASSERT exists(r.propname)       
        '''
        self.cypherCommand = "CREATE CONSTRAINT ON ()-[p:{}]-() ASSERT exists(p.{})".format(relationship, prop)
        
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
    
    @pyqtSlot()
    def on_pbAddToList_clicked(self):
        """
        Get the property name in the combo box and add it to the list
        """
        self.lstProperty.addItem(self.cbProperty.currentText())
    
    @pyqtSlot()
    def on_pbRemoveList_clicked(self):
        """
        Remove the selected property from the list
        """
        self.lstProperty.takeItem(self.lstProperty.currentRow())
    
    @pyqtSlot()
    def on_rbUnique_clicked(self):
        """
        Slot documentation goes here.
        """
        self.cbLabel.setEnabled(True)
        self.cbProperty.setEnabled(True)
        self.cbRelationships.setEnabled(False)
        self.pbAddToList.setEnabled(True)
        self.pbRemoveList.setEnabled(True)
    
    @pyqtSlot()
    def on_rbNodePropExists_clicked(self):
        """
        Slot documentation goes here.
        """
        self.cbLabel.setEnabled(True)
        self.cbProperty.setEnabled(True)
        self.cbRelationships.setEnabled(False)
        self.pbAddToList.setEnabled(True)
        self.pbRemoveList.setEnabled(True)
    
    @pyqtSlot()
    def on_rbNodeKey_clicked(self):
        """
        Slot documentation goes here.
        """
        self.cbLabel.setEnabled(True)
        self.cbProperty.setEnabled(True)
        self.cbRelationships.setEnabled(False)
        self.pbAddToList.setEnabled(True)
        self.pbRemoveList.setEnabled(True)
    
    @pyqtSlot()
    def on_rbRelPropExists_clicked(self):
        """
        Slot documentation goes here.
        """
        self.cbLabel.setEnabled(False)
        self.cbProperty.setEnabled(True)
        self.cbRelationships.setEnabled(True)
        self.pbAddToList.setEnabled(True)
        self.pbRemoveList.setEnabled(True)
