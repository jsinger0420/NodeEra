# -*- coding: utf-8 -*-
''' 
    UC-02 Connection Manager
        Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
'''
from PyQt5.QtCore import Qt, QSettings, pyqtSlot
from PyQt5.QtWidgets import QDialog, QInputDialog, QMessageBox, QAbstractItemView,  QApplication
from PyQt5.QtGui import QStandardItemModel,  QStandardItem

from forms.Ui_dlgNeoCon import Ui_dlgNeoCons
from forms.NeoConPropertyBox import NeoConPropertyBox
#from core.neocon import NeoCon
from core.NeoDriver import NeoDriver
from core.helper import Helper

NEO4JNAME = 0
NEO4JHOSTNAME = 1
NEO4JUSERID = 2
NEO4JURL = 3

class dlgNeoCons(QDialog, Ui_dlgNeoCons):
    """
    Modal Dialog that displays Neo4j Connections using UI_dlgNeoCons.
    Displays a grid of Neo4j Connection definitions and
    allows the user to add/edit/delete/test them.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(dlgNeoCons, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.settings=QSettings()
        self.selectedNeoConName = None
        self.selectedNeoConDict = None
        self.helper = Helper()
        self.initUI()

    def initUI(self, ):
        
        #Neo4j Page
        # get saved neoCons
        self.neoCons = {}
        self.gridNeoCons.setSelectionBehavior(QAbstractItemView.SelectRows) 
        self.gridNeoCons.setSelectionMode(QAbstractItemView.SingleSelection)
        self.gridNeoCons.setModel(self.createNeoConModel())
        self.gridNeoCons.horizontalHeader().setStretchLastSection(True)
        self.gridNeoCons.setShowGrid(True)
        self.settings.beginGroup("NeoCon/connection")
        neoKeys = self.settings.childKeys()
        for key in neoKeys:
            neoDict=self.settings.value(key)
            self.neoCons[key] = neoDict
            self.addNeoConRow(neoDict) 
        self.settings.endGroup()
        
    def createNeoConModel(self):
        model = QStandardItemModel(0, 4)
        model.setHeaderData(NEO4JNAME, Qt.Horizontal, "Connection")
        model.setHeaderData(NEO4JHOSTNAME, Qt.Horizontal, "Host Name")
        model.setHeaderData(NEO4JUSERID, Qt.Horizontal, "User ID")
        model.setHeaderData(NEO4JURL, Qt.Horizontal, "URL")
        return model     


    def validate(self, ):
        indexes = self.gridNeoCons.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
#            print("{}-{}".format(index.row(), index.column()))
            self.selectedNeoConName = self.gridNeoCons.model().item(index.row(), NEO4JNAME).text()        
            self.selectedNeoConDict = self.neoCons[self.selectedNeoConName]
            return True
        else:
            return False
        
    def apply(self, ):
        return
        
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        if self.validate():
            self.apply()
            QDialog.accept(self)
        else:
            return
            
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        QDialog.reject(self)   
        
    @pyqtSlot()
    def on_btnAdd_clicked(self):
        """
        Slot documentation goes here.
        """
        self.editNeoCon(mode="NEW")
    
    @pyqtSlot()
    def on_btnEdit_clicked(self):
        """
        Slot documentation goes here.
        """
        self.editNeoCon(mode="EDIT")
        
    def editNeoCon(self, mode=None, objectDict = None):
        if mode == "NEW":
            slot, ok = QInputDialog.getText(self, 'New Connection', 'Enter the Connection Name:              ')
            if ok:
                if len(slot.strip()) < 1 :
                    self.helper.displayErrMsg("New Connection","Must enter a connection name." )
                    return
                if slot in self.neoCons:
                    self.helper.displayErrMsg("New Connection","Neo4j Connection {} already exists.".format(slot) )
                    return
                    
                newNeoCon = NeoDriver(name=slot)
                neoDict = newNeoCon.neoDict       
                d = NeoConPropertyBox(self, mode=mode, objectDict=neoDict)
                if d.exec_():
                    self.neoCons[slot] = d.objectDict
                    self.addNeoConRow(d.objectDict)
                    self.settings.setValue("NeoCon/connection/{}".format(d.objectDict["slot"]),d.objectDict)
                    
        if mode == "EDIT":
            indexes = self.gridNeoCons.selectionModel().selectedIndexes()
            if len(indexes) > 0:
                index = indexes[0]
#                print("{}-{}".format(index.row(), index.column()))
                # get the connection name
                slotItem = self.gridNeoCons.model().item(index.row(), NEO4JNAME)
                neoDict = self.neoCons[slotItem.text()]
                # make sure it isn't open - can't edit an open connection
                if neoDict["slot"] in self.parent.pageDict:
                    self.helper.displayErrMsg("Edit Connection","Cannot edit connection {} because it is open. Close the connection first.".format(neoDict["slot"]) )
                    return
                
                d = NeoConPropertyBox(self, mode=mode, objectDict=neoDict)
                if d.exec_():
                    self.settings.setValue("NeoCon/connection/{}".format(d.objectDict["slot"]),d.objectDict)
                    # update grid row to reflect new values
                    x1 = self.gridNeoCons.model().createIndex(index.row(), NEO4JHOSTNAME )
                    item1 = QStandardItem(d.objectDict["host"])
                    item1.setEditable(False)
                    self.gridNeoCons.model().setItem(x1.row(), x1.column(), item1)              
                    x2 = self.gridNeoCons.model().createIndex(index.row(), NEO4JUSERID )
                    item2 = QStandardItem(d.objectDict["userid"])
                    item2.setEditable(False)
                    self.gridNeoCons.model().setItem(x2.row(), x2.column(), item2)                          
                    return
            else:
                self.helper.displayErrMsg("Edit Connection","Please select a connection from the grid" )
                
        
    def addNeoConRow(self, neoDict):
        self.gridNeoCons.setSortingEnabled(False)    
        item1 = QStandardItem(neoDict["slot"])
        item1.setEditable(False)
        item2 = QStandardItem(neoDict["host"])
        item2.setEditable(False)
        item3 = QStandardItem(neoDict["userid"])
        item3.setEditable(False)
        item4 = QStandardItem(neoDict["URL"])
        item4.setEditable(False)
        self.gridNeoCons.model().appendRow([item1,item2, item3, item4])
        self.gridNeoCons.resizeColumnsToContents() 
        # force a repaint of the grid.  this is needed as a workaround for MAC OS
        self.gridNeoCons.repaint()
            
    @pyqtSlot()
    def on_btnTest_clicked(self):
        """
        User clicks the test button
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        indexes = self.gridNeoCons.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            slotItem = self.gridNeoCons.model().item(index.row(), NEO4JNAME)
            neoDict = self.neoCons[slotItem.text()]
            # see if we need to prompt for password
            pw = None
            if neoDict["prompt"] == "True":
                # prompt for a password
                pw = ''
                while len(pw) < 1:            
                    pw = self.helper.passwordPrompt(conName=slotItem.text(), conURL=neoDict["URL"])
                    if not pw is None:
                        if len(pw) > 0:
                            pw = self.helper.putText(pw)
                        else:
                            self.helper.displayErrMsg("Prompt Password", "You must enter a password.")

            neoDriver = NeoDriver(name=slotItem.text(), promptPW=pw)
            rc, resultMsg = neoDriver.test()
            if rc:
                # save the neocon dictionary in settings since url etc may have been updated
                neoDict = neoDriver.neoDict
                self.settings.setValue("NeoCon/connection/{}".format(neoDict["slot"]),neoDict) 
                # update the grid layout with the url
                x = self.gridNeoCons.model().createIndex(index.row(), NEO4JURL)
                item1 = QStandardItem(neoDict.get("URL", "No URI"))
                item1.setEditable(False)
                self.gridNeoCons.model().setItem(x.row(), x.column(), item1)
                self.gridNeoCons.model().dataChanged.emit(x, x)
                # tell the user it worked
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Test Neo4j Connection")
                msg.setText(resultMsg)
                msg.setStandardButtons(QMessageBox.Close)
                msg.exec_()                
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Test Neo4j Connection")
                msg.setText(resultMsg)
                msg.setStandardButtons(QMessageBox.Close)
                msg.exec_()                                                
        else:
            self.helper.displayErrMsg("Test Connection","Please select a connection from the grid" )

        QApplication.restoreOverrideCursor()
    
    @pyqtSlot()
    def on_btnRemove_clicked(self):
        """
        User requests to remove the connection definition that is selected on the grid.
        """
        indexes = self.gridNeoCons.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            slotItem = self.gridNeoCons.model().item(index.row(), NEO4JNAME)
            if slotItem.text() in self.parent.pageDict:
                self.helper.displayErrMsg("Remove Connection","Cannot remove connection {} because it is open. Close the connection first.".format(slotItem.text()) )
                return
            # check to see if you are removing the default neoCon
            defaultNeoCon = self.settings.value("NeoCon/Default")
            if defaultNeoCon == slotItem.text():
                self.helper.displayErrMsg("Remove Connection", "You cannot remove the {} connection".format(defaultNeoCon))
                return
            # remove the neoCon from the dictionary of all neoCons
            del self.neoCons[slotItem.text()]
            # remove the neoCon from the settings
            self.settings.remove("NeoCon/connection/{}".format(slotItem.text()))
            # remove the row from the grid
            self.gridNeoCons.model().removeRows(index.row(),1)
        else:
            self.helper.displayErrMsg("Remove Connection","Please select a connection from the grid" )
    
