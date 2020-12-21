# -*- coding: utf-8 -*-

"""
NodeInstance.py provides a class to manage a Node in a Neo4j database.
The managed node can appear on many diagrams in a project.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
import uuid

from core.NeoTypeFunc import NeoTypeFunc
from core.helper import Helper

# ENUM for property grid
PROPERTY, DATATYPE, VALUE = range(3)      
# return codes from node check
FOUNDMATCH,  FOUNDNOMATCH, NOTFOUND = range(3)

class NodeInstance():
    ''' 
    This represents one node in a Neo4j instance that may be on one or more instance diagrams.
    This class manages reading and writing the node to Neo4j
    The NodeItem class manages displaying a NodeInstance on a diagram
    '''
    def __init__(self, parent=None, nodeInstanceDict=None, model=None):
        self.helper = Helper()
        self.neoTypeFunc = NeoTypeFunc()
        self.logMsg = None
        # neo4j node object - used for database operations
        self.node = None 
        self.diagramType = "Instance Node"
        self.model = model
        self.neoCon = self.model.modelNeoCon
        self.nodeInstanceDict = nodeInstanceDict

        # set local variables to what is in the dictionary
        if self.nodeInstanceDict:
            self.nodeTemplate = self.nodeInstanceDict.get("nodeTemplate", None)
            self.labelList = self.nodeInstanceDict.get("labels", [])
            self.propList = self.nodeInstanceDict.get("properties", [])
            if self.nodeInstanceDict.get("NZID", None) == None:
                self.NZID = str(uuid.uuid4())
            else:
                self.NZID = self.nodeInstanceDict["NZID"]        
            self.neoID=self.nodeInstanceDict.get("neoID", None)
        # if  no dictionary passed then set defaults
        else:
            self.nodeTemplate = None
            self.labelList = []
            self.propList = []
            self.NZID = str(uuid.uuid4())
            self.neoID=None
            # create the node instance dictionary
            self.nodeInstanceDict = self.getObjectDict()
            
        # remember current width and height
        self.oldNodeWidth = 0
        self.oldNodeHeight = 0

        
    def reloadDictValues(self, ):
        '''
        This function will reset the local variables to the instance node dictionary.
        This is needed when open diagram node instances need to be updated.
        '''
        index, nodeDict = self.model.getDictByName(topLevel="Instance Node",objectName=self.NZID)
        if nodeDict:
            # set local variables to what is in the dictionary
            self.nodeInstanceDict = nodeDict
            self.nodeTemplate = self.nodeInstanceDict.get("nodeTemplate", None)
            self.labelList = self.nodeInstanceDict.get("labels", [])
            self.propList = self.nodeInstanceDict.get("properties", [])
            self.NZID = self.nodeInstanceDict["NZID"]        
            self.neoID=self.nodeInstanceDict.get("neoID", None)


    def getDisplayName(self):
        label = self.labelList[0] if len(self.labelList)> 0 else "No Labels"
        property = self.propList[0] if len(self.propList)> 0 else "No Properties"
        name = "{}-{}-{}".format(label, property, self.NZID)
        return name
        
    def getObjectDict(self, ):
        '''
        This function returns a dictionary with all the data that represents this node instance.  
        '''
        objectDict = {}
        objectDict["name"] = self.NZID
        
        objectDict["NZID"] = self.NZID
        objectDict["neoID"] = self.neoID
        objectDict["diagramType"] = self.diagramType
        objectDict["nodeTemplate"] = self.nodeTemplate
        objectDict["labels"] = self.labelList
        objectDict["properties"] = self.propList
        self.genNodeSignature(objectDict)
        return objectDict

    def genNodeSignature(self, nodeDict):
        nodeID = self.neoID
        if self.neoID is None:
            nodeID = self.NZID
        lblList = self.helper.genLabelList("n", nodeDict)
        propList = self.helper.genPropValueList("n", nodeDict)
        signature = "({} {} {}{}{} )".format(str(nodeID), lblList, "{", propList, "}")
        nodeDict["displayName"] =  signature
        
    def setLogMethod(self, logMethod=None):
        if logMethod is None:
            if self.logMsg is None:
                self.logMsg = self.noLog
        else:
            self.logMsg = logMethod
            
    def noLog(self, msg):
        return
        
    def deleteNode(self, logMethod=None):
        '''This method deletes the node from the database.'''
        # set the logging method
        self.setLogMethod(logMethod)
        # if it doesn't have a neoID it's never been created in the db so nothing to delete
        if self.neoID is None:
            self.logMsg("The Node does not exist in the database.  Cannot delete.")
            return True, "No Node to delete."
        # delete the node based on the neoID    
        cypher = "match (n) where id(n) = " + str(self.neoID) + " detach delete n"
        rc, msg = self.neoCon.runCypherAuto(cypher)
        self.logMsg(msg)
        return rc, msg  

    def checkNode(self, logMethod=None):
        '''
          This method determines if the node instance matches the node that is 
          stored in the graph database.
        '''
        # set the logging method
        self.setLogMethod(logMethod)
        # if it doesn't have a neoID it's never been created in the db
        if self.neoID is None:
            rc = NOTFOUND
            msg = "Diagram Node with id({}) doesn't exist in graph".format(self.neoID)
            return rc, msg
        
        # see if the node still exists in the db based on the node id
        cypher = "match (n) where id(n) = {} return n".format(str(self.neoID)) 
        rc, msg = self.neoCon.runCypherExplicit(cypher)
        if rc is False:
            self.logMsg(msg)
            msg = "Error Querying Graph."     
            return NOTFOUND,  msg
        else:
            firstRec = None
            if len(self.neoCon.resultSet) > 0:
                firstRec = self.neoCon.resultSet[0] 
            if not firstRec is None:
                self.node =   firstRec["n"]
                if self.compareNode():
                    return FOUNDMATCH, "Diagram Node with id({}) matches node in Graph".format(self.neoID)
                else:
                    return FOUNDNOMATCH, "Diagram Node with id({}) doesn't match node in graph".format(self.neoID)
            else:
                return NOTFOUND, "Diagram Node with id({}) doesn't exist in graph".format(self.neoID)
                

    def compareNode(self):
        '''Compare the node object retrieved from the database with the current state of the node item'''
        rc = True
        # compare graph labels to diagram labels
        for lbl in self.node.labels:
            if [lbl] in self.labelList:
                continue
            else:
                rc = False
                break
        # compare diagram labels to graph labels
        for lbl in self.labelList:
            if lbl[0] in self.node.labels:
                continue
            else:
                rc = False
                break        
        # compare graph properties to diagram properties
        for propName, propVal in dict(self.node).items():
            try:
                dataType = self.neoTypeFunc.getNeo4jDataType(value=propVal)
                dataVal = self.neoTypeFunc.convertTypeToString(propVal)
                # special case as an integer is also a valid float
                if dataType == "Integer":
                    if ([propName, "Integer", dataVal] in self.propList or [propName, "Float", dataVal] in self.propList):
                        continue
                    else:
                        rc = False
                        break
                elif [propName, dataType, dataVal] in self.propList:
                    continue
                else:
                    rc = False
                    break
            except:
                rc = False
                break
                
        # compare diagram properties to graph properties
        for prop in self.propList:
            try:
                # is the property name one of the keys in the node
                if prop[0] in [propName for propName, propVal in dict(self.node).items() ]:
                    pVal = [propVal for propName, propVal in dict(self.node).items() if propName == prop[0]][0]
                    # does the datatype and data value match - special case for Float because the value could be an int or a float 
                    if (prop[1] == "Float" and self.neoTypeFunc.getNeo4jDataType(value=pVal) in ["Float", "Integer"] and prop[2] == self.neoTypeFunc.convertTypeToString(pVal) ):
                        continue
                    elif (prop[1] == self.neoTypeFunc.getNeo4jDataType(value=pVal) and prop[2] == self.neoTypeFunc.convertTypeToString(pVal)):
                        continue
                    else:
                        rc = False
                        break
                else:
                    # is the prop missing in the neo4j node because it's null on the diagram?
                    if prop[2] == "Null":
                        continue
                    else:
                        rc = False
                        break
            except:
                    rc = False
                    break
                
        
        return rc
            
    def getNode(self, logMethod=None):
        '''This method creates a node object
           based on the state of the node in the neo4j instance.
           If the node doesn't exist in the neo4j instance a new blank one is created
        '''
        # set the logging method
        self.setLogMethod(logMethod)
        
        # if it doesn't have a neoID it's never been created in the db so create a blank one
        if self.neoID is None:
            rc, msg = self.createBlankNode() 
            return rc, msg
        # try to retrieve the node based on the neoID    
        cypher = "match (n) where id(n) = " + str(self.neoID) + " return n"
        rc, msg = self.neoCon.runCypherExplicit(cypher)
        if rc is False:
            self.logMsg(msg)
            return rc, msg   
        else:
            firstRec = None
            if len(self.neoCon.resultSet) > 0:
                firstRec = self.neoCon.resultSet[0] 
            if not firstRec is None:
                self.node =   firstRec["n"]
                return True, "Node [{}] Found".format(self.neoID)
            else:
                rc,  msg = self.createBlankNode()   # the node wasn't found so it must have been deleted through the backend.  create a new node.  
                return rc, msg

        
    def createBlankNode(self, ):
        # new create node method
        cypher = "create (n) return id(n), n"

        rc, msg = self.neoCon.runCypherExplicit(cypher)

        if rc is True:
            firstRec = self.neoCon.resultSet[0]
            if not firstRec is None:
                self.neoID =  firstRec["id(n)"]
                self.nodeInstanceDict["neoID"] = self.neoID
                self.node = firstRec["n"]
            else:
                self.logMsg(msg)
            
        return rc, msg

        
    def syncToDB(self, logMethod = None ):
        # set the logging method
        self.setLogMethod(logMethod)
        #  add or update this node in the db'            
        rc, msg = self.getNode()
        if rc is True:
            # now update the node in the neo4j instance
            updateCypher = self.helper.genUpdateCypher(neoID = self.neoID, nodeInstanceDict = self.getObjectDict(),  node = self.node)
#            print("syncToDB {}".format(updateCypher))
            rc, msg = self.neoCon.runCypherAuto(updateCypher)
            return rc, msg
        else:
            return rc, msg

    def syncFromDB(self, logMethod=None):
        # set the logging method
        self.setLogMethod(logMethod)     
        # should never happen, but if this instance node has no neoID it can't be matched to a neo4j node so no way to sync it from neo4j
        if self.neoID is None:
            msg = "Error - this instance node has never been saved to Neo4j"
            self.helper.displayErrMsg("Sync From DB", msg)
            return False, msg
        rc, msg = self.getNode()
        if rc is True:
            # get the list of labels from the node object
            lbls = [[lbl] for lbl in self.node.labels]  
            # get the dictionary of properties from the node object  and convert it to a list
            props = []
            for key, val in dict(self.node).items():
                props.append( [key, self.neoTypeFunc.getNeo4jDataType(value=val),self.neoTypeFunc.convertTypeToString(dataValue=val) ])
            # set instance labels and props to look like what's in the neo4j node object just retrieved    
            self.nodeInstanceDict["labels"] = lbls
            self.nodeInstanceDict["properties"] = props
            self.genNodeSignature(self.nodeInstanceDict)
            return True, "Instance Node Synced"
        else:
            return False, "Error syncing Instance Node"


