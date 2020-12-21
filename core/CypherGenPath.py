#!/usr/bin/env python3
''' CypherGenPath
    This class generates cypher statements based on a path template and is used by the generic datagrid widget
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
'''
from PyQt5.QtCore import Qt
from core.CypherGridGeneric import CypherGridGeneric
from core.helper import Helper
from core.QueryPathNode import QueryPathNode

LABEL, REQUIRED, NODEKEY = range(3)
#PROPERTY, DATATYPE, EXISTS, UNIQUE, PROPNODEKEY = range(5)
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS = range(5)
PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP, RELNAME, UNKNOWN = range(9)
#enums for returnProps
PROPRETURN, PROPPARM, PROPNAME, COLNAME = range(4)

class CypherGenPath(CypherGridGeneric):
    def __init__(self, parent=None, templateDict=None):
        self.parent = parent
        self.templateDict = templateDict
        self.type = "Path"
        self.helper = Helper()
        self.designModel= self.parent.designModel
        
    # this determines if the DataGridWidget should call genMatch on a grid refresh or should it suppy it's own cypher
    def isGeneric(self, ):
        return False
        
    # set which button driven functionality will be enabled        
    # a path template can update properties and optional labels in the nodes and relationships in the path.
    # a path template cannot do an add new or a delete
        
    def refreshOK(self, ):
        return True        
    def exportOK(self, ):
        return True
    def newOK(self, ):
        return False
    def deleteOK(self, ):
        return False
    def rowSelect(self, ):
        return False        
    def setNullOK(self, ):
        return True

        
    def genMatch(self):
        '''generate a match return cypher statement for the entire path
        '''
        # create a list of the individual paths
        matchPatternList = []
        if len(self.templateDict["queryPath"]) < 1:
#            print("No path defined")
            return None, None
        # initialize the first match pattern
        matchPattern = []
        prevID = None
        for tvPathDict in self.templateDict["queryPath"]:
            # create the tree view path item object
            pathNode = QueryPathNode(designModel=self.designModel, nodeDict=tvPathDict)
#            print("{} id{} parent{}".format(pathNode.displayName, pathNode.order, pathNode.parentOrder))  
            if pathNode.type in ["Node", "Relationship"]:
                # is this the first node in the first matchpattern
                if (prevID is None):
                    # save the parent of this matchPattern
                    parentPathNode = QueryPathNode(designModel=self.designModel, nodeDict=tvPathDict)                    
                    # init new one
                    matchPattern = []
                    prevID = parentPathNode.order
                # is this the start of the 2nd or beyond matchPattern
                elif (pathNode.parentOrder != prevID):
                    # save the current match pattern
                    matchPatternList.append(matchPattern)  
                    # save the parent of this matchPattern which is further back up the tree
                    parentDict = [nodeDict for nodeDict in self.templateDict["queryPath"] if nodeDict.get("order", None) == parentPathNode.order][0]
                    parentPathNode = QueryPathNode(designModel=self.designModel, nodeDict=parentDict)                    
                    # init new one
                    matchPattern = []
                    prevID = parentPathNode.order       
                    # add to list
                    matchPattern.append(parentPathNode)                    
                if pathNode.type == "Node":
                    # add to list
                    matchPattern.append(pathNode)
                    prevID = pathNode.order
                if pathNode.type == "Relationship":
                    matchPattern.append(pathNode)
                    prevID = pathNode.order
                    
        # save the last match pattern created
        if len(matchPattern) > 0:
            # save the current one
            matchPatternList.append(matchPattern)  
                
        mp = 1
        cypher = ""
        patternList = []
        allVarList = []
        for matchPattern in matchPatternList:
#            print("Match Pattern {}".format(str(mp)))
            # initialize an empty variable list
            varList = []
            # initialize an empty match pattern
            cypherPattern = ""
            optionalPattern = False
            lastAddType = ""
            for qp in matchPattern:
                # save the variable name
                varList.append(qp.cypherVar)
                # add to the match pattern
                lastAddType = qp.type    
