#!/usr/bin/env python3
''' AddNodeCypher
    This class generates cypher statements for the copy node dialog box
    Author: John Singer

Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.

'''
PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP, RELNAME, UNKNOWN = range(9)
LABEL, REQUIRED, NODEKEY = range(3)
PROPERTY, EXISTS, UNIQUE, PROPNODEKEY = range(4)

class AddNodeCypher():
    def __init__(self,  ):
        
        self.type = "Generic Query"
        self.templateDict = None
        
    # this determines if the DataGridWidget should call genMatch on a grid refresh or should it suppy it's own cypher
    def isGeneric(self, ):
        return False
        
    # turn uneeded data grid buttons off
    def refreshOK(self, ):
        return False    
    def exportOK(self, ):
        return False
    def newOK(self, ):
        return False
    def deleteOK(self, ):
        return False
    def setNullOK(self, ):
        return False
        
    def rowSelect(self, ):
        return True

    def genDeleteDetach(self,  ):

        return None

    def genUpdateLabel(self, ):

        return None     
        
    def genUpdateProp(self, ):

        return None
        
    def genNewNode(self):

        return None    
        
    def genMatch(self, **kwargs):
        nodeTemplate = "No Template Selected"
        useTemplate = False
        if kwargs is not None:
            nodeTemplate = kwargs.get("nodeTemplate", "No Template Selected")
            self.templateDict = kwargs.get("nodeTemplateDict", None)
            useTemplate = kwargs.get("useTemplate", None)

            # query for all nodes, possibly filtered by node template
            if useTemplate == True:
                # user hasn't selected a template so don't run a query
                if nodeTemplate == "No Template Selected":
                    return None,  None
                else:
                    if not self.templateDict is None:
                        cypher, editParmDict = self.genTemplateMatch()
                        return cypher,  editParmDict
            else:
                editParmDict = [[UNKNOWN, False] for x in range(4)]
                cypher =    '''match (n) \n  return  id(n), \n labels(n), \n properties(n), \n n limit 10000'''
                return cypher,  editParmDict                

        # this shouldn't happen
        return None, None

    def genTemplateMatch(self):
        nodeName = "n"
        p1 = self.genWhereLabelList(nodeName)
        if len(p1) > 0:
            p1 = " where " + p1
        p2 = " id(" + nodeName +  ") as nodeID, \n n as Node  "
        p3 = self.genReturnLblList(nodeName)
        p4 = self.genReturnPropList(nodeName)
        if p3 != "":
            p2 = p2 + " , "
        if p4 != "" and p3 != "":
            p3 = p3 + " , "
        if p4 != "" and p3 == "":
            p2 = p2 + " , "
        if len(p1) > 0:
            p5 = ""
        else:
            p5 = " limit 5000"
            
        cypher = 'match (n) \n {} \n return  {} \n {} \n {} {}  '.format(p1, p2, p3, p4, p5)

#PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP        
        editParmDict = []
        editParmDict.append( [NODEID, False] )
        editParmDict.append( [NODE, False] )
        for label in self.templateDict["labels"]:
            editParmDict.append([REQLBL, False])
        for prop in self.templateDict["properties"]:
            editParmDict.append([PROP, False])
            
        return cypher, editParmDict
    
    def genWhereLabelList(self, nodeName):
        'only check for labels that are marked required'
        lblList = ""
        if len(self.templateDict["labels"]) > 0:
            lblList = nodeName + ":" + ":".join(x[LABEL] for x in self.templateDict["labels"] if x[REQUIRED] == 2)
        if lblList == "{}:".format(nodeName):
            return ""
        else:
            return lblList
            
    def genReturnPropList(self, nodeName):
        'return all properties in the template'
        propList = ""
        propList = ",".join(nodeName + "." + x[PROPERTY] + " as " + x[PROPERTY] for x in self.templateDict["properties"] ) 
        return propList
    
    def genReturnLblList(self, nodeName):
        'return all labels in the template'
        lblList = ""
        lblList = ",".join(nodeName + ":" + x[LABEL]  + " as " + x[LABEL] for x in self.templateDict["labels"] )
        return lblList        
