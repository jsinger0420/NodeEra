#!/usr/bin/env python3
"""
- The NeoDriver class encapsulates all calls to the neo4j V4 python driver.  This class only makes use of the
native python driver.
- This replaces the original neocon class which encorporated a mixture of the native pythin  driver and py2neo

    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2020 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
    
"""
import datetime
import logging

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
from neo4j.exceptions import DriverError

from PyQt5.QtCore import QSettings

from core.helper import Helper

#############################################################################
# this class acts as a wrapper to the neo4j V4 python driver
#############################################################################
class NeoDriver():

    def __init__(self, name=None,  promptPW=None):
        self.name = name
        self.settings = QSettings()     
        self.neoDict = None
        self.helper = Helper()
        
        # setup the dictionary that defines this neo4j connection
        self.getSavedConnection()

        # if we prompted the user for a password, save it in the neocon dictionary
        if not promptPW is None:
            self.neoDict["password"] = promptPW
        
        # driver used by this NeoDriver object
        self.myDriver = None
        # session used for unmanaged transaction
        self.session = None
        # transaction used for unmanaged transaction
        self.tx = None
        # result object used while consuming query results and saving them to self.resultSet
        self.result = None
        # persistent result set and summary
        self.resultSet = None
        self.resultSummary = None
        
        # manage chunking your way thru a result set
        self.cursorChunk = None
        self.chunkStart = 0         # this is the record number of the first record in the chunk
        self.chunkEnd = 0           # this is the record number of the last record in the chunk
        self.chunkSize = 10     # some day we'll make this a parameter setting
        self.curRecord = 0          # this is the last record retrieved
        self.endReached = False
        
        # track query statistics
        self.stats = None 
        # default to true
        self.autoCommit = True
        # dictionary that gathers up facts about an individual cypher execution.
        self.cypherLogDict = {} 

    def logMsg(self, msg):

        if logging:
            logging.info(msg)      

    def logScript(self, script):
#        if logging:
#            logging.info(script)
#        print(script)
        return

    def logDriverStatus(self, ):
        return
        
#        if not self.myDriver is None:
#            driverStat = "Open"
#        else:
#            driverStat = "None"
#        if not self.session is None:
#            sessionStat = "Open"
#        else:
#            sessionStat = "None"
#        if not self.tx is None:
#            if self.tx.closed():
#                txStat = "Closed"
#            else:
#                 txStat = "Open"
#        else:
#            txStat = "None"
#            
#        if not self.result is None:
#            if self.result.peek() == None:
#                resultStat = "No Data Left"
#            else:
#                resultStat = "Data Remains"
#        else:
#            resultStat = "None"
#            
#        driverStatus = "Driver: {} Session: {} Txn: {} Result: {}".format(driverStat, sessionStat, txStat, resultStat)
#        print(driverStatus)
            
    def setAutoCommit(self, setting):
        self.autoCommit = setting
        
    def getSavedConnection(self, ):
        '''
        get the dictionary from a saved connection in settings and use it to initialize this neoDriver
        if you don't find it, then create a new blank dictionary'
        '''
        if not (self.name is None):
            self.neoDict = self.settings.value("NeoCon/connection/{}".format(self.name))
            if self.neoDict is None:
                self.neoDict = self.newNeoDriverDict()  
            else:
                self.name = self.neoDict["slot"]
        else:
            self.neoDict = self.newNeoDriverDict()        
            
    def newNeoDriverDict(self, ):
        # returns a default empty dictionary of neodriver properties
        neoDict = {}
        if self.name is None:
            neoDict["slot"] = "Unnamed"
        else:
            neoDict["slot"] = self.name
        neoDict["URL"] = "never connected"
        neoDict["port"] = ""
        neoDict["conType"] = ""
        neoDict["host"] = ""
        neoDict["userid"] = ""
        neoDict["password"] = ""
        neoDict["usesecure"] = "False"
        neoDict["prompt"] = "False"

        return neoDict
        
    def localNeoConDict(self, ):
        # returns a neoCon dictionary ready to access a localhost system using bolt
        neoDict = {}
        neoDict["slot"] = "LOCAL"
        neoDict["URL"] = "never connected"
        neoDict["port"] = "7687"
        neoDict["conType"] = "bolt"
        neoDict["host"] = "localhost"
        neoDict["userid"] = "neo4j"
        pw = self.helper.putText("neo4j")
        neoDict["password"] = pw
        neoDict["usesecure"] = "False"
        neoDict["prompt"] = "False"

        return neoDict
        
    def displayNode(self, node):
        '''return the string representation of the node or a blank string
        '''
        strNode = ""
        if not node is None:
            strNode = str(node)
        
        return strNode

    def displayRelationship(self, relationship):
        '''return the string representation of the relationship or a blank string
        '''
        strRel = ""
        if not relationship is None:
            strRel = str(relationship)
        
        return strRel        

    def runCypherAuto(self, cypherText, cypherParms=None):
        '''
            run a cypher in an automatic transaction.
            save the entire result.
        '''
        
        # first create the driver  object if we haven't done that yet
        if self.myDriver is not None:
            pass
        else:
            rc, msg = self.setDriver()
            if rc == False:
                return False, msg
                

        # now run the query and save the result set
        errSuffix = "Run Cypher Auto Error"
        try:
            rc = False
            self.cypherLogDict = {}
            self.cypherLogDict["error"] = ""
            self.cypherLogDict["startTime"] = datetime.datetime.now()  
            self.cypherLogDict["offset"] = -1
            self.cypherLogDict["cypher"] = cypherText
            
            # create a session
            self.logScript('aSession = aDriver.session()')
            self.session = self.myDriver.session()
            self.logDriverStatus()
            
            # run an autocommit transaction
            self.logScript('aResult = aSession.run({})'.format(cypherText))
            self.result = self.session.run(cypherText)
            self.logDriverStatus()
            
            # save the result as a list of records
            self.logScript('self.resultSet = []')
            self.logScript('for rec in self.result:')
            self.logScript('    self.resultSet.append(rec)')
            self.resultSet = []
            for rec in self.result:
                self.resultSet.append(rec)            
            
