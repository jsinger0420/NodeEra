# -*- coding: utf-8 -*-

"""
Module implementing FrmDateTime.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import pyqtSlot, QDateTime, QDate
from PyQt5.QtWidgets import QWidget

from .Ui_FrmDateTime import Ui_FrmDateTime


class FrmDateTime(QWidget, Ui_FrmDateTime):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, tz=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FrmDateTime, self).__init__(parent)
        self.setupUi(self)
        if tz is None:
            tz = True
        # set timezone fields
        if tz == True:
            self.editTZ.setVisible(True)
            self.lblTZ.setVisible(True)
        else:
            self.editTZ.setVisible(False)
            self.lblTZ.setVisible(False)        
            
    def setText(self, dateTimeData=None):
        # set the qdateedit widget value
        if dateTimeData =="Null":
            aDate = QDate.currentDate()
            self.editDate.setDate(aDate)
        elif dateTimeData != "Null":
            aDate = QDate.fromString(dateTimeData, "yyyy-MM-dd")
            self.editDate.setDate(aDate)
#        '''
#        pull the time out of the string.
#        hh:mm:s.sssssssss+/-zzzz
#        '''
#        if dateTimeData is None:
#            return
#        if dateTimeData == '':
#            return
#        if dateTimeData == "Null":
#            # need to find current utc offset
#            data = ["0", "0", "0", "0"]
#            UTCpart = ""
#        else:
#            # look for timezone
#            if (dateTimeData.find("+") > 0):
#                UTCpart = dateTimeData[dateTimeData.find("+"):len(dateTimeData)]
#                timePart = dateTimeData[0:dateTimeData.find("+")]
#            elif (dateTimeData.find("-") > 0):
#                UTCpart = dateTimeData[dateTimeData.find("-"):len(dateTimeData)]
#                timePart = dateTimeData[0:dateTimeData.find("-")]
#            else:
#                UTCpart = ""
#                timePart = dateTimeData
#            # split on colons
#            data = timePart.strip().split(":")
#
#        self.editTZ.setText(UTCpart)
        
    def getText(self, ):
        '''
        create a string that looks like the cypher time function
        '''
        aDateTime = self.editDateTime.dateTime()
        returnDate = aDateTime.toString("yyyy-MM-dd")
        returnTime = aDateTime.toString("hh:mm:ss")
        returnString = "{}T{}".format(returnDate, returnTime)
        return returnString
        
        
