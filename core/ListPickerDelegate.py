#!/usr/bin/python
''' 
    Author: John Singer
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
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
