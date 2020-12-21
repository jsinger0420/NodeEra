#!/usr/bin/env python3
''' CypherGridGeneric
    This class generates cypher statements and is used by the generic datagrid widget.
    This class should be overridden to customize behaviour of the datagrid widget.
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
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS = range(5)
PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP, RELNAME = range(8)

class CypherGridGeneric():
    def __init__(self, parent=None, templateDict=None):
        self.parent = parent
        self.templateDict = templateDict
        self.type = None
        # helper contains many cypher generation functions
        self.helper = Helper()
            
    def isGeneric(self, ):
        '''
        this determines if the DataGridWidget should call genMatch on a grid refresh or should it suppy it's own cypher
        False - call genMatch as it provides a context specific match statement
        True - the application will supply it's own cypher to the grid
        '''
        return False
        
    # set which button driven functionality will be enabled on the grid   
        
    def refreshOK(self, ):
        return True        
    def exportOK(self, ):
        return False
    def newOK(self, ):
        return False
    def deleteOK(self, ):
        return False
    def rowSelect(self, ):
        return False        
    def setNullOK(self, ):
        return False

    def genDeleteDetach(self, row=None, dataGrid=None):
        '''
        this should be overridden to return a context specific delete cypher statement.
        this is called with the user clicks on the delete row button
        '''
        return "// no cypher generated"
       
    def genUpdateProp(self, updateIndex=None, dataGrid=None):
        '''
        this should be overridden to return a context specific match and property set cypher statement.
        this is called when an editable property column has changed in the grid
        '''
        return "// no cypher generated"


    def genRemoveProp(self, updateIndex=None, dataGrid=None):
        '''
        this should be overridden to return a context specific match and remove property cypher statement.
        this is called when an editable property column has been changed to null by the set null button on the data grid
        '''
        return "// no cypher generated"

    def genMatch(self):
        '''
        this should be overridden to return a context specific match and return cypher statement.
        isGeneric must be false for this method to be called by the datagrid.
        this is called when the grid is initially displayed or if the refresh button is clicked.
        both a cypher statement and an editParm dictionary must be returned.
        '''
        return "// no cypher generated"
        nodeName = "n"
        p1 = ""
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
        editParmDict.append( [NODE, False] )

        return cypher, editParmDict        

    
##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
## the following functions perform cypher generation tasks
##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#    def genReturnPropList(self, nodeName):
#        'return all properties in the template'
#        propList = ""
#        propList = ",".join(nodeName + "." + x[PROPERTY] + " as " + x[PROPERTY] + " \n" for x in self.templateDict["properties"] ) 
#        return propList
#    
#    def genSetPropList(self, nodeName):
#        'return a set statement for each property that has a default value (i.e. required)'
#        setPropList = []
#        if not self.templateDict is None:
#            for prop in self.templateDict["properties"]:
#                # if the property has a default value then generate the set statement.
#                if prop[PROPDEF] != "":
#                    # generate the correct syntax that you set the property equal to
#                    setEqualTo = self.helper.genPropEqualTo(dataValue=prop[PROPDEF], neoType = prop[DATATYPE])
#                    setPropList.append("set {}.{} = {}".format(nodeName, prop[PROPERTY], setEqualTo))
#        setProps = " \n ".join(setProp for setProp in setPropList)
#        return setProps        
               
