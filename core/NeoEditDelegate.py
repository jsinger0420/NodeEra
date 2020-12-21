#!/usr/bin/python
''' 
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
'''

import neo4j.time
from neo4j.time import Date, DateTime,  Time, Duration
from PyQt5.QtCore import Qt, QDate, QSize, QRect
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit, QComboBox, QDateTimeEdit
from core.helper import Helper
from core.Enums import DataType
from forms.FrmPoint import FrmPoint
from forms.FrmGPoint import FrmGPoint


class NeoEditDelegate(QStyledItemDelegate):
    def __init__(self, owner):
        super(NeoEditDelegate, self).__init__(owner)
        self.booleanItems=["True", "False"]
        self.hintSize = None
        self.helper = Helper()
        
    def createEditor(self, parent, option, index):
        # create the appropriate widget based on the datatype
        dataType = index.data(Qt.UserRole+1)
        self.hintSize = QSize(option.rect.width(), option.rect.height())
        if dataType == DataType.INT.value:
            self.editor = QLineEdit(parent)
            self.editor.setValidator(QIntValidator())
        elif dataType == DataType.FLOAT.value:
            self.editor = QLineEdit(parent)
            self.editor.setValidator(QDoubleValidator())
        elif dataType == DataType.STRING.value:
            self.editor = QLineEdit(parent)
        elif dataType == DataType.BOOLEAN.value:
            self.editor = QComboBox(parent)
            self.editor.addItems(self.booleanItems)
        elif dataType == DataType.POINTWGS84.value:
            self.editor = FrmGPoint(parent)
            self.editor.setAutoFillBackground(True)
            self.hintSize = QSize(300, 40)
        elif dataType == DataType.POINTCARTESIAN.value:
            self.editor = FrmPoint(parent)
            self.editor.setAutoFillBackground(True)
            self.hintSize = QSize(300, 40)
        elif dataType == DataType.TIME.value:
#            self.editor = FrmTime(parent=parent, tz=True)
            self.editor = QLineEdit(parent)
        elif dataType == DataType.LOCALTIME.value:
#            self.editor = FrmTime(parent=parent, tz=False)
            self.editor = QLineEdit(parent)
        elif dataType == DataType.DATE.value:
            self.editor = QDateTimeEdit(parent)
            self.editor.setCalendarPopup(True)
            self.editor.setDisplayFormat("yyyy/MM/dd")
        elif dataType == DataType.DATETIME.value:
