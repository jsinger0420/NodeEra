#!/usr/bin/env python3
''' RelTemplateCypher
    This class generates cypher statements based on a relationship template
    Author: John Singer
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
'''
from PyQt5.QtCore import Qt

from core.helper import Helper

LABEL, REQUIRED, NODEKEY = range(3)
#PROPERTY, DATATYPE, EXISTS, UNIQUE, PROPNODEKEY = range(5)
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS = range(5)
PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP, RELNAME = range(8)

class RelTemplateCypher():
    def __init__(self, parent=None, templateDict=None):
        self.parent = parent
        self.templateDict = templateDict
        self.type = "Relationship"
        self.helper = Helper()
        
    # this determines if the DataGridWidget should call genMatch on a grid refresh or should it suppy it's own cypher
    def isGeneric(self, ):
        return False
        
    # set which button driven functionality will be enabled        
        
    def refreshOK(self, ):
        return True        
    def exportOK(self, ):
        return True
    def newOK(self, ):
        return True
    def deleteOK(self, ):
        return True
    def rowSelect(self, ):
        return False        
    def setNullOK(self, ):
        return True

    def genDeleteDetach(self, row=None, dataGrid=None):
        model = dataGrid.model()
        # get the relID
        self.relID = None
        for header in range(model.columnCount()):
            if model.headerData(header, Qt.Horizontal, Qt.DisplayRole) == "rel_id":
                self.relID = model.item(row,header).data(Qt.EditRole)
        
        if not self.relID is None:
            p1 = self.relID
            cypher = " ".join(["match (f)-[r]->(t) \n", 
                                      "where id(r) = {} \n", 
                                      "delete r"
                                    ]).format(p1)
         
        return cypher

       
    def genUpdateProp(self, updateIndex=None, dataGrid=None):
        cypher = ""
        rc = True        
        model = dataGrid.model()
        # get the RELATIONSHIP ID
        self.relID = None
        for header in range(model.columnCount()):
            if model.headerData(header, Qt.Horizontal, Qt.DisplayRole) == "rel_id":
                self.relID = model.item(updateIndex.row(),header).data(Qt.EditRole)
        
        if self.relID is None:
            return False, "Relationship ID not found."
        
        try:
            self.updateData = model.item(updateIndex.row(),updateIndex.column()).data(Qt.EditRole)
            self.updateProp = model.headerData(updateIndex.column(), Qt.Horizontal, Qt.DisplayRole)
            # get the correct neo4j type 
            neoType = model.item(updateIndex.row(),updateIndex.column()).data(Qt.UserRole+1)
            # if the datatype comes back unknown then generate cypher comment
            if neoType == 'Unknown':
                cypher = "Can't update unknown datatype, correct datatype in relationship template."
                rc = False
            else:
                # generate the correct syntax that you set the property equal to
                self.setEqualTo = self.helper.genPropEqualTo(dataValue=self.updateData, neoType = neoType)
                p1 = self.relID
                p2 = self.updateProp
                p3 = self.setEqualTo
                
                cypher = " ".join(["match (f)-[r]->(t) \n", 
                                          "where id(r) = {} \n", 
                                          "set r.{} = {}"
                                        ]).format(p1, p2, p3)
                rc = True
                
        except BaseException as e:
            # something went wrong
            cypher = "Error generating cypher: {}".format(repr(e))
            rc = False
        finally:
            return rc, cypher

    def genRemoveProp(self, updateIndex=None, dataGrid=None):
        model = dataGrid.model()
        cypher = None
        self.relID = None
        # get the relID
        for header in range(model.columnCount()):
            if model.headerData(header, Qt.Horizontal, Qt.DisplayRole) == "rel_id":
                self.relID = model.item(updateIndex.row(),header).data(Qt.EditRole)
        if self.relID is None:
            return cypher
        # get the property name
        self.updateProp = model.headerData(updateIndex.column(), Qt.Horizontal, Qt.DisplayRole)        
        # MAKE SURE IT ISN'T A REQUIRED PROPERTY
        for prop in self.templateDict["properties"]:
            if prop[PROPERTY] == self.updateProp:
                if prop[PROPREQ] != Qt.Checked:
                    p1 = self.relID
                    p2 = self.updateProp
                    cypher = "match (f)-[r]->(t) \n where id(r) = {}  \n remove r.{} ".format(p1, p2)
                else:
                    self.helper.displayErrMsg("Set Null", "Property {} is required by the Relationship Template. Cannot remove this property.".format(self.updateProp))
        return cypher      

        
    def genMatch(self):
        '''
        Generate the match cypher statement that the data grid will use to refresh the grid.
        Generate the editParmDict dictionary that tells the data grid how to handle each column in the result set
        '''
#        fromNodeVar = "f"
#        toNodeVar = "t"
        relVar = "r"
        p1  = self.templateDict["relname"]
        p3 = self.genReturnPropList(relVar)
        if len(p3) > 1:
            p2 = ","
        else:
            p2 = ""

        
        cypher = " ".join(["match (f)-[r]->(t) \n", 
                    "where type(r) = '{}' \n", 
                    "return  id(f) as From_NodeID, \n" , 
                    "id(t) as To_NodeID, \n" , 
                    "id(r) as rel_id, \n", 
                    "type(r) as rel_name {} \n", 
                    "{} \n",
                    ]).format(p1, p2, p3)
        
#PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP, RELNAME        
        editParmDict = []
        editParmDict.append([NODEID, False])
        editParmDict.append([NODEID, False])  
        editParmDict.append([RELID, False])  
        editParmDict.append([RELNAME, False])          
        for prop in self.templateDict["properties"]:
            editParmDict.append([PROP, True])        
        
        return cypher, editParmDict
    
                
    def genReturnPropList(self, nodeName):
        'return all properties in the template'
        propList = ""
        propList = ",".join(nodeName + "." + x[PROPERTY] + " as " + x[PROPERTY] + " \n" for x in self.templateDict["properties"] ) 
        return propList
    
    def genSetPropList(self, nodeName):
        'return a set statement for each property that has a default value (i.e. required)'
        setPropList = []
        if not self.templateDict is None:
            for prop in self.templateDict["properties"]:
                # if the property has a default value then generate the set statement.
                if prop[PROPDEF] != "":
                    # generate the correct syntax that you set the property equal to
                    setEqualTo = self.helper.genPropEqualTo(dataValue=prop[PROPDEF], neoType = prop[DATATYPE])
                    setPropList.append("set {}.{} = {}".format(nodeName, prop[PROPERTY], setEqualTo))
        setProps = " \n ".join(setProp for setProp in setPropList)
        return setProps        
               
