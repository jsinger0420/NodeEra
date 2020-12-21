# -*- coding: utf-8 -*-

"""
Module implementing FrmGPoint.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QDoubleValidator
from .Ui_FrmGPoint import Ui_FrmGPoint


class FrmGPoint(QWidget, Ui_FrmGPoint):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FrmGPoint, self).__init__(parent)
        self.setupUi(self)
        self.editLat.setValidator(QDoubleValidator())
        self.editLon.setValidator(QDoubleValidator())
        self.editHeight.setValidator(QDoubleValidator())        
        
    def setText(self, pointData=None):
        '''
        pull the coordinates out of the string
        '''
        if pointData is None:
            return
        if pointData == '':
            return
        if pointData == "Null":
            data = ["", "", ""]
        else:
            start = pointData.find("(")  
            end = pointData.find(")")
            data = pointData[start+1:end].strip().split(" ")
        if len(data) >= 2:
            self.editLon.setText(data[0])
            self.editLat.setText(data[1])
        if len(data) > 2:
            self.editHeight.setText(data[2])
        else:
            self.editHeight.hide()
            self.lblHeight.hide()
    
    def getText(self, ):
        '''
        create a string that looks like the str(Point)
        '''
        if self.lblHeight.isHidden() or self.editHeight.text() == "":
            if self.editLon.text() == "" and self.editLat.text() == "":
                aPoint = "Null"
            else:
                lonFloat = str(float(self.editLon.text()) if len(self.editLon.text())>0 else "0.0") 
                latFloat = str(float(self.editLat.text()) if len(self.editLat.text())>0 else "0.0")                
                aPoint = "POINT({} {})".format(lonFloat,latFloat)
#                aPoint = "POINT({} {})".format(self.editLon.text(), self.editLat.text())
        else:
            if self.editLon.text() == "" and self.editLat.text() == "" and self.editHeight.text() == "":
                aPoint = "Null"
            else:
                lonFloat = str(float(self.editLon.text()) if len(self.editLon.text())>0 else "0.0") 
                latFloat = str(float(self.editLat.text()) if len(self.editLat.text())>0 else "0.0")
                zFloat = str(float(self.editHeight.text()) if len(self.editHeight.text())>0 else "0.0")
                aPoint = "POINT({} {} {})".format(lonFloat,latFloat, zFloat)
#                aPoint = "POINT({} {} {})".format(self.editLon.text(), self.editLat.text(), self.editHeight.text())
        return aPoint
