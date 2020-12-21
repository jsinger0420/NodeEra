# -*- coding: utf-8 -*-

"""
Module implementing HelloUserDlg.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication,  QDesktopWidget

from .Ui_HelloUserDlg import Ui_HelloUserDlg


class HelloUserDlg(QDialog, Ui_HelloUserDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(HelloUserDlg, self).__init__(parent)
        self.setupUi(self)
        self.parent=parent
        self.parent.displayWelcomeMsg.connect(self.displayWelcomeMsg)
        self.parent.closeWelcomeMsg.connect(self.closeWelcomeMsg)
        # center the dialog box on the screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
    @pyqtSlot(str)
    def displayWelcomeMsg(self, msg):
        self.txtMessageArea.append("{}".format(msg))
        QApplication.processEvents()
        
    @pyqtSlot()
    def closeWelcomeMsg(self,):
        """
        application requests to close the dialog box
        """
        QDialog.accept(self)
        QApplication.processEvents()
        
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        User clicks the Close button
        """
        QDialog.accept(self)
    
