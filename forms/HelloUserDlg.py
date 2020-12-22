# -*- coding: utf-8 -*-

"""
Module implementing HelloUserDlg.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
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
    
