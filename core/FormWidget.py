#!/usr/bin/env python3
'''    
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
'''

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QToolButton



''' 
frameWidget defines a qframe used on a row formitem
'''
class FrameWidget(QFrame):
    
    def __init__(self, formItem=None, parentFrame=None ):
        
        super().__init__()
        self._formItem = formItem        
        # configure the frame
        self.setParent(parentFrame)
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Plain)
        self.setObjectName(formItem.itemDict["itemName"])        
        
        # create a layout for the frame
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setContentsMargins(1, 1, 1, 1)
        self.vLayout.setSpacing(1)
        self.vLayout.setObjectName("{}layout".format(formItem.itemDict["itemName"]))



    @property
    def formItem(self): 
        '''the formItem this widget is associated with'''
        return self._formItem
        
    @formItem.setter
    def formItem(self, value):
        self._formItem = value          
        

    def mousePressEvent(self, event):
        '''
        Process left button clicks
        '''
        if event.button()==Qt.LeftButton:
            print("clicked on {}".format(self.formItem.itemDict["itemName"]))
            
''' 
LabelWidget defines a qlabel
'''
class LabelWidget(QLabel):
    
    def __init__(self, formItem=None, parentFrame=None ):
        
        super().__init__()
        self._formItem = formItem        
        # configure the qlabel
        self.setParent(parentFrame)
        self.setObjectName(formItem.itemDict["itemName"])      
        self.size().setHeight(15)
        self.setText("this is a label")
        # add the label to its parents layout
        parentFrame.layout().addWidget(self)
        
    @property
    def formItem(self): 
        '''the formItem this widget is associated with'''
        return self._formItem
        
    @formItem.setter
    def formItem(self, value):
        self._formItem = value          
        

    def mousePressEvent(self, event):
        '''
        Process left button clicks
        '''
        if event.button()==Qt.LeftButton:
            print("clicked on {}".format(self.formItem.itemDict["itemName"]))
            print("font: {} height: {} width: {}".format(str(self.formItem.widget.font()),str(self.formItem.widget.height()), str(self.formItem.widget.width())))
            


''' 
ButtonWidget defines a qlabel
'''
class ButtonWidget(QToolButton):
    
    def __init__(self, formItem=None, parentFrame=None ):
        
        super().__init__()
        self._formItem = formItem        
        # configure the qbutton
        self.setParent(parentFrame)
        self.setObjectName(formItem.itemDict["itemName"])        
        self.setText("button text")
        # add the label to its parents layout
        parentFrame.layout().addWidget(self)
        
    @property
    def formItem(self): 
        '''the formItem this widget is associated with'''
        return self._formItem
        
    @formItem.setter
    def formItem(self, value):
        self._formItem = value          
        

    def mousePressEvent(self, event):
        '''
        Process left button clicks
        '''
        if event.button()==Qt.LeftButton:
            print("clicked on {}".format(self.formItem.itemDict["itemName"]))
