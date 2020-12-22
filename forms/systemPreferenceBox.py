# -*- coding: utf-8 -*-

''' 
    UC-03 System Preferences
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
'''

from PyQt5.QtCore import pyqtSlot, QRectF
from PyQt5.QtWidgets import QDialog, QFileDialog, QGraphicsView,  QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem

from forms.Ui_SystemPreferenceBox import Ui_SystemPreferenceBox
from forms.INodeFormatDlg import INodeFormatDlg, INodeFormat
from forms.TNodeFormatDlg import TNodeFormatDlg, TNodeFormat
from forms.IRelFormatDlg import IRelFormatDlg, IRelFormat
from forms.TRelFormatDlg import TRelFormatDlg, TRelFormat
from core.helper import PageSetup, PageSizes

class SystemPreferenceBox(QDialog, Ui_SystemPreferenceBox):
    """
    Modal Dialog box that displays System Preferences.
    The user may update and save the preferences.
    """
    def __init__(self, parent=None, settings = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(SystemPreferenceBox, self).__init__(parent)
        self.settings=settings
        self.INtestItem = None
        self.IRtestItem = None
        self.TNtestItem = None
        self.TRtestItem = None
        self.pageSetup = None
        self.setupUi(self)
        self.initUI()
        self.stackedWidget.setCurrentIndex(0)
        
    def initUI(self, ):
        #General Page
        dir = str(self.settings.value("Default/ProjPath"))
        self.lblProjPath.setText(dir)
        self.lblProjPath.setToolTip(dir)

        logdir = str(self.settings.value("Default/LoggingPath"))
        self.lblLoggingPath.setText(logdir)
        self.lblLoggingPath.setToolTip(logdir)
        
        # page settings
        self.pageSizes = PageSizes()
        self.pageSizes.loadDropDown(self.cmbPageSize)
        self.pageSetup = PageSetup(objectDict=self.settings.value("Default/PageSetup"))        
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
      
        #Instance Formats
#        print("node format is {}".format(self.settings.value("Default/Format/InstanceNode")))
        formatDict = self.settings.value("Default/Format/InstanceNode") 
        self.instanceNodeFormat = INodeFormat(formatDict=formatDict)
        relFormatDict = self.settings.value("Default/Format/InstanceRelation") 
        self.instanceRelFormat = IRelFormat(formatDict=relFormatDict)
        
        #Template Formats
        formatDict = self.settings.value("Default/Format/TemplateNode") 
        self.templateNodeFormat = TNodeFormat(formatDict=formatDict)
        relFormatDict = self.settings.value("Default/Format/TemplateRelation") 
        self.templateRelFormat = IRelFormat(formatDict=relFormatDict)

        # complete scene setups
        self.INgraphicsView = QGraphicsView(parent=self.frmInstanceNodeViewer)        
        self.INscene = QGraphicsScene(self)
        self.INscene.setSceneRect(0, 0, 300, 600)
        self.INgraphicsView.setScene(self.INscene)
        self.drawInstanceNode()
        
        self.IRgraphicsView = QGraphicsView(parent=self.frmInstanceRelViewer)        
        self.IRscene = QGraphicsScene(self)
        self.IRscene.setSceneRect(0, 0, 300, 600)
        self.IRgraphicsView.setScene(self.IRscene)
        self.drawInstanceRel()
        
        self.TNgraphicsView = QGraphicsView(parent=self.frmTemplateNodeViewer)        
        self.TNscene = QGraphicsScene(self)
        self.TNscene.setSceneRect(0, 0, 300, 600)
        self.TNgraphicsView.setScene(self.TNscene)
        self.drawTemplateNode()
        
        self.TRgraphicsView = QGraphicsView(parent=self.frmRelTemplateViewer)        
        self.TRscene = QGraphicsScene(self)
        self.TRscene.setSceneRect(0, 0, 300, 600)
        self.TRgraphicsView.setScene(self.TRscene)
        self.drawTemplateRel() 

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
        rbrush = self.instanceRelFormat.brush()
        self.IRtestItem = QGraphicsLineItem(5, 50, 100, 50, parent=None)
        self.IRtestItem.setPen(rpen)
        self.IRscene.addItem(self.IRtestItem)
        
    def drawTemplateRel(self, ):  
        if not (self.TRtestItem is None):
            self.TRscene.removeItem(self.TRtestItem)
        rpen = self.templateRelFormat.pen()
        rbrush = self.templateRelFormat.brush()
        self.TRtestItem = QGraphicsLineItem(5, 50, 100, 50, parent=None)
        self.TRtestItem.setPen(rpen)
        self.TRscene.addItem(self.TRtestItem)  
        
    def drawInstanceNode(self, ):
        if not (self.INtestItem is None):
            self.INscene.removeItem(self.INtestItem)
        npen = self.instanceNodeFormat.pen()
        nbrush = self.instanceNodeFormat.brush()
        self.INtestItem = QGraphicsEllipseItem(QRectF(5, 5,self.instanceNodeFormat.formatDict["nodeWidth"],self.instanceNodeFormat.formatDict["nodeHeight"]), parent=None)
        self.INtestItem.setBrush(nbrush)
        self.INtestItem.setPen(npen)
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
        
    def validate(self, ):
        return True
        
    def apply(self, ):
        self.settings.setValue("Default/ProjPath",self.lblProjPath.text())
        self.settings.setValue("Default/LoggingPath",self.lblLoggingPath.text())
        self.settings.setValue("Default/PageSetup", self.pageSetup.objectDict)
        

#####################################################################
# template format methods
#####################################################################
    @pyqtSlot()
    def on_pbTemplateNode_clicked(self):
        """
        User requests edit a Node Template Format
        """
        # create a TNodeFormat object from the system settings dictionary
        x = self.settings.value("Default/Format/TemplateNode")
        d = TNodeFormatDlg(self, modelData = None, nodeFormat = TNodeFormat(formatDict=x))
        if d.exec_():
            self.settings.setValue("Default/Format/TemplateNode",d.nodeFormat.formatDict)
            self.templateNodeFormat = TNodeFormat(formatDict=self.settings.value("Default/Format/TemplateNode"))
            self.drawTemplateNode()

    
    @pyqtSlot()
    def on_pbRelTemplate_clicked(self):
        """
        User requests edit a Relationship Template Format
        """
        # create a RelFormat object from the system settings dictionary
        x = self.settings.value("Default/Format/TemplateRelation")
        d = TRelFormatDlg(self, modelData = None, relFormat = TRelFormat(formatDict=x))
        if d.exec_():
            self.settings.setValue("Default/Format/TemplateRelation",d.relFormat.formatDict)
            self.templateRelFormat = TRelFormat(formatDict=self.settings.value("Default/Format/TemplateRelation"))
            self.drawTemplateRel()


#####################################################################
# instance format methods
#####################################################################

    @pyqtSlot()
    def on_pbInstanceNode_clicked(self):
        """
        Slot documentation goes here.
        """
        # create a NodeFormat object from the system settings dictionary
        x = self.settings.value("Default/Format/InstanceNode")
        d = INodeFormatDlg(self, modelData = None, nodeFormat = INodeFormat(formatDict=x))
        if d.exec_():
            self.settings.setValue("Default/Format/InstanceNode",d.nodeFormat.formatDict)
            self.instanceNodeFormat = INodeFormat(formatDict=self.settings.value("Default/Format/InstanceNode"))
            self.drawInstanceNode()
    
    @pyqtSlot()
    def on_pbInstanceRel_clicked(self):
        """
        Slot documentation goes here.
        """
        # create a RelFormat object from the system settings dictionary
        x = self.settings.value("Default/Format/InstanceRelation")
        d = IRelFormatDlg(self, modelData = None, relFormat = IRelFormat(formatDict=x))
        if d.exec_():
            self.settings.setValue("Default/Format/InstanceRelation",d.relFormat.formatDict)
            self.instanceRelFormat = IRelFormat(formatDict=self.settings.value("Default/Format/InstanceRelation"))
            self.drawInstanceRel()
    
#    @pyqtSlot()
#    def on_pbTestConnection_clicked(self):
#        """
#        Slot documentation goes here.
#        """
#        print("pbTestConnection clicked")
#    
#    @pyqtSlot()
#    def on_pbDefineConnection_clicked(self):
#        """
#        Slot documentation goes here.
#        """
#        print("DefineConnection clicked")

########################################################################
# General Settings
########################################################################
    @pyqtSlot()
    def on_btnProjPath_clicked(self):
        """
        User selects Path button to select a default project path
        """
        curDir = self.lblProjPath.text()
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setDirectory(curDir)
        file = str(dlg.getExistingDirectory(self, "Select Directory"))
        if file:
            self.lblProjPath.setText(str(file))
            self.lblProjPath.setToolTip(str(file))

    @pyqtSlot()
    def on_btnLoggingPath_clicked(self):
        """
        User selects Path button to select a logging path
        """
        curDir = self.lblLoggingPath.text()
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setDirectory(curDir)
        file = str(dlg.getExistingDirectory(self, "Select Directory"))
        if file:
            self.lblLoggingPath.setText(str(file))
            self.lblLoggingPath.setToolTip(str(file))
            
########################################################################
# side buttons that control what settings page to show
########################################################################

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
#        print("general preferences clicked")
        self.stackedWidget.setCurrentIndex(0)
        
    @pyqtSlot()
    def on_pbPageSettings_clicked(self):
        """
        Slot documentation goes here.
        """
#        print("page settings clicked")
        self.stackedWidget.setCurrentIndex(1) 

    
    @pyqtSlot()
    def on_pbInstanceFormats_clicked(self):
        """
        Slot documentation goes here.
        """
#        print("instance formats clicked")
        self.stackedWidget.setCurrentIndex(2)
    
    @pyqtSlot()
    def on_pbTemplateFormats_clicked(self):
        """
        Slot documentation goes here.
        """
#        print("template formats clicked")
        self.stackedWidget.setCurrentIndex(3)
    
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        User presses close.  Save changes and close dialog box.
        """
        self.apply()
        QDialog.accept(self)
    

