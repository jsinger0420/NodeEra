# -*- coding: utf-8 -*-

"""
Module implementing CSVWriterWidget.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QFileDialog

from .Ui_CSVWriterWidget import Ui_Form


class CSVWriterWidget(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(CSVWriterWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        
        # init selection fields, these are typical windows excel settings
        self.chkWriteHeader.setCheckState(Qt.Checked)
        self.cmbQuoteChar.setEditable(False)
        self.cmbQuoteChar.setCurrentIndex(2)        
        self.cmbDelimiter.setEditable(False)
        self.cmbDelimiter.setCurrentIndex(0)
        self.cmbUseQuotes.setEditable(False)
        self.cmbUseQuotes.setCurrentIndex(1)
        self.cmbDoubleQuote.setEditable(False)
        self.cmbDoubleQuote.setCurrentIndex(0)
        self.cmbEscapeCharacter.setEditable(False)
        self.cmbEscapeCharacter.setCurrentIndex(1)
        self.cmbLineTerminator.setEditable(False)
        self.cmbLineTerminator.setCurrentIndex(0)
        
    @pyqtSlot()
    def on_btnSaveCSVFile_clicked(self):
        """
        select the file name to save
        """
        # get filename to save as 
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setDefaultSuffix("csv")
        dlg.setNameFilters(["Data Export File (*.csv)","all files (*.*)"])
        dlg.setDirectory(self.parent.settings.value("Default/ProjPath"))
        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            try:
                if fileNames:
                    self.fileName = fileNames[0]
                    self.txtCSVFileName.setText(self.fileName)
            except BaseException as e:
                msg = "{} - {}".format("Select CSV file failed.", repr(e))
                self.helper.displayErrMsg("Export CSV Error",  msg)
    

    
    @pyqtSlot(int)
    def on_cmbDelimiter_currentIndexChanged(self, index):
        """
        if they selected custom allow them to edit the value in the combobox
        
        @param index DESCRIPTION
        @type int
        """
        if index == 4:
            self.cmbDelimiter.setEditable(True)
        else:
            self.cmbDelimiter.setEditable(False)
    
    @pyqtSlot(int)
    def on_cmbQuoteChar_currentIndexChanged(self, index):
        """
        if they selected custom allow them to edit the value in the combobox
        
        @param index DESCRIPTION
        @type int
        """
        if index == 3:
            self.cmbQuoteChar.setEditable(True)
        else:
            self.cmbQuoteChar.setEditable(False)
    
    @pyqtSlot(int)
    def on_cmbEscapeCharacter_currentIndexChanged(self, index):
        """
        if they selected custom allow them to edit the value in the combobox
        
        @param index DESCRIPTION
        @type int
        """
        if index == 4:
            self.cmbEscapeCharacter.setEditable(True)
        else:
            self.cmbEscapeCharacter.setEditable(False)
    
    @pyqtSlot(int)
    def on_cmbLineTerminator_currentIndexChanged(self, index):
        """
        if they selected custom allow them to edit the value in the combobox
        
        @param index DESCRIPTION
        @type int
        """
        if index == 3:
            self.cmbLineTerminator.setEditable(True)
        else:
            self.cmbLineTerminator.setEditable(False)
