# -*- coding: utf-8 -*-

"""
Module implementing FormMain.  This provides the UI widget for the zerocode data form
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFrame

from core.FormItem import FormDef, FormRowDef, LabelWidgetDef, ButtonWidgetDef
from core.FormWidget import FrameWidget, LabelWidget, ButtonWidget

from .Ui_FormMain import Ui_FormMain


class FormMain(QWidget, Ui_FormMain):
    """
    FormMain is a widget that displays and runs a user defined form
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FormMain, self).__init__(parent)
        # parent is the frame widget of the parent form that the form widget will be displayed in
        self.parent = parent
        self.setupUi(self)
        self.formDict = None
        self.formItemList = []
        self.topFrame = None
        
    def findParentItem(self, parentID = None):
        returnItem = None
        returnItem = [item for item in self.formItemList if item.itemDict["idNum"] == parentID]
        if len(returnItem) > 0:
            return returnItem[0]

    def clearForm(self):
        '''clear all generated widgets from the top level frame
        '''
        self.topFrame.setParent(None)
        del self.topFrame
        
    def frame_clicked(self, ):
        '''a frame was clicked on
        '''
        print("clicked on frame:".format())
        
    def generateForm(self, formDict=None):
        if not formDict is None:
            # create the list of form items
            self.formDict = formDict
            self.formItemList = []
            if not self.topFrame is None:
                self.clearForm()
            # generate fromes and widgets
            if len(self.formDict["formOutline"]) > 0:
                for formItemDict in self.formDict["formOutline"]:
                    # create the form item object and add it to the list
                    if formItemDict["type"] == "Form":
                        formItem = FormDef(itemDict=formItemDict)
                        self.formItemList.append(formItem)
                    if formItemDict["type"] == "Row":
                        formItem = FormRowDef(itemDict=formItemDict)
                        self.formItemList.append(formItem)
                    if formItemDict["type"] == "Widget":
                        if formItemDict["widgetType"] == "Label":
                            formItem = LabelWidgetDef(itemDict=formItemDict)  
                        if formItemDict["widgetType"] == "Button":
                            formItem = ButtonWidgetDef(itemDict=formItemDict) 
                        if not formItem is None:
                            self.formItemList.append(formItem) 
            else:
                print("no items defined for the form")
                return
            
            # create frame objects and populate with ui widgets
            for formItem in self.formItemList:
                if formItem.itemDict["type"] == "Form":
                    # add top level frame to the parent
                    print("add to top level layout")
                    # create frame object
                    self.topFrame = QFrame(self.frmMain)
                    self.topFrame.setFrameShape(QFrame.Panel)
                    self.topFrame.setFrameShadow(QFrame.Plain)
                    self.topFrame.setObjectName(formItem.itemDict["itemName"])
                    # create a layout for the frome on the UI_FormMain 
                    self.horizontalLayout = QtWidgets.QHBoxLayout(self.frmMain)
                    self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
                    self.horizontalLayout.setSpacing(1)
                    self.horizontalLayout.setObjectName("formMainLayout")                    
                    # add the forms top frame to it's parents layout
                    self.frmMain.layout().addWidget(self.topFrame)
                    # create a vertical layout for the frome
                    self.vLayout = QtWidgets.QVBoxLayout(self.topFrame)
                    self.vLayout.setContentsMargins(1, 1, 1, 1)
                    self.vLayout.setSpacing(1)
                    self.vLayout.setObjectName("{}layout".format(formItem.itemDict["itemName"]))
                    # tell this formItem what his frame is
                    formItem.frame = self.topFrame
                    # tell this formItem who is parent frame is
                    formItem.parentFrame = self.parent
                    
                    
                elif not formItem.itemDict["parentID"] is None:      
                    # get the parent formItem
                    parentItem = self.findParentItem(formItem.itemDict["parentID"])
                    print("add {}:{} to parent: {}".format(formItem.itemDict["type"], formItem.itemDict["itemName"], parentItem.itemDict["itemName"]))
                    if formItem.itemDict["type"] == "Row":
                        # create frame object
                        self.newFrame = FrameWidget(formItem=formItem,  parentFrame=parentItem.frame)
                        # add the frame to it's parents layout
                        parentItem.frame.layout().addWidget(self.newFrame)
                        # tell this formItem what his frame is
                        formItem.frame = self.newFrame
                        # tell this formItem who its parent frame is
                        formItem.parentFrame = parentItem.frame
                        
                    elif formItem.itemDict["type"] == "Widget":
                        if formItem.itemDict["widgetType"] == "Label":
                            # create label widget
                            newWidget = LabelWidget(formItem=formItem,  parentFrame=parentItem.frame)
                            newWidget.setText(formItem.itemDict["text"])
                        if formItem.itemDict["widgetType"] == "Button":
                            # create label widget
                            newWidget = ButtonWidget(formItem=formItem,  parentFrame=parentItem.frame)
                            newWidget.setText(formItem.itemDict["text"])
                        # tell this formItem who its widget and parent frame is
                        formItem.widget = newWidget
                        formItem.parentFrame = parentItem.frame
    
    def frameMousePress(self):
        print("frame mouse press")