#            self.logScript('aResultSet = aResult.data()')
#            self.resultSet = self.result.data()
            self.logDriverStatus()
            
            # this gets the query stats
            self.logScript('aResultSummary = aResult.consume()')
            self.resultSummary = self.result.consume()
            self.logDriverStatus()
            
            rc = True
            msg = "Query Completed"
            
        except Neo4jError as e:
            msg =  "Neo4j Error :{} - {}".format(repr(e), errSuffix)
        except DriverError as e:
            msg =  "Driver Error :{} - {}".format(repr(e), errSuffix)
        except BaseException as e:
            msg =   "Base Exception :{} - {}".format(repr(e), errSuffix) 
            
        finally:
            self.cypherLogDict["endTime"] = datetime.datetime.now()
            
            # save query results if present
            if not self.resultSummary is None:
                if not self.resultSummary.plan is None:
                    self.cypherLogDict["plan"] = self.resultSummary.plan
                else:
                    self.cypherLogDict["plan"] = {}
                if not self.resultSummary.profile is None:
                    self.cypherLogDict["profile"] = self.resultSummary.profile
                else:
                    self.cypherLogDict["profile"] = {}
                if not self.resultSummary.counters is None:
                    self.stats = self.resultSummary.counters
                else:
                    self.stats  = None                    
            
            if rc == False:
                # save error message for log grid
                self.cypherLogDict["error"] = msg
                # see if there is a syntax error                
                if msg.find("CypherSyntaxError") > -1:
                    if msg.find("(offset: ") > -1:
                        self.cypherLogDict["offset"] =  int(msg[msg.find("(offset: ")+9 : msg.find(")", msg.find("(offset: ")) ])
            
            if not self.session is None:
                self.logScript('aSession.close()')
                self.session.close()
                self.logDriverStatus()
                
            return rc, msg         

    def runCypherExplicit(self, cypherText, parmData=None):
        '''  run a cypher query in an explicit txn
            consume the entire result set
            leave the transaction open for possible further queries
        '''
        

        # first create the driver  object if we haven't done that yet
        if self.myDriver is not None:
            pass
        else:
            rc, msg = self.setDriver()
            if rc == False:
                return False, msg
        
        try:
            rc = False
            errSuffix = "Run Cypher Explicit Error"   
            
            # create a session if we don't have one
            if self.session is None:
               self.logScript('aSession = aDriver.session()') 
               self.session =  self.myDriver.session()
               self.logDriverStatus()
               

                
            # get a new transaction if needed
            self.getNewTransaction()
            
            # now run the query 
            self.chunkStart = 0
            self.chunkEnd = 0    
            self.endReached = False
            self.cypherLogDict = {}
            self.cypherLogDict["error"] = ""
            self.cypherLogDict["offset"] = 0
            self.cypherLogDict["cypher"] = cypherText
            self.cypherLogDict["startTime"] = datetime.datetime.now()    

            if parmData is None:
                self.logScript('aResult = aTx.run("{}")'.format(cypherText))
                self.result = self.tx.run(cypherText)
                self.logDriverStatus()
            else:
                self.logScript('aResult = aTx.run("{}",parameters="{}"'.format(cypherText, parmData))
                self.result = self.tx.run(cypherText, parameters=parmData)
                self.logDriverStatus()
                

            # this consumes the entire result and saves it
