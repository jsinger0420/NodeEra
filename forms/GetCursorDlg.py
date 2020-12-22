# -*- coding: utf-8 -*-

"""
Module implementing GetCursorDlg.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
import time, datetime

from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QDialog

from core.NeoThread import NeoThread
from .Ui_GetCursorDlg import Ui_GetCursorDlg


class GetCursorDlg(QDialog, Ui_GetCursorDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, neoCon=None, cypher=None, mode=None, parmData=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(GetCursorDlg, self).__init__(parent)
        self.setupUi(self)
        self.rc = False
        self.msg = "No Response"
        self.neoCon = neoCon
        self.cypher = cypher
        self.parmData = parmData
        self.timer = QTimer(self)
        self.timer.setInterval(1000)         
        self.timer.timeout.connect(self.timeRefresh)
        self.neoThread = NeoThread(neoCon=self.neoCon, cypher=self.cypher, mode=mode, parmData=self.parmData)
        self.neoThread.neoCallComplete.connect(self.getReturnData)
        self.neoThread.finished.connect(self.getDataFinished)
        self.neoThread.start()
        self.timeStart = time.time()
        self.timeRefresh()
        self.timer.start() 
        
    @pyqtSlot(bool, str)
    def getReturnData(self, rc, msg ):
#        print("getReturnData")
        self.rc = rc
        self.msg = msg
        
    def getDataFinished(self, ):
#        print("getDataFinished")
        self.neoThread.exit(0)
        self.timer.stop()
        QDialog.accept(self)

    def timeRefresh(self, ):
        delta = round((time.time()-self.timeStart), 2)
        try:
            self.lblElapsedTime.setText(str(datetime.timedelta(seconds=delta)).split('.', 2)[0])
        except:
            self.lblElapsedTime.setText(str(datetime.timedelta(seconds=delta)))
        
    @pyqtSlot()
    def on_btnCancel_clicked(self):
        """
        User clicks on Cancel button so close the dialog
        """
#        print("btnCancel_clicked")
        self.neoThread.exit(0)
        self.timer.stop()
        self.rc = False
        self.msg = "User Cancelled Query"
        QDialog.accept(self)
