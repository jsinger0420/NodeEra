# -*- coding: utf-8 -*-

"""
Module implementing ConstraintNodePropExistsDlg.  
    Author: John Singer

 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QApplication
from .Ui_ConstraintNodePropExistsDlg import Ui_ConstraintNodePropExistsDlg
from core.helper import Helper

class ConstraintNodePropExistsDlg(QDialog, Ui_ConstraintNodePropExistsDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ConstraintNodePropExistsDlg, self).__init__(parent)
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
        CREATE CONSTRAINT ON (p:Person) ASSERT exists(p.name)            
        '''
        self.cypherCommand = "CREATE CONSTRAINT ON (p:{}) ASSERT exists(p.{})".format(label, prop)

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
    
