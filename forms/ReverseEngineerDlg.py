# -*- coding: utf-8 -*-

"""
Module implementing dlgReverseEngineer.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QStandardItemModel,  QStandardItem
from PyQt5.QtWidgets import QDialog, QAbstractButton
from PyQt5.QtWidgets import QApplication, QHeaderView
from .Ui_ReverseEngineerDlg import Ui_dlgReverseEngineer

from datetime import datetime
from core.helper import Helper
from core.NeoTypeFunc import NeoTypeFunc

# results columns for node templates
GENERATE, TEMPLATENAME, LABELPATTERN, PROPERTYPATTERN, NODECOUNT = range(5)
# results columns for rel templates
GENERATE, RELTEMPLATENAME, RELATIONSHIPNAME, FROMTEMPLATE, TOTEMPLATE, RELPROPERTYPATTERN, RELCOUNT, RELKEY = range(8)
# constraint and index
CONTYPE, CONLBL, CONPROP, CONPROPLIST = range(4)
AUTOINDEX, IDXLBL, IDXPROPLIST = range(3)

class dlgReverseEngineer(QDialog, Ui_dlgReverseEngineer):
    """
    This dialog box provides a facility to scan a neo4j database and generate node and relationship templates
    """
    def __init__(self, parent=None, schemaModel = None, model = None, settings = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(dlgReverseEngineer, self).__init__(parent)
        self.parent=parent
        self.schemaModel = schemaModel
        self.echo = True
        self.settings=settings
        self.model=model
        self.helper = Helper()
        self.neoTypeFunc = NeoTypeFunc()
        self.myNeoCon = self.model.modelNeoCon
        self.setupUi(self)
        self.initPage()

    def initPage(self, ):
        # header area
        self.editNeoURL.setText("{} - {}".format( self.myNeoCon.name, self.myNeoCon.neoDict["URL"]))
        self.cbScanNodes.setCheckState(Qt.Checked) 
        self.cbScanRels.setCheckState(Qt.Checked) 
        # count of nodes and rels
        self.countStuff()
        # update percents
        self.testScan()
        # results area
        self.clearResults()
        # buttons
        self.stopScan = False
        self.btnStop.setEnabled(False)
        self.btnStart.setEnabled(True)

        
    def countStuff(self, ):
        # get max ID's in use
        try:
            cypher = '''call dbms.queryJmx("org.neo4j:instance=kernel#0,name=Primitive count") yield attributes
                        with  keys(attributes) as k , attributes
                        unwind k as row
                        return "ID Allocations" as type,row,attributes[row]["value"]
                     '''
            #run the query
            rc1, msg1 = self.myNeoCon.runCypherAuto(cypher)
            if rc1:
                self.maxRelId = 0
                self.maxNodeId = 0
                for row in self.myNeoCon.resultSet:
                    if row["row"] == 'NumberOfNodeIdsInUse':
                        self.maxNodeId = row['attributes[row]["value"]']
                    if row["row"] == 'NumberOfRelationshipIdsInUse':
                        self.maxRelId = row['attributes[row]["value"]']
                msg = "Max Node ID: {} Max Relationship ID: {}".format(self.maxNodeId, self.maxRelId )        
#                    self.editNumNodes.setText(str(self.myNeoCon.resultSet[0]["count(*)"]))
            else:
                msg = "Get Max ID Error {}".format(msg1)
        except BaseException as e:
            msg = "{} - Get Max ID failed.".format(repr(e))
        finally: 
            QApplication.restoreOverrideCursor()
            self.displayScanMsg(msg) 
        
        # get number of nodes
        try:
            cypher = "MATCH (n) RETURN count(*)"
            #run the query
            rc1, msg1 = self.myNeoCon.runCypherAuto(cypher)
            if rc1:
                msg = "Counted {} Nodes.".format(str(self.myNeoCon.resultSet))
                self.editNumNodes.setText(str(self.myNeoCon.resultSet[0]["count(*)"]))
            else:
                msg = "Count Nodes Error {}".format(msg1)
        except BaseException as e:
            msg = "{} - Node Count failed.".format(repr(e))
        finally: 
            QApplication.restoreOverrideCursor()
            self.displayScanMsg(msg)   
            
        # get number of rels
        try:
            cypher = "MATCH ()-[r]->() RETURN count(*)"
            #run the query
            rc1, msg1 = self.myNeoCon.runCypherAuto(cypher)
            if rc1:
                msg = "Counted {} Relationships.".format(str(self.myNeoCon.resultSet))
                self.editNumRels.setText(str(self.myNeoCon.resultSet[0]["count(*)"]))
            else:
                msg = "Count Relationships Error {}".format(msg1)
        except BaseException as e:
            msg = "{} - Relationships Count failed.".format(repr(e))
        finally: 
            QApplication.restoreOverrideCursor()
            self.displayScanMsg(msg) 
                
    def clearResults(self, ):
        # message text area
        self.editProgress.clear()
        # NODE results grid
#        GENERATE,, TEMPLATENAME, LABELPATTERN, PROPERTYPATTERN
        self.gridTemplates.setModel(self.createResultsModel())
        self.gridTemplates.setColumnWidth(GENERATE, 50)
        self.gridTemplates.setColumnWidth(TEMPLATENAME, 150)
        self.gridTemplates.setColumnWidth(LABELPATTERN, 300)
        self.gridTemplates.setColumnWidth(PROPERTYPATTERN, 300)
        self.gridTemplates.setColumnWidth(NODECOUNT, 100)

        header = self.gridTemplates.horizontalHeader()
        header.setSectionResizeMode(GENERATE, QHeaderView.Fixed)  
        header.setSectionResizeMode(TEMPLATENAME, QHeaderView.Interactive)  
        header.setSectionResizeMode(LABELPATTERN, QHeaderView.Interactive)      
        header.setSectionResizeMode(PROPERTYPATTERN, QHeaderView.Interactive)  
        header.setSectionResizeMode(NODECOUNT, QHeaderView.Fixed)  
        
        # RELATIONSHIP results grid
#       GENERATE, RELTEMPLATENAME, RELATIONSHIPNAME, FROMTEMPLATE, TOTEMPLATE, RELPROPERTYPATTERN = range(6)
        self.gridTemplates_Rel.setModel(self.createRelResultsModel())
        self.gridTemplates_Rel.setColumnWidth(GENERATE, 50)
        self.gridTemplates_Rel.setColumnWidth(RELTEMPLATENAME, 150)
        self.gridTemplates_Rel.setColumnWidth(RELATIONSHIPNAME, 125)
        self.gridTemplates_Rel.setColumnWidth(FROMTEMPLATE, 150)
        self.gridTemplates_Rel.setColumnWidth(TOTEMPLATE, 150)
        self.gridTemplates_Rel.setColumnWidth(RELPROPERTYPATTERN, 300)
        self.gridTemplates_Rel.setColumnWidth(RELCOUNT, 100)
        self.gridTemplates_Rel.setColumnWidth(RELKEY, 100)

        header = self.gridTemplates_Rel.horizontalHeader()
        header.setSectionResizeMode(GENERATE, QHeaderView.Fixed)  
        header.setSectionResizeMode(RELTEMPLATENAME, QHeaderView.Interactive)
        header.setSectionResizeMode(RELATIONSHIPNAME, QHeaderView.Interactive)  
        header.setSectionResizeMode(FROMTEMPLATE, QHeaderView.Interactive)   
        header.setSectionResizeMode(TOTEMPLATE, QHeaderView.Interactive)      
        header.setSectionResizeMode(RELPROPERTYPATTERN, QHeaderView.Interactive)      
        header.setSectionResizeMode(RELCOUNT, QHeaderView.Fixed)      
        header.setSectionResizeMode(RELKEY, QHeaderView.Fixed) 
        
    def createRelResultsModel(self):
#       GENERATE, TEMPLATENAME, RELATIONSHIPNAME, FROMTEMPLATE, TOTEMPLATE, PROPERTYPATTERN = range(6)
        model = QStandardItemModel(0, 8)
        model.setHeaderData(GENERATE, Qt.Horizontal, "")
        model.setHeaderData(RELTEMPLATENAME, Qt.Horizontal, "Template Name")
        model.setHeaderData(RELATIONSHIPNAME, Qt.Horizontal, "Relationship Name")
        model.setHeaderData(FROMTEMPLATE, Qt.Horizontal, "From Node Template")
        model.setHeaderData(TOTEMPLATE, Qt.Horizontal, "To Node Template")
        model.setHeaderData(RELPROPERTYPATTERN, Qt.Horizontal, "Property Pattern")
        model.setHeaderData(RELCOUNT, Qt.Horizontal, "# Scanned")
        model.setHeaderData(RELKEY, Qt.Horizontal, "Unique Key")
        model.dataChanged.connect(self.templateRelGridChanged)
        return model  

    def createResultsModel(self):
#        GENERATE, TEMPLATENAME, LABELPATTERN, PROPERTYPATTERN
        model = QStandardItemModel(0, 5)
        model.setHeaderData(GENERATE, Qt.Horizontal, "")
        model.setHeaderData(TEMPLATENAME, Qt.Horizontal, "Template Name")
        model.setHeaderData(LABELPATTERN, Qt.Horizontal, "Label Pattern")
        model.setHeaderData(PROPERTYPATTERN, Qt.Horizontal, "Property Pattern")
        model.setHeaderData(NODECOUNT, Qt.Horizontal, "# Scanned")
        model.dataChanged.connect(self.templateGridChanged)
        return model  
        
    def addResultRow(self, model, c1, c2, c3, c4, c5):
#        GENERATE, TEMPLATENAME, LABELPATTERN, PROPERTYPATTERN, COUNT
        item1 = QStandardItem(c1)
        item1.setEditable(True)
        item1.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item2 = QStandardItem(c2)
        item3 = QStandardItem(c3)
        item3.setEditable(False)  
        item4 = QStandardItem(c4)
        item4.setEditable(False)    
        item5 = QStandardItem(c5)
        item5.setEditable(False)    
        if c1 in [0, 1, 2]:
            item1.setCheckState(c1)  
        else:
            item1.setCheckState(Qt.Unchecked)  
        
        model.appendRow([item1,item2, item3, item4, item5])          
        
    def addRelResultRow(self, model, c1, c2, c3, c4, c5, c6, c7, c8):
#       GENERATE, RELTEMPLATENAME, RELATIONSHIPNAME, FROMTEMPLATE, TOTEMPLATE, PROPERTYPATTERN, COUNT
        item1 = QStandardItem(c1)
        item1.setEditable(True)
        item1.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item2 = QStandardItem(c2)
        # save the original rel templatename in case the user renames it on the grid.
        item2.setData(c2, Qt.UserRole)
        item3 = QStandardItem(c3)
        item3.setEditable(False)        
        item4 = QStandardItem(c4)
        item4.setEditable(False)  
        item5 = QStandardItem(c5)
        item5.setEditable(False)   
        item6 = QStandardItem(c6)
        item6.setEditable(False)            
        item7 = QStandardItem(c7)
        item7.setEditable(False)       
        item8 = QStandardItem(c8)
        item8.setEditable(False)            
        if c1 in [0, 1, 2]:
            item1.setCheckState(c1)  
        else:
            item1.setCheckState(Qt.Unchecked)  
        
#        print(c1, c2, c3, c4, c5, c6, c7, c8)
        model.appendRow([item1,item2, item3, item4, item5, item6, item7, item8])      
        
    def newScan(self, ):
        self.clearResults()
        self.patternList = []           # keeps track of the unique label combinations
#        self.patternListCount = []   # keeps track of the number of nodes matching the unique label combinations in patternList
        self.relPatternListCount = [] 
        self.nodeDict = {}            # dictionary to hold discovered node patterns
        self.relDict = {}               # dictionary to hold discovered relationship patterns
        

    def displayScanMsg(self, text):
        if self.echo:
            # display on UI
            self.editProgress.appendPlainText("{}: {}".format(str(datetime.now()), text))
            QApplication.processEvents()
        # add real logging here
#        logging.info(text)    
    
    def logMessage(self, msg):
        if self.echo:
            # display on UI
            self.browserOutput.append(msg)
            QApplication.processEvents()
#        logging.info(msg)        

    def templateGridChanged(self, index1, index2):
        '''
        The user can over write the automatically generted Node template name.
        This needs to be recorded in the nodeDict template dictionary so it
        can be properly generated.
        '''
        if index1.column() == TEMPLATENAME:
#            print("row - {}, col - {}, data - {}".format(index1.row(), index1.column(), index1.data(role = Qt.DisplayRole)))
#            print("before:{}".format(self.nodeDict["{0:0>5}".format(index1.row())]))
            beforeTemplateName = self.nodeDict["{0:0>5}".format(index1.row())]["templateLblName"]            
            afterTemplateName =  index1.data(role = Qt.DisplayRole)
            #update the node pattern dictionary with the new name
            try:
                self.nodeDict["{0:0>5}".format(index1.row())]["templateLblName"] = afterTemplateName
                # update the rel dict
                for key, value in self.relDict.items():
                    if value["toTemplate"] == beforeTemplateName:
                        value["toTemplate"] = afterTemplateName
                    if value["fromTemplate"] == beforeTemplateName:
                        value["fromTemplate"] = afterTemplateName  
                # update the rel template grid on the UI
                model = self.gridTemplates_Rel.model()
                numrows = model.rowCount() 
                for row in range(0,numrows):
                    curRelTemplateName = model.item(row,RELTEMPLATENAME).data(Qt.EditRole)
                    if model.item(row,FROMTEMPLATE).data(Qt.EditRole) == beforeTemplateName:
                        model.setData(model.index(row, FROMTEMPLATE), afterTemplateName )
                        model.setData(model.index(row, RELTEMPLATENAME), curRelTemplateName.replace(beforeTemplateName,afterTemplateName ) )
                    if model.item(row,TOTEMPLATE).data(Qt.EditRole) == beforeTemplateName:
                        model.setData(model.index(row, TOTEMPLATE), afterTemplateName )
                        model.setData(model.index(row, RELTEMPLATENAME), curRelTemplateName.replace(beforeTemplateName,afterTemplateName ) )

            except:
                pass
#                print("error")
                
            finally:
                pass
#                print("AFTER:{}".format(self.nodeDict["{0:0>5}".format(index1.row())]))

    def templateRelGridChanged(self, index1, index2):
        '''
        The user can over write the automatically generated Relationship template name.
        '''
        return

                
    @pyqtSlot()
    def on_btnStart_clicked(self):
        """
        Reverse Engineer The current Graph.
        Create Node and Relationship templates
        """
        # switch to the progress tab
        self.tabWidget.setCurrentIndex(0)
        
        # for now, must scan nodes
        if self.cbScanNodes.isChecked() == False:
            self.cbScanNodes.setCheckState(Qt.Checked)
            
        #setup for a new scan    
        self.newScan()
        self.stopScan = False
        self.btnStop.setEnabled(True)
        self.btnStart.setEnabled(False)
        
        # do the scan
        self.scanAll()

        # reset the buttons
        self.btnStop.setEnabled(False)
        self.btnStart.setEnabled(True)
        
        # switch to the results tab
        self.tabWidget.setCurrentIndex(1)
        

    def getDataTypes(self, nodeID=None, relID = None,  propDataTypeDict=None, propList=None):            
            if not nodeID is None:
                returnPropList = self.genReturnPropList("n", propList)
                if len(returnPropList) > 0:
                    cypher = "match (n) where id(n) = {} return {}".format(str(nodeID), returnPropList )
                else:
                    return
            if not relID is None:
                returnPropList = self.genReturnPropList("r", propList)
                if len(returnPropList) > 0:
                    cypher = "match ()-[r]->() where id(r) = {} return {}".format(str(relID), returnPropList )
                else:
                    return
                    
            #run the query
            rc1, msg1 = self.myNeoCon.runCypherAuto(cypher)
            if rc1:
                record = self.myNeoCon.resultSet[0]
                # get the datatype for each property
                # value has the correct python object for each cell in the result set
                for index, value in record.items():
                    if not value is None:
                        dataType = self.neoTypeFunc.getNeo4jDataType(value)
                        propDataTypeDict[index] = dataType
                
                
    def genReturnPropList(self, nodeName, propList):
        'return all properties in the template'
        genPropList = ""
        genPropList = ",".join(nodeName + "." + x + " as " + x for x in propList ) 
        return genPropList        


    def scanAll(self, ):
        msg = "Scan finished"
        if self.cbScanNodes.isChecked() == True:
            # scan the nodes
            self.displayScanMsg("Start Scanning Nodes.")
            limitAmt = self.spinProcessSize.value()
            skipIncrement = self.spinSkipAmt.value()
            skipAmt = 0
            totAmt = 0
            self.moreData = True
            try:
                while (self.moreData and self.stopScan == False):
                    rc = False
                    cypher = "match (n) return id(n) as nodeID, labels(n), keys(n) skip {} limit {}".format(str(skipAmt), str(limitAmt))
                    #run the query
                    rc1, msg1 = self.myNeoCon.runCypherAuto(cypher)
                    if rc1 == True:                    
                        x = self.processModelChunk()
                        if x > 0:
                            totAmt = totAmt + x 
                            self.displayScanMsg("Skip to: {} Processed: {} Total Processed {} Nodes.".format(str(skipAmt), str(limitAmt),totAmt))
                            skipAmt = skipAmt + limitAmt + skipIncrement
                        else:
                            self.moreData = False
                            rc = True
                            msg = "Scan Nodes complete"                                  
                    else:
                        msg = "Scan Nodes Error {}".format(msg1)
                        self.moreData = False                    


            except BaseException as e:
                msg = "{} - Node Scan failed.".format(repr(e))
            finally: 
                self.displayScanMsg(msg)
            # add scanned node templates to the grid
            if self.stopScan == False:
                self.genNodeResult()

        if self.cbScanRels.isChecked() == True:        
            # scan the relationships
            self.displayScanMsg("Start Scanning Relationships.")
            limitAmt = self.spinProcessSize.value()
            skipIncrement = self.spinSkipAmt.value()
            skipAmt = 0
            totAmt = 0
            self.moreData = True
            try:
                while (self.moreData and self.stopScan == False):     
                    rc = False
                    cypher = "match (f)-[r]->(t) return id(r), keys(r), type(r), labels(f), labels(t) skip {} limit {}".format(str(skipAmt), str(limitAmt))
                    #run the query
                    rc1, msg1 = self.myNeoCon.runCypherAuto(cypher)
                    if rc1:
                        x = self.processRelModelChunk()
                        if x > 0:
                            totAmt = totAmt + x 
                            self.displayScanMsg("Skip to: {} Processed: {} Total Processed {} Relationships.".format(str(skipAmt), str(x),totAmt))
                            skipAmt = skipAmt + limitAmt + skipIncrement
                        else:
                            self.moreData = False
                            rc = True
                            msg = "Scan Relationships complete"                                  
                    else:
                        msg = "Scan Relationships Error {}".format(msg1)
                        self.moreData = False
                            
            except BaseException as e:
                msg = "{} - Relationships Scan failed.".format(repr(e))
            finally: 
                self.displayScanMsg(msg) 
                
            if self.stopScan == False:
                self.genRelResult()   
           
            return rc, msg
        
    def processModelChunk(self, ):
        ctr = 0
        for record in self.myNeoCon.resultSet:
            ctr = ctr + 1
            labels = record["labels(n)"]
            props = record["keys(n)"] 
            nodeID = record["nodeID"]
            try:
                x = self.patternList.index(labels)
                patternName = "{0:0>5}".format(x)
            except ValueError:
                nextx = len(self.patternList)
                self.patternList.insert(nextx, labels)
                patternName = "{0:0>5}".format(nextx)
                self.nodeDict[patternName]={}
                self.nodeDict[patternName]["propList"] = []
                self.nodeDict[patternName]["labelList"] = labels
                self.nodeDict[patternName]["templateName"] = "Node{}".format(patternName)
                self.nodeDict[patternName]["templateLblName"] = "{}".format("_".join(labels))
                self.nodeDict[patternName]["propDataType"] = {}
                self.nodeDict[patternName]["count"] = 0
            finally:
                count = self.nodeDict[patternName]["count"] + 1
                self.nodeDict[patternName]["count"] = count
                # get datatypes for newly discovered properties
                newProps = list(set(props) - set(self.nodeDict[patternName].get("propList", [])))
                if len(newProps) > 0:
                    self.getDataTypes(nodeID=nodeID, propDataTypeDict=self.nodeDict[patternName]["propDataType"], propList=newProps )
                # merge in any newly discovered properties
                self.nodeDict[patternName]["propList"] = list(set(self.nodeDict[patternName].get("propList", [])+props))
        return ctr
    
    def processRelModelChunk(self, ):
        ctr = 0
        for record in self.myNeoCon.resultSet:
            ctr = ctr + 1
            relProps = record["keys(r)"]
            relType = record["type(r)"]
            fromLbls = record["labels(f)"]
            toLbls = record["labels(t)"]
            relID = record["id(r)"]
            # get from and to node templates
            fromTemplate = "Unknown"
            toTemplate = "Unknown"
            for nodepattern, nodedata in self.nodeDict.items():
                if nodedata["labelList"]==fromLbls:
                    fromTemplate = nodedata["templateLblName"]
                if nodedata["labelList"] == toLbls:
                    toTemplate = nodedata["templateLblName"]
            try:
                relKey = "{}:{}:{}".format(relType, fromTemplate, toTemplate )
                # check to see if the relKey entry in the dictionary already exists, if it doesn't you get a KeyError
                check = self.relDict[relKey]
            except KeyError:
                # count how many times the relType has been used in a rel template
                countReltypeUsed = self.countRelType(relType)
                # the relkey doesn't exist so add it to the dictionary
                self.relDict[relKey]={}
                self.relDict[relKey]["propList"] = []
                self.relDict[relKey]["propDataType"] = {}
                if countReltypeUsed > 0:
                    self.relDict[relKey]["templateName"] = "{0}{1:0>3}".format(relType, countReltypeUsed)
                else:
                    self.relDict[relKey]["templateName"] = relType
                self.relDict[relKey]["relName"] = relType
                self.relDict[relKey]["fromTemplate"] = fromTemplate
                self.relDict[relKey]["toTemplate"] = toTemplate                
                self.relDict[relKey]["count"] = 0
            finally:
                count = self.relDict[relKey]["count"] + 1
                self.relDict[relKey]["count"] = count
                # get datatypes for newly discovered properties
                newProps = list(set(relProps) - set(self.relDict[relKey].get("propList", [])))
                if len(newProps) > 0:
                    self.getDataTypes(relID = relID, propDataTypeDict=self.relDict[relKey]["propDataType"], propList=newProps )
                # merge in the properties
                self.relDict[relKey]["propList"] = list(set(self.relDict[relKey].get("propList", [])+relProps))            
        
        return ctr
        
    def countRelType(self, relType):
        cnt = 0
        for key in self.relDict.keys() :
            if self.relDict[key]["relName"]==relType:        
                cnt = cnt + 1
        return cnt
        
    def testScan(self):
        '''simulate the scan to get total nodes and percent nodes
        '''
        # simulate Node Count
        self.stopScan = False
        totNodes = int(self.editNumNodes.text())
        nodesRemaining = totNodes
        totRels = int(self.editNumRels.text())
        relsRemaining = totRels
        limitAmt = self.spinProcessSize.value()
        skipIncrement = self.spinSkipAmt.value()
        skipAmt = 0
        totAmt = 0
        self.moreData = True        
        try:
            while (self.moreData and self.stopScan == False):
                if nodesRemaining > limitAmt:
                    x = limitAmt
                    nodesRemaining = nodesRemaining - limitAmt  - skipIncrement
                else:
                    x = nodesRemaining
                    nodesRemaining = 0
                if x > 0:
                    totAmt = totAmt + x 
#                    print("Skip to: {} Processed: {} Total Processed {} Nodes.".format(str(skipAmt), str(limitAmt),totAmt))
                    skipAmt = skipAmt + limitAmt + skipIncrement
                else:
                    self.moreData = False                 
            else:
                self.moreData = False                    
        except BaseException as e:
            self.helper.displayErrMsg ("Calcuate Percents","{} - Error Calculating Percents.".format(repr(e)))
        finally: 
            # update UI
            self.txtNodeScanAmt.setText(str(totAmt))
            displayPercent = "{0:.0%}".format(totAmt/totNodes)
            self.txtNodePercent.setText(displayPercent)

        # simulate Rel Count
        self.stopScan = False
        totRels = int(self.editNumRels.text())
        relsRemaining = totRels
        limitAmt = self.spinProcessSize.value()
        skipIncrement = self.spinSkipAmt.value()
        skipAmt = 0
        totAmt = 0
        self.moreData = True        
        try:
            while (self.moreData and self.stopScan == False):
                if relsRemaining > limitAmt:
                    x = limitAmt
                    relsRemaining = relsRemaining - limitAmt  - skipIncrement
                else:
                    x = relsRemaining
                    relsRemaining = 0
                if x > 0:
                    totAmt = totAmt + x 
#                    print("Skip to: {} Processed: {} Total Processed {} Nodes.".format(str(skipAmt), str(limitAmt),totAmt))
                    skipAmt = skipAmt + limitAmt + skipIncrement
                else:
                    self.moreData = False                 
            else:
                self.moreData = False                    
        except BaseException as e:
            self.helper.displayErrMsg ("Calcuate Percents","{} - Error Calculating Percents.".format(repr(e)))
        finally: 
            # update UI
            self.txtRelScanAmt.setText(str(totAmt))
            if totRels == 0 or totRels is None:
                displayPercent = "{0:.0%}".format(0)
            else:
                displayPercent = "{0:.0%}".format(totAmt/totRels)
            self.txtRelPercent.setText(displayPercent)
    
    def genNodeResult(self, ):
        '''
        Scan the reverse engineered node dictionary and create Node Template rows in the grid
        GENERATE, TEMPLATENAME, LABELPATTERN, PROPERTYPATTERN        
        '''
        for key in sorted(self.nodeDict.keys()):
            value = self.nodeDict[key]
            self.addResultRow(self.gridTemplates.model(), Qt.Checked, str(value["templateLblName"]), str(value["labelList"]), str(value["propList"]), str(value["count"]) )            
#            print("{}-{} {}".format(key, value["labelList"], value["propList"]))    

    def genNodeTemplates(self, ):
        '''
        Scan the reverse engineered node dictionary and create Node Templates
        GENERATE, TEMPLATENAME, LABELPATTERN, PROPERTYPATTERN
        '''
        # generate node templates
        model = self.gridTemplates.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            genFlag = model.item(row,GENERATE).checkState()
            # is the pattern checked?
            if genFlag == Qt.Unchecked:
                continue
            if self.genNodeTemplate(model, row) == False:
                break
            # uncheck the template
            model.item(row,GENERATE).setCheckState(Qt.Unchecked)
            # refresh the treeview
            self.model.updateTV()     
            
    def genRelTemplates(self, ):                
        # generate rel templates
        model = self.gridTemplates_Rel.model()
        numrows = model.rowCount() 
        for row in range(0,numrows):
            genFlag = model.item(row,GENERATE).checkState()     
            # is the pattern checked?
            if genFlag == Qt.Unchecked:
                continue            
            if self.genRelTemplate(model, row) == False:
                break
            # uncheck the template
            model.item(row,GENERATE).setCheckState(Qt.Unchecked)
            # refresh the treeview
            self.model.updateTV()    

    def genNodeTemplate(self, model, row ):
        
        templateName = model.item(row,TEMPLATENAME).data(Qt.EditRole)
        labelPattern = model.item(row,LABELPATTERN).data(Qt.EditRole)        
        # find entry in nodeDict that matches the label pattern in the grid
        # you can't use the template name because the user may have overwritten it
        labelPatternList = None
        for key, value in self.nodeDict.items():
            if str(value["labelList"]) == labelPattern:
                labelPatternList = value["labelList"]
                propertyPatternList = value["propList"]
                propertyDataTypeDict = value.get("propDataType", {})
        # this should never happen        
        if labelPatternList == None:
            self.helper.displayErrMsg("Create New Node Template Error", "The label pattern {} not found".format(labelPattern))
            self.gridTemplates.setFocus()
            return False
        # make sure there is a template name
        if self.helper.NoTextValueError(templateName, "You must supply a name for the Node Template"):
            self.gridTemplates.setFocus()
            return False
        #make sure template name doesn't exist
        index, nodeDict = self.model.getDictByName("Node Template", templateName)
        if not nodeDict is None:
            self.helper.displayErrMsg("Create New Node Template Error", "The node template {} already exists".format(templateName))
            self.gridTemplates.setFocus()
            return False
#        print("{} {} {}".format(templateName, str(labelPatternList),str(propertyPatternList) ))
        labelList = []
        for label in labelPatternList:
            nodeLbl = [label, Qt.Checked, Qt.Unchecked]
            self.model.newLabel(label)
            labelList.append(nodeLbl)
        propList = []
        for property in propertyPatternList:
            dataType = propertyDataTypeDict.get(property, "Unknown")
            nodeProp = [property, dataType,Qt.Unchecked,"", Qt.Unchecked, Qt.Unchecked, Qt.Unchecked]
            self.model.newProperty(property, dataType = dataType)
            propList.append(nodeProp)
        
        # generate the constraints and indexes
        conList = []
        # CONTYPE, CONLBL, CONPROP, CONPROPLIST
        # look at each constraint in the schemaModel and see if it belongs to the node template
        self.schemaModel.matchConstraintNodeTemplate(conList, [lbl[0] for lbl in labelList ], [prop[0] for prop in propList])
        # look at each index in the schemaModel and see if it belongs to the node template
        idxList = []
        self.schemaModel.matchIndexNodeTemplate(idxList, [lbl[0] for lbl in labelList ], [prop[0] for prop in propList])
        
        #save it to the model
        nodeTemplateDict = self.model.newNodeTemplate(name=templateName, labelList=labelList, propList=propList, 
                                                                conList=conList, idxList = idxList, 
                                                               desc="Template generated from Reverse Engineering.")
        
        self.model.modelData["Node Template"].append(nodeTemplateDict)
        
        return True

    def genRelTemplate(self, model, row ):
        '''
        Create a relationship template based on the row in the results grid
        GENERATE, RELTEMPLATENAME, RELATIONSHIPNAME, FROMTEMPLATE, TOTEMPLATE, RELPROPERTYPATTERN = range(6)
        '''
        # templateName and relationship name
        templateName = model.item(row,RELTEMPLATENAME).data(Qt.EditRole)        
        relName = model.item(row,RELATIONSHIPNAME).data(Qt.EditRole) 
        fromTemplate = model.item(row,FROMTEMPLATE).data(Qt.EditRole) 
        toTemplate = model.item(row,TOTEMPLATE).data(Qt.EditRole) 
        uniqueKey = model.item(row,RELKEY).data(Qt.EditRole)

#        # get property pattern from relDict since it is an actual list, not a string like what is stored in the grid 
        propertyPatternList = self.relDict[uniqueKey]["propList"]
        propertyDataTypeDict = self.relDict[uniqueKey].get("propDataType", {})
        # make sure there is a relationship name
        if self.helper.NoTextValueError(relName, "You must supply a name for the Relationship"):
            self.gridTemplates_Rel.setFocus()
            return False
        # make sure there is a template name
        if self.helper.NoTextValueError(templateName, "You must supply a name for the Relationship Template"):
            self.gridTemplates_Rel.setFocus()
            return False
        #make sure template name doesn't exist
        index, nodeDict = self.model.getDictByName("Relationship Template", templateName)
        if not nodeDict is None:
            self.helper.displayErrMsg("Create New Relationship Template Error", "The Relationship template {} already exists".format(templateName))
            self.gridTemplates.setFocus()
            return False

#        print("{} {}".format(templateName,str(propertyPatternList) ))
        # if its a new rel type then add it to the model
        self.model.newRelationship(relName)
        # properties
        propList = []
        for property in propertyPatternList:
            dataType = propertyDataTypeDict.get(property, "Unknown")
            relProp = [property, dataType,Qt.Unchecked,"", Qt.Unchecked]
            self.model.newProperty(property, dataType = dataType)
            propList.append(relProp)
        # generate the constraints
        conList = []
        # look at each constraint in the schemaModel and see if it belongs to the rel template
        self.schemaModel.matchConstraintRelTemplate(conList, [prop[0] for prop in propList], relName=relName)
        
        relDict = self.model.newRelTemplateDict(name=templateName, relname = relName, propList=propList, fromTemplate=fromTemplate, toTemplate=toTemplate, conList=conList,  desc="Template generated from Reverse Engineering.")
        self.model.modelData["Relationship Template"].append(relDict)
        return True
    
    def genRelResult(self, ):
        '''
        Scan the reverse engineered relationship dictionary and create Relationship Template rows in the grid
        '''
        for key in sorted(self.relDict.keys()):
            value = self.relDict[key]
#            self.addRelResultRow(self.gridTemplates_Rel.model(), Qt.Checked, "{}".format(key), str(value["relName"]), str(value["fromTemplate"]), str(value["toTemplate"]), str(value["propList"]), str(value["count"]) )
            self.addRelResultRow(self.gridTemplates_Rel.model(), Qt.Checked, str(value["templateName"]), str(value["relName"]), str(value["fromTemplate"]), str(value["toTemplate"]), str(value["propList"]), str(value["count"]) , key)

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        Slot documentation goes here.
        
        @param button DESCRIPTION
        @type QAbstractButton
        """
        QDialog.accept(self)
    
