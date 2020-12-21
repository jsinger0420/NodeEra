# -*- coding: utf-8 -*-

"""
Module implementing OnlineHelpDLG.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot
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
    
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        Slot documentation goes here.
        """
        QDialog.accept(self)
