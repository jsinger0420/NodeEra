# -*- coding: utf-8 -*-

"""
Module implementing NeoConPropertyBox.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox
from core.helper import Helper
from .Ui_NeoConPropertyBox import Ui_NeoConPropertyBox


class NeoConPropertyBox(QDialog, Ui_NeoConPropertyBox):
    """
    Display the property editor for a neo4j connection definition
    """
    def __init__(self, parent=None, mode=None, objectDict=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(NeoConPropertyBox, self).__init__(parent)
        self.parent = parent
        self.mode = mode
        self.objectDict = objectDict
        self.helper = Helper()
        self.setupUi(self)
        self.chkSecureCon.setTristate(False)
        self.populateUIfromObject()
        
    def populateUIfromObject(self, ):
        
        # window title
        self.setWindowTitle("Neo4j Connection: {}".format(self.objectDict["slot"]))
        
        if self.objectDict["usesecure"] == "True":
            self.chkSecureCon.setCheckState(Qt.Checked)
        else:
            self.chkSecureCon.setCheckState(Qt.Unchecked)
            
        if self.objectDict["prompt"] == "True":
            self.chkPromptForPW.setCheckState(Qt.Checked)
            self.editPassWord.setReadOnly(True)
            self.btnShow.setEnabled(False)            
        else:
            self.chkPromptForPW.setCheckState(Qt.Unchecked)      
            
        self.conType = self.objectDict.get("conType", "bolt")
        index = self.cboScheme.findText(self.conType)
        if index >= 0:
            self.cboScheme.setCurrentIndex(index)
        
        self.editHostName.insert(self.objectDict["host"])
        self.editPort.insert(self.objectDict.get("port", ""))
        self.editUserid.insert(self.objectDict["userid"])
        pw = self.objectDict["password"]
        if len(pw) > 0:
            displayPw = self.helper.getText(pw)
        else:
            displayPw = ""
        # only display the password if the prompt checkbox is unchecked.
        if self.objectDict["prompt"] == "False":        
            self.editPassWord.insert(displayPw)   
        
    @pyqtSlot(str)
    def on_cboScheme_currentIndexChanged(self, p0):
        """
        User selects the connection type from the dropdown.
        Change the secure connection checkbox as appropriate
        
        @param p0 DESCRIPTION
        @type str
        """
        pass
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        User selects OK button, edit data, then save/close the dialog box if ok.
        """
        if self.validate():
            self.apply()
            QDialog.accept(self)
        else:
            return
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        User selects Cancel button, close dialog box without saving
        """
        QDialog.reject(self)

    def validate(self):
        '''
        Validate the user has entered correct data.
        '''
        # edit host name field
        if self.helper.NoTextValueError(self.editHostName.text(), "Must supply a host name."):
            return False
        # edit port field
        if self.helper.NoTextValueError(self.editPort.text(), "Must supply a port number."):
            return False        
        # userid field
        if self.helper.NoTextValueError(self.editUserid.text(), "Must supply a user id."):
            return False        
        
        
        return True
        
    def apply(self, ):
        self.objectDict["conType"] = self.cboScheme.currentText()
        self.objectDict["port"] = self.editPort.text()
        self.objectDict["host"] = self.editHostName.text()
        self.objectDict["userid"] = self.editUserid.text()
        pw = self.editPassWord.text()
        if len(pw) > 0:
            savePw = self.helper.putText(pw)
        else:
            savePw = ""
        self.objectDict["password"] = savePw
        if self.chkSecureCon.isChecked():
            self.objectDict["usesecure"] = "True"
        else:
            self.objectDict["usesecure"] = "False"
        if self.chkPromptForPW.isChecked():
            self.objectDict["prompt"] = "True"
        else:
            self.objectDict["prompt"] = "False"

        return
    
    @pyqtSlot()
    def on_btnShow_clicked(self):
        """
        User clicked the Show button so show the password in clear text
        """
        if self.btnShow.text() == "Show":
            self.btnShow.setText("Hide")
            self.editPassWord.setEchoMode(QLineEdit.Normal)
        else:
            self.btnShow.setText("Show")
            self.editPassWord.setEchoMode(QLineEdit.Password)            
        return
    
    @pyqtSlot(bool)
    def on_chkPromptForPW_clicked(self, checked):
        """
        User selects to prompt for password instead of saving the password.
        
        @param checked DESCRIPTION
        @type bool
        """
        # user sets prompt for password to true
        if checked:
            # warn user the currently set password will be cleared
            if len(self.editPassWord.text()) > 0:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("Warning: This will clear the password from the screen. Do you want to continue?")
                msgBox.setWindowTitle("CONFIRM CLEAR PASSWORD")
                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                result = msgBox.exec_()
                if result == QMessageBox.No:
                    # clear the checkbox
                    self.chkPromptForPW.setChecked(Qt.Unchecked)
                    return   
            # return password text edit to normal state if it is currently showing
            if self.btnShow.text() == "Hide":
                self.btnShow.setText("Show")
            self.editPassWord.setEchoMode(QLineEdit.Password)
            # clear the text edit
            self.editPassWord.setText("")
            # disable password entry
            self.editPassWord.setReadOnly(True)
            self.btnShow.setEnabled(False)
            # clear the password from settings
            
        else:
            # enable password entry
            self.editPassWord.setReadOnly(False)
            self.btnShow.setEnabled(True)
            self.editPassWord.setEchoMode(QLineEdit.Password)
            if self.btnShow.text() == "Hide":
                self.btnShow.setText("Show")
