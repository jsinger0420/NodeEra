# -*- coding: utf-8 -*-

"""
Module implementing DataGridWidget.
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

import datetime
import csv
import logging

#from neo4j.util import watch

from PyQt5.QtCore import pyqtSlot, Qt, QModelIndex, QFile, QTextStream, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QAbstractItemView, QHeaderView, QFileDialog
from PyQt5.QtGui import QStandardItemModel,  QStandardItem

from core.helper import Helper
from core.Enums import DataType
from core.NeoEditDelegate import NeoEditDelegate
from core.NeoTypeFunc import NeoTypeFunc
from forms.Ui_DataGridWidget import Ui_DataGridWidget
from forms.GetCursorDlg import GetCursorDlg
from forms.ExportCSVFile import DlgExportCSV
from forms.EditNodeDlg import EditNodeDlg
from forms.EditRelDlg import EditRelDlg

DATA, LOG, TRACE = range(3)

TS, DURATION, CYPHER, PLAN,  ERROR,  UPDATES, LBLADD, LBLDEL, PROPSET, NODEADD,  NODEDEL, RELADD,  RELDEL, CONADD, CONDEL, IDXADD, IDXDEL = range(17)

LABEL, REQUIRED, NODEKEY = range(3)
PROPERTY, EXISTS, UNIQUE, PROPNODEKEY = range(4)
PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP, RELNAME, UNKNOWN = range(9)

class DataGridWidget(QWidget, Ui_DataGridWidget):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, neoCon=None, genCypher=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DataGridWidget, self).__init__(parent)
        self.setupUi(self)
        self.helper = Helper()
        self.neoTypeFunc = NeoTypeFunc()
        self.resultSet = None
        self.cypher = None
        self.parmData = None
        self.editParmDict = None
        self.genCypher = genCypher
        self.templateDict = self.genCypher.templateDict
        # the parent widget must supply a neoCon
        # this is the NeoDriver instance, but we still use the older neocon variable at this level in the code
        self.neoCon = neoCon        
        self.parent = parent
        try:
            self.designModel = parent.designModel
        except:
            self.designModel = None
        
        self.neoCon.setAutoCommit(True)
        
        self.initUI()
        
        # data grid scrolling
        self.topRow = 1
        
        # data grid cell selection variables
        self.saveIndex = None
        self.prevIndex = None
        self.saveData = None
        
    def initUI(self, ):

        # get list of allowed functions on the data grid widget
        self.btnRefresh.setEnabled(self.genCypher.refreshOK())
        self.btnExport.setEnabled(self.genCypher.exportOK())
        self.btnNew.setEnabled(self.genCypher.newOK())
        self.btnDelete.setEnabled(self.genCypher.deleteOK())
        self.btnSetNull.setEnabled(self.genCypher.setNullOK())
        self.btnRefresh.setVisible(self.genCypher.refreshOK())
        self.btnExport.setVisible(self.genCypher.exportOK())
        self.btnNew.setVisible(self.genCypher.newOK())
        self.btnDelete.setVisible(self.genCypher.deleteOK())
        self.btnSetNull.setVisible(self.genCypher.setNullOK())

            
        # log grid
        self.gridLog.setModel(self.createLogModel())
        self.gridLog.setSortingEnabled(False)
        self.gridLog.setWordWrap(True)
        self.gridLog.setColumnWidth(0, 150)
        self.gridLog.setColumnWidth(PLAN, 100)
        self.gridLog.setColumnWidth(ERROR, 100)
        self.gridLog.setColumnWidth(CYPHER, 500)
        for x in range(UPDATES, IDXDEL+1):
            self.gridLog.setColumnWidth(x, 150)
            
        self.gridLog.verticalHeader().setDefaultAlignment (Qt.AlignTop)

        # data grid
        self.gridCypherData.setAlternatingRowColors(True)
        # turn on row selection mode 
        if self.genCypher.rowSelect():
            self.gridCypherData.setSelectionBehavior(QAbstractItemView.SelectRows)        
            
        
    def logMsg(self, msg):
        '''
        This method writes the message to the trace tab and the application log
        '''
#        print("datagridwidget log method: {}".format(msg))
        # add message to the log
        if logging:
            logging.info(msg)        
        
        # add message to the trace tab
        ts = ('%s' % datetime.datetime.now())
        outmsg = "{} - {}".format(ts, msg)
        self.textTrace.append(outmsg)   
        
    def logWatch(self, ):
        return
        
#        httpWatch = self.httpCapturer.getvalue()
#        boltWatch = self.boltCapturer.getvalue()
#                
#        # update trace tab 
#        if len(httpWatch) > 0:
#            self.logMsg("HTTP Watch: {}".format(httpWatch))
#        if len(boltWatch) > 0:    
#            self.logMsg("BOLT Watch: {}".format(boltWatch))       
#       # close and reopen the stream to clear it out  
#        self.closeWatch()
#        self.initWatch()   
        
#####################################################################################
# methods related to the log tab
#####################################################################################
    def createLogModel(self, ):
#        TS, DURATION, CYPHER, ERROR, PLAN, UPDATES, LBLADD, LBLREMOVE, PROPSET, NODEADD,  NODEDEL, RELADD,  RELDEL, CONADD, CONDEL, IDXADD, IDXDEL = range(15)

        model = QStandardItemModel(0, 17)
        model.setHeaderData(TS, Qt.Horizontal, "Start Time")
        model.setHeaderData(DURATION, Qt.Horizontal, "Duration")
        model.setHeaderData(CYPHER, Qt.Horizontal, "Cypher")
        model.setHeaderData(ERROR, Qt.Horizontal, "Error")
        model.setHeaderData(PLAN, Qt.Horizontal, "Plan")
        model.setHeaderData(UPDATES, Qt.Horizontal, "Updates")
        model.setHeaderData(LBLADD, Qt.Horizontal, "Labels Added")
        model.setHeaderData(LBLDEL, Qt.Horizontal, "Labels Removed")
        model.setHeaderData(PROPSET, Qt.Horizontal, "Properties Updated")
        model.setHeaderData(NODEADD, Qt.Horizontal, "Nodes Created")
        model.setHeaderData(NODEDEL, Qt.Horizontal, "Nodes Deleted")
        model.setHeaderData(RELADD, Qt.Horizontal, "Relationships Created")
        model.setHeaderData(RELDEL, Qt.Horizontal, "Relationships Deleted")
        model.setHeaderData(CONADD, Qt.Horizontal, "Constraints Added")
        model.setHeaderData(CONDEL, Qt.Horizontal, "Constraints Deleted")
        model.setHeaderData(IDXADD, Qt.Horizontal, "Indexes Added")
        model.setHeaderData(IDXDEL, Qt.Horizontal, "Indexes Deleted")
        
        model.rowsInserted.connect(self.autoScroll)
        
        return model        

    def refreshSchemaTreeView(self):
        '''
        tell the schema editor to refresh its tree view if any schema objects changed
        '''
        if not self.neoCon.stats is None:
            try:
                # see if any schema objects changed
                if (self.neoCon.stats.constraints_added > 0 
                    or self.neoCon.stats.constraints_removed > 0 
                    or self.neoCon.stats.indexes_added > 0 
                    or self.neoCon.stats.indexes_removed > 0 
                    or self.neoCon.stats.labels_added > 0 
                    or self.neoCon.stats.labels_removed > 0 
                    ):
#                    print("refresh schema model")
                    self.parent.parent.refreshSchemaModel()
            except:
                pass

            
        return
        
    def addGridRow(self,):
#        TS, DURATION, CYPHER, ERROR, PLAN, UPDATES, LBLADD, LBLREMOVE, PROPSET, NODEADD,  NODEDEL, RELADD,  RELDEL, CONADD, CONDEL, IDXADD, IDXDEL = range(15)
        '''
        add a row to the log grid
        '''
        cypherLogDict = self.neoCon.cypherLogDict
        model = self.gridLog.model()
        stats = self.neoCon.stats
        self.refreshSchemaTreeView()    
        
        try:
            deltaTime = ('%s' % (cypherLogDict['endTime'] - cypherLogDict['startTime'] ))
        except:
            deltaTime = "no delta time"
        
        item1 = QStandardItem('%s' % cypherLogDict.get('startTime', 'no start time'))
        item1.setEditable(False)
        item1.setData(Qt.AlignTop, Qt.TextAlignmentRole)
        
        item2 = QStandardItem(deltaTime)
        item2.setEditable(False)
        item2.setData(Qt.AlignTop, Qt.TextAlignmentRole)
        
        item3 = QStandardItem(cypherLogDict.get('cypher', 'no cypher'))
        item3.setEditable(False)
        item3.setData(Qt.AlignTop, Qt.TextAlignmentRole)
        
        # make the plan column wider if there is any output
        if (str(cypherLogDict.get('plan', "")) == "{}" or str(cypherLogDict.get('plan', "")) == "") or cypherLogDict.get('plan', None) is None:
            planOutput = ""
        else:
            planOutput = str(cypherLogDict.get('plan', "No Plan Output"))
            # increase the width of the column. 
            self.gridLog.setColumnWidth(PLAN, 300)
            
        itemX = QStandardItem(planOutput)
        itemX.setEditable(False)
        itemX.setData(Qt.AlignTop, Qt.TextAlignmentRole)  

        # make the error message column wider if there is any output
        if (str(cypherLogDict.get('error', "")) == "{}" or str(cypherLogDict.get('error', "")) == ""):
            errorOutput = ""
        else:
            errorOutput = cypherLogDict.get('error', "")
            self.gridLog.setColumnWidth(ERROR, 300)
            
        itemE = QStandardItem(errorOutput)
        itemE.setEditable(False)
        itemE.setData(Qt.AlignTop, Qt.TextAlignmentRole)  
        
        if not stats is None:
            try:
                updates = stats.contains_updates
            except:
                updates = 'unknown'
                    
            item4 = QStandardItem(str(updates))
            item4.setEditable(False)
            item4.setData(Qt.AlignTop, Qt.TextAlignmentRole)
            item5 = QStandardItem(str(stats.labels_added))            
            item5.setEditable(False)
            item5.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)
            item6 = QStandardItem(str(stats.labels_removed))     
            item6.setEditable(False)
            item6.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)
            item7 = QStandardItem(str(stats.properties_set))     
            item7.setEditable(False)
            item7.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)
            item8 = QStandardItem(str(stats.nodes_created))     
            item8.setEditable(False)    
            item8.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)
            item9 = QStandardItem(str(stats.nodes_deleted))     
            item9.setEditable(False)    
            item9.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)        
            item10 = QStandardItem(str(stats.relationships_created))     
            item10.setEditable(False)    
            item10.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)             
            item11 = QStandardItem(str(stats.relationships_deleted))     
            item11.setEditable(False)    
            item11.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)             
            item12 = QStandardItem(str(stats.constraints_added))     
            item12.setEditable(False)    
            item12.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)             
            item13 = QStandardItem(str(stats.constraints_removed))     
            item13.setEditable(False)    
            item13.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)             
            item14 = QStandardItem(str(stats.indexes_added))     
            item14.setEditable(False)    
            item14.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)             
            item15 = QStandardItem(str(stats.indexes_removed))     
            item15.setEditable(False)    
            item15.setData(Qt.AlignTop | Qt.AlignRight, Qt.TextAlignmentRole)    
        else:
            item4 = QStandardItem('')
            item4.setEditable(False)
            item4.setData(Qt.AlignTop, Qt.TextAlignmentRole)
            item5 = QStandardItem('')
            item5.setEditable(False)
            item5.setData(Qt.AlignTop, Qt.TextAlignmentRole)
            item6 = QStandardItem('')
            item6.setEditable(False)
            item6.setData(Qt.AlignTop, Qt.TextAlignmentRole)
            item7 = QStandardItem('')
            item7.setEditable(False)
            item7.setData(Qt.AlignTop, Qt.TextAlignmentRole)
            item8 = QStandardItem('')
            item8.setEditable(False)    
            item8.setData(Qt.AlignTop, Qt.TextAlignmentRole)
            item9 = QStandardItem('')
            item9.setEditable(False)    
            item9.setData(Qt.AlignTop, Qt.TextAlignmentRole)        
            item10 = QStandardItem('')
            item10.setEditable(False)    
            item10.setData(Qt.AlignTop, Qt.TextAlignmentRole)             
            item11 = QStandardItem('')
            item11.setEditable(False)    
            item11.setData(Qt.AlignTop, Qt.TextAlignmentRole)             
            item12 = QStandardItem('')
            item12.setEditable(False)    
            item12.setData(Qt.AlignTop, Qt.TextAlignmentRole)             
            item13 = QStandardItem('')
            item13.setEditable(False)    
            item13.setData(Qt.AlignTop, Qt.TextAlignmentRole)             
            item14 = QStandardItem('')
            item14.setEditable(False)    
            item14.setData(Qt.AlignTop, Qt.TextAlignmentRole)             
            item15 = QStandardItem('')
            item15.setEditable(False)    
            item15.setData(Qt.AlignTop, Qt.TextAlignmentRole)  

        model.appendRow([item1,item2,item3, itemX, itemE, item4,item5,item6,item7,item8,item9,item10,item11,item12,item13,item14,item15,])
        
        self.gridLog.resizeRowsToContents() 
        
        QTimer.singleShot(0, self.gridLog.scrollToBottom)

    def autoScroll(self):
        # position on last row in gird
        lastRow = self.gridLog.model().rowCount()
        index = self.gridLog.model().index(lastRow, 0, parent = QModelIndex())
        self.gridLog.scrollTo(index, hint = QAbstractItemView.PositionAtTop)
        self.gridLog.selectRow(index.row())        

    def clearGridLog(self, ):
        self.gridLog.model().removeRows( 0, self.gridLog.model().rowCount() )
        
    @pyqtSlot()
    def on_btnExportLog_clicked(self):
        """
        Export the contents of the log tab to .csv file
        """
        # get filename to save as 
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setDefaultSuffix("csv")
        dlg.setNameFilters(["Log File (*.csv)","all files (*.*)"])
        dlg.setDirectory(self.parent.settings.value("Default/ProjPath"))
        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            try:
                if fileNames:
                    self.fileName = fileNames[0]
                    # save the file
                    with open(self.fileName, 'w', newline='') as csvfile:
                        csvWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for row in range(self.gridLog.model().rowCount()):
                            rowItems = []
                            for col in range(self.gridLog.model().columnCount()):
                                value = self.gridLog.model().index( row, col, QModelIndex() ).data( Qt.DisplayRole )
                                rowItems.append(value)
                            csvWriter.writerow(c for c in rowItems)                        
            except BaseException as e:
                msg = "{} - {} failed.".format("Write CSV", repr(e))
                self.helper.displayErrMsg("Export CSV Error",  msg)



    @pyqtSlot()
    def on_btnClearLog_clicked(self):
        """
        Clear the log grid
        """
        self.clearGridLog() 
        
#####################################################################################
# methods related to the data tab
#####################################################################################
    def forceSelectionChange(self, ):
        '''
        this method changes the current selection to force any unprocessed updates to take place.
        '''
        self.gridCypherData.clearSelection()
        
    def displayDataRetrievedMsg(self, ):
        if self.neoCon.endReached == True:
            msg = "All Data Retrieved."
        else:
            msg = "More Data Exists."
        self.displayGridMessage("Retrieved {} records. {}".format(self.neoCon.chunkEnd, msg ))
#        self.txtPosition.setText("Retrieved {} records. {}".format(self.neoCon.chunkEnd, msg ))

    def displayGridMessage(self, message):
        if not message is None:
            self.txtPosition.setText(message)
        else:
            self.txtPosition.setText("")
        
    def clearModel(self):
        # if we already have a model get rid of it
        if not (self.resultSet is None):
            del self.resultSet        
        self.gridCypherData.setModel(None) 
        
    def newResultModel(self):
        
#        headers = self.neoCon.cursor.keys()
        headers = self.neoCon.result.keys()
        if not (headers is None):
            self.resultModel = QStandardItemModel(0, len(headers))
            for index, header in enumerate(headers):
                self.resultModel.setHeaderData(index, Qt.Horizontal, header)

        # assign the model to the grid
        self.gridCypherData.setModel(self.resultModel) 
        # set the editor delegate
        self.gridCypherData.setItemDelegate(NeoEditDelegate(self))
        # connect model slots 
        self.resultModel.itemChanged.connect(self.resultModelItemChanged)
        # connect grid slots
        self.gridCypherData.selectionModel().selectionChanged.connect(self.dataGridSelectionChanged)
        
        self.gridCypherData.resizeColumnsToContents()
        
    def runFileCursor(self, ):
        '''
        1. start dialog box to Run a cypher query and return a cursor to the result set
        2. Retrieve the first chunk of data
        '''
#        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.logMsg("User requests retrieve {}".format(self.genCypher.type))
        # clear the grid
        self.clearModel()

        try:
            rc = False 
            self.logMsg(self.cypher)
            # the dialog box actually spins up a thread that runs the query
            d = GetCursorDlg(neoCon=self.neoCon, cypher=self.cypher, mode="cursor", parmData=self.parmData)
            if d.exec_():
                rc1 = d.rc
                msg1 = d.msg

            if rc1:
                self.logMsg("run cypher {}".format(msg1))
                if not self.neoCon.stats is None:
                    self.logMsg("stats {}".format(self.neoCon.stats))
                self.newResultModel()
                #get the first chunk
                x, msg2  = self.neoCon.forwardCursor()
                self.logMsg("rows fetched: {} - {}".format(str(x), msg2))                
                self.loadModelChunk()
                self.tabWidget.setCurrentIndex(DATA)
                self.displayDataRetrievedMsg()
                # force a repaint of the grid.  this is needed as a workaround for MAC OS
                self.gridCypherData.repaint()
                # end workaround
                rc = True
                msg = "Run cypher complete"
            else:
                msg = "run cypher Error {}".format(msg1)
        except BaseException as e:
            msg = "{} - Query failed.".format(repr(e))
        finally: 
            # update trace tab           
            self.logWatch()
            # add the row to the log grid
            self.addGridRow()
            # set tab focus depending on results
            QApplication.restoreOverrideCursor()
            if rc == False:
                # display error message then switch to trace tab
                self.helper.displayErrMsg("Run Query With Cursor",  msg)
                self.tabWidget.setCurrentIndex(TRACE)
            else:
                # switch to data tab
                self.tabWidget.setCurrentIndex(DATA)
                
            self.logMsg(msg)   
            
    # - append the table model with the current cursor chunk
    def loadModelChunk(self,):
        self.gridCypherData.setSortingEnabled(False) 
        
        for record in self.neoCon.cursorChunk:
            itemList = []
            # generate the qstandarditem for each column in the result set based on the editParmDict dictionary
            # value has the correct python object for each cell in the result set
            # need to store both the original value and the string representation
            for index, value in enumerate(record.values()):
                item = QStandardItem()
#PROP, REQLBL, OPTLBL, NODEID, RELID, NODE, RELATIONSHIP, RELNAME     
                if not self.editParmDict is None:
                    columnType = self.editParmDict[index][0]
                    editable  = self.editParmDict[index][1]
                else:
                    columnType = UNKNOWN
                    editable = False
                    
                # get the data type of the retrieved data if not null
                if not value is None:
                    dataType = self.neoTypeFunc.getNeo4jDataType(value)
                else:
                    # get the property name from the header
                    propName = self.gridCypherData.model().headerData(index,Qt.Horizontal, Qt.DisplayRole)
                    if not self.editParmDict is None:
                        dataTypeLookup = ""
                        dataType = None
                        # get the datatype defined for the property name in the node or rel template
                        if "properties" in self.templateDict:
                            dataTypeLookup = [prop[1] for prop in self.templateDict["properties"] if prop[0] == propName ]
                        if len(dataTypeLookup) > 0:
                            dataType = dataTypeLookup[0] 
                        else:
                            # see if you can infer the datatype from the column type
                            if columnType == NODE:
                                dataType = "Node"
                            if columnType == RELATIONSHIP:
                                dataType = "Relationship"   
                            

                        if dataType is None:
                            dataType = DataType.UNKNOWN.value  
                    else:
                        dataType = DataType.UNKNOWN.value  
                
                # UNKNOWN DATA TYPES FROM DYNAMIC CYPHER
                if columnType == UNKNOWN:
                    if dataType == "Node":
                        nodeText = ("({} {})".format(str(value.labels), str(dict(value))))
                        item.setText(nodeText)
                    else:
                        if value is None:
                            item.setText("Null")
                        else:
                            displayText = self.neoTypeFunc.convertTypeToString(value)
                            item.setText(displayText)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # these are never editable so just display them
                elif columnType in (NODEID, RELID, RELNAME):
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setText(str(value))

                elif columnType == NODE:
#                    if str(editable) != "True":
                    # if not editable then set the flags, otherwise the default flags are ok
                    if not editable:
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    if value is None:
                        item.setText("Null")
                    else:
                        nodeText = ("({} {})".format(str(value.labels), str(dict(value))))
                        item.setText(nodeText)    
                
                elif columnType == RELATIONSHIP:
                    if str(editable) == "True":
                        item.setText(str(value))
                    else:
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    
                    if value is None:
                        item.setText("Null")
                    else:
                        item.setText(str(value))                  
                
                elif columnType == PROP:
                    if not editable:
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    if value is None:
                        item.setText("Null")
                    else:
                        displayText = self.neoTypeFunc.convertTypeToString(value)
                        item.setText(displayText)
                        
                elif columnType in (OPTLBL, REQLBL):
                    item.setFlags(Qt.NoItemFlags)
                    self.gridCypherData.setColumnWidth(index, 100)
                    self.gridCypherData.horizontalHeader().setSectionResizeMode(index, QHeaderView.Fixed)
                    # set the state of the checkbox based on the data returned by the query.  
                    if value is None:
                        item.setCheckState(Qt.Unchecked)  
                    elif str(value) == 'True':
                        item.setCheckState(Qt.Checked)  
                    else:
                        item.setCheckState(Qt.Unchecked)  
                    if str(editable) == "True":
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    else:
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
                
                # store the actual data in the user defined role
                item.setData(value, Qt.UserRole)                
                # store the datatype in role + 1                
                item.setData(dataType, Qt.UserRole+1)
                
#                print("Column:  Value retrieved: {} python type: {}".format(str(value), type(value)))
                # add the item just created to the item list
                itemList.append(item)    

            # add the entire item list to the model.  this adds a row of data to the grid 
            self.gridCypherData.model().appendRow(itemList)
        # set 
        self.gridCypherData.resizeColumnsToContents()
    
        
    def runCypher(self, requestType, cypher):
        '''
        Run a Cypher query and return the entire result set
        '''
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.logMsg("User requests {}".format(requestType))
        try:
            rc = False 
            self.logMsg(cypher)
            #run the query
            rc1, msg1 = self.neoCon.runCypherAuto(cypher)
            if rc1:
                self.logMsg("{} Node {}".format(requestType, msg1))
                self.logMsg("stats {}".format(self.neoCon.stats))
                rc = True
                msg = "{} Node complete".format(requestType)
            else:
                msg = "{} Node Error {}".format(requestType,  msg1)
        except BaseException as e:
            msg = "{} - {} failed.".format(requestType, repr(e))
        finally: 
            # update trace tab
            self.logWatch()
            # add the row to the log grid
            self.addGridRow()
            # set tab focus depending on results
            QApplication.restoreOverrideCursor()
            if rc == False:
                self.helper.displayErrMsg("Process Node",  msg)
                self.tabWidget.setCurrentIndex(TRACE)
            else:
                # show positive message at bottom of grid
                self.displayGridMessage(msg)
                self.tabWidget.setCurrentIndex(DATA)
            self.logMsg(msg)   

    @pyqtSlot()
    def on_btnExport_clicked(self):
        """
        Export the query result set to a csv file
        """
        self.logMsg("User requests export current query")
        # get filename to save as 
        dlg = DlgExportCSV(parent=self)
        if dlg.exec_():
            try:
                self.logMsg("export {}".format(dlg.fileName))
    #            # run the query, fetch all rows into the resultset
                if (not self.cypher is None and len(self.cypher) > 0):
                    self.runCypher("Export Current Query",self.cypher )
                    # write the csv file
                    with open(dlg.fileName, 'w', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile, 
                                                            delimiter=dlg.delimiterChar, 
                                                            quotechar=dlg.quoteChar, 
                                                            quoting=dlg.useQuote, 
                                                            doublequote=dlg.doubleQuote, 
                                                            escapechar = dlg.escapeChar, 
                                                            lineterminator = dlg.lineTerminator
                                                            )
                        if dlg.writeHeader:
#                            csvwriter.writerow(self.neoCon.cursor.keys())
                            csvwriter.writerow(self.neoCon.result.keys())
                        for record in self.neoCon.resultSet:
                            csvwriter.writerow(record.values())        
                        self.helper.displayErrMsg("Export Query","Data Export Complete!")   
                        
                else:
                    self.logMsg("No current query to export")                
                    self.helper.displayErrMsg("Export Query","No current query to export")
                    
            except BaseException as e:
                self.logMsg("Error Exporting Data - {}".format(repr(e)))
                self.helper.displayErrMsg("Export Query","Error Exporting Data - {}".format(repr(e)))
    
    @pyqtSlot()
    def on_btnBegin_clicked(self):
        """
        position back to the first row in the result set
        """
        self.logMsg("User requests scroll to top")
        index = self.gridCypherData.model().index(0, 0, parent = QModelIndex())
        self.gridCypherData.scrollTo(index, hint = QAbstractItemView.PositionAtTop)
        self.gridCypherData.selectRow(0)      
        self.displayDataRetrievedMsg()
        self.gridCypherData.repaint()
    
    @pyqtSlot()
    def on_btnBack_clicked(self):
        """
        scroll the table back one "chunk"
        """
        # set top row to the row of the currently selected item
        if self.gridCypherData.currentIndex().row() < 0:
            self.topRow = 0
        else:
            self.topRow = self.gridCypherData.currentIndex().row()
        # backup by chunksize
        self.topRow = self.topRow - self.neoCon.chunkSize    
        if self.topRow < 0:
            self.topRow = 0
        index = self.gridCypherData.model().index(self.topRow, 0, parent = QModelIndex())
        self.gridCypherData.scrollTo(index, hint = QAbstractItemView.PositionAtTop)
        self.gridCypherData.selectRow(self.topRow)        
        self.displayDataRetrievedMsg()
        self.gridCypherData.repaint()
        
    @pyqtSlot()
    def on_btnForward_clicked(self):
        """
        if positioned in the last chunk:
            move the cursor through the result set one "chunk". 
            scroll the table to the first row of the most recently retrieved chunk.
        if positioned prior to the last chunk:
            scroll the table forward to the beginning of the next chunk. no data is retrieved.
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.logMsg("User requests scroll forward")
        # set top row to the currently selected row
        if self.gridCypherData.currentIndex().row() < 0:
            self.topRow = 0
        else:
            self.topRow = self.gridCypherData.currentIndex().row()
