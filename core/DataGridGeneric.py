#!/usr/bin/env python3
''' 
    DataGridGeneric
    This class provides configuration setup information to the DataGridWidget.  This customizes the 
    data grid to the specific use case as appropriate.
    Author: John Singer
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
'''
#from PyQt5.QtCore import Qt

LABEL, REQUIRED, NODEKEY = range(3)
PROPERTY, EXISTS, UNIQUE, PROPNODEKEY = range(4)
PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP, RELNAME = range(8)

class DataGridGeneric():
    def __init__(self, parent=None, ):
        self.parent = parent
        self.type = "Dynamic Cypher"
        self.templateDict = None
        self.cypher = ""
    
    # this determines if the DataGridWidget should call genMatch on a grid refresh or should it suppy it's own cypher
    def isGeneric(self, ):
        return True
        
    # set which button driven functionality will be enabled
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
        return False    