#                print("type:{}".format(lastAddType))
#                print("template {}".format(qp.templateName))
                if qp.type == "Node":
                    # save all the return properties
                    for prop in qp.returnProps:
                        if prop[PROPRETURN] == Qt.Checked:
                            # make sure the property isn't already in the list
                            if not prop[PROPNAME] in (prop[1] for prop in allVarList):
                                allVarList.append([qp.cypherVar, prop[PROPNAME], prop[COLNAME]])
                    
                    # save the node template name
                    lastNodeTemplate = qp.templateName
                    # get required labels for this node template
                    reqLbls = self.designModel.genReqLbls(qp.templateName)                    
                    if qp.templateName == "Anonymous Node":
                         # add the node to the current path
                         cypherPattern = cypherPattern + "( )"
                    else:
                        # add the node to the current path
                        cypherPattern = cypherPattern + "({}{})".format(str(qp.cypherVar), reqLbls )
                    # save it in case we need it for an optional match
                    saveNodePattern = "({}{})".format(str(qp.cypherVar), reqLbls )
                elif qp.type == "Relationship":
                    # save all the return properties
                    for prop in qp.returnProps:
                        if prop[PROPRETURN] == Qt.Checked:
                            # make sure the property isn't already in the list
                            if not prop[PROPNAME] in (prop[1] for prop in allVarList):
                                allVarList.append([qp.cypherVar, prop[PROPNAME], prop[COLNAME]])             
                    index, relDict = self.designModel.getDictByName(topLevel="Relationship Template",objectName=qp.templateName)
#                    print("relationship dict {}".format(relDict))
                    relType = self.designModel.getRelType(qp.templateName)
                    # if relationship is optional then must start a new pattern
#                    print("optional: {}".format(qp.optional))
                    if qp.optional == True:
                        # finish previous pattern
#                        print("pattern {}".format(cypherPattern))
                        patternList.append([optionalPattern, cypherPattern])
                        mp = mp + 1
                        # start a new pattern
                        varList = []
                        # initialize an empty match pattern
                        cypherPattern = ""
                        optionalPattern = True
                        lastAddType = ""
                        # add the last node of the previous pattern which is the first node in this optional  pattern
                        cypherPattern = cypherPattern + saveNodePattern
                        # add the relationship
                        # determine which way the direction is going and set arrow accordingly
                        if relDict["fromTemplate"] == lastNodeTemplate:
                            prefix = "-"
                            postfix = "->"
                        else:
                            prefix = "<-"
                            postfix = "-"      
                        if qp.templateName == "Anonymous Relationship":
                            cypherPattern = cypherPattern + "{}[ ]{}".format(prefix, postfix) 
                        else:
                            cypherPattern = cypherPattern + "{}[{}:{}]{}".format(prefix, qp.cypherVar, relType, postfix)
                        
                        
                    else:
                        if qp.templateName == "Anonymous Relationship":   
                            prefix = "-"
                            postfix = "-"                           
                            cypherPattern = cypherPattern + "{}[ ]{}".format(prefix, postfix)      
                        else:
                        # determine which way the direction is going and set arrow accordingly
                            if relDict["fromTemplate"] == lastNodeTemplate:
                                prefix = "-"
                                postfix = "->"
                            else:
                                prefix = "<-"
                                postfix = "-"    
                            cypherPattern = cypherPattern + "{}[{}:{}]{}".format(prefix, qp.cypherVar, relType, postfix)
                    
                
#            print("pattern {}".format(cypherPattern))
            patternList.append([optionalPattern, cypherPattern])
            mp = mp + 1
            optionalPattern = False
            
#        print(patternList)
#        print(allVarList)
        
        p1 = ",\n".join(pattern[1] for pattern in patternList if pattern[0]==False)
        p3 = "\n".join("\nOPTIONAL MATCH " + pattern[1] for pattern in patternList if pattern[0]== True) 
        p2 = ",\n".join("{}.{} AS {} ".format(var[0], var[1], var[2]) for var in allVarList)
        
        cypher = 'MATCH {} {} \n RETURN {}'.format(p1, p3, p2)

#PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP        
        editParmDict = []
        for var in allVarList:
            editParmDict.append( [PROP, False] )

        return cypher, editParmDict        
        
