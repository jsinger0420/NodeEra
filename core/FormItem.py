#!/usr/bin/env python3
'''    
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
'''

from PyQt5.QtCore import Qt

#############################################################################
# this super class defines information about an item used in a form definition.  This is inherited by all form item specific classes
#############################################################################


class FormItem():
    
    def __init__(self, parentID=None, itemName=None, root=None, description=None, itemDict=None,  idNum=None,  type=None):

        # initialize common properties of form items.  subclasses initialize their specific properties
        if not itemDict is None:
            self.itemDict = itemDict
        else:
            # build object based on individual values
            self.itemDict = {}
            self.itemDict["idNum"] = idNum
            self.itemDict["parentID"] = parentID
            self.itemDict["type"] = type
            self.itemDict["itemName"] = itemName
            self.itemDict["root"] = root
            self.itemDict["description"] = description

         
        self._treeItem = None 
        self._frame = None
        self._parentFrame = None
        self._widget = None

    def updateAttr(self, name=None, value=None):
        if name in self.itemDict:
            self.itemDict[name] = value
            
    def updateTreeView(self):
        self._treeItem.setText(0, self.displayName)
        
    def __str__(self, ):
        '''generate the display name for this form Item
        '''
        if self.itemDict["itemName"] is None:
            name = "Not Selected"
        else:
            name = self.itemDict["itemName"]
        return "{}:{}".format(str(self.itemDict["type"]), str(name))

    @property
    def frame(self):
        '''the frame this item is displayed in'''
        return self._frame
        
    @frame.setter
    def frame(self, value):
        self._frame   = value  

    @property
    def parentFrame(self):
        '''the parent frame this item is displayed in'''
        return self._parentFrame
        
    @parentFrame.setter
    def parentFrame(self, value):
        self._parentFrame   = value  
        
    @property
    def treeItem(self):
        '''the tree item this formItem is associated with'''
        return self._treeItem
        
    @treeItem.setter
    def treeItem(self, value):
        self._treeItem   = value  

    @property
    def widget(self):
        '''the tree item this formItem is associated with'''
        return self._widget
        
    @widget.setter
    def widget(self, value):
        self._widget   = value  
        
    @property
    def displayName(self):
        '''the text that is displayed on the treeview'''
        return str(self)


    def dict(self):
        '''returns a dictionary of the properties which is used to store in the design model file.'''
        return self.itemDict

''' 
FormDef defines the overall properties of the form
'''
class FormDef(FormItem):
    
    def __init__(self, itemName=None, root=None, description=None,  idNum=None,  parentID=None,  type=None , itemDict=None):
        super().__init__(itemName=itemName, root=root, description=description,  idNum=idNum,  parentID=parentID,  type=type, itemDict=itemDict)
    
        
    def attributes(self):
        '''Returns all the properties as a list of lists.  This is used to populate the metabox and control editing.  
          1st is the column name for the grid.
          2nd is the value itself.
          3rd is the editable indicator
          
          The properties saved to the design model are controlled by the dict() function.'''
        attrList = []
        attrList.append(["Type", "type", False])
        attrList.append(["Name", "itemName", True])
        attrList.append(["Description", "description", True])
        attrList.append(["ID", "idNum", False])
        attrList.append(["Parent ID", "parentID", False])
        
        return attrList
        
''' 
FormRowDef defines a row on the form
'''
class FormRowDef(FormItem):
    
    def __init__(self, itemName=None, root=None, description=None,  idNum=None,  parentID=None,  type=None, itemDict=None ):
        super().__init__(itemName=itemName, root=root, description=description,  idNum=idNum,  parentID=parentID,  type=type, itemDict=itemDict)
    
        
    def attributes(self):
        '''Returns all the properties as a list of lists.  This is used to populate the metabox and control editing.  
          1st is the column name for the grid.
          2nd is the value itself.
          3rd is the editable indicator
          
          The properties saved to the design model are controlled by the dict() function.'''
        attrList = []
        attrList.append(["Type", "type", False])
        attrList.append(["Name", "itemName", True])
        attrList.append(["Description", "description", True])
        attrList.append(["ID", "idNum", False])
        attrList.append(["Parent ID", "parentID", False])
        
        return attrList


''' 
LabelWidgetDef defines a label widget
'''
class LabelWidgetDef(FormItem):
    
    def __init__(self, itemName=None, root=None, description=None,  idNum=None, parentID=None,  type=None, itemDict=None ):
        # super init sets common properties
        super().__init__(itemName=itemName, root=root, description=description,  idNum=idNum,  parentID=parentID,  type=type, itemDict=itemDict)

        # initialize widget specific dictionary key/value pairs
        if not "widgetType" in self.itemDict:
            # build object based on individual values
            self.itemDict["widgetType"] = "Label"
        if not "text" in self.itemDict:
            self.itemDict["text"]  = "label text"        

        
    def attributes(self):
        '''Returns all the properties as a list of lists.  This is used to populate the metabox and control editing.  
          1st is the column name for the grid.
          2nd is the value itself.
          3rd is the editable indicator
          
          The properties saved to the design model are controlled by the dict() function.'''
        attrList = []
        attrList.append(["Type", "type", False])
        attrList.append(["Widget Type", "widgetType", True])
        attrList.append(["Text", "text", True])
        attrList.append(["Name", "itemName", True])
        attrList.append(["Description", "description", True])
        attrList.append(["ID", "idNum", False])
        attrList.append(["Parent ID", "parentID", False])
        
        return attrList


''' 
ButtonWidgetDef defines a button widget
'''
class ButtonWidgetDef(FormItem):
    
    def __init__(self, itemName=None, root=None, description=None,  idNum=None, parentID=None,  type=None, itemDict=None ):
        # super init creates itemDict and sets common properties
        super().__init__(itemName=itemName, root=root, description=description,  idNum=idNum,  parentID=parentID,  type=type, itemDict=itemDict)

        # initialize widget specific dictionary key/value pairs
        if not "widgetType" in self.itemDict:
            # build object based on individual values
            self.itemDict["widgetType"] = "Button"
        if not "text" in self.itemDict:
            self.itemDict["text"]  = "button text"        
        if not "action" in self.itemDict:
            self.itemDict["action"] =  "No_Action"
        
    def attributes(self):
        '''Returns all the properties as a list of lists.  This is used to populate the metabox and control editing.  
          1st is the column name for the grid.
          2nd is the value itself.
          3rd is the editable indicator
          
          The properties saved to the design model are controlled by the dict() function.'''
        attrList = []
        attrList.append(["Type", "type", False])
        attrList.append(["Widget Type", "widgetType", True])
        attrList.append(["Text", "text", True])
        attrList.append(["Name", "itemName", True])
        attrList.append(["Action", "action", True])
        attrList.append(["Description", "description", True])
        attrList.append(["ID", "idNum", False])
        attrList.append(["Parent ID", "parentID", False])
        
        return attrList