#            self.editor = QDateTimeEdit(parent)
#            self.editor.setCalendarPopup(False)
#            self.editor.setDisplayFormat("yyyy-MM-dd hh:mm:ss:zzz")
            self.editor = QLineEdit(parent)
        elif dataType == DataType.LOCALDATETIME.value:
            self.editor = QLineEdit(parent)
        elif dataType == DataType.DURATION.value:
            self.editor = QLineEdit(parent)
        else:
            self.editor = QLineEdit(parent)
            
        return self.editor
        
    def setEditorData(self, editor, index):
        '''
        this takes the string stored in the grid cell and populates the editor widget with that value.
        '''
        value = index.data(Qt.DisplayRole)
        dataType = index.data(Qt.UserRole+1)
        if isinstance(editor, QLineEdit):
            if ((dataType == DataType.INT.value or dataType == DataType.FLOAT.value)
                  and value == "Null"):
                editor.setText("")
            else:    
                editor.setText(value)
        # boolean datatype uses a listbox
        elif isinstance(editor, QComboBox):
            try:
                num = self.booleanItems.index(value)
                editor.setCurrentIndex(num)
            except:
                editor.setCurrentIndex(0)            
        elif isinstance(editor, FrmPoint ):
            self.editor.setText(value)
        elif isinstance(editor, FrmGPoint ):
            self.editor.setText(value)   
        elif isinstance(editor, QDateTimeEdit):
            try:
                aDate = None
                if dataType == DataType.DATE.value:
                    if value == "Null":
                        aDate = QDate.currentDate()
                        editor.setDate(aDate)
                    else:
                        aDate = QDate.fromString(value, format=Qt.ISODate)
                        editor.setDate(aDate)
                    
            except:
                pass
        
            
    def setModelData(self, editor, model, index):
        '''
        this takes the current value of the editor widget, converts it back to a string and stores it back in the item model
        '''
        dataType = index.data(Qt.UserRole+1)
        # string, integer, and float use a qlineedit
        if isinstance(editor, QLineEdit):  
            if dataType == DataType.DATETIME.value:            
                value = editor.text()
                try:
                    aNeoDateTime = DateTime.from_iso_format(value)
                    saveStr = aNeoDateTime.iso_format()
                    model.setData(index, saveStr, Qt.DisplayRole)
                except:
                    self.helper.displayErrMsg("Date Time", "Entered text [{}] is not a valid ISO date time.".format(value))
                    model.setData(index, value, Qt.DisplayRole)       
            elif dataType == DataType.LOCALDATETIME.value:            
                value = editor.text()
                try:
                    aNeoDateTime = DateTime.from_iso_format(value)
                    saveStr = aNeoDateTime.iso_format()
                    model.setData(index, saveStr, Qt.DisplayRole)
                except:
                    self.helper.displayErrMsg("Date Time", "Entered text [{}] is not a valid ISO date time.".format(value))
                    model.setData(index, value, Qt.DisplayRole)                    
            elif dataType in  [DataType.LOCALTIME.value, DataType.TIME.value]:            
                value = editor.text()
                try:
                    aNeoTime = Time.from_iso_format(value)
                    saveStr = aNeoTime.iso_format()
                    tz=""
                    if aNeoTime.tzinfo is not None:
                        offset = aNeoTime.tzinfo.utcoffset(self)
                        tz = "%+03d:%02d" % divmod(offset.total_seconds() // 60, 60)
                    returnStr = "{}{}".format(saveStr, tz)
                    model.setData(index, returnStr, Qt.DisplayRole)
                except:
                    self.helper.displayErrMsg("Time", "Entered text [{}] is not a valid ISO time.".format(value))
                    model.setData(index, value, Qt.DisplayRole)                    
            else:
                value = editor.text()
                model.setData(index, value, Qt.DisplayRole)
        # boolean datatype uses a listbox
        elif isinstance(editor, QComboBox):   
            value = editor.currentText()
            model.setData(index, value, Qt.DisplayRole)
        elif isinstance(editor, FrmPoint ):
            value = editor.getText()
            model.setData(index, value, Qt.DisplayRole)
        elif isinstance(editor, FrmGPoint ):
            value = editor.getText()
            model.setData(index, value, Qt.DisplayRole)
#        elif isinstance(editor, FrmTime ):
#            value = editor.getText()
#            model.setData(index, value, Qt.DisplayRole)
#        elif isinstance(editor, FrmDateTime ):
#            value = editor.getText()
#            model.setData(index, value, Qt.DisplayRole)            
        elif isinstance(editor, QDateTimeEdit):
            if dataType == DataType.DATE.value:            
                value = editor.date().toString(Qt.ISODate)
                model.setData(index, value, Qt.DisplayRole)
#            if dataType == DataType.DATETIME.value:
#                value = editor.dateTime().toString("yyyy-MM-dd hh:mm:ss:zzz")
##                print("editor datetime: {} editor string: {}".format(editor.dateTime(), value))
#                model.setData(index, value, Qt.DisplayRole)
        
    def updateEditorGeometry(self, editor, option, index):
        dataType = index.data(Qt.UserRole+1)
        if isinstance(editor, FrmPoint):
            editor.setGeometry(QRect(option.rect.left(), option.rect.top(), editor.frameGeometry().width(),  editor.frameGeometry().height()))  
            self.editor.parent().parent().setRowHeight (index.row(), editor.frameGeometry().height())   
            self.editor.parent().parent().setColumnWidth (index.column(), editor.frameGeometry().width())  
        elif isinstance(editor, FrmGPoint):
            editor.setGeometry(QRect(option.rect.left(), option.rect.top(), editor.frameGeometry().width(),  editor.frameGeometry().height()))  
            self.editor.parent().parent().setRowHeight (index.row(), editor.frameGeometry().height())
            self.editor.parent().parent().setColumnWidth (index.column(), editor.frameGeometry().width())
        elif isinstance(editor, QDateTimeEdit):
            if dataType == DataType.DATETIME.value:
                # for some reason, the qdatetimeedit doesn't know it's width so we hard code it
                editor.setGeometry(QRect(option.rect.left(), option.rect.top(), 180,  editor.frameGeometry().height()))  
                self.editor.parent().parent().setRowHeight (index.row(), editor.frameGeometry().height())
                self.editor.parent().parent().setColumnWidth (index.column(), editor.frameGeometry().width())
            else:
                editor.setGeometry(QRect(option.rect.left(), option.rect.top(), 100,  editor.frameGeometry().height()))  
                self.editor.parent().parent().setRowHeight (index.row(), editor.frameGeometry().height())
                self.editor.parent().parent().setColumnWidth (index.column(), editor.frameGeometry().width())
                
        
        else:
            editor.setGeometry(option.rect)   
        

        