#            self.logScript('aResultSet = aResult.data()')
            self.logScript('self.resultSet = []')
            self.logScript('for rec in self.result:')
            self.logScript('    self.resultSet.append(rec)')
            self.resultSet = []
            for rec in self.result:
                self.resultSet.append(rec)
            self.logDriverStatus()
            
            # this gets the query stats
            self.logScript('aResultSummary = aResult.consume()')
            self.resultSummary = self.result.consume()
            self.logDriverStatus() 
            
            # if autocommit is true then force a commit of this txn
            if self.autoCommit == True:
                self.commitTxn()
                             
            rc = True
            msg = "Cursor Created"
        except Neo4jError as e:
            msg =  "Neo4j Error :{} - {}".format(repr(e), errSuffix)
        except DriverError as e:
            msg =  "Driver Error :{} - {}".format(repr(e), errSuffix)
        except BaseException as e:
            msg =   "Base Exception :{} - {}".format(repr(e), errSuffix) 
        finally:
            self.cypherLogDict["endTime"] = datetime.datetime.now()
            # save query summary if present
            if not self.resultSummary is None:
                if not self.resultSummary.plan is None:
                    self.cypherLogDict["plan"] = self.resultSummary.plan
                else:
                    self.cypherLogDict["plan"] = {}
                if not self.resultSummary.profile is None:
                    self.cypherLogDict["profile"] = self.resultSummary.profile
                else:
                    self.cypherLogDict["profile"] = {}
                if not self.resultSummary.counters is None:
                    self.stats = self.resultSummary.counters
                else:
                    self.stats  = None                     

            if rc == False:
                # save error message for log grid
                self.cypherLogDict["error"] = msg
                # see if there is a syntax error
                if msg.find("SyntaxError") > -1:
                    if msg.find("(offset: ") > -1:
                        self.cypherLogDict["offset"] =  int(msg[msg.find("(offset: ")+9 : msg.find(")", msg.find("(offset: ")) ])

                # if we had an error then close the session
                if not self.session is None:
                    # if there's a transaction, then close it
                    if not self.tx is None:
                        self.closeTxn()
                        self.logDriverStatus()
                        
                    self.logScript('aSession.close()') 
                    self.session.close()
                    self.logDriverStatus()
                    
            return rc, msg  

    def forwardCursor(self, ):
        ctr = 0
        self.cursorChunk = []
        self.endReached = False
        try:
            errSuffix = "Error fetching rows"

            # make sure we have a result
            if not self.resultSet is None:
                # make sure there's at least one record
                if len(self.resultSet) > 0:
                    if len(self.resultSet) > self.chunkStart+self.chunkSize:
                        self.chunkEnd = self.chunkStart+self.chunkSize
                    else:
                        self.chunkEnd = len(self.resultSet)
                        self.endReached = True
                    # get the next chunk of records
                    for record in self.resultSet[self.chunkStart:self.chunkEnd]:
                        # append the next record to the chunk
                        self.cursorChunk.append(record)
                        ctr = ctr + 1
                        
                    self.chunkStart = self.chunkEnd
                    
                else:
                    self.endReached = True
                
            msg = "Fetch complete"
        except BaseException as e:
            msg =   "Base Exception :{} - {}".format(repr(e), errSuffix) 
        finally:
