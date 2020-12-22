# -*- coding: utf-8 -*-

"""
Module implementing DlgExportCSV.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
import csv
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout

from .Ui_ExportCSVFile import Ui_DlgExportCSV
from forms.CSVWriterWidget import CSVWriterWidget
from core.helper import Helper

class DlgExportCSV(QDialog, Ui_DlgExportCSV):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DlgExportCSV, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.settings = parent.parent.settings
        self.helper = Helper()

        # add the CSV File widget.  
        self.CSVWriterWidget = CSVWriterWidget(parent=self )

        self.CSVLayout = QVBoxLayout(self.frmCSVWidget)
        self.CSVLayout.setObjectName("CSVLayout")
        self.CSVLayout.addWidget(self.CSVWriterWidget)    
    

    def validate(self, ):
        # edit the csv parameters entered by the user for correctness
        if self.CSVWriterWidget.chkWriteHeader.checkState() == Qt.Checked:
            self.writeHeader = True
        else:
            self.writeHeader = False
        self.writeHeader = self.CSVWriterWidget.chkWriteHeader.checkState()
        self.fileName = self.CSVWriterWidget.txtCSVFileName.text()
        if self.helper.NoTextValueError(self.fileName, "Must enter a file name"):
            self.CSVWriterWidget.txtCSVFileName.setFocus()
            return False               
        self.delimiterChar = self.CSVWriterWidget.cmbDelimiter.currentText()
        if self.helper.textBadLengthError(self.delimiterChar, 1, 1, "Delimiter can only be one character"):
            self.CSVWriterWidget.cmbDelimiter.setFocus()
            return False     
        self.quoteChar = self.CSVWriterWidget.cmbQuoteChar.currentText()
        if self.quoteChar != "None":
            if self.helper.textBadLengthError(self.quoteChar, 1, 1, "Quote Character can only be one character"):
                self.CSVWriterWidget.cmbQuoteChar.setFocus()
                return False 
        else:
            self.quoteChar = ''
            
        if self.CSVWriterWidget.cmbUseQuotes.currentText() == "All":
            self.useQuote = csv.QUOTE_ALL
        if self.CSVWriterWidget.cmbUseQuotes.currentText() == "Minimal":
            self.useQuote = csv.QUOTE_MINIMAL
        if self.CSVWriterWidget.cmbUseQuotes.currentText() == "Non-Numeric":
            self.useQuote = csv.QUOTE_NONNUMERIC
        if self.CSVWriterWidget.cmbUseQuotes.currentText() == "None":
            self.useQuote = csv.QUOTE_NONE
            
        self.doubleQuote = self.CSVWriterWidget.cmbDoubleQuote.currentText()
        self.escapeChar = self.CSVWriterWidget.cmbEscapeCharacter.currentText()
        if self.escapeChar != "None":
            if self.helper.textBadLengthError(self.escapeChar, 1, 1, "Escape Character can only be one character"):
                self.CSVWriterWidget.cmbEscapeCharacter.setFocus()
                return False   
        else:
            self.escapeChar = ''
        self.lineTerminator = self.CSVWriterWidget.cmbLineTerminator.currentText()
        # this seems crazy but it won't work if you just use the commented line above.
        if self.CSVWriterWidget.cmbLineTerminator.currentText() == r'\r\n':
            self.lineTerminator = '\r\n'
        if self.CSVWriterWidget.cmbLineTerminator.currentText() == r'\r':
            self.lineTerminator = '\r'
        if self.CSVWriterWidget.cmbLineTerminator.currentText() == r'\n':
            self.lineTerminator = '\n'  
            
        if self.helper.NoTextValueError(self.fileName, "Must enter a file name"):
            self.CSVWriterWidget.cmbLineTerminator.setFocus()
            return False               
        
        # all edits passed
        return True
        
    
    @pyqtSlot()
    def on_btnExport_clicked(self):
        """
        User clicks the Export button.  Validate and if no errors then accept and exit dialog
        The data grid widget does the actual csv write operation
        """
        if self.validate():
            QDialog.accept(self)
    
    @pyqtSlot()
    def on_btnCancel_clicked(self):
        """
        User clicks cancel so reject dialog and exit
        """
        QDialog.reject(self)
