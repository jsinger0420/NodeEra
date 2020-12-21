#!/usr/bin/python
''' 
    Author: John Singer
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
'''

from PyQt5.QtCore import Qt, QSize
#from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit, QComboBox


class MetaBoxDelegate(QStyledItemDelegate):
    def __init__(self, owner):
        super(MetaBoxDelegate, self).__init__(owner)
        self.booleanItems=["True", "False"]
        self.hintSize = None
        
#    def eventFilter(self, editor, event):
#        if (event.type() == QEvent.KeyPress and
#            event.key() == Qt.Key_Tab):
#            print( "Tab captured in editor")
#            self.commitData.emit(editor) 
#            self.closeEditor.emit(editor, QAbstractItemDelegate.NoHint) 
#            return True
#        return QStyledItemDelegate.eventFilter(self,editor,event)   
        
    def createEditor(self, parent, option, index):
        # create the appropriate widget based on the datatype
        columnName = index.data(Qt.UserRole)
        self.hintSize = QSize(option.rect.width(), option.rect.height())
        if columnName == "Node Template":
            self.editor = QComboBox(parent)
            self.editor.addItems(self.loadNodeTemplateDropdown())
        elif columnName == "Relationship Template":
            self.editor = QComboBox(parent)
            self.editor.addItems(self.loadRelTemplateDropdown())
        elif columnName in ["Blank Template", "Optional"]:
            self.editor = QComboBox(parent)
            self.editor.addItems(self.booleanItems)
        else:
            self.editor = QLineEdit(parent)
            
        return self.editor
        
    def setEditorData(self, editor, index):
        '''
        this takes the string stored in the grid cell and populates the editor widget with that value.
        '''
        value = index.data(Qt.DisplayRole)
        columnName = index.data(Qt.UserRole)
        if columnName in [ "Node Template", "Relationship Template"]:
            index = editor.findText(value)
            if index >= 0:
                editor.setCurrentIndex(index)
        elif columnName in ["Blank Template", "Optional"]:
            try:
                num = self.booleanItems.index(value)
                editor.setCurrentIndex(num)
            except:
                editor.setCurrentIndex(0)            
        # default qlineedit
        elif isinstance(editor, QLineEdit):
            editor.setText(value)
        else:
            #shouldn't happen     
            editor.setText(value)       

    def setModelData(self, editor, model, index):
        '''
        this takes the current value of the editor widget, converts it back to a string and stores it back in the item model
        '''
        columnName = index.data(Qt.UserRole)
        if columnName in [ "Node Template", "Relationship Template"]:
            value=editor.currentText()
            model.setData(index, value, Qt.DisplayRole)
        # true/false properties
        elif columnName in ["Blank Template", "Optional"]:    
            value = editor.currentText()
            model.setData(index, value, Qt.DisplayRole)
        # default editor is a qlineedit
        elif isinstance(editor, QLineEdit):        
            value = editor.text()
            model.setData(index, value, Qt.DisplayRole)
        else:
            #shouldn't happen
            value = editor.text()
            model.setData(index, value, Qt.DisplayRole)            

        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)   

    def loadNodeTemplateDropdown(self, ):
        # load node template dropdown
        dropdownList = ["Anonymous Node"]
        dropdownList.extend(sorted(self.parent().parent.model.instanceList("Node Template")))
        return dropdownList

    def loadRelTemplateDropdown(self, ):
        # load node template dropdown
        dropdownList = ["Anonymous Relationship"]
        dropdownList.extend(sorted(self.parent().parent.model.instanceList("Relationship Template")))
        return dropdownList