#            print('resultLen:{} chunkStart:{} chunkEnd:{}'.format(str(len(self.resultSet)), self.chunkStart, self.chunkEnd))
            return ctr, msg         
            
    def getNewTransaction(self, ):
        # create a new transaction if needed
        if self.tx is None:
            self.logScript('aTx = aSession.begin_transaction()')
            self.tx = self.session.begin_transaction()
            self.logDriverStatus()
            
            self.logMsg("Start first txn - AutoCommit = {}".format(self.autoCommit))
        else:
            if self.tx.closed() is True:
                self.logScript('aTx = aSession.begin_transaction()')
                self.tx = self.session.begin_transaction()
                self.logDriverStatus()
                
                self.logMsg("Start another txn - AutoCommit = {}".format(self.autoCommit))
            else:
                self.logMsg("Using the same transaction - AutoCommit = {}".format(self.autoCommit))    
                
    def commitTxn(self, ):
        '''
            if we are in a txn then commit it.
        '''
        try:
            rc = False
            errSuffix = "Commit Error"
            if not self.tx is None:
                if not self.tx.closed():
                    self.logScript('aTx.commit()')
                    self.tx.commit()
                    self.logDriverStatus()
                    
                    rc = True 
                    msg = "Transaction Committed"
                else:
                    rc = True
                    msg = "no active txn to commit"
            else:
                rc = True
                msg = "no txn exists to commit"
            
        except Neo4jError as e:
            msg =  "Neo4j Error :{} - {}".format(repr(e), errSuffix)
        except DriverError as e:
            msg =  "Driver Error :{} - {}".format(repr(e), errSuffix)
        except BaseException as e:
            msg =   "Base Exception :{} - {}".format(repr(e), errSuffix) 
        finally:
            self.logMsg(msg)
            return rc, msg             
        
    def closeTxn(self, ):
        '''
            if we are in a txn then close it.  uncommitted txn's will be rolled back
        '''
        try:
            rc = False
            errSuffix = "Txn Close Error"
            if not self.tx is None:
                if not self.tx.closed():
                    self.logScript('aTx.close() # implied rollback')
                    self.tx.close()
                    self.logDriverStatus()
                    
                    rc = True 
                    msg = "Transaction Closed"
                else:
                    rc = True
                    msg = "no active txn to close"
            else:
                rc = True
                msg = "no txn exists to close"
            
        except Neo4jError as e:
            msg =  "Neo4j Error :{} - {}".format(repr(e), errSuffix)
        except DriverError as e:
            msg =  "Driver Error :{} - {}".format(repr(e), errSuffix)
        except BaseException as e:
            msg =   "Base Exception :{} - {}".format(repr(e), errSuffix) 
        finally:
            self.logMsg(msg)
            return rc, msg             
        
        
    def rollbackTxn(self, ):    
        '''
            if we are in a txn then do a rollback.
        '''
        try:
            rc = False
            errSuffix = "RollBack Error"
            if not self.tx is None:
                if not self.tx.closed():
                    self.logScript('aTx.rollback()')
                    self.tx.rollback()
                    self.logDriverStatus()
                    
                    rc = True 
                    msg = "Transaction Rolled Back"
                else:
                    rc = True
                    msg = "no active txn to roll back"
            else:
                rc = True
                msg = "no txn exists to roll back"
            
        except Neo4jError as e:
            msg =  "Neo4j Error :{} - {}".format(repr(e), errSuffix)
        except DriverError as e:
            msg =  "Driver Error :{} - {}".format(repr(e), errSuffix)
        except BaseException as e:
            msg =   "Base Exception :{} - {}".format(repr(e), errSuffix) 
        finally:
            self.logMsg(msg)
            return rc, msg             
            
    def setDriver(self):
        # create a driver object to run transactions
        try:
            if self.myDriver is None:                
                rc = False
                errSuffix = "Driver Object Error"
                # get the keyword parameters from the necon dictionary
                uri = "bolt://{}:{}".format(self.neoDict["host"], self.neoDict["port"])
                # create a base driver graphdatabase object, this verifies connectivity and authentication and will produce usable error messages if anything is wrong.
                self.myDriver = None
                
                self.logScript('aDriver = GraphDatabase.driver({},auth=({},{})'.format(uri, self.neoDict['userid'], self.neoDict['password']))
                self.myDriver = GraphDatabase.driver(uri,auth=(self.neoDict['userid'], self.neoDict['password']))
                self.logDriverStatus()
                
                rc = True 
                msg = "Connection Created"
                # save the URI 
                self.neoDict["URL"] = uri
            else:
                rc = True
                msg = "Connection Exists"
        except Neo4jError as e:
            msg =  "Neo4j Error :{} - {}".format(repr(e), errSuffix)
        except DriverError as e:
            msg =  "Driver Error :{} - {}".format(repr(e), errSuffix)
        except BaseException as e:
            msg =   "Base Exception :{} - {}".format(repr(e), errSuffix) 
        finally:
            if rc == False:
                self.myDriver = None
            return rc, msg             
            

    def test(self):
        # test the connection to see if it is working
        # this will create a new driver object if none has been created or it will use the existing driver
        try:
            rc = False
            errSuffix = "Test Neo4j Connection: {}".format(self.name)
            rc, msg = self.runCypherAuto("match (n) return n limit 1")
            if rc == True:
                msg = "Connection Successful: {}".format(self.name)
        except Neo4jError as e:
            msg =  "Neo4j Error :{} - {}".format(repr(e), errSuffix)
        except DriverError as e:
            msg =  "Driver Error :{} - {}".format(repr(e), errSuffix)
        except BaseException as e:
            msg =   "Base Exception :{} - {}".format(repr(e), errSuffix) 
        finally:
            return rc, msg                     
