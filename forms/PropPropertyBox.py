# -*- coding: utf-8 -*-

"""
Module implementing propPropertyBox.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from forms.Ui_PropPropertyBox import Ui_propPropertyBox
from core.helper import Helper
from core.Enums import DataType

class PropPropertyBox(QDialog, Ui_propPropertyBox):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, mode=None, objectDict=None, designModel=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(PropPropertyBox, self).__init__(parent)
        self.helper = Helper()
        self.setupUi(self)
        self.designModel = designModel
        self.modelData = self.designModel.modelData
        self.objectDict = objectDict
        self.mode = mode
        # load combo box
        self.loadDataTypeDropDown()
        #populate ui data from object
        self.populateUIfromObject()
            
        if self.mode == "NEW":
            # set focus to name
            pass
        else: 
            # disable name entry and set focus to description
            self.editName.setEnabled(False)
            self.editDescription.setFocus()
            
    def populateUIfromObject(self, ):
        # default combobox to first entry which is Unknown
        self.cmbDataType.setCurrentIndex(0) 
        if self.objectDict is not None:
            self.editName.insert(str(self.objectDict["name"]))
            self.editDescription.appendPlainText(self.objectDict["desc"])
            index = self.cmbDataType.findText(self.objectDict.get("dataType", "Unknown"))
            if index >= 0:
                self.cmbDataType.setCurrentIndex(index)       

            
    def loadDataTypeDropDown(self):
        '''
        load datatype dropdown
        '''
        dropdownList = []
        dataTypeList = dropdownList + [dataType.value for dataType in DataType]
        self.cmbDataType.addItems(dataTypeList)
            
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.validate():
            self.apply()
            QDialog.accept(self)
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        QDialog.reject(self)

    def validate(self):
        if self.objectDict is None:
            self.objectDict = {}
        name = self.editName.text()
        if self.helper.NoTextValueError(name, "Must enter a Name"):
            self.editName.setFocus()
            return False
        if self.mode == 'NEW':
            if self.helper.DupObjectError(designModel = self.designModel, objName=name, topLevel = "Property", txtMsg = "A Property named {} already exists".format(name)):
                self.editName.setFocus()
                return False
        # must have a data type
        if self.helper.NoTextValueError(self.cmbDataType.currentText(), "Must select a data type"):
            self.cmbDataType.setFocus()
            return False

        return True
        
    def apply(self, ):
        self.objectDict["name"] = self.editName.text()
        desc = self.editDescription.toPlainText()
        if desc is not None:
            self.objectDict["desc"] = desc
        if self.cmbDataType.currentIndex() > 0:
            self.objectDict["dataType"] = self.cmbDataType.currentText()
        else:
            self.objectDict["dataType"] = 'Unknown'
#        print(self.objectDict)
    
    @pyqtSlot(int)
    def on_cmbDataType_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        return
