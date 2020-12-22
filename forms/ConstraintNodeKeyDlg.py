# -*- coding: utf-8 -*-

"""
Module implementing ConstraintNodeKeyDlg.  
    Author: John Singer

 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QApplication
from .Ui_ConstraintNodeKeyDlg import Ui_ConstraintNodeKeyDlg
from core.helper import Helper

class ConstraintNodeKeyDlg(QDialog, Ui_ConstraintNodeKeyDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ConstraintNodeKeyDlg, self).__init__(parent)
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
        if self.helper.NoTextValueError(self.lstProperty, "You must have at least one property in the list."):
            return False
        
        return True
        
    def apply(self, ):
        """
        Generate and run the create constraint statement
        """
        propList = ["p." + str(self.lstProperty.item(i).text()) for i in range(self.lstProperty.count())]
        propComma = ",".join(x for x in propList)
        label = self.cbLabel.currentText()
        self.cypherCommand = None
            
        '''
        CREATE CONSTRAINT ON (p:Person) ASSERT (p.firstname, p.surname) IS NODE KEY            
        '''
        self.cypherCommand = "CREATE CONSTRAINT ON (p:{}) ASSERT ({}) IS NODE KEY".format(label, str(propComma))
               
        if self.cypherCommand:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            rc, msg = self.schemaModel.createConstraint(self.cypherCommand)
            QApplication.restoreOverrideCursor()            
            self.helper.displayErrMsg("Create Node KeyConstraint", msg)
        else:
            self.helper.displayErrMsg("Create Node Key Constraint", "Error Generating Node Key Constraint Statement.")
            
                
        
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
        if len(self.lstProperty.findItems(self.cbProperty.currentText(), Qt.MatchFixedString)) == 0:
            self.lstProperty.addItem(self.cbProperty.currentText())
        else:
            self.helper.displayErrMsg("Create Node Key Constraint", "You can't use the same property twice.")
            
    
    @pyqtSlot()
    def on_pbRemoveList_clicked(self):
        """
        Remove the selected property from the list
        """
        self.lstProperty.takeItem(self.lstProperty.currentRow())
    
    @pyqtSlot()
    def on_btnMoveUp_clicked(self):
        """
        User clicks the Move Up button, move the selected property up on in the list
        """
        self.helper.moveListItemUp(self.lstProperty)
    
    @pyqtSlot()
    def on_btnMoveDown_clicked(self):
        """
        User clicks the Move Down button, move the selected property down on in the list
        """
        self.helper.moveListItemDown(self.lstProperty)        
