# -*- coding: utf-8 -*-

"""
Module implementing FrmTime.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import  QDoubleValidator

from .Ui_FrmTime import Ui_FrmTime


class FrmTime(QWidget, Ui_FrmTime):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, tz=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FrmTime, self).__init__(parent)
        if tz is None:
            tz = True
        self.setupUi(self)
        self.editHH.setValidator(QDoubleValidator())
        self.editHH.validator().setRange(0, 23, decimals=0)
        self.editMM.setValidator(QDoubleValidator())
        self.editMM.validator().setRange(0, 59, decimals=0)
        self.editSS.setValidator(QDoubleValidator())
        self.editHH.validator().setRange(0, 59, decimals=9)
        # set timezone fields
        if tz == True:
            self.editTZ.setVisible(True)
            self.lblTZ.setVisible(True)
        else:
            self.editTZ.setVisible(False)
            self.lblTZ.setVisible(False)
            
    def setText(self, timeData=None):
        '''
        pull the time out of the string.
        hh:mm:s.sssssssss+/-zzzz
        '''
        if timeData is None:
            return
        if timeData == '':
            return
        if timeData == "Null":
            # need to find current utc offset
            data = ["0", "0", "0", "0"]
            UTCpart = ""
        else:
            # look for timezone
            if (timeData.find("+") > 0):
                UTCpart = timeData[timeData.find("+"):len(timeData)]
                timePart = timeData[0:timeData.find("+")]
            elif (timeData.find("-") > 0):
                UTCpart = timeData[timeData.find("-"):len(timeData)]
                timePart = timeData[0:timeData.find("-")]
            else:
                UTCpart = ""
                timePart = timeData
            # split on colons
            data = timePart.strip().split(":")
        if len(data) >= 2:
            self.editHH.setText(data[0])
            self.editMM.setText(data[1])
            
        if len(data) > 2:
            self.editSS.setText(data[2])
        else:
            self.editSS.setText('0.0')
        self.editTZ.setText(UTCpart)
        
    def getText(self, ):
        '''
        create a string that looks like the cypher time function
        '''
        aTime = "{}:{}:{}{}".format(self.editHH.text(), self.editMM.text(), self.editSS.text(), self.editTZ.text())
        return aTime
        
