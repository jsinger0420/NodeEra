#!/usr/bin/env python3
'''    
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
'''

from PyQt5.QtCore import Qt

#############################################################################
# this class defines information about a node on the query path tree view
#############################################################################
#enums for propbox grid
PROPRETURN, PROPPARM, PROPNAME, COLNAME = range(4)

class QueryPathNode():
    
    def __init__(self, designModel=None, root=None, description=None, nodeDict=None,  order=None, parentOrder = None, type=None, 
                        templateName=None, cypherVar=None , optional=None, returnProps=None):
        self.designModel = designModel
        # build object based on dictionary
        if not nodeDict is None:
            self._treeItem = None
            self._order = nodeDict.get("order", 0)
            self._parentOrder = nodeDict.get("parentOrder", None)
            self._type = nodeDict.get("type", "Unknown")
            self._templateName = nodeDict.get("templateName", "Unknown")
            self._relType = self.designModel.getRelType(self._templateName)
            self._cypherVar = nodeDict.get("cypherVar", "")
            self._root = nodeDict.get("root", "False")
            self._description = nodeDict.get("description", "")
            self.optional = nodeDict.get("optional", False)
            self._returnProps = nodeDict.get("returnProps", [])
        else:
            # build object based on individual values
            self._treeItem = None
            self._order = order
            self._parentOrder = parentOrder
            self._type = type
            self._templateName = templateName
            self._relType = self.designModel.getRelType(self._templateName)
            self._cypherVar = cypherVar
            self._root = root
            self._description = description
            self._optional = optional
            if optional in [True, False]:
                self._optional = optional 
            elif optional == "True":
                self._optional = True
            elif optional == "False":
                self._optional = False
            else:
                self._optional = False

            if returnProps is None:
                self._returnProps = []
            else:
                self._returnProps = returnProps
                
        # get the template dictionary for this node or rel template 
        self.getTemplateDict()

        
    def __str__(self, ):
        '''generate the display name for this path node
        '''
        if self._type == "Node":
            if self._templateName == "Anonymous Node":
                return "( )"
            else:
                return "({}.{})".format(self._cypherVar, self._templateName)
        elif self._type == "Relationship":
            if self._templateName == "Anonymous Relationship":
                return "[ ]"
            else:
                return "[{}.{}]".format(self._cypherVar, self._templateName)
        elif self._type == "Path Template":
            return "Path Template"
        
        return "Unknown QueryPathNode type"
        
    @property
    def treeItem(self):
        '''the tree item this querypathnode is associated with'''
        return self._treeItem
        
    @treeItem.setter
    def treeItem(self, value):
        self._treeItem = value  

    @property
    def root(self):
        '''indicates that this object is the root of the query path tree'''
        return self._root
        
    @root.setter
    def root(self, value):
        '''insure the value is true or false'''
        if not value in [True, False]:
            self._root = False
        else:
            self._root = value  

        
    @property
    def order(self):
        '''defines the order of this object in the query path tree'''
        return self._order
        
    @order.setter
    def order(self, value):
        ''' insure order is an integer or None'''
        if value is None:
            self._order = None
            return
        try:
            value = int(value)
            self._order = value   
        except:
            raise ValueError("Order must be an integer")

    @property
    def parentOrder(self):
        '''defines the parentOrder of this object in the query path tree'''
        return self._parentOrder
        
    @parentOrder.setter
    def parentOrder(self, value):
        ''' insure order is an integer or None'''
        if value is None:
            self._parentOrder = None
            return
        try:
            value = int(value)
            self._parentOrder = value   
        except:
            raise ValueError("Order must be an integer")
            
    @property
    def type(self):
        '''defines the type of node on the query path tree'''
        return self._type
        
    @type.setter
    def type(self, value):
        '''insure the type is Node or Relationship'''
        if value is None:
            self._type = None
        elif not value in ["Node", "Relationship"]:
            raise ValueError("Type must be Node or Relationship")
        else:
            self._type = value  
            
    @property
    def templateName(self):
        '''the node or relationship template name this query path node is based on'''
        if self._templateName is None:
            returnStr = "No Template Selected"
        else:
            returnStr = self._templateName
            
        return returnStr
        
    @templateName.setter
    def templateName(self, value):
        self._templateName = value        
        # get new template dictionary and property list since the node/rel template changed
        self.getTemplateDict()
        self.loadPropList()
        if value == "No Template Selected":
            self._blankTemplate = True
            self.returnProps = []
        else:
            self._blankTempldate = False
        

    @property
    def relType(self):
        '''the relationship type.'''
        if self._relType is None:
            returnStr = "Unknown"
        else:
            returnStr = self.designModel.getRelType(self._templateName)
        return returnStr
        
    @relType.setter
    def relType(self, value):
        self._relType = value            

    @property
    def cypherVar(self):
        '''the cypher variable used to represent this node or relationship'''
        return self._cypherVar
        
    @cypherVar.setter
    def cypherVar(self, value):
        self._cypherVar = value     

    @property
    def description(self):
        '''a brief description of this item in the path tree'''
        return self._description
        
    @description.setter
    def description(self, value):
        self._description = value             

    @property
    def returnProps(self):
        '''a list of properties for the node or rel and an indicator if they are in the Return clause'''
        return self._returnProps
        
    @returnProps.setter
    def returnProps(self, value):
        self._returnProps = value             


    @property
    def optional(self):
        '''Identifies the relationship as optional in the query pattern'''
        return self._optional
        
    @optional.setter
    def optional(self, value):
        ''' insure optional is boolean'''
        if value is None:
            self._optional = False
            return
        try:
            if value in [True, False]:
                self._optional = value 
            elif value == "True":
                self._optional = True
            elif value == "False":
                self._optional = False
            else:
                self._optional = False
        except:
            raise ValueError("Optional must be True or False")

     
    @property
    def displayName(self):
        '''the text that is displayed on the treeview'''
        return str(self)

    def updateTreeView(self):
        self._treeItem.setText(0, self.displayName)
        
    def numReturnProps(self, ):
        '''count the number of props for this query path node that are returned'''
        numReturn = 0
        if not self._templateName in ["Anonymous Node", "Anonymous Relationship"]:
            for returnProp in self.returnProps:
                if returnProp[0] == Qt.Checked:
                    numReturn = numReturn + 1
        return numReturn
        
    def getTemplateDict(self):
        # get the template dictionary for this node or rel template
        if self.type in ["Node", "Relationship"]:
            index, templateDict = self.designModel.getDictByName(topLevel="{} Template".format(self.type),objectName=self.templateName)
            self.templateDict = templateDict
        else:
            self.templateDict = None 

    def updateProp(self, prop):
        if prop is None:
            return
        # only update a property that is in the list
        for propReturn in self._returnProps:
            if propReturn[PROPNAME] == prop[PROPNAME]:
                propReturn[PROPRETURN] = prop[PROPRETURN]
                propReturn[PROPPARM] = prop[PROPPARM]
                propReturn[COLNAME] = prop[COLNAME]
                
    def addProp(self, propName=None, propReturn=None, propParm=None, colName=None ):
