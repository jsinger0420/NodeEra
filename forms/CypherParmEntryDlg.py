# -*- coding: utf-8 -*-

"""
Module implementing CypherParmEntryDlg.
This provides a dialog box that allows the user to enter values for cypher query parameters
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import Qt,  pyqtSlot
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QStandardItemModel,  QStandardItem

from .Ui_CypherParmEntryDlg import Ui_CypherParmEntryDlg
from core.helper import Helper, CBDelegate
from core.Enums import DataType
from core.NeoEditDelegate import NeoEditDelegate
from core.NeoTypeFunc import NeoTypeFunc

# ENUM for property grid
PARM, DATATYPE, VALUE = range(3)

class CypherParmEntryDlg(QDialog, Ui_CypherParmEntryDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, parms = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(CypherParmEntryDlg, self).__init__(parent)
        self.parent = parent
        self.parms = parms
        self.helper = Helper()
        self.neoTypeFunc = NeoTypeFunc()
        self.parmDict = None
        self.setupUi(self)
        self.initUI()
        
        #load Property grid    
        for parm in self.parms:
            # generate datatype from parm name if possible
            try:
                if 'pointc' in parm.lower():
                    dataType = DataType.POINTCARTESIAN.value
                elif 'pointg' in parm.lower():
                    dataType = DataType.POINTWGS84.value                
                elif 'int' in parm.lower():
                    dataType = DataType.INT.value
                elif 'float' in parm.lower():
                    dataType = DataType.FLOAT.value
                elif 'bool' in parm.lower():
                    dataType = DataType.BOOLEAN.value
                elif 'localdatetime' in parm.lower():
                    dataType = DataType.LOCALDATETIME.value
                elif 'datetime' in parm.lower():
                    dataType = DataType.DATETIME.value
                elif 'date' in parm.lower():
                    dataType = DataType.DATE.value     
                elif 'localtime' in parm.lower():
                    dataType = DataType.LOCALTIME.value
                elif 'time' in parm.lower():
                    dataType = DataType.TIME.value                    
                elif 'pointc' in parm.lower():
                    dataType = DataType.POINTCARTESIAN.value
                elif 'pointg' in parm.lower():
                    dataType = DataType.POINTWGS84.value
                else:
                    dataType = 'String'
            except BaseException as e:
                dataType = 'String'
            finally:
                self.addParm(self.gridParms.model(), parm, dataType, "")

    def initUI(self, ):
        
        # property grid
        self.gridParms.setModel(self.createParmModel())
        self.gridParms.setSortingEnabled(False)
#        comboPropList = [""] 
#        comboPropList.extend(sorted(set(self.model.instanceList("Property") + self.schemaModel.instanceList("Property"))))
        dataTypeList = [dataType.value for dataType in DataType]
        self.gridParms.setItemDelegate(NeoEditDelegate(self))
        self.gridParms.setItemDelegateForColumn(DATATYPE, CBDelegate(self, dataTypeList, setEditable=False))
#        self.gridProps.setItemDelegateForColumn(PROPERTY, CBDelegate(self, comboPropList, setEditable=True ))
        self.gridParms.setColumnWidth(PARM, 200)
        self.gridParms.setColumnWidth(DATATYPE, 125)
        self.gridParms.setColumnWidth(VALUE, 400)
        self.gridParms.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridParms.setSelectionMode(QAbstractItemView.SingleSelection)
        header = self.gridParms.horizontalHeader()
        header.setSectionResizeMode(PARM, QHeaderView.Interactive)
        header.setSectionResizeMode(DATATYPE, QHeaderView.Fixed)
        header.setSectionResizeMode(VALUE, QHeaderView.Stretch)

    def createParmModel(self):

        model = QStandardItemModel(0, 3)
        model.setHeaderData(PARM, Qt.Horizontal, "Parameter")
        model.setHeaderData(DATATYPE, Qt.Horizontal, "Data Type")
        model.setHeaderData(VALUE, Qt.Horizontal, "Value")
        # connect model slots 
        model.itemChanged.connect(self.propModelItemChanged)
        
        return model  
        
    def addParm(self,model,parm, dataType, value):
        '''
        add a row to the property grid
        '''
        self.gridParms.setSortingEnabled(False)
        item1 = QStandardItem(parm)
        item1.setEditable(True)
        item11 = QStandardItem(dataType)
        item11.setEditable(True)
        item2 = QStandardItem(value)
        item2.setData(dataType, Qt.UserRole + 1)
        item2.setEditable(True)
        model.appendRow([item1, item11, item2])

    def validate(self, ):
        # force a repaint of the grid.  this is needed as a workaround for MAC OS
        self.gridParms.setFocus()
        self.gridParms.repaint()
        
        # parm grid checks
        if self.helper.gridNoNameError(grid=self.gridParms, col=VALUE, txtMsg="You must enter a value for each parameter"):
            self.gridParms.setFocus()
            return False
        
        return True
        
    @pyqtSlot()
    def on_btnCancel_clicked(self):
        """
        User Clicked on the Cancel Query button
        """
        self.parmDict = self.genParmDict()
        QDialog.reject(self)
        
    @pyqtSlot()
    def on_btnRunQuery_clicked(self):
        """
        User clicked Run Query button, validate the data then exit
        """
        
        if self.validate():
            self.parmDict = self.genParmDict()
            QDialog.accept(self)
            
    def genParmDict(self, ):
        self.parmDict = {}
        try:
            model = self.gridParms.model()
            numrows = model.rowCount()
            for row in range(0,numrows):
                parmName = model.item(row,PARM).data(Qt.EditRole)
                parmType = model.item(row,DATATYPE).data(Qt.EditRole)
                parm = parmName[1:len(parmName)]                             # strip off the dollar sign
                val = model.item(row,VALUE).data(Qt.EditRole)  
                parmVal = self.neoTypeFunc.castType(stringValue = val, dataType=parmType)
                self.parmDict[parm] = parmVal
        except BaseException as e:
            self.parmDict = None
        finally:
            return self.parmDict
        
    def propModelItemChanged(self, item):
        columnNum = item.index().column()
        if columnNum == DATATYPE:
            # if datatype has changed then change value to "Null" 
            self.gridParms.model().item(item.index().row(), VALUE).setText("Null")
            dataType = self.gridParms.model().item(item.index().row(),DATATYPE).data(Qt.EditRole)
            self.gridParms.model().item(item.index().row(), VALUE).setData(dataType, Qt.UserRole+1)
    

