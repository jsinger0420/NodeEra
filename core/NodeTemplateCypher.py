#!/usr/bin/env python3
''' NodeTemplateCypher
    This class generates cypher statements based on a node template
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
'''

from PyQt5.QtCore import Qt

from core.helper import Helper

LABEL, REQUIRED, NODEKEY = range(3)
PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP, RELNAME = range(8)
# node template property list
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS, UNIQUE, PROPNODEKEY = range(7)

class NodeTemplateCypher():
    def __init__(self, parent=None, templateDict=None):
        self.parent = parent
        self.templateDict = templateDict
        self.type = "Node"
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
        # get the nodeID
        self.nodeID = "no node"
        for header in range(model.columnCount()):
            if model.headerData(header, Qt.Horizontal, Qt.DisplayRole) == "nodeID":
                self.nodeID = model.item(row,header).data(Qt.EditRole)

        cypher = 'match (n)  \n where id(n) = {}  \n detach delete n'.format(self.nodeID)
         
        return cypher

    def genUpdateLabel(self, updateIndex=None, dataGrid=None):
        model = dataGrid.model()
        # get the nodeID
        for header in range(model.columnCount()):
            if model.headerData(header, Qt.Horizontal, Qt.DisplayRole) == "nodeID":
                self.nodeID = model.item(updateIndex.row(),header).data(Qt.EditRole)
        
        # get if the checkbox is checked or not
        if model.item(updateIndex.row(),updateIndex.column()).checkState() == Qt.Checked:
            self.operation = "Set"
        else:
            self.operation = "Remove"
        
        # get the label name
        self.updateLabel = model.headerData(updateIndex.column(), Qt.Horizontal, Qt.DisplayRole)
            
        p1 = self.nodeID
        p2 = self.operation
        p3 = self.updateLabel
        cypher = 'match (n) \n where id(n) = {}  \n {} n:{} '.format(p1, p2, p3)
        
        return cypher     
        
    def genUpdateProp(self, updateIndex=None, dataGrid=None):
        cypher = ""
        rc = True
        model = dataGrid.model()
        self.nodeID = None
        # get the nodeID
        for header in range(model.columnCount()):
            if model.headerData(header, Qt.Horizontal, Qt.DisplayRole) == "nodeID":
                self.nodeID = model.item(updateIndex.row(),header).data(Qt.EditRole)
        if self.nodeID is None:
            return False, "Node ID not found."
        
        try:
            # get the new data value which is a string
            self.updateData = model.item(updateIndex.row(),updateIndex.column()).data(Qt.EditRole)
            # get the property name
            self.updateProp = model.headerData(updateIndex.column(), Qt.Horizontal, Qt.DisplayRole)
            # get the correct neo4j type 
            neoType = model.item(updateIndex.row(),updateIndex.column()).data(Qt.UserRole+1)
            # if the datatype comes back unknown then generate cypher comment
            if neoType == 'Unknown':
                cypher = "Can't update unknown datatype, correct datatype in node template."
                rc = False
            else:
                # generate the correct syntax that you set the property equal to
                self.setEqualTo = self.helper.genPropEqualTo(dataValue=self.updateData, neoType = neoType)
                p1 = self.nodeID
                p2 = self.updateProp
                p3 = self.setEqualTo
                cypher = "match (n) \n where id(n) = {}  \n set n.{} = {} ".format(p1, p2, p3)
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
        self.nodeID = None
        # get the nodeID
        for header in range(model.columnCount()):
            if model.headerData(header, Qt.Horizontal, Qt.DisplayRole) == "nodeID":
                self.nodeID = model.item(updateIndex.row(),header).data(Qt.EditRole)
        if self.nodeID is None:
            return cypher
            
        # get the property name
        self.updateProp = model.headerData(updateIndex.column(), Qt.Horizontal, Qt.DisplayRole)
        # MAKE SURE IT ISN'T A REQUIRED PROPERTY
        for prop in self.templateDict["properties"]:
            if prop[PROPERTY] == self.updateProp:
                if prop[PROPREQ] != Qt.Checked:
                    p1 = self.nodeID
                    p2 = self.updateProp
                    cypher = "match (n) \n where id(n) = {}  \n remove n.{} ".format(p1, p2)
                else:
                    self.helper.displayErrMsg("Set Null", "Property {} is required by the Node Template. Cannot remove this property.".format(self.updateProp))
        return cypher      
            
    def genNewNode(self):
        nodeName = "n"
        p1 = self.genWhereLabelList(nodeName)
        p11 = self.genSetPropList(nodeName)
        p2 = " id(" + nodeName +  ") as nodeID "
        p3 = self.genReturnLblList(nodeName)
        p4 = self.genReturnPropList(nodeName)
        if p3 != "":
            p2 = p2 + " , "
        if p4 != "" and p3 != "":
            p3 = p3 + " , "
        if p4 != "" and p3 == "":
            p2 = p2 + " , "
            
        cypher = 'create ({}) \n {} \n return  {} \n {} \n {} '.format(
                    p1, p11, p2, p3, p4
                    )
        return cypher    

    def genMatchReturnNodeOnly(self):
        nodeName = "n"
        p1 = self.genWhereLabelList(nodeName)
        if len(p1) > 0:
            p1 = " where " + p1
        p2 = " id(" + nodeName +  ") as nodeID "
        p3 = " n as Node"
            
        cypher = 'match (n) \n {} \n return  {}, \n {} '.format(
                    p1, p2, p3
                    )

#PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP        
        editParmDict = []
        editParmDict.append( [NODEID, False] )
#        editParmDict.append( [PROP, False] )
#        editParmDict.append( [NODE, False] )
        for label in self.templateDict["labels"]:
            if label[REQUIRED] == 2:
                editParmDict.append([REQLBL, False])
            else:
                editParmDict.append([OPTLBL, True])
        for prop in self.templateDict["properties"]:
            editParmDict.append([PROP, True])
            
        return cypher, editParmDict        
        
    def genMatch(self):
        nodeName = "n"
        p1 = self.genWhereLabelList(nodeName)
        if len(p1) > 0:
            p1 = " where " + p1
#        p2 = " id(" + nodeName +  ") as nodeID, \n n.NZID, \n n as Node "
        p2 = " id(" + nodeName +  ") as nodeID "
        p3 = self.genReturnLblList(nodeName)
        p4 = self.genReturnPropList(nodeName)
        if p3 != "":
            p2 = p2 + " , "
        if p4 != "" and p3 != "":
            p3 = p3 + " , "
        if p4 != "" and p3 == "":
            p2 = p2 + " , "
            
        cypher = 'match (n) \n {} \n return  {} \n {} \n {}  '.format(
                    p1, p2, p3, p4
                    )

#PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP        
        editParmDict = []
        editParmDict.append( [NODEID, False] )
#        editParmDict.append( [PROP, False] )
#        editParmDict.append( [NODE, False] )
        for label in self.templateDict["labels"]:
            if label[REQUIRED] == 2:
                editParmDict.append([REQLBL, False])
            else:
                editParmDict.append([OPTLBL, True])
        for prop in self.templateDict["properties"]:
            editParmDict.append([PROP, True])
            
        return cypher, editParmDict
    
    def genWhereLabelList(self, nodeName):
        'only check for labels that are marked required'
        lblList = ""
        if len(self.templateDict["labels"]) > 0:
            lblList = nodeName + ":" + ":".join(x[LABEL] for x in self.templateDict["labels"] if x[REQUIRED] == 2)
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
                    

