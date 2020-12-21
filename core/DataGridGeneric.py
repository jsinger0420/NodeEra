#!/usr/bin/env python3
''' 
    DataGridGeneric
    This class provides configuration setup information to the DataGridWidget.  This customizes the 
    data grid to the specific use case as appropriate.
    Author: John Singer
    Copyright: SingerLinks Consulting LLC 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
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


