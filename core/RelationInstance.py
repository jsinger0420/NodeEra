# -*- coding: utf-8 -*-
"""
RelationInstance - manages a relation instance in the project.  
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
import uuid
from core.helper import Helper
from core.NeoTypeFunc import NeoTypeFunc

from forms.IRelFormatDlg import IRelFormat

FOUNDMATCH,  FOUNDNOMATCH, NOTFOUND = range(3)
########################################################################
# represents an actual relationship in Neo4j on the diagram
########################################################################        
class RelationInstance():
    ''' This represents one NodeEra managed relationship that can be on one or more diagrams.
        This class manages reading and writing the relationship to Neo4j
        The RelationItem class creates the arc graphics item and the text graphics item and draws them on the scene.
        startNode and endNode must be a node instance
    '''    
    def __init__(self, parent, relationInstanceDict=None, startNode=None, endNode=None, model=None):
        self.helper = Helper()
        self.neoTypeFunc = NeoTypeFunc()
        self.diagramType = "Instance Relationship"
        self.logMsg = None
        self.relationInstanceDict = relationInstanceDict
        
        self.parent = parent
        self.model = model
        self.neoCon = self.model.modelNeoCon
        
        self.relationship = None 

        # set local variables to what is in the dictionary
        if self.relationInstanceDict:
            self.relTemplate = self.relationInstanceDict.get("relTemplate", None)
            self.relName = self.relationInstanceDict.get("relName", "NoRelationshipName")
            self.propList = self.relationInstanceDict.get("properties", [])
            self.startNZID = self.relationInstanceDict.get("startNZID", None)
            self.endNZID = self.relationInstanceDict.get("endNZID", None)
            
            self.startNode = None
            self.endNode = None

            if self.relationInstanceDict.get("NZID", None) == None:
                self.NZID = str(uuid.uuid4())
            else:
                self.NZID = self.relationInstanceDict["NZID"]        
            self.neoID=self.relationInstanceDict.get("neoID", None)
        # if  no dictionary passed then set defaults
        else:
            self.relName = "NoRelationshipName"
            self.relTemplate = None
            self.propList = []
            self.NZID = str(uuid.uuid4())
            self.neoID=None
            self.startNZID = None
            self.endNZID = None
            self.startNode = None
            self.endNode = None
        
        # get start and end node item objects
        if not startNode is None:
            self.startNode = startNode
            self.startNZID = self.startNode.NZID
        if not endNode is None:
            self.endNode = endNode
            self.endNZID = self.endNode.NZID
       
        self.getFormat()

        if not self.relationInstanceDict:
            self.relationInstanceDict = self.getObjectDict()
            
    def reloadDictValues(self, ):
        '''
        This function will reset the local variables to the instance rel dictionary.
        This is needed when open diagram relationship instances need to be updated.
        '''
        index, relDict = self.model.getDictByName(topLevel="Instance Relationship",objectName=self.NZID)
        if relDict:
            # set local variables to what is in the dictionary
            self.relInstanceDict = relDict
            self.nodeTemplate = self.relInstanceDict.get("relTemplate", None)
            self.propList = self.relInstanceDict.get("properties", [])
            self.NZID = self.relInstanceDict["NZID"]        
            self.neoID=self.relInstanceDict.get("neoID", None)        
    
    def getFormat(self, ):
        '''
        determine if the rel instance has a template format or should use the project default format
        '''
        # get the default
        self.relFormat = IRelFormat(formatDict=self.model.modelData["IRformat"])
        # get a custom template format if there is one
        if not self.relTemplate is None:
            index, relTemplateDict = self.model.getDictByName(topLevel="Relationship Template",objectName=self.relTemplate)
            if not relTemplateDict is None:
                self.instanceRelFormatDict = relTemplateDict.get("IRformat", None)
                if not self.instanceRelFormatDict is None:
                    self.relFormat = IRelFormat(formatDict=self.instanceRelFormatDict) 
                    

    def getObjectDict(self, ):
        objectDict = {}
        objectDict["NZID"] = self.NZID
        objectDict["name"] = self.NZID
        objectDict["neoID"] = self.neoID
        objectDict["diagramType"] = self.diagramType
        objectDict["relName"] = self.relName        
        objectDict["properties"] = self.propList
        objectDict["startNZID"] = self.startNZID
        objectDict["endNZID"] = self.endNZID
        objectDict["relTemplate"] = self.relTemplate
        self.genRelSignature(objectDict)
        return objectDict
        
    def genRelSignature(self, relDict):
        '''generate the display name for a relationship instance
        '''
        if self.neoID is None:
            relID = self.NZID        
        else:
            relID = self.neoID
            
        if (self.startNode is None or self.startNode.neoID is None):
            fromID = "0"
        else:
            fromID = self.startNode.neoID
            
        if (self.endNode is None or self.startNode.neoID is None):
            toID = "0"
        else:
            toID = self.endNode.neoID            

        propList = self.helper.genPropValueList("n", relDict)
        signature = "({})-[{}:{} {}{}{}]->({})".format(str(fromID), str(relID), self.relName, "{", propList, "}", str(toID))
        relDict["displayName"] =  signature   
        
    def setLogMethod(self, logMethod=None):
        if logMethod is None:
            if self.logMsg is None:
                self.logMsg = self.noLog
        else:
            self.logMsg = logMethod
            
    def noLog(self, msg ):
        return
        
    def deleteRel(self, logMethod=None):
        '''This method deletes the relationship from the database.'''
        # set the logging method
        self.setLogMethod(logMethod)
        # if it doesn't have a neoID it's never been created in the db so nothing to delete
        if self.neoID is None:
            self.logMsg("The Relationship does not exist in the database.  Cannot delete.")
            return True, "No Relationship to delete."
        # delete the Relationship based on the neoID    
        cypher = "match ()-[r]->() where id(r) = " + str(self.neoID) + "  delete r"
        rc, msg = self.neoCon.runCypherAuto(cypher)
        self.logMsg(msg)
        return rc, msg


    def checkRelationship(self, logMethod=None):
        '''This method checks to see if a matching relationship exists in the database.
        '''
        # set the logging method
        self.setLogMethod(logMethod)
        # if it doesn't have a neoID it's never been created in the db so create a blank one
        if self.neoID is None:
            rc = NOTFOUND
            msg = "Diagram Relationship Doesn't Exist in the Graph"
            return rc, msg
        
        # see if the node still exists in the db based on the node id
        cypher = "match ()-[r]->() where id(r) = " + str(self.neoID) + " return r"
        rc, msg = self.neoCon.runCypherExplicit(cypher)
        if rc is False:
            self.logMsg(msg)
            msg = "Error Querying Graph."     
            return NOTFOUND,  msg
        else:
            if len(self.neoCon.resultSet) > 0:
                firstRec = self.neoCon.resultSet[0]
                if not firstRec is None:
                    self.relationship = firstRec["r"]  # the rel was found so set it
                    if self.compareRel():
                        return FOUNDMATCH, "Diagram Relationship Matches Graph"
                    else:
                        return FOUNDNOMATCH, "Diagram Relationship Doesn't Match Graph"
                else:
                    return NOTFOUND, "Diagram Relationship Doesn't Exist in Graph"
            else:
                return NOTFOUND,  "Diagram Relationship Doesn't Exist in Graph"
        return

    def compareRel(self):
        '''Compare the Relationship object retrieved from the database with the current state of the relationship item'''
        rc = True
        # need to check if the start and end nodes are the same
        pass
        # compare graph properties to diagram properties
        for propName, propVal in dict(self.relationship).items():
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
                if prop[0] in [propName for propName, propVal in dict(self.relationship).items() ]:
                    pVal = [propVal for propName, propVal in dict(self.relationship).items() if propName == prop[0]][0]
                    # does the datatype and data value match - special case for Float because the value could be an int or a float 
                    if (prop[1] == "Float" and self.neoTypeFunc.getNeo4jDataType(value=pVal) in ["Float", "Integer"] and prop[2] == self.neoTypeFunc.convertTypeToString(pVal) ):
                        continue
                    elif (prop[1] == self.neoTypeFunc.getNeo4jDataType(value=pVal) and prop[2] == self.neoTypeFunc.convertTypeToString(pVal)):
                        continue
                    else:
                        rc = False
                        break
                else:
                    # is the prop missing in the neo4j relationship because it's null on the diagram?
                    if prop[2] == "Null":
                        continue
                    else:
                        rc = False
                        break
            except:
                    rc = False
                    break
        
        return rc
        
    def getRelationship(self, logMethod=None):
        '''
        This method retrieves the relationship from Neo4j and sets the relationship object.  At this point the relationship object looks like it is in Neo4j
        '''
        # set the logging method
        self.setLogMethod(logMethod)
        # if there's no neoID then there isn't a relationship in neo4j
        if self.neoID is None:
            return None, "Relationship [{}] doesn't exist in Neo4j".format(self.neoID)
        # try to retrieve the relationship based on the neoid    
        cypher = "match ()-[r]->() where id(r) = " + str(self.neoID) + " return r"
        rc, msg = self.neoCon.runCypherAuto(cypher)
        if rc is False:
            return  rc, "Retrieve Relationship [{}] error - {}".format(self.neoID, msg) 
        else:
            # relationship found, save it
            firstRec = None
            if len(self.neoCon.resultSet) > 0:
                firstRec = self.neoCon.resultSet[0]
            if not firstRec is None:
                self.relationship = firstRec["r"]  # the rel was found so set it
                return True, "Relationship [{}] Found".format(self.neoID)            
            # relationship not found, it might have been deleted thru the backend
            else:
                return None, "Relationship [{}] Not Found".format(self.neoID)


    def createNewRelationship(self, logMethod=None):
        '''
        create a new relationship in neo4j based on the current state of the relation instance object
        '''
        # set the logging method
        self.setLogMethod(logMethod)
        # force creation of the start and end nodes in Neo4j if they don't exist
        rc, msg = self.startNode.getNode(logMethod)
        if rc == False:
            return rc, "Create Relationship error on from node - {}".format(msg)
        rc, msg = self.endNode.getNode(logMethod)
        if rc == False:
            return rc, "Create Relationship error on to node - {}".format(msg)
        
        # generate cypher stmt to create the relationship
        cypher = self.helper.genCreateRelCypher(relInstanceDict = self.getObjectDict(), rel = self.relationship, fromNeoID = self.startNode.neoID, toNeoID=self.endNode.neoID)
        # run the create 
        rc, msg = self.neoCon.runCypherAuto(cypher)      

        if rc is True:            
            firstRec = None
            if len(self.neoCon.resultSet) > 0:
                firstRec = self.neoCon.resultSet[0]
            if not firstRec is None:
                self.relationship = firstRec["r"]  # the rel was found so set it
                self.neoID = firstRec["id(r)"]
                self.relationInstanceDict["neoID"] = self.neoID
                return rc, "New Relationship Created - {}".format(msg)
        else:
            self.logMsg(msg)                
            return rc, "Create New Relationship [{}] error - {}".format(self.NZID, msg)
        
        return False, "Unexpected Error"
        
    def updateRelProps(self, ):
        '''
        set the properties of the relationship  object to what has been entered on the dialog
        '''
        # properties
        relProps = dict(self.relationship)
        #set all existing property values in the relationship object to None
        for key in relProps:
            self.relationship[key]=None
        # set all property values from the grid
        for property in self.propList:
            self.relationship[property[0]]=property[1]
            
    def updateRelationship(self, logMethod=None):
        '''
        relationship already exists, so all you can do is change the properties if any
        '''
        # set the logging method
        self.setLogMethod(logMethod)
        # generate cypher stmt to create the relationship 
        cypher = self.helper.genUpdateRelCypher(relInstanceDict = self.getObjectDict(), rel = self.relationship, relID = self.neoID)
        # run the create
        rc, msg = self.neoCon.runCypherAuto(cypher)    
        if rc is True:
            return rc, "Existing Relationship Updated - {}".format(msg)
        else:
            self.logMsg(msg)                
            return rc, "Update Existing Relationship [{}] error - {}".format(self.NZID, msg)        

        
    def syncToDB(self, logMethod=None):

        # get the relationship from the db, 
        rc, msg = self.getRelationship(logMethod)
        if rc is True:
            # relationship found in neo4j and relationship object set.  generate cypher to update relationship to look like the ui
            rc, msg = self.updateRelationship(logMethod)
            if rc is True:
                return rc, "Sync Relationship OK - {}".format(msg)
            else:
                return rc, "Sync Relationship Error - {}".format(msg)                
        elif rc is False:
            # error processing the match statement - big fail
            return rc, "Sync Relationship Error - {}".format(msg)   
            
        elif rc is None:
            # relationship object was not found in neo4j so create it
            rc, msg = self.createNewRelationship(logMethod)
            if rc is True:
                return rc, "Sync Relationship OK - {}".format(msg)
            else:
                return rc, "Sync Relationship Error - {}".format(msg)                

        else:
            return rc, "Unknown Sync Relationship Error - {}".format(msg)

    def syncFromDB(self, logMethod=None):
        # set the logging method
        self.setLogMethod(logMethod)     
        # should never happen, but if this instance rel has no neoID it can't be matched to a neo4j node so no way to sync it from neo4j
        if self.neoID is None:
            msg = "Error - this instance relationship has never been saved to Neo4j"
            self.helper.displayErrMsg("Sync From DB", msg)
            return False, msg
        rc, msg = self.getRelationship()
        if rc is True:
            # get the dictionary of properties from the relationship object  and convert it to a list
            props = []
            for key, val in dict(self.relationship).items():
                props.append( [key, self.neoTypeFunc.getNeo4jDataType(value=val),self.neoTypeFunc.convertTypeToString(dataValue=val) ])
            # set instance props to look like what's in the neo4j relationship object just retrieved    
            self.propList = props
            # update the object dictionary
            self.relationInstanceDict = self.getObjectDict()
            # save it to the design model
            self.saveToModel()
            return True, "Instance Relationship Synced"
        else:
            return False, "Error syncing Instance Relationship"        

    def saveToModel(self, ):
        # save the current state of the relation instance to the project model
        saveIndex = self.model.instanceTopLevelIndex("Instance Relationship", self.NZID)
        if not saveIndex is None:
            self.model.modelData["Instance Relationship"][saveIndex]=self.relationInstanceDict
