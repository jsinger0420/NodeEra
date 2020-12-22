# -*- coding: utf-8 -*-

"""
UC-21 Instance Relation Format Template Editor
Module implementing dlgNodeTemplate.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QColorDialog, QGraphicsView,  QGraphicsScene,  QGraphicsLineItem
from PyQt5.QtGui import QColor,  QPen, QBrush

from forms.Ui_IRelFormatDlg import Ui_IRelFormatDlg

class IRelFormat():
    def __init__(self, formatDict=None):
        """
        Constructor
        """
        self.formatDict = formatDict
        if self.formatDict is None:
            self.formatDict = {}
        
#        self.formatDict.setdefault("nodeWidth", 125)
#        self.formatDict.setdefault("nodeHeight", 75)
        self.formatDict.setdefault("fillStyle", "Fill")
        self.formatDict.setdefault("lineStyle", "Solid")
        self.formatDict.setdefault("lineWidth", 1)
        self.formatDict.setdefault("patternNumber", 1)
        self.formatDict.setdefault("lineColor", QColor(Qt.black).name())
        self.formatDict.setdefault("fillColor", QColor(Qt.white).name())
        
    def pen(self, ):
        # this function returns a QPen based on the format settings
        aPen = QPen()
        aColor = QColor()
        QColor.setNamedColor(aColor, self.formatDict["lineColor"])
        aPen.setColor(aColor)
        aPen.setWidth(self.formatDict["lineWidth"])
        if self.formatDict["lineStyle"] == "No Line":
            aPen.setStyle(Qt.NoPen)  
        if self.formatDict["lineStyle"] == "Solid":
            aPen.setStyle(Qt.SolidLine)
        if self.formatDict["lineStyle"] == "Dash":
            aPen.setStyle(Qt.DashLine)
        if self.formatDict["lineStyle"] == "Dot":
            aPen.setStyle(Qt.DotLine)
        if self.formatDict["lineStyle"] == "DashDot":
            aPen.setStyle(Qt.DashDotLine)
        if self.formatDict["lineStyle"] == "DashDotDot":
            aPen.setStyle(Qt.DashDotDotLine)
        return aPen
        
    def brush(self, ):
        # this function returns a QBrush based on the format settings
        aBrush = QBrush()
        aColor = QColor()
        QColor.setNamedColor(aColor, self.formatDict["fillColor"])
        aBrush.setColor(aColor)
        if self.formatDict["fillStyle"] == "None":
            aBrush.setStyle(Qt.NoBrush)
        if self.formatDict["fillStyle"] == "Fill":
            aBrush.setStyle(Qt.SolidPattern)
        if self.formatDict["fillStyle"] == "Pattern":
            aBrush.setStyle(int(self.formatDict["patternNumber"])+1) 
        return aBrush
        
class IRelFormatDlg(QDialog, Ui_IRelFormatDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, modelData=None, relFormat=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(IRelFormatDlg, self).__init__(parent)
        self.modelData = modelData
        self.relFormat=relFormat
        if self.relFormat is None:
            self.relFormat = IRelFormat()
        self.testItem = None
        self.setupUi(self)
        # complete ui setups
        self.graphicsView = QGraphicsView(parent=self.frmView)        
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 300, 600)
        self.graphicsView.setScene(self.scene)
        
        self.populateUIfromObject()
        self.drawLine()
        
    def populateUIfromObject(self, ):

        self.spinLineWidth.setValue(self.relFormat.formatDict["lineWidth"])
            
        #line style            
        if self.relFormat.formatDict["lineStyle"] == "Solid":
            self.rbSolidLine.setChecked(True) 
        if self.relFormat.formatDict["lineStyle"] == "Dash":
            self.rbDashLine.setChecked(True) 
        if self.relFormat.formatDict["lineStyle"] == "Dot":
            self.rbDotLine.setChecked(True) 
        if self.relFormat.formatDict["lineStyle"] == "DashDot":
            self.rbDashDotLine.setChecked(True) 
        if self.relFormat.formatDict["lineStyle"] == "DashDotDot":
            self.rbDashDotDotLine.setChecked(True) 
      
    def drawLine(self, ):
        if not (self.testItem is None):
            self.scene.removeItem(self.testItem)
        pen = self.relFormat.pen()
        #brush = self.relFormat.brush()
        self.testItem = QGraphicsLineItem(5, 50, 100, 50, parent=None)
        self.testItem.setPen(pen)
        self.scene.addItem(self.testItem)
        
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        return
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        QDialog.reject(self)
    
    @pyqtSlot()
    def on_rbNone_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbNone.isChecked() == True:
            self.relFormat.formatDict["fillStyle"] = "None"
            self.drawLine()
    
    @pyqtSlot()
    def on_rbFill_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbFill.isChecked() == True:
            self.relFormat.formatDict["fillStyle"] = "Fill"
            self.drawLine()
    
    @pyqtSlot()
    def on_rbPattern_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbPattern.isChecked() == True:
            self.relFormat.formatDict["fillStyle"] = "Pattern"
            self.drawLine()
    
    
    @pyqtSlot(int)
    def on_spinPattern_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.relFormat.formatDict["patternNumber"]=self.spinPattern.value()
        self.drawLine()
        
    @pyqtSlot()
    def on_btnFillColor_clicked(self):
        """
        fill color push button
        """
        aColor = QColor()
        QColor.setNamedColor(aColor, self.relFormat.formatDict["fillColor"])
        newColor = QColorDialog.getColor (initial = aColor, parent = None)
        if newColor.isValid():
            self.relFormat.formatDict["fillColor"]=newColor.name()
            self.drawLine()
            
    @pyqtSlot()
    def on_btnLineColor_clicked(self):
        """
        Slot documentation goes here.
        """
        aColor = QColor()
        QColor.setNamedColor(aColor, self.relFormat.formatDict["lineColor"])
        newColor = QColorDialog.getColor (initial = aColor, parent = None)
        if newColor.isValid():
            self.relFormat.formatDict["lineColor"]=newColor.name()
            self.drawLine()
            
    @pyqtSlot()
    def on_rbNoLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbNoLine.isChecked() == True:
            self.relFormat.formatDict["lineStyle"] = "No Line"
            self.drawLine()
    
    @pyqtSlot()
    def on_rbSolidLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbSolidLine.isChecked() == True:
            self.relFormat.formatDict["lineStyle"] = "Solid"
            self.drawLine()

    
    @pyqtSlot()
    def on_rbDashLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbDashLine.isChecked() == True:
            self.relFormat.formatDict["lineStyle"] = "Dash"
            self.drawLine()
    
    @pyqtSlot()
    def on_rbDotLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbDotLine.isChecked() == True:
            self.relFormat.formatDict["lineStyle"] = "Dot"
            self.drawLine()    
            
    @pyqtSlot()
    def on_rbDashDotLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbDashDotLine.isChecked() == True:
            self.relFormat.formatDict["lineStyle"] = "DashDot"
            self.drawLine()    
    
    @pyqtSlot()
    def on_rbDashDotDotLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbDashDotDotLine.isChecked() == True:
            self.relFormat.formatDict["lineStyle"] = "DashDotDot"
            self.drawLine()    
    
    @pyqtSlot(int)
    def on_spinLineWidth_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.relFormat.formatDict["lineWidth"]=self.spinLineWidth.value()
        self.drawLine()
        