#        PROPRETURN, PARAMETER, PROPNAME, COLNAME
        if propName is None:
            return
        # only add a property if itisn'talready in the list
        if not propName in (propReturn[PROPNAME] for propReturn in self._returnProps):
            self._returnProps.append([propReturn, propParm, propName, colName])
            
            
    def removeProp(self, propName=None):
        if propName is None:
            return
        if propName in self._returnProps:
            self._returnProps.remove(propName)    
    
    def updateAttr(self, name=None, value=None):
        if name == "Node Template":
            self.templateName = value
        if name == "Relationship Template":
            self.templateName = value
        if name == "Cypher Variable":
            self.cypherVar = value
        if name == "Description":
            self.description = value
        if name == "Optional":
            self.optional = value
        if name == "Blank Template":
            self.blankTemplate = value
            
    def attributes(self):
        '''Returns all the properties as a list of lists.  This is used to populate the metabox and control editing.  
          1st is the column name for the grid.
          2nd is the value itself.
          3rd is the editable indicator
          
          The properties saved to the design model are controlled by the dict() function.'''
        print (self.type)
        attrList = []
        if self.type in ["Node"]:
            attrList.append(["Node Template", self.templateName, True])
            attrList.append(["Cypher Variable", self.cypherVar, True])
            attrList.append(["Display Name", self.displayName, False])
            attrList.append(["Description", self.description, True])
        
        elif self.type == "Relationship":
            attrList.append(["Relationship Template", self.templateName, True])
            attrList.append(["Relationship Type", self.relType, False])
            attrList.append(["Cypher Variable", self.cypherVar, True])
            attrList.append(["Display Name", self.displayName, False])
            attrList.append(["Optional", self.optional, True])
            attrList.append(["Description", self.description, True])
            
        elif self.type == "Path Template":
            attrList.append(["Type", self.type, False])
            attrList.append(["Description", self.description, True])
            
#            attrList.append(["Type", self.type, False])
#            attrList.append(["Order", self.order, False])
#            attrList.append(["Parent Order", self.parentOrder, False])            
            
        return attrList

    def dict(self):
        '''returns a dictionary of the properties which is used to store in the design model file'''
        returnDict = {}
        if self.type in ["Node", "Relationship"]:
            returnDict["type"]=self.type
            returnDict["displayName"]=self.displayName
            returnDict["templateName"]=self.templateName
            returnDict["cypherVar"]=self.cypherVar
            returnDict["order"]=self.order
            returnDict["parentOrder"]=self.parentOrder
            returnDict["description"]=self.description
            returnDict["returnProps"]=self.returnProps
        if self.type in ["Relationship"]:
            returnDict["optional"]=self.optional
            returnDict["returnProps"]=self.returnProps
        if self.type == "Path Template": 
            returnDict["type"]=self.type
            returnDict["root"]=self.root
            returnDict["order"]=self.order
            returnDict["parentOrder"]=self.parentOrder
            
        return returnDict

    def loadPropList(self):
        '''load the properties from the template into the querypathnode.
          - only if blank template is false
          - clear existing property list first
          '''
        self.returnProps = []
        if not self._templateName in ["Anonymous Node", "Anonymous Relationship"]:
            # add node/rel props to the returnprops if they're not already there.
            if not self.templateDict is None:
                for prop in self.templateDict["properties"]:
                    colName = "{}_{}".format(self.cypherVar, prop[0])
                    self.addProp( propName=prop[0], propReturn=Qt.Unchecked, propParm=Qt.Unchecked, colName=colName )


        
#    def mergePropList(self):
#        '''this merges the return properties with the properties in the node/rel template
#          eliminate any return properties that are no longer in the template''' 
#        
#        # only return props if there is a template and blank template is false
#        if self.blankTemplate == False:
#            # add node/rel props to the returnprops if they're not already there.
#            if not self.templateDict is None:
#                for prop in self.templateDict["properties"]:
#                    colName = "{}_{}".format(self.cypherVar, prop[0])
#                    self.addProp( propName=prop[0], propReturn=Qt.Unchecked, propParm=Qt.Unchecked, colName=colName )
#                
#        return 
        
