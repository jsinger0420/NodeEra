# -*- coding: utf-8 -*-

"""
Module implementing ProjectPropertyBox.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import pyqtSlot, QRectF
from PyQt5.QtWidgets import QDialog, QGraphicsView,  QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem

from forms.Ui_ProjectPropertyBox import Ui_dlgProjectPreferences
from forms.INodeFormatDlg import INodeFormatDlg, INodeFormat
from forms.TNodeFormatDlg import TNodeFormatDlg, TNodeFormat
from forms.IRelFormatDlg import IRelFormatDlg, IRelFormat
from core.helper import PageSetup, PageSizes
#from core.neocon import NeoCon

class ProjectPropertyBox(QDialog, Ui_dlgProjectPreferences):
    """
    Display the project property box UI
    """
    def __init__(self, parent=None, model = None, settings=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ProjectPropertyBox, self).__init__(parent)
        self.model = model
        self.formatChanged = False
        self.modelData = self.model.modelData
        self.settings=settings
        self.INtestItem = None
        self.IRtestItem = None
        self.TNtestItem = None
        self.TRtestItem = None
        self.pageSetup = None
        self.setupUi(self)
        self.initUI()
        
    def initUI(self, ):
        # page settings
        self.pageSizes = PageSizes()
        self.pageSizes.loadDropDown(self.cmbPageSize)
        self.pageSetup = PageSetup(objectDict=self.modelData["pageSetup"])        
        index = self.cmbPageSize.findText(self.pageSetup.objectDict["pageSize"])
        if index >= 0:
            self.cmbPageSize.setCurrentIndex(index)
        if self.pageSetup.objectDict["pageOrientation"] == "Portrait":
            self.rbPortrait.setChecked(True)
            self.rbLandscape.setChecked(False)
        else:
            self.rbLandscape.setChecked(True)
            self.rbPortrait.setChecked(False)
        self.setPageHeightWidth()            
        self.spinRows.setValue(self.pageSetup.objectDict["pageRows"])  
        self.spinColumns.setValue(self.pageSetup.objectDict["pageCols"])  

        # general settings
        self.txtAuthor.setText(self.modelData["Author"])
        self.txtDescription.appendPlainText(self.modelData["Description"])
        
        # diagram settings
        if self.modelData["TemplateLineType"] == "Elbows":
            self.rbElbow.setChecked(True)
            self.rbStraight.setChecked(False)
        else:
            self.rbElbow.setChecked(False)
            self.rbStraight.setChecked(True)
        
        #Instance Formats
#        print("node format is {}".format(self.settings.value("Default/Format/InstanceNode")))
        
        # complete scene setups
        self.INgraphicsView = QGraphicsView(parent=self.frmInstanceNodeViewer)        
        self.INscene = QGraphicsScene(self)
        self.INscene.setSceneRect(0, 0, 300, 600)
        self.INgraphicsView.setScene(self.INscene)
        x = self.modelData["INformat"]
        self.instanceNodeFormat = INodeFormat(formatDict=x)
        self.drawInstanceNode()
        
        self.IRgraphicsView = QGraphicsView(parent=self.frmInstanceRelViewer)        
        self.IRscene = QGraphicsScene(self)
        self.IRscene.setSceneRect(0, 0, 300, 600)
        self.IRgraphicsView.setScene(self.IRscene)
        x = self.modelData["IRformat"]
        self.instanceRelFormat = IRelFormat(formatDict=x)
        self.drawInstanceRel()  
        
        self.TNgraphicsView = QGraphicsView(parent=self.frmTemplateNodeViewer)        
        self.TNscene = QGraphicsScene(self)
        self.TNscene.setSceneRect(0, 0, 300, 600)
        self.TNgraphicsView.setScene(self.TNscene)
        x = self.modelData["TNformat"]
        self.templateNodeFormat = TNodeFormat(formatDict=x)
        self.drawTemplateNode()
        
        self.TRgraphicsView = QGraphicsView(parent=self.frmRelTemplateViewer)        
        self.TRscene = QGraphicsScene(self)
        self.TRscene.setSceneRect(0, 0, 300, 600)
        self.TRgraphicsView.setScene(self.TRscene)
        x = self.modelData["TRformat"]
        self.templateRelFormat = IRelFormat(formatDict=x)
        self.drawTemplateRel()    
        
    def validate(self, ):
        return True
        
    def apply(self, ):
        # what about rel format?
        self.modelData["INformat"] = self.instanceNodeFormat.formatDict
        self.modelData["pageSetup"] = self.pageSetup.objectDict
        self.modelData["Description"] = self.txtDescription.toPlainText()
        self.modelData["Author"] = self.txtAuthor.text()
        return
        
####################################################################################
# PAGE SETTING METHODS
####################################################################################
    def setPageHeightWidth(self, ):
        # this sets the page height width based on page type and orientation
        height, width = self.pageSetup.getHeightWidth()
        self.txtHeight.setText(str(height))
        self.txtWidth.setText(str(width))
        
    @pyqtSlot()
    def on_rbLandscape_clicked(self):
        """
        Slot documentation goes here.
        """
#        print("landscape")
        self.pageSetup.objectDict["pageOrientation"] = "Landscape"
        self.setPageHeightWidth()
        
    @pyqtSlot()
    def on_rbPortrait_clicked(self):
        """
        Slot documentation goes here.
        """
#        print("portrait")
        self.pageSetup.objectDict["pageOrientation"] = "Portrait"
        self.setPageHeightWidth() 
        
    @pyqtSlot(int)
    def on_cmbPageSize_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
#        print("dropdown changed {}".format(self.cmbPageSize.currentText()))
        if self.pageSetup is None:
            return
        newPageSize = str(self.cmbPageSize.currentText())
        self.pageSetup.objectDict["pageSize"] = self.pageSizes.pageTypes[newPageSize].name
        self.pageSetup.objectDict["pageHeight"] = self.pageSizes.pageTypes[newPageSize].height
        self.pageSetup.objectDict["pageWidth"] = self.pageSizes.pageTypes[newPageSize].width
        self.setPageHeightWidth()
    
    @pyqtSlot(int)
    def on_spinRows_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.pageSetup.objectDict["pageRows"] = self.spinRows.value()
    
    @pyqtSlot(int)
    def on_spinColumns_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        self.pageSetup.objectDict["pageCols"] = self.spinColumns.value()
        
    def drawInstanceRel(self, ):  
        if not (self.IRtestItem is None):
            self.IRscene.removeItem(self.IRtestItem)
        rpen = self.instanceRelFormat.pen()
#        rbrush = self.instanceRelFormat.brush()
        self.IRtestItem = QGraphicsLineItem(5, 50, 100, 50, parent=None)
        self.IRtestItem.setPen(rpen)
        self.IRscene.addItem(self.IRtestItem)    
        
    def drawTemplateRel(self, ):  
        if not (self.TRtestItem is None):
            self.TRscene.removeItem(self.TRtestItem)
        rpen = self.templateRelFormat.pen()
#        rbrush = self.templateRelFormat.brush()
        self.TRtestItem = QGraphicsLineItem(5, 50, 100, 50, parent=None)
        self.TRtestItem.setPen(rpen)
        self.TRscene.addItem(self.TRtestItem)  
        
    def drawInstanceNode(self, ):
        if not (self.INtestItem is None):
            self.INscene.removeItem(self.INtestItem)
        pen = self.instanceNodeFormat.pen()
        brush = self.instanceNodeFormat.brush()
        self.INtestItem = QGraphicsEllipseItem(QRectF(5, 5,self.instanceNodeFormat.formatDict["nodeWidth"],self.instanceNodeFormat.formatDict["nodeHeight"]), parent=None)
        self.INtestItem.setBrush(brush)
        self.INtestItem.setPen(pen)
        self.INscene.addItem(self.INtestItem)
        
    def drawTemplateNode(self, ):
        if not (self.TNtestItem is None):
            self.TNscene.removeItem(self.TNtestItem)
        npen = self.templateNodeFormat.pen()
        nbrush = self.templateNodeFormat.brush()
        self.TNtestItem = QGraphicsRectItem(QRectF(5, 5,self.templateNodeFormat.formatDict["nodeWidth"],self.templateNodeFormat.formatDict["nodeHeight"]), parent=None)
        self.TNtestItem.setBrush(nbrush)
        self.TNtestItem.setPen(npen)
        self.TNscene.addItem(self.TNtestItem) 
        
    @pyqtSlot()
    def on_pbTemplateNode_clicked(self):
        """
        Display the Template Node format dialog box and allow the user to change the project level Template node format
        """
        d = TNodeFormatDlg(self, modelData = None, nodeFormat = TNodeFormat(formatDict=self.templateNodeFormat.formatDict))
        if d.exec_():
            self.templateNodeFormat = TNodeFormat(formatDict=d.nodeFormat.formatDict)
            self.drawTemplateNode()
            self.formatChanged = True
    
    @pyqtSlot()
    def on_pbRelTemplate_clicked(self):
        """
        Slot documentation goes here.
        """
        d = IRelFormatDlg(self, modelData = None, relFormat = IRelFormat(formatDict=self.templateRelFormat.formatDict))
        if d.exec_():
            self.instanceRelFormat = IRelFormat(formatDict=d.relFormat.formatDict)
            self.drawTemplateRel()
            self.formatChanged = True

    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.validate():
            self.apply()
            QDialog.accept(self)
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        QDialog.reject(self)
    
    @pyqtSlot()
    def on_pbInstanceNode_clicked(self):
        """
        Display the Instance Node format dialog box and allow the user to change the project level instance node format
        """
        d = INodeFormatDlg(self, modelData = None, nodeFormat = INodeFormat(formatDict=self.instanceNodeFormat.formatDict))
        if d.exec_():
            self.instanceNodeFormat = INodeFormat(formatDict=d.nodeFormat.formatDict)
            self.drawInstanceNode()
            self.formatChanged = True
    
    @pyqtSlot()
    def on_pbInstanceRel_clicked(self):
        """
        Slot documentation goes here.
        """
        d = IRelFormatDlg(self, modelData = None, relFormat = IRelFormat(formatDict=self.instanceRelFormat.formatDict))
        if d.exec_():
            self.instanceRelFormat = IRelFormat(formatDict=d.relFormat.formatDict)
            self.drawInstanceRel()
            self.formatChanged = True
        

    @pyqtSlot()
    def on_pbPageSettings_clicked(self):
        """
        User clicks page settings button
        """
#        print("instance formats clicked")
        self.stackedWidget.setCurrentIndex(1)  
        
    @pyqtSlot()
    def on_pbInstanceFormats_clicked(self):
        """
        User clicks instance format button
        """
#        print("instance formats clicked")
        self.stackedWidget.setCurrentIndex(2) 
        
    @pyqtSlot()
    def on_pbTemplateFormats_clicked(self):
        """
        User click template formats button
        """
#        print("template formats clicked")
        self.stackedWidget.setCurrentIndex(3)
    
    @pyqtSlot()
    def on_pbTemplateDiagram_clicked(self):
        """
        User clicks template diagram button
        """
        self.stackedWidget.setCurrentIndex(4)
    
    @pyqtSlot()
    def on_rbElbow_clicked(self):
        """
        User clicks the elbows radio button
        """
        self.modelData["TemplateLineType"] = "Elbows"
        self.formatChanged = True
    
    @pyqtSlot()
    def on_rbStraight_clicked(self):
        """
        user clicks the straight line radio button
        """
        self.modelData["TemplateLineType"] = "Straight"
        self.formatChanged = True
    
    @pyqtSlot()
    def on_pbGeneral_clicked(self):
        """
        User clicks on general settings button
        """
        self.stackedWidget.setCurrentIndex(0)  
