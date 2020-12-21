# -*- coding: utf-8 -*-

"""
Module implementing FrmPoint.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
#from neo4j.v1.types.spatial import CartesianPoint, WGS84Point

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QDoubleValidator
from .Ui_FrmPoint import Ui_FrmPoint


class FrmPoint(QWidget, Ui_FrmPoint):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FrmPoint, self).__init__(parent)
        self.setupUi(self)
        self.editX.setValidator(QDoubleValidator())
        self.editY.setValidator(QDoubleValidator())
        self.editZ.setValidator(QDoubleValidator())
        
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
            self.editX.setText(data[0])
            self.editY.setText(data[1])
        if len(data) > 2:
            self.editZ.setText(data[2])
        else:
            self.editZ.hide()
            self.lblZ.hide()
    
    def getText(self, ):
        '''
        create a string that looks like the str(Point)
        '''
        if self.lblZ.isHidden() or self.editZ.text() == "":
            if self.editX.text() == "" and self.editY.text() == "":
                aPoint = "Null"
            else:
                xFloat = str(float(self.editX.text()) if len(self.editX.text())>0 else "0.0") 
                yFloat = str(float(self.editY.text()) if len(self.editY.text())>0 else "0.0")                
                aPoint = "POINT({} {})".format(xFloat,yFloat)
        else:
            if self.editX.text() == "" and self.editY.text() == "" and self.editZ.text() == "":
                aPoint = "Null"
            else:
                xFloat = str(float(self.editX.text()) if len(self.editX.text())>0 else "0.0") 
                yFloat = str(float(self.editY.text()) if len(self.editY.text())>0 else "0.0")
                zFloat = str(float(self.editZ.text()) if len(self.editZ.text())>0 else "0.0")
                aPoint = "POINT({} {} {})".format(xFloat,yFloat, zFloat)
        return aPoint