#        print("starting top row:{}".format(self.topRow))
        # if we are positioned inside the most recently retrieved chunk then get another chunk
        if self.topRow + 1 >= self.neoCon.chunkStart:
#            print("begin chunkstart:{} chunkend:{} topRow:{}".format(self.neoCon.chunkStart, self.neoCon.chunkEnd, self.topRow))
            ctr, msg = self.neoCon.forwardCursor()
            # update trace tab
            self.logWatch()
            self.logMsg("Retrieved {} records. Message:{}".format(ctr, msg))
            self.loadModelChunk()
            self.topRow = self.topRow + self.neoCon.chunkSize + 1
            # see if past end of tableview
            if self.topRow > self.gridCypherData.model().rowCount():
                self.topRow = self.gridCypherData.model().rowCount()
            index = self.gridCypherData.model().index(self.topRow-1, 0, parent = QModelIndex())
            self.gridCypherData.scrollTo(index, hint = QAbstractItemView.PositionAtTop)
            self.gridCypherData.selectRow(index.row())
#            print("read data. chunkstart:{} chunkend:{} topRow:{}".format(self.neoCon.chunkStart, self.neoCon.chunkEnd, self.topRow))
            
        else:
            # we are positioned in a previously retrieved chunk not the current chunk so just scroll forward chunkSize
            self.topRow = self.topRow + self.neoCon.chunkSize
