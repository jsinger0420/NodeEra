# -*- coding: utf-8 -*-

"""
UC-20 Instance Node Format Template Editor
Module implementing dlgNodeTemplate.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot, Qt,  QRectF
from PyQt5.QtWidgets import QDialog, QColorDialog, QGraphicsView,  QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtGui import QColor, QPen, QBrush

from forms.Ui_INodeFormatDlg import Ui_INodeFormat

class INodeFormat():
    def __init__(self, formatDict=None):
        """
        Constructor for a default Instance Node Format
        """
        self.formatDict = formatDict
        if self.formatDict is None:
            self.formatDict = {}
        
        self.formatDict.setdefault("nodeWidth", 125)
        self.formatDict.setdefault("nodeHeight", 75)
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
        
class INodeFormatDlg(QDialog, Ui_INodeFormat):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, modelData=None, nodeFormat=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(INodeFormatDlg, self).__init__(parent)
        self.modelData = modelData
        self.nodeFormat=nodeFormat
        if self.nodeFormat is None:
            self.nodeFormat = INodeFormat()
        self.testItem = None
        self.setupUi(self)
        # complete ui setups
        self.graphicsView = QGraphicsView(parent=self.frmView)        
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        
        self.populateUIfromObject()
        self.drawNode()
        
    def populateUIfromObject(self, ):
        self.spinHeight.setValue(self.nodeFormat.formatDict["nodeHeight"])
        self.spinWidth.setValue(self.nodeFormat.formatDict["nodeWidth"])
        self.spinLineWidth.setValue(self.nodeFormat.formatDict["lineWidth"])
        self.spinPattern.setValue(self.nodeFormat.formatDict["patternNumber"])
        #fill style
        if self.nodeFormat.formatDict["fillStyle"] == "None":
            self.rbNone.setChecked(True)
        if self.nodeFormat.formatDict["fillStyle"] == "Fill":
            self.rbFill.setChecked(True)
        if self.nodeFormat.formatDict["fillStyle"] == "Pattern":
            self.rbPattern.setChecked(True)    
            
        #line style    
        if self.nodeFormat.formatDict["lineStyle"] == "No Line":
            self.rbNoLine.setChecked(True)                   
        if self.nodeFormat.formatDict["lineStyle"] == "Solid":
            self.rbSolidLine.setChecked(True) 
        if self.nodeFormat.formatDict["lineStyle"] == "Dash":
            self.rbDashLine.setChecked(True) 
        if self.nodeFormat.formatDict["lineStyle"] == "Dot":
            self.rbDotLine.setChecked(True) 
        if self.nodeFormat.formatDict["lineStyle"] == "DashDot":
            self.rbDashDotLine.setChecked(True) 
        if self.nodeFormat.formatDict["lineStyle"] == "DashDotDot":
            self.rbDashDotDotLine.setChecked(True) 
      
    def drawNode(self, ):
        if not (self.testItem is None):
            self.scene.removeItem(self.testItem)
        nodeWidth = self.nodeFormat.formatDict["nodeWidth"]
        nodeHeight = self.nodeFormat.formatDict["nodeHeight"]
        pen = self.nodeFormat.pen()
        brush = self.nodeFormat.brush()
        self.testItem = QGraphicsEllipseItem(QRectF(5, 5,nodeWidth + 5,nodeHeight + 5), parent=None)
        self.testItem.setBrush(brush)
        self.testItem.setPen(pen)
        self.scene.addItem(self.testItem)
        self.graphicsView.setSceneRect(1, 1, 500, 500)        
        
        
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
            self.nodeFormat.formatDict["fillStyle"] = "None"
            self.drawNode()
    
    @pyqtSlot()
    def on_rbFill_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbFill.isChecked() == True:
            self.nodeFormat.formatDict["fillStyle"] = "Fill"
            self.drawNode()
    
    @pyqtSlot()
    def on_rbPattern_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbPattern.isChecked() == True:
            self.nodeFormat.formatDict["fillStyle"] = "Pattern"
            self.drawNode()
    
    @pyqtSlot(int)
    def on_spinPattern_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.nodeFormat.formatDict["patternNumber"]=self.spinPattern.value()
        self.drawNode()
        
    @pyqtSlot()
    def on_btnFillColor_clicked(self):
        """
        fill color push button
        """
        aColor = QColor()
        QColor.setNamedColor(aColor, self.nodeFormat.formatDict["fillColor"])
        newColor = QColorDialog.getColor (initial = aColor, parent = None)
        if newColor.isValid():
            self.nodeFormat.formatDict["fillColor"]=newColor.name()
            self.drawNode()
    @pyqtSlot()
    def on_btnLineColor_clicked(self):
        """
        Slot documentation goes here.
        """
        aColor = QColor()
        QColor.setNamedColor(aColor, self.nodeFormat.formatDict["lineColor"])

        newColor = QColorDialog.getColor (initial = aColor, parent = None)
        if newColor.isValid():
            self.nodeFormat.formatDict["lineColor"]=newColor.name()
            self.drawNode()
    @pyqtSlot()
    def on_rbNoLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbNoLine.isChecked() == True:
            self.nodeFormat.formatDict["lineStyle"] = "No Line"
            self.drawNode()
    
    @pyqtSlot()
    def on_rbSolidLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbSolidLine.isChecked() == True:
            self.nodeFormat.formatDict["lineStyle"] = "Solid"
            self.drawNode()

    
    @pyqtSlot()
    def on_rbDashLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbDashLine.isChecked() == True:
            self.nodeFormat.formatDict["lineStyle"] = "Dash"
            self.drawNode()
    
    @pyqtSlot()
    def on_rbDotLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbDotLine.isChecked() == True:
            self.nodeFormat.formatDict["lineStyle"] = "Dot"
            self.drawNode()    
            
    @pyqtSlot()
    def on_rbDashDotLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbDashDotLine.isChecked() == True:
            self.nodeFormat.formatDict["lineStyle"] = "DashDot"
            self.drawNode()    
    
    @pyqtSlot()
    def on_rbDashDotDotLine_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.rbDashDotDotLine.isChecked() == True:
            self.nodeFormat.formatDict["lineStyle"] = "DashDotDot"
            self.drawNode()    
    
    @pyqtSlot(int)
    def on_spinLineWidth_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.nodeFormat.formatDict["lineWidth"]=self.spinLineWidth.value()
        self.drawNode()
        
    @pyqtSlot(int)
    def on_spinHeight_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.nodeFormat.formatDict["nodeHeight"]=self.spinHeight.value()
        self.drawNode()
    
    @pyqtSlot(int)
    def on_spinWidth_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.nodeFormat.formatDict["nodeWidth"]=self.spinWidth.value()
        self.drawNode()