#    @pyqtSlot()
#    def on_rbAllNodes_clicked(self):
#        """
#        User selects to scan all nodes so set relationships to scan all
#        """
#        if self.rbAllNodes.isChecked():
#            self.rbAllRels.setChecked(True)
#        else:
#            self.rbAllRels.setChecked(False)
    
#    @pyqtSlot()
#    def on_rbPercentNodes_clicked(self):
#        """
#        User selects to scan a percentage of nodes so set relationships to scan percentage
#        """
#        if self.rbPercentNodes.isChecked():
#            self.rbPercentRels.setChecked(True)
#        else:
#            self.rbPercentRels.setChecked(False)
#    
#    @pyqtSlot()
#    def on_rbAllRels_clicked(self):
#        """
#        User selects to scan all Rels, so set nodes to scan all
#        """
#        if self.rbAllRels.isChecked():
#            self.rbAllNodes.setChecked(True)
#        else:
#            self.rbAllNodes.setChecked(False)
#    
#    @pyqtSlot()
#    def on_rbPercentRels_clicked(self):
#        """
#        User selects to scan a percentage of relationships
#        Set nodes to scan percentage
#        """
#        if self.rbPercentRels.isChecked():
#            self.rbPercentNodes.setChecked(True)
#        else:
#            self.rbPercentNodes.setChecked(False)
    
    @pyqtSlot()
    def on_btnSaveTemplates_clicked(self):
        """
        User requests to Generate the node templates
        """
        self.genNodeTemplates()
        return
    
    @pyqtSlot(bool)
    def on_cbScanRels_clicked(self, checked):
        """
        The scan relationships checkbox has been clicked
        Check to make sure the scan Nodes relationship has also been clicked.
        You can't scan relationships without having scanned node patterns.
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked:
            self.cbScanNodes.setCheckState(Qt.Checked)
    
    @pyqtSlot()
    def on_pbUncheck_clicked(self):
        """
        Uncheck all the node templates
        """
        model = self.gridTemplates.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            model.item(row,GENERATE).setCheckState(Qt.Unchecked)

    
    @pyqtSlot()
    def on_pbCheck_clicked(self):
        """
        check all the node template checkboxes
        """
        model = self.gridTemplates.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            model.item(row,GENERATE).setCheckState(Qt.Checked)
    
    @pyqtSlot()
    def on_pbUncheck_Rel_clicked(self):
        """
        Uncheck all the relationship templates
        """
        model = self.gridTemplates_Rel.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            model.item(row,GENERATE).setCheckState(Qt.Unchecked)
    
    @pyqtSlot()
    def on_pbCheck_Rel_clicked(self):
        """
        check all the node template checkboxes
        """
        model = self.gridTemplates_Rel.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            model.item(row,GENERATE).setCheckState(Qt.Checked)
    
    @pyqtSlot()
    def on_btnSaveTemplates_Rel_clicked(self):
        """
        User requests to Generate the relationship templates
        """
        self.genRelTemplates()
        return
    
    @pyqtSlot(bool)
    def on_cbScanNodes_clicked(self, checked):
        """
        The scan nodes checkbox has been clicked
        If they unchecked it display a message and turn it back on.  You always have to scan Nodes
        """
        if not checked:
            self.helper.displayErrMsg("Reverse Engineer", "You always have to scan the Nodes")
            self.cbScanNodes.setCheckState(Qt.Checked)
    
    @pyqtSlot()
    def on_btnStop_clicked(self):
        """
        User  clicks the stop button to stop reverse engineering
        """
        self.stopScan = True
        self.displayScanMsg("User Canceled Scan")
    
    @pyqtSlot(int)
    def on_spinProcessSize_valueChanged(self, p0):
        """
        User changed the process size spin box
        
        @param p0 DESCRIPTION
        @type int
        """
        # update the percents
        self.testScan()
    
    @pyqtSlot(int)
    def on_spinSkipAmt_valueChanged(self, p0):
        """
        User changed the skip amount spin box
        
        @param p0 DESCRIPTION
        @type int
        """
        #update the percents
        self.testScan()
