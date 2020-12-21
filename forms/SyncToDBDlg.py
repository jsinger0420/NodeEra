# -*- coding: utf-8 -*-

"""
    Module implementing SyncToDBDlg.
    The SyncToDBDlg class manages the modal dialog box that allows the user to synchronize 
    an Instance Diagram's objects to the graph database.

    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtGui import QStandardItemModel,  QStandardItem
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QHeaderView
from .Ui_SyncToDBDlg import Ui_Dialog
from core.helper import Helper, CBDelegate

# action columns
ITEMKEY, ITEMTYPE, DIAGRAMITEM, ACTION, GRAPHDBITEM, MATCH = range(6)

# action dropdown
#SYNCTO = "Diagram => Neo4j"
#SYNCNONE = "No Action"
#SYNCFROM = "Neo4j => Diagram"
SYNCTO = "Sync -->"
SYNCNONE = "No Action"
SYNCFROM = "<-- Sync"
# return codes from node check
FOUNDMATCH,  FOUNDNOMATCH, NOTFOUND = range(3)

class SyncToDBDlg(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(SyncToDBDlg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.objectName = self.parent.diagramName
        self.designModel = self.parent.model
        self.syncNeoCon = self.designModel.modelNeoCon
        self.itemDict = self.parent.itemDict
        self.helper = Helper()
        self.initPage()
        #populate ui data from object
        self.populateUIfromObject()           
        
    def initPage(self, ):

        # header area
        self.txtDiagramName.setText(self.objectName)  
        self.txtNeoCon.setText("{} - {}".format( self.syncNeoCon.name, self.syncNeoCon.neoDict["URL"]))

        # action grid
#        ITEMTYPE, DIAGRAMITEM, GRAPHDBITEM, MATCH, ACTION
        self.gridSyncActions.setModel(self.createSyncActionModel())
        self.gridSyncActions.setColumnWidth(ITEMKEY, 50)
        self.gridSyncActions.setColumnWidth(ITEMTYPE, 125)
        self.gridSyncActions.setColumnWidth(DIAGRAMITEM, 400)
        self.gridSyncActions.setColumnWidth(ACTION, 120)
        self.gridSyncActions.setColumnWidth(GRAPHDBITEM, 400)
        self.gridSyncActions.setColumnWidth(MATCH, 80)
        
        self.gridSyncActions.setItemDelegateForColumn(ACTION, CBDelegate(self, [SYNCTO,SYNCNONE,SYNCFROM] ))
        header = self.gridSyncActions.horizontalHeader()
        header.setSectionResizeMode(ITEMKEY, QHeaderView.Fixed)  
        header.setSectionResizeMode(ITEMTYPE, QHeaderView.Fixed)  
        header.setSectionResizeMode(DIAGRAMITEM, QHeaderView.Interactive)
        header.setSectionResizeMode(GRAPHDBITEM, QHeaderView.Interactive)  
        header.setSectionResizeMode(MATCH, QHeaderView.Fixed)  
        header.setSectionResizeMode(ACTION, QHeaderView.Fixed)  
        header.setHighlightSections(False)

    
    def createSyncActionModel(self):
#        ITEMTYPE, DIAGRAMITEM, ACTION, GRAPHDBITEM, MATCH
        model = QStandardItemModel(0, 6)
        model.setHeaderData(ITEMKEY, Qt.Horizontal, "Key")
        model.setHeaderData(ITEMTYPE, Qt.Horizontal, "Type")
        model.setHeaderData(DIAGRAMITEM, Qt.Horizontal, "Diagram Item")
        model.setHeaderData(ACTION, Qt.Horizontal, "Action")
        model.setHeaderData(GRAPHDBITEM, Qt.Horizontal, "Neo4j Item")
        model.setHeaderData(MATCH, Qt.Horizontal, "Match")
        
        return model  
    
    def populateUIfromObject(self, ):
        if self.itemDict is not None:
            # scan the nodes        
            for key, value in self.itemDict.items():
                objectItemDict = value.getObjectDict()
                if objectItemDict["diagramType"] == "Instance Node":
                    rc, msg = value.itemInstance.checkNode()
                    self.addActionRow(rc, msg, value)
                
            # scan the relationships
            for key, value in self.itemDict.items():
                objectItemDict = value.getObjectDict()
                if objectItemDict["diagramType"] == "Instance Relationship":
                    rc, msg = value.relationInstance.checkRelationship()
                    self.addActionRow(rc, msg, value)

                        
    def addActionRow(self, rc, msg, diagramItem):
#        ITEMTYPE, DIAGRAMITEM, ACTION, GRAPHDBITEM, MATCH
        objectItemDict = diagramItem.getObjectDict()
        
        item0 = QStandardItem(diagramItem.NZID())
        item0.setEditable(False)
        
        item1 = QStandardItem(objectItemDict["diagramType"])
        item1.setEditable(False)
        
        if objectItemDict["diagramType"] == "Instance Node":
            objectDict = diagramItem.itemInstance.getObjectDict()
#            item2 = QStandardItem("({} {})".format(diagramItem.itemInstance.labelList, diagramItem.itemInstance.propList))
            item2 = QStandardItem(objectDict["displayName"])
            item2.setEditable(False)
            item3 = QStandardItem(self.syncNeoCon.displayNode(diagramItem.itemInstance.node))
            item3.setEditable(False)
        elif objectItemDict["diagramType"] == "Instance Relationship":
            objectDict = diagramItem.relationInstance.getObjectDict()
#            item2 = QStandardItem("({})".format(diagramItem.relationInstance.propList))
            item2 = QStandardItem(objectDict["displayName"])
            item2.setEditable(False)
            item3 = QStandardItem(self.syncNeoCon.displayRelationship(diagramItem.relationInstance.relationship))
            item3.setEditable(False)
        else:
            item2 = QStandardItem("({})".format("No Object"))
            item2.setEditable(False)
            item3 = QStandardItem("No Object")
            item3.setEditable(False)
            
            
        if rc == FOUNDMATCH:
            item4 = QStandardItem("Match")
        if rc == FOUNDNOMATCH:
            item4 = QStandardItem("Different")
        if rc == NOTFOUND:
            item4 = QStandardItem("Not in Neo4j")
        item4.setEditable(False)      
        
        if rc == FOUNDMATCH:
            item5 = QStandardItem(SYNCNONE)
        if rc == FOUNDNOMATCH:
            item5 = QStandardItem(SYNCTO)
        if rc == NOTFOUND:
            item5 = QStandardItem(SYNCTO)
        item5.setEditable(True)        

        self.gridSyncActions.model().appendRow([item0, item1,item2, item5, item3, item4])  

        
    def validate(self, ):
        
        return True
        
    def apply(self, ):
        '''
        The dialog passes all edits so process all the sync actions.
        '''
        model = self.gridSyncActions.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            syncAction = model.item(row,ACTION).data(Qt.EditRole)
            rc = None
            msg = ""
            if syncAction == SYNCTO:
                key = model.item(row,ITEMKEY ).data(Qt.EditRole)
                item = self.itemDict[key]
                if item.diagramType == "Instance Relationship":
                    rc, msg = item.relationInstance.syncToDB()
                if item.diagramType == "Instance Node":    
                    rc, msg = item.itemInstance.syncToDB()
            if syncAction == SYNCFROM:
                key = model.item(row,ITEMKEY ).data(Qt.EditRole)
                item = self.itemDict[key]
                if item.diagramType == "Instance Relationship":
                    rc, msg = item.relationInstance.syncFromDB()
                if item.diagramType == "Instance Node":    
                    rc, msg = item.itemInstance.syncFromDB()     
            # display error message if any
            if not rc is None:
                if rc == False:
                     self.helper.displayErrMsg("Sync Diagram Error", msg)
                     
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
