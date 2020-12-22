# -*- coding: utf-8 -*-

"""
Module implementing DropObjectDlg.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
import logging

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QApplication

from core.helper import Helper
from .Ui_DropObjectDlg import Ui_DropObjectDlg


class DropObjectDlg(QDialog, Ui_DropObjectDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, objectType=None, objectName=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DropObjectDlg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.objectType = objectType
        self.objectName = objectName
        self.schemaModel = self.parent.schemaModel
        self.helper = Helper()
        self.initUi()  
        
    def initUi(self, ):
        self.lblTitle.setText("Drop {}".format(self.objectType))
        self.editObject.setText(self.objectName)
        return
        
    def logMsg(self, msg):
        '''
        If logging is active, then log the message
        '''
        if logging:
            logging.info(msg)      
            
    def validate(self, ):

        return True
        
    def apply(self, ):
        """
        Generate the drop statement
        """
        if self.objectType == "User":
            self.cypherCommand = "CALL dbms.security.deleteUser('{}')".format(self.objectName)
        elif self.objectType == "Role":
            self.cypherCommand = "CALL dbms.security.deleteRole('{}')".format(self.objectName)
        else:
            if (not "ASSERT (" in self.objectName and self.objectType == "Node Key"):
                self.objectName = self.objectName.replace("ASSERT ", "ASSERT (")
                self.objectName = self.objectName.replace(" IS", ") IS")
                self.cypherCommand = "Drop {}".format(self.objectName)
            else:
                self.cypherCommand = "Drop {}".format(self.objectName)
        
        if self.cypherCommand:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            rc, msg = self.schemaModel.dropObject(self.cypherCommand)
            QApplication.restoreOverrideCursor()            
            self.helper.displayErrMsg("Drop Schema Object", msg)
            self.logMsg("Drop Schema Object - {}".format(msg))
        else:
            self.helper.displayErrMsg("Drop Schema Object", "Error Generating Drop Schema Object Statement.")
            self.logMsg("Error Generating Drop Schema Object Statement.")
        
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
