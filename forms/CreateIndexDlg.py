# -*- coding: utf-8 -*-

"""
Module implementing CreateIndexDlg.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QApplication

from .Ui_CreateIndexDlg import Ui_CreateIndexDlg
from core.helper import Helper

class CreateIndexDlg(QDialog, Ui_CreateIndexDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(CreateIndexDlg, self).__init__(parent)
        self.helper = Helper()
        self.setupUi(self)
        self.parent = parent
        self.schemaModel = self.parent.schemaModel
        self.initUi()
        
    def initUi(self, ):
        aList = self.schemaModel.instanceList("Label")
        self.cbLabel.addItem("")
        aSortedList = sorted(aList)
        for indexName in aSortedList:
            self.cbLabel.addItem(indexName)
        
        aList = sorted(self.schemaModel.instanceList("Property"))
        self.cbProperty.addItem("")
        for indexName in aList:
            self.cbProperty.addItem(indexName)
        return

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
        Generate the create index statement
        """
        propList = [str(self.lstProperty.item(i).text()) for i in range(self.lstProperty.count())]
        propComma = ",".join(x for x in propList) 
        self.cypherCommand = "CREATE INDEX ON :{}({})".format(self.cbLabel.currentText(), str(propComma))
        if self.cypherCommand:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            rc, msg = self.schemaModel.createIndex(self.cypherCommand)
            QApplication.restoreOverrideCursor()            
            self.helper.displayErrMsg("Create Index", msg)
        else:
            self.helper.displayErrMsg("Create Index", "Error Generating Index Statement.")

    
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
    def on_btnMoveUp_clicked(self):
        """
        User clicks the Move Up button, move the selected property up on in the list
        """
        self.helper.moveListItemUp(self.lstProperty)
    
    @pyqtSlot()
    def on_btnMoveDown_clicked(self):
        """
        User clicks the Move Down button, move the selected property up on in the list
        """
        self.helper.moveListItemDown(self.lstProperty)        
