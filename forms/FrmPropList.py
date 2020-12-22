# -*- coding: utf-8 -*-

"""
Module implementing FrmPropList.
Author: John Singer
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFrame

from .Ui_FrmPropList import Ui_Frame
from core.helper import Helper


        
class FrmPropList(QFrame, Ui_Frame):
    """
    This frame provides a UI for selecting a set of properties from all properties and setting their order
    """
    def __init__(self, parent=None, curVal=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FrmPropList, self).__init__(parent)
        self.setupUi(self)
        self.helper = Helper()
        self.curVal = curVal
        
    def addProps(self, propList):
        # load the list of all properties in the template
        for prop in propList:
            if len(prop) > 0:
                self.gridAllProps.addItem(prop)
        # load the list of selected properties
        if not self.curVal is None:
            selectedPropList = self.curVal.split(", ")
            for selectedProp in selectedPropList:
                if selectedProp in [str(self.gridAllProps.item(i).text()) for i in range(self.gridAllProps.count())]:
                    self.gridSelectedProps.addItem(selectedProp)
        
        self.setPropListDisplay()
        
        
    def genPropList(self, ):
        '''
        generate a comma seperated list of properties from the selected properties list view
        '''
        propComma = ""
        propList = [str(self.gridSelectedProps.item(i).text()) for i in range(self.gridSelectedProps.count())]
        propComma = ", ".join(x for x in propList) 
        return propComma

    def setPropListDisplay(self, ):
        '''
        set the label with the generated property list
        '''
        self.lblPropList.setText(self.genPropList())
        
    @pyqtSlot()
    def on_btnAdd_clicked(self):
        """
        User clicks >> button to add a prop to the prop list
        """
        index = self.gridAllProps.currentRow()
        if (index is not None and index > -1):
            selProperty = self.gridAllProps.item(index).text()
            if selProperty in [str(self.gridSelectedProps.item(i).text()) for i in range(self.gridSelectedProps.count())]:
                self.helper.displayErrMsg("Add Property", "Property {} can only be selected once".format(selProperty))
            else:
                self.gridSelectedProps.addItem(self.gridAllProps.item(index).text())
            self.setPropListDisplay()
        else:
            self.helper.displayErrMsg("Add Property", "You must select a property to add.")
            
    @pyqtSlot()
    def on_btnRemove_clicked(self):
        """
        user clicks the << button to remove a prop from the proplist
        """
        self.gridSelectedProps.takeItem(self.gridSelectedProps.currentRow())
        self.setPropListDisplay()
    
    @pyqtSlot()
    def on_btnMoveUp_clicked(self):
        """
        User clicks the Move Up button, move the selected property up on in the list
        """
        self.helper.moveListItemUp(self.gridSelectedProps)
        self.setPropListDisplay()
    
    @pyqtSlot()
    def on_btnMoveDown_clicked(self):
        """
        User clicks the Move Down button, move the selected property up on in the list
        """
        self.helper.moveListItemDown(self.gridSelectedProps)        
        self.setPropListDisplay()
