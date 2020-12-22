# -*- coding: utf-8 -*-

"""
Module implementing EditUserDlg.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QApplication

from core.helper import Helper

from .Ui_EditUserDlg import Ui_EditUserDlg


class EditUserDlg(QDialog, Ui_EditUserDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, mode=None, userName=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(EditUserDlg, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.userName=userName
        self.mode=mode
        self.helper = Helper()
            
        self.initUI()

    def initUI(self, ):
        self.txtUserName.setText(self.userName)
        self.txtUserName.setReadOnly(True)
        
        # get the user status and change password flag
        self.resetFlags()
            
        # populate the role combo box
        self.cbRoleName.addItems(self.parent.schemaModel.instanceList("Role"))
        # populate users roles in the list box
        userRoles = self.parent.schemaModel.getUserRoles(userName=self.userName)
        for userRole in userRoles:
            self.lstUserRoles.addItem(userRole)
        
    def resetFlags(self, ):
        # get the user status and change password flag
        self.userFlags = self.parent.schemaModel.getUserFlags(userName=self.userName)
        if "is_suspended" in self.userFlags:
            self.pbActivate.setChecked(False)
            self.pbSuspend.setChecked(True)
        else:
            self.pbSuspend.setChecked(False)
            self.pbActivate.setChecked(True)
        if "password_change_required" in self.userFlags:
            self.pbChangeOnLogin.setChecked(True)
        else:
            self.pbChangeOnLogin.setChecked(False)            
        # the password change required flag can't be changed, the radio button just indicates how it is currently set
        self.pbChangeOnLogin.setEnabled(False)
        
    @pyqtSlot()
    def on_btnAddRole_clicked(self):
        """
        Give the user a role from the combobox of roles
        """
        addRole = self.cbRoleName.currentText()
        currentRoles = [str(self.lstUserRoles.item(i).text()) for i in range(self.lstUserRoles.count())]
        if addRole in currentRoles:
            # error, the user already has the selected role
            self.helper.displayErrMsg("Edit User", "The user already has this role.")
        else:
            # give the user the role
            QApplication.setOverrideCursor(Qt.WaitCursor)
            rc, msg = self.parent.schemaModel.addUserRole(userName=self.userName, role=addRole)
            if rc:
                self.lstUserRoles.addItem(addRole)
            else:
                self.helper.displayErrMsg("Add Role to User Error", msg)
            QApplication.restoreOverrideCursor()                
            
    
    @pyqtSlot()
    def on_btnRemoveRoles_clicked(self):
        """
        Remove the selected role from the user
        """
        removeRole = self.lstUserRoles.currentItem().text()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        rc, msg = self.parent.schemaModel.removeUserRole(userName=self.userName, role=removeRole)
        if rc:
            self.lstUserRoles.takeItem(self.lstUserRoles.currentRow())
        else:
            self.helper.displayErrMsg("Remove Role from User Error", msg)
        QApplication.restoreOverrideCursor() 
        
        
    
    @pyqtSlot()
    def on_dlgBtnBox_accepted(self):
        """
        User clicks Close
        """
        QDialog.accept(self)
        
    @pyqtSlot()
    def on_dlgBtnBox_rejected(self):
        """
        User clicks something that generates the reject
        """
        QDialog.reject(self)
    
    @pyqtSlot()
    def on_pbActivate_clicked(self):
        """
        Activate a suspended user
        """
        if not "is_suspended" in self.userFlags:
            # nothing to do
            return
            
        QApplication.setOverrideCursor(Qt.WaitCursor)
        rc, msg = self.parent.schemaModel.activateUser(userName=self.userName)
        if rc:
            self.resetFlags()
        else:
            self.helper.displayErrMsg("Activate User Error", msg)
            self.resetFlags()
            
        QApplication.restoreOverrideCursor() 
    
    @pyqtSlot()
    def on_pbSuspend_clicked(self):
        """
        Suspend an active user
        """
        if "is_suspended" in self.userFlags:
            # nothing to do
            return
            
        QApplication.setOverrideCursor(Qt.WaitCursor)
        rc, msg = self.parent.schemaModel.suspendUser(userName=self.userName)
        if rc:
            self.resetFlags()
        else:
            self.helper.displayErrMsg("Suspend User Error", msg)
            self.resetFlags()
            
        QApplication.restoreOverrideCursor() 
    
        
    @pyqtSlot()
    def on_btnChangePassword_clicked(self):
        """
        User requests to change the password.
        """
        if not self.helper.NoTextValueError(self.txtNewPassword.text(), "You must supply a new password"):
            QApplication.setOverrideCursor(Qt.WaitCursor)
            rc, msg = self.parent.schemaModel.changePassword(userName=self.userName, pw=self.txtNewPassword.text(), forceChange=self.pbChangeOnLogin.isChecked())
            if rc:
                self.helper.displayErrMsg("Change Password", "The password has been changed")
            else:
                self.helper.displayErrMsg("Change Password Error", msg)
            self.resetFlags()    
            QApplication.restoreOverrideCursor()         
    
