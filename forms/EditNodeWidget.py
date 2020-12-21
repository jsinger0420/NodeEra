# -*- coding: utf-8 -*-

"""
Module implementing EditNodeWidget.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel,  QStandardItem

from .Ui_EditNodeWidget import Ui_EditNodeWidget
from core.NeoEditDelegate import NeoEditDelegate

# labels in node template
LABEL, REQUIRED, NODEKEY = range(3)
# node template property list
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS, UNIQUE, PROPNODEKEY = range(7)
# ENUM for property grid
PROPERTY, DATATYPE, VALUE = range(3)

class EditNodeWidget(QWidget, Ui_EditNodeWidget):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, templateDict=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(EditNodeWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.templateDict = templateDict
        
        # LABEL GRID
        self.gridLabels.setModel(self.createLabelModel())
        self.gridLabels.setColumnWidth(LABEL, 200)
        self.gridLabels.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridLabels.setSelectionMode(QAbstractItemView.SingleSelection)
        header = self.gridLabels.horizontalHeader()
        header.setSectionResizeMode(LABEL, QHeaderView.Interactive) 

        # property grid
        self.gridProps.setSortingEnabled(False)
        self.gridProps.setModel(self.createPropModel())
        self.gridProps.setItemDelegate(NeoEditDelegate(self))
        self.gridProps.setColumnWidth(PROPERTY, 200)
        self.gridProps.setColumnWidth(DATATYPE, 125)
        self.gridProps.setColumnWidth(VALUE, 300)
        self.gridProps.setSelectionBehavior(QAbstractItemView.SelectItems) 
        self.gridProps.setSelectionMode(QAbstractItemView.SingleSelection)
        header = self.gridProps.horizontalHeader()
        header.setSectionResizeMode(PROPERTY, QHeaderView.Interactive)
        header.setSectionResizeMode(DATATYPE, QHeaderView.Fixed)
        header.setSectionResizeMode(VALUE, QHeaderView.Stretch)

        self.populateUIfromObject()
        
    def createLabelModel(self):
        # LABEL, REQUIRED, NODEKEY
        model = QStandardItemModel(0, 1)
        model.setHeaderData(LABEL, Qt.Horizontal, "Label")
        return model
        
    def createPropModel(self):

        model = QStandardItemModel(0, 3)
        model.setHeaderData(PROPERTY, Qt.Horizontal, "Property")
        model.setHeaderData(DATATYPE, Qt.Horizontal, "Data Type")
        model.setHeaderData(VALUE, Qt.Horizontal, "Value")
        
        return model  
        
    def populateUIfromObject(self, ):
        if self.templateDict is not None:
            #load Labels  LABEL, REQUIRED, NODEKEY
            for nodeLbl in self.templateDict["labels"]:
                self.addLabel(self.gridLabels.model(), nodeLbl[LABEL], nodeLbl[REQUIRED])
            #load props  PROPERTY, EXISTS, PROPREQ,PROPDEF,UNIQUE, PROPNODEKEY
            for nodeProp in self.templateDict["properties"]:
                self.addProp(self.gridProps.model(), nodeProp[PROPERTY], nodeProp[DATATYPE], nodeProp[PROPREQ], nodeProp[PROPDEF] )

    def addLabel(self,model,label, required):
        # LABEL, REQUIRED, NODEKEY
        item1 = QStandardItem(label)
        item1.setEditable(True)
        item1 = QStandardItem()
        item1.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item1.setText(label)
        if required == Qt.Checked:
            item1.setCheckState(required)
            item1.setEnabled(False)
            item1.setText("{}".format(label))
        else:
            item1.setCheckState(Qt.Unchecked)  
            item1.setText(label)
        
        model.appendRow([item1])

    def addProp(self,model,prop, dataType, required, default):
        '''
        add a row to the property grid
        '''
        self.gridProps.setSortingEnabled(False)
        if required == Qt.Checked:
            item1 = QStandardItem("{}".format(prop))
        else:
            item1 = QStandardItem("{}".format(prop))
        item1.setEditable(False)
        item2 = QStandardItem(dataType)
        item2.setEditable(False)
        if default is None or default == "":
            item3 = QStandardItem("Null")
        else:
            item3 = QStandardItem(default)
        item3.setData(dataType, Qt.UserRole + 1)
        item3.setEditable(True)
        model.appendRow([item1, item2, item3])
        
        

    @pyqtSlot()
    def on_btnSetNull_clicked(self):
        """
        User requests to set a property value to Null
        """
        # grid only allows single selection
        indexes = self.gridProps.selectionModel().selectedIndexes()
        for index in indexes:
            valueIndex = self.gridProps.model().index(index.row(), VALUE)
            self.gridProps.model().setData(valueIndex, "Null", Qt.DisplayRole)
    
    @pyqtSlot()
    def on_btnAddNew_clicked(self):
        """
        Slot documentation goes here.
        """
        self.parent.on_btnAddNew_clicked()