#            print("chunkstart:{} chunkend:{} newtop: {}".format(self.neoCon.chunkStart, self.neoCon.chunkEnd, self.topRow))
            if self.topRow > self.neoCon.chunkEnd -1:
                self.topRow = self.neoCon.chunkEnd
            index = self.gridCypherData.model().index(self.topRow-1, 0, parent = QModelIndex())
            self.gridCypherData.scrollTo(index, hint = QAbstractItemView.PositionAtTop)
            self.gridCypherData.selectRow(index.row())     
        
        QApplication.restoreOverrideCursor() 
        self.displayDataRetrievedMsg() 
        self.gridCypherData.repaint()
    
    @pyqtSlot()
    def on_btnEnd_clicked(self):
        """
        User clicks the move to end button.  Do Fetch cursor until all rows retrieved and loaded to the grid
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.logMsg("User requests scroll to end")
        while self.neoCon.forwardCursor()[0] > 0:
            self.logMsg("Advanced to record {}".format(self.neoCon.chunkEnd))
            self.loadModelChunk()
        index = self.gridCypherData.model().index(self.neoCon.chunkEnd-1, 0, parent = QModelIndex())
        self.gridCypherData.scrollTo(index, hint = QAbstractItemView.PositionAtTop)
        self.gridCypherData.selectRow(index.row())
        QApplication.restoreOverrideCursor()
        self.displayDataRetrievedMsg()
        self.gridCypherData.repaint()

    def createBlankNode(self, ):
        self.neoID = None
        self.cypher = self.genCypher.genNewNode()
        self.runCypher("New Node", self.cypher) 
        if self.neoCon.resultSet:
            self.neoID = self.neoCon.resultSet[0]["nodeID"]  
        return self.neoID
        
    @pyqtSlot()
    def on_btnRefresh_clicked(self):
        """
        Generate the match query and run it.
        """
        self.refreshGrid()
        
    def refreshGrid(self,  **kwargs):
        '''
        1. if special use data grid then generate the cypher match statement
        2. run the cypher statement and populate the grid
        the calling application is responsible for locking the cursor
        '''
        if not self.genCypher.isGeneric():
            
            # see if a nodetemplatedict is being passed in as a kwarg
            aTemplateDict = kwargs.get("nodeTemplateDict", None)  
            if not aTemplateDict is None:
                self.templateDict = aTemplateDict
            self.cypher, self.editParmDict = self.genCypher.genMatch(**kwargs)
        else:
            self.editParmDict = None
        
        if not self.cypher is None:
            self.runFileCursor()
        else:
            self.clearModel()



    @pyqtSlot()
    def on_btnNew_clicked(self):
        """
        Create a new Node/Rel based on the template
        """
        if self.genCypher.type == "Node":
            # display the new node dialog box
            dlg = EditNodeDlg(parent=self)        
            dlg.exec()
            # refresh the grid
            self.refreshGrid()
            # position to the new node
            if not dlg.neoID is None:
                findIt = self.gridCypherData.model().findItems (str(dlg.neoID), flags = Qt.MatchExactly, column = 0)
                if len(findIt) > 0:
                    findItem = findIt[0]
                    self.gridCypherData.scrollTo(findItem.index())
                    self.gridCypherData.selectRow(findItem.row())
                    
        if self.genCypher.type == "Relationship":
            # display the new rel dialog box
            dlg = EditRelDlg(parent=self)        
            dlg.exec()
            # refresh the grid
            self.refreshGrid()
            # position to the new rel
            if not dlg.neoID is None:
                findIt = self.gridCypherData.model().findItems (str(dlg.neoID), flags = Qt.MatchExactly, column = 2)
                if len(findIt) > 0:
                    findItem = findIt[0]
                    self.gridCypherData.scrollTo(findItem.index())
                    self.gridCypherData.selectRow(findItem.row())
                    
    @pyqtSlot()
    def on_btnDelete_clicked(self):
        """
        Delete the node or relationship identified by the rows selected in the grid.
        """
        indexes = self.gridCypherData.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            startIndex = indexes[0]
            endIndex = indexes[len(indexes)-1]
            if self.helper.delRowsPrompt(startIndex.row()+1, endIndex.row()+1):
#                print("delete rows {}-{}".format(startIndex.row()+1, endIndex.row()+1))
                for row in range(startIndex.row(), endIndex.row()+1):
                    # delete the node in neo4j
                    self.deleteDetachCypher = self.genCypher.genDeleteDetach(row=row, dataGrid=self.gridCypherData)
                    # do the update
                    self.runCypher("Delete/Detach Node", self.deleteDetachCypher)
                # refresh the grid to make deleted rows go away
                self.on_btnRefresh_clicked()
            else:
                pass
#                print("delete canceled")
        else:
             self.helper.displayErrMsg("Delete Row", "You must select a row or rows to delete.")
                    
        
#####################################################################################
# methods related to the trace tab
#####################################################################################

        
    @pyqtSlot()
    def on_btnExportTrace_clicked(self):
        """
        Export the contents of the trace tab to .txt file
        """
        # get filename to save as 
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setDefaultSuffix("txt")
        dlg.setNameFilters(["Trace File (*.txt)","all files (*.*)"])
        dlg.setDirectory(self.parent.settings.value("Default/ProjPath"))
        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            if fileNames:
                self.fileName = fileNames[0]
                # save the file
                file = QFile(self.fileName)
                if not file.open(QFile.WriteOnly | QFile.Text):
                    self.helper.displayErrMsg("Export Trace Error",  "Cannot write file {} {}".format(self.fileName, file.errorString()))
                    return 
                outstr = QTextStream(file)
                QApplication.setOverrideCursor(Qt.WaitCursor)
                outstr << self.textTrace.toPlainText()
                QApplication.restoreOverrideCursor()    
                
    @pyqtSlot()
    def on_btnClearTrace_clicked(self):
        """
        clear the contents of the trace tab
        """
        self.textTrace.clear()
    


###########################################################################
# KEYBOARD AND MOUSE EVENTS - keep these functions as examples and for debugging when needed
###########################################################################

#    @pyqtSlot(QModelIndex)
#    def on_gridCypherData_pressed(self, index):
#        """
#        Slot documentation goes here.
#        
#        @param index DESCRIPTION
#        @type QModelIndex
#        """
#        print("Cell pressed {} {}".format(index.row(), index.column()))
    
