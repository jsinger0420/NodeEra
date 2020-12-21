# -*- coding: utf-8 -*-

"""
Module implementing dlgPageSetup.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from core.helper import PageSizes, PageSetup
from forms.Ui_PageSetupDlg import Ui_dlgPageSetup


class dlgPageSetup(QDialog, Ui_dlgPageSetup):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, objectDict=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(dlgPageSetup, self).__init__(parent)
        self.setupUi(self)
        self.objectDict = objectDict
        self.pageSetup = None
        self.initUI()

    def initUI(self, ):
        # page settings
        self.pageSizes = PageSizes()
        self.pageSizes.loadDropDown(self.cmbPageSize)
        self.pageSetup = PageSetup(objectDict=self.objectDict)        
        index = self.cmbPageSize.findText(self.pageSetup.objectDict["pageSize"])
        if index >= 0:
            self.cmbPageSize.setCurrentIndex(index)
        if self.pageSetup.objectDict["pageOrientation"] == "Portrait":
            self.rbPortrait.setChecked(True)
            self.rbLandscape.setChecked(False)
        else:
            self.rbLandscape.setChecked(True)
            self.rbPortrait.setChecked(False)
        self.setPageHeightWidth()            
        self.spinRows.setValue(self.pageSetup.objectDict["pageRows"])  
        self.spinColumns.setValue(self.pageSetup.objectDict["pageCols"])  

####################################################################################
# PAGE SETTING METHODS
####################################################################################
    def setPageHeightWidth(self, ):
        # this sets the page height width based on page type and orientation
        height, width = self.pageSetup.getHeightWidth()
        self.txtHeight.setText(str(height))
        self.txtWidth.setText(str(width))
        
    @pyqtSlot()
    def on_rbLandscape_clicked(self):
        """
        Slot documentation goes here.
        """
#        print("landscape")
        self.pageSetup.objectDict["pageOrientation"] = "Landscape"
        self.setPageHeightWidth()
        
    @pyqtSlot()
    def on_rbPortrait_clicked(self):
        """
        Slot documentation goes here.
        """
#        print("portrait")
        self.pageSetup.objectDict["pageOrientation"] = "Portrait"
        self.setPageHeightWidth() 
        
    @pyqtSlot(int)
    def on_cmbPageSize_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
#        print("dropdown changed {}".format(self.cmbPageSize.currentText()))
        if self.pageSetup is None:
            return
        newPageSize = str(self.cmbPageSize.currentText())
        self.pageSetup.objectDict["pageSize"] = self.pageSizes.pageTypes[newPageSize].name
        self.pageSetup.objectDict["pageHeight"] = self.pageSizes.pageTypes[newPageSize].height
        self.pageSetup.objectDict["pageWidth"] = self.pageSizes.pageTypes[newPageSize].width
        self.setPageHeightWidth()
    
    @pyqtSlot(int)
    def on_spinRows_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.pageSetup.objectDict["pageRows"] = self.spinRows.value()
    
    @pyqtSlot(int)
    def on_spinColumns_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.pageSetup.objectDict["pageCols"] = self.spinColumns.value()      
        
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

        return True
        
    def apply(self, ):
        return
    
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
