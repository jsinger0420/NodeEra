# -*- coding: utf-8 -*-

"""
Module implementing ChangeUserPW.

 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
import logging

from PyQt5.QtCore import pyqtSlot, Qt, QSettings
from PyQt5.QtWidgets import QDialog, QLineEdit, QApplication

from .Ui_ChangeUserPW import Ui_ChangeUserPW
from core.helper import Helper
#from core.neocon import NeoCon
from core.NeoDriver import NeoDriver

class ChangeUserPW(QDialog, Ui_ChangeUserPW):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ChangeUserPW, self).__init__(parent)
        self.setupUi(self)
        self.helper = Helper()
        self.settings = QSettings()
        self.parent = parent
        self.editPW.setEchoMode(QLineEdit.Password)
        self.editNewPW.setEchoMode(QLineEdit.Password)
        self.editRepeatPW.setEchoMode(QLineEdit.Password)
        
    def logMessage(self, msg):
        if logging:
            logging.info(msg)                    
            
    @pyqtSlot()
    def on_btnCurrentShow_clicked(self):
        """
        User clicks the show button for the current password
        """
        if self.btnCurrentShow.text() == "Show":
            self.btnCurrentShow.setText("Hide")
            self.editPW.setEchoMode(QLineEdit.Normal)
        else:
            self.btnCurrentShow.setText("Show")
            self.editPW.setEchoMode(QLineEdit.Password)            
    
    @pyqtSlot()
    def on_btnNewShow_clicked(self):
        """
        User clicks the show button for the new passwords
        """
        if self.btnNewShow.text() == "Show":
            self.btnNewShow.setText("Hide")
            self.editNewPW.setEchoMode(QLineEdit.Normal)
            self.editRepeatPW.setEchoMode(QLineEdit.Normal)
        else:
            self.btnNewShow.setText("Show")
            self.editNewPW.setEchoMode(QLineEdit.Password)      
            self.editRepeatPW.setEchoMode(QLineEdit.Password)      
    
    @pyqtSlot()
    def on_btnReset_clicked(self):
        """
        User clicks the reset password button so do it
        """
        if self.validate():
            self.resetPassword()

    def validate(self, ):
        if self.helper.NoTextValueError(self.editUserID.text(), "You must enter a user ID to login with."):
            self.editUserID.setFocus()
            return False        
        if self.helper.NoTextValueError(self.editPW.text(), "You must enter a password to login with."):
            self.editPW.setFocus()
            return False        
        if self.helper.NoTextValueError(self.editNewPW.text(), "You must enter a new password."):
            self.editNewPW.setFocus()
            return False        
        if self.helper.NoTextValueError(self.editRepeatPW.text(), "You must repeat the new password."):
            self.editRepeatPW.setFocus()
            return False      
        if self.editNewPW.text() != self.editRepeatPW.text():
            self.helper.displayErrMsg("Reset Password", "The new password does not match the repeat password.")
            self.editNewPW.setFocus()
            return False    
        
        return True

    def resetPassword(self):
        '''login to Neo4j and reset the password
        '''
        # get the currently selected schema tab's neocon name
        newConName = self.parent.pageItem.neoConName
        # get the neocon dictionary from settings
        newConDict = self.settings.value("NeoCon/connection/{}".format(newConName))
        newConDict["userid"]=self.editUserID.text()
        savePW = self.helper.putText(self.editPW.text())
        newConDict["password"]=savePW
        # create a new neoCon using the userid/password the person entered on this form
        self.newNeoCon = NeoDriver(name=newConName,  neoDict = newConDict)
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        rc, msg = self.changePassword(userName=self.editUserID.text(), pw=self.editNewPW.text(), forceChange=False)
        if rc:
            self.helper.displayErrMsg("Change Password", msg)
        else:
            self.helper.displayErrMsg("Change Password Error", msg)
        QApplication.restoreOverrideCursor()         

    def changePassword(self, userName=None, pw=None, forceChange=None):
        try:
#            cypherCmd = "CALL dbms.security.changeUserPassword('{}','{}',{})".format(userName, pw, str(forceChange))
            cypherCmd = "CALL dbms.changePassword('{}')".format(pw)
            self.logMessage("Attempting: {}".format(cypherCmd))
            #run the query
            rc1, msg1 = self.newNeoCon.runCypherAuto(cypherCmd)
            if rc1:
                msg = "Password Changed."       
            else:
                msg = "Change Password Error {}".format(msg1)
        except BaseException as e:
            msg = "{} - Change Password Error.".format(repr(e))
        finally: 
            self.logMessage(msg) 
            return rc1, msg                          
        
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        User clicks the Close button so exit the dialog
        """
        QDialog.accept(self)