#    @pyqtSlot(QModelIndex)
#    def on_gridCypherData_clicked(self, index):
#        """
#        Slot documentation goes here.
#        
#        @param index DESCRIPTION
#        @type QModelIndex
#        """
#        print("Cell clicked {} {} - data {}".format(index.row(), index.column(), index.data(role=Qt.DisplayRole)))
    
#    @pyqtSlot(QModelIndex)
#    def on_gridCypherData_entered(self, index):
#        """
#        Slot documentation goes here.
#        
#        @param index DESCRIPTION
#        @type QModelIndex
#        """
#        print("Cell entered {} {}".format(index.row(), index.column()))
    
#    @pyqtSlot(QModelIndex)
#    def on_gridCypherData_activated(self, index):
#        """
#        Slot documentation goes here.
#        
#        @param index DESCRIPTION
#        @type QModelIndex
#        """
#        print("Cell activated {} {} - data {}".format(index.row(), index.column(), index.data(role=Qt.DisplayRole)))


    def dataGridSelectionChanged(self, selected, deselected):
        # no longer used.
#        print("dataGridSelectionChanged")
        return
        
        
    def resultModelItemChanged(self, item):
        
#        print("item data changed {} at row:{} col:{}".format(str(item.checkState()), item.index().row(), item.index().column()))
        # a cell changed so update the node label or property
        columnIndex = item.index().column()
        if not self.editParmDict is None:
            columnType = self.editParmDict[columnIndex][0]
        else:
            columnType = UNKNOWN
        # is this a label column?
        if columnType in (OPTLBL, REQLBL):
            # force selection of this cell
            self.gridCypherData.setCurrentIndex(item.index())
            # update the node in neo4j
            self.updateCypher = self.genCypher.genUpdateLabel(updateIndex=item.index(), dataGrid=self.gridCypherData)
            # do the update
            self.runCypher("Update Label", self.updateCypher)     
        if columnType == PROP:
            # generate a cypher match/set statement aka update
            rc, self.updateCypher = self.genCypher.genUpdateProp(updateIndex=item.index(), dataGrid=self.gridCypherData)
