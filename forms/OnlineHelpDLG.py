# -*- coding: utf-8 -*-

"""
Module implementing OnlineHelpDLG.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
from PyQt5.QtGui import QDesktopServices

from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWidgets import QDialog

from .Ui_OnlineHelpDLG import Ui_OnlineHelpDLG


class OnlineHelpDLG(QDialog, Ui_OnlineHelpDLG):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(OnlineHelpDLG, self).__init__(parent)
        self.setupUi(self)
        
        self.txtHelp.setHtml('''
        <p><b>NodeEra Help</b></p>
        <p></p>
        <p>The NodeEra Users manual and how to videos are available online.  Click the Online Help button below to open the help webpage or paste https://singerlinks.com/nodeera-user-manual into your web browser</p>
        ''')
        

        
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        Slot documentation goes here.
        """
        QDialog.accept(self)
    
    @pyqtSlot()
    def on_btnHelp_clicked(self):
        """
        Slot documentation goes here.
        """
        QDesktopServices.openUrl(QUrl("https://singerlinks.com/nodeera-user-manual/"))   
