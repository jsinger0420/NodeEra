#!/usr/bin/python
''' 
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
'''
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import QStyledItemDelegate
from forms.FrmPropList import FrmPropList

########################################################
# listpicker delegate for grid
########################################################
class ListPickerDelegate(QStyledItemDelegate):
    def __init__(self, owner, items, setEditable=None):
        super(QStyledItemDelegate, self).__init__(owner)
        self.items = items
        self.setEditable = setEditable
    
    def sizeHint(self, option, index):
        width = 428
        height = 187
        return QSize(width, height)
    
    def createEditor(self, parent, option, index):
        self.editor = FrmPropList(parent, curVal=index.data(Qt.DisplayRole))
        if self.setEditable:
            self.editor.setEditable(self.setEditable)
        self.editor.addProps(self.items)
        return self.editor
        
    def setEditorData(self, editor, index):

        editor.setPropListDisplay()
        
    def setModelData(self, editor, model, index):
        value = editor.lblPropList.text()
        model.setData(index, value, Qt.DisplayRole)
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(QRect(option.rect.left(), option.rect.top(), editor.frameGeometry().width(),  editor.frameGeometry().height()))  
        editor.parent().parent().setRowHeight (index.row(), editor.frameGeometry().height())   
        editor.parent().parent().setColumnWidth (index.column(), editor.frameGeometry().width())  