#            print("data changed from {} to {} cypher {}".format(self.saveData, item.index().data(role = Qt.DisplayRole), self.updateCypher))
            # do the update
            if rc == True:
                self.runCypher("Update Property", self.updateCypher)
            else:
                self.helper.displayErrMsg("Update Property", self.updateCypher)
    
    @pyqtSlot()
    def on_btnSetNull_clicked(self):
        """
        User clicks the set property value null button
        """
        indexes = self.gridCypherData.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            selectedIndex = indexes[0]
            columnNum = indexes[0].column()
            if not self.editParmDict is None:
                columnType = self.editParmDict[columnNum][0]
            else:
                columnType = UNKNOWN
            if columnType == PROP:
#                print("set item null {} at row:{} col:{}".format(selectedIndex.data(role = Qt.DisplayRole), selectedIndex.row(), selectedIndex.column()))
                # generate a cypher match/set statement aka update
                self.removeCypher = self.genCypher.genRemoveProp(updateIndex=selectedIndex, dataGrid=self.gridCypherData)
                # do the update
                if self.removeCypher !=None:
                    self.runCypher("Remove Property", self.removeCypher)   
                    self.refreshGrid()
            else:
                self.helper.displayErrMsg("Set Value Null", "You must select a property value.")
        else:
            self.helper.displayErrMsg("Set Value Null", "You must select a property value.")
