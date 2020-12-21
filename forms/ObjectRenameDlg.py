# -*- coding: utf-8 -*-

"""
Module implementing ObjectRenameDlg.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot, QSettings, Qt
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QStandardItemModel,  QStandardItem

from .Ui_ObjectRenameDlg import Ui_Dialog
from core.helper import Helper

OBJECTTYPE, OBJECTNAME, OBJECTUSAGE = range(3)

class ObjectRenameDlg(QDialog, Ui_Dialog):
    """
    Provide a modal dialog that allows the user to rename a toplevel object.
    """
    def __init__(self, parent=None, mode = None, objectType = None, objectName = None, designModel = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ObjectRenameDlg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.objectType = objectType
        self.objectName = objectName
        self.designModel = designModel
        self.settings = QSettings()
        self.mode = mode
        self.helper = Helper()
        self.instanceObjectChanged = False
        # initialize UI
        self.txtCurrentObject.insert(self.objectType)
        self.txtCurrentName.insert(self.objectName)
        
        if self.mode == "VIEW":
            self.editNewName.setVisible(False) 
            self.label_2.setVisible(False) 
            self.lblInstructions.setVisible(False)
            self.lblInstructions2.setVisible(False)
            self.setWindowTitle("Where Used")

        if self.mode == "DELETE":
            self.editNewName.setVisible(False) 
            self.label_2.setVisible(False) 
            self.lblInstructions.setVisible(True)
            self.lblInstructions.setText("Press OK to delete the object from the project and remove it from everywhere it is used.")
            self.lblInstructions2.setVisible(True)
            self.lblInstructions2.setText("Press Cancel to exit this dialog without deleting.")
            self.setWindowTitle("Delete Object From Project")

        # setup usage grid
        self.gridUsage.setModel(self.createUsageModel())
        self.gridUsage.setColumnWidth(OBJECTTYPE, 200)
        self.gridUsage.setColumnWidth(OBJECTNAME, 200)
        self.gridUsage.setColumnWidth(OBJECTUSAGE, 200)
        self.gridUsage.setSelectionBehavior(QAbstractItemView.SelectRows) 
        self.gridUsage.setSelectionMode(QAbstractItemView.SingleSelection)        
        header = self.gridUsage.horizontalHeader()
        header.setSectionResizeMode(OBJECTTYPE, QHeaderView.Interactive) 
        header.setSectionResizeMode(OBJECTNAME, QHeaderView.Interactive)
        header.setSectionResizeMode(OBJECTUSAGE, QHeaderView.Interactive)        
        
        # get where used descriptions
        self.displayList = []
        self.hitList = self.designModel.scanForObjectUse(self.objectType, self.objectName)
        
        # display in grid        
        for hit in self.hitList:
            self.addHit(self.gridUsage.model(), hit[OBJECTTYPE], hit[OBJECTNAME], hit[OBJECTUSAGE])

    def createUsageModel(self):
        # OBJECTTYPE, OBJECTNAME, OBJECTUSAGE
        model = QStandardItemModel(0, 3)
        model.setHeaderData(OBJECTTYPE, Qt.Horizontal, "Used In Object Type")
        model.setHeaderData(OBJECTNAME, Qt.Horizontal, "Used In Object Name")
        model.setHeaderData(OBJECTUSAGE, Qt.Horizontal, "Usage")
        return model
        
    def addHit(self, model, objectType, objectName, objectUsage):
        # OBJECTTYPE, OBJECTNAME, OBJECTUSAGE
        item1 = QStandardItem(objectType)
        item1.setEditable(False)
        item2 = QStandardItem(objectName)
        item2.setEditable(False)
        item3 = QStandardItem(objectUsage)
        item3.setEditable(False)       
        
        model.appendRow([item1,item2,item3])
        
        
    def validate(self, ):
        if self.mode == "RENAME":
            if self.helper.NoTextValueError(self.editNewName.text().strip(), "You must enter a new Name"):
                self.editNewName.setFocus()
                return False
            
            if self.helper.DupObjectError(designModel = self.designModel, objName=self.editNewName.text(), topLevel = self.objectType, txtMsg = "That name is already used.  Enter a new name."):
                self.editNewName.setFocus()
                return False        
        
        return True
        
    def apply(self, ):
        '''The dialog passes all edits so do the rename.'''
        if self.mode == "RENAME":
            hitList = self.designModel.renameTopLevelObject(topLevel = self.objectType, objectName=self.objectName, newName=self.editNewName.text())
            # check to see if something changed that might require a redraw of open diagrams
            if not hitList is None:
                if len(hitList) > 0:
                    self.instanceObjectChanged = True
        
        if self.mode == "DELETE":
            hitList = self.designModel.deleteTopLevelObject(topLevel = self.objectType, objectName=self.objectName)
            # check to see if something changed that might require a redraw of open diagrams
            if not hitList is None:
                if len(hitList) > 0:
                    self.instanceObjectChanged = True
                    

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        if self.validate():
            self.apply()
            QDialog.accept(self)
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        QDialog.reject(self)
