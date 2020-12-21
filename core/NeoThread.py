#!/usr/bin/env python3
"""
    Class NeoThread - This class runs cypher queries on a subthread so the main thread can run a timer and update the UI with progress
    Author: John Singer
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import QThread, pyqtSignal

class NeoThread(QThread):
    '''
    This class provides a thread that is used to call the  neoDriver runCypherExplicit function
    '''
    neoCallComplete = pyqtSignal(bool, str)
    
    def __init__(self, neoCon=None, cypher=None, mode=None, parmData=None):
        QThread.__init__(self)
#        print("NeoThread init")
        self.neoCon = neoCon
        self.cypher = cypher
        self.parmData = parmData
        self.mode = mode
        
        
    def run(self, ):
#        print("NeoThread Run")
        if self.mode == "cursor":
            if self.parmData is None:
                rc, msg = self.neoCon.runCypherExplicit(self.cypher)
                self.neoCallComplete.emit(rc, msg)
            else:
#                print("cypher:{} parms:{}".format(self.cypher, self.parmData))
                rc, msg = self.neoCon.runCypherExplicit(self.cypher, parmData = self.parmData)
                self.neoCallComplete.emit(rc, msg)
                
        elif self.mode == "query":
            rc, msg = self.neoCon.runCypherAuto(self.cypher)
            self.neoCallComplete.emit(rc, msg)
        else:
            rc = False
            msg = "Invalid mode"
            self.neoCallComplete.emit(rc, msg)
            
            
