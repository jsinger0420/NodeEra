# -*- coding: utf-8 -*-

"""
Module implementing pageWidget.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot, QSettings
from PyQt5.QtWidgets import QWidget

from .Ui_tabPageWidget import Ui_pageWidget


class PageWidget(QWidget, Ui_pageWidget):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(PageWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.settings = QSettings()
        self.pageType = "UNKNOWN"

#    def close(self):
#        print("page widget close")
#    
#    def closeTab(self, tabPage, tabWidget):
#        print("page widget closeTab. tabPage:{} tabWidget: {}".format(tabPage, tabWidget))
        
    @pyqtSlot(int)
    def on_tabPage_tabCloseRequested(self, index):
        """
        Close the current tab page - could be a project or the schema tab
        
        @param index DESCRIPTION
        @type int
        """
#        print("tabPage tabCloseRequested index: {}".format(index)) 
        aTab = self.tabPage.widget(index)
        if aTab.pageType == "PROJECT":
            aTab.save()
            self.tabPage.removeTab(index)
            return
        if aTab.pageType == "CYPHER":
            # build a list of all the tabs
            tabList = []
            for tabIndex in range(0, self.tabPage.count()):
                tabList.append(self.tabPage.widget(tabIndex))
            # go thru the list and save/remove all the project tabs
            for tab in tabList:
                if tab.pageType == "PROJECT":
                    self.tabPage.setCurrentIndex(self.tabPage.indexOf(tab))
                    tab.save()
                    self.tabPage.removeTab(self.tabPage.indexOf(tab))
                        
            # tell the schema tab to save all open cypher query tabs in the cyphereditngrid
            aTab.save()
            # not sure what this does
            aTab.close()
            # the main page must close the connection itself
            self.parent.removeConnection()
        
        
        
        
#        if self.tabPage.currentWidget():
#            if self.tabPage.currentWidget().pageType == "PROJECT":
#                self.tabPage.currentWidget().save()
#                self.tabPage.removeTab(index)
#                return
#            # this is the schema tab
#            if self.tabPage.currentWidget().pageType == "CYPHER":
#                # build a list of all the tabs
#                tabList = []
#                for tabIndex in range(0, self.tabPage.count()):
#                    tabList.append(self.tabPage.widget(tabIndex))
#                # go thru the list and save/remove all the project tabs
#                for tab in tabList:
#                    if tab.pageType == "PROJECT":
#                        self.tabPage.setCurrentIndex(self.tabPage.indexOf(tab))
#                        tab.save()
#                        self.tabPage.removeTab(self.tabPage.indexOf(tab))
#                        
#                # tell the schema tab to save all open cypher query tabs in the cyphereditngrid
#                self.tabPage.currentWidget().save()
#                # not sure what this does
#                self.tabPage.currentWidget().close()
##                # the main page must close the connection itself
#                self.parent.removeConnection()
#                
    def closeSchemaTab(self,  ):
        '''the main menu calls this when closing a connection and  all its related tabs
        '''
#        print("close schema tab")
        schemaTab = self.tabPage.widget(0)

        if schemaTab.pageType == "CYPHER":
            # build a list of all the tabs
            tabList = []
            for tabIndex in range(0, self.tabPage.count()):
                tabList.append(self.tabPage.widget(tabIndex))
            # go thru the list and save/remove all the project tabs
            for tab in tabList:
                if tab.pageType == "PROJECT":
                    self.tabPage.setCurrentIndex(self.tabPage.indexOf(tab))
                    tab.save()
                    self.tabPage.removeTab(self.tabPage.indexOf(tab))
                    
            # tell the schema tab to save all open cypher query tabs in the cyphereditngrid
            schemaTab.save()
            # not sure what this does
            schemaTab.close()

                
    @pyqtSlot(int)
    def on_tabPage_currentChanged(self, index):
        """
        User has switched tab pages for a connection so update menu action enabled
        
        @param index DESCRIPTION
        @type int
        """
        self.parent.setMenuAccess()

                
