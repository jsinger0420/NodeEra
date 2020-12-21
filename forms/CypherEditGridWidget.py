# -*- coding: utf-8 -*-

"""
    UC-04.3 Cypher Workspace
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
    
    Module implementing CypherEditGridWidget.  
    This combine a Qscintilla object on the top and a DataGridWidget on the bottom.
"""


import datetime
import ntpath
import logging

from PyQt5.QtCore import pyqtSlot, QFile, QTextStream, Qt, QFileInfo, QSettings
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QFileDialog,  QVBoxLayout
from PyQt5.Qsci import QsciScintilla

#from forms.ExportCSVFile import DlgExportCSV
from forms.DataGridWidget import DataGridWidget
from forms.CypherParmEntryDlg import CypherParmEntryDlg
from core.helper import CypherLexer, Helper
from core.NeoDriver import NeoDriver
from core.DataGridGeneric import DataGridGeneric

MODENEW = 1
MODEEDIT = 2
TS, DURATION, CYPHER, PLAN, UPDATES, LBLADD, LBLDEL, PROPSET, NODEADD,  NODEDEL, RELADD,  RELDEL, CONADD, CONDEL, IDXADD, IDXDEL = range(16)
DATA, LOG, TRACE = range(3)
from .Ui_CypherEditGridWidget import Ui_cypherEditGridWidget


class CypherEditGridWidget(QWidget, Ui_cypherEditGridWidget):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, fileName = None, fileText = None, mode=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(CypherEditGridWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent    
        self.settings = QSettings()        
        self.initUI()   
        self.initScintilla()
        self.helper = Helper()
        self.mode = mode
        self.tabType = "CYPHER"
        self.tabName = fileName
        self.tabIndex = None       # this is the index into the tabWidget of the tab this widget is on
        self.fileName = fileName
        self.fileText = fileText
        self.resultSet = None        



        # create a neocon object for this file tab
        self.neoDriver = NeoDriver(name=self.parent.pageItem.neoConName,  promptPW=self.parent.pageItem.promptPW)
        
        # add the data grid widget.  
        self.dataGridGeneric = DataGridGeneric()
        self.dataGrid = DataGridWidget(self, neoCon=self.neoDriver, genCypher=self.dataGridGeneric)
        self.nodeGridLayout = QVBoxLayout(self.frmDataGrid)
        self.nodeGridLayout.setObjectName("nodeGridLayout")
        self.nodeGridLayout.setContentsMargins(1, 1, 1, 1)
        self.nodeGridLayout.setSpacing(1)
        self.nodeGridLayout.addWidget(self.dataGrid)            
        
        if self.mode == MODENEW:
            if not self.fileText is None:
                self.loadText()
            
        if self.mode == MODEEDIT:
            self.loadFile()    
            
        # position the splitter
        self.show()  # you have to do this to force all the widgets sizes to update 
        half = int((self.frmEditnGrid.height()  / 2)) 
        self.splitter.setSizes([half, half])            


    def logMsg(self, msg):

        if logging:
            logging.info(msg)       
            
    def initUI(self, ):
        #initialize state of commit buttons and dropdown
        self.btnCommit.setEnabled(False)
        self.btnRollBack.setEnabled(False)
        self.cmbAutoCommit.setCurrentIndex(0)      

        
    def initScintilla(self):
        # add and initialize the control to self.frmEditor
        self.editor = QsciScintilla()
        self.editor.setLexer(None)
        self.editor.setUtf8(True)  # Set encoding to UTF-8
        self.editor.setWrapMode(QsciScintilla.WrapNone)
        self.editor.setEolVisibility(False)
        self.editor.setIndentationsUseTabs(False)
        self.editor.setTabWidth(4)
        self.editor.setIndentationGuides(True)
        self.editor.setAutoIndent(True)
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "00000")
        self.editor.setMarginsForegroundColor(QColor("#ffffffff"))
        self.editor.setMarginsBackgroundColor(QColor("#00000000"))
        self.verticalLayout_2.addWidget(self.editor)
        # setup the lexer
        self.lexer = CypherLexer(self.editor)
        self.editor.setLexer(self.lexer)        
        self.setScintillaFontSize()        
        self.editor.SendScintilla(self.editor.SCI_GETCURRENTPOS, 0)
        self.editor.setCaretForegroundColor(QColor("#ff0000ff"))
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor("#1f0000ff"))
        self.editor.setCaretWidth(2)
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

    def setScintillaFontSize(self, ):
        # set font size to value saved in settings
        try:
            fontSize = int(self.settings.value("Lexer/FontSize", "10"))
        except:
            fontSize = 10
        finally:
            for style in range(5):
                self.editor.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, style, fontSize) 
            self.editor.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, 34, fontSize)
            self.editor.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, 35, fontSize)

#####################################################################################
# methods related to the cypher file
#####################################################################################
    def loadText(self, ):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.editor.append(self.fileText)
        self.editor.setModified(True)
        QApplication.restoreOverrideCursor()
        
    def loadFile(self, ):
        file = QFile(self.fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "NodeMaker",
                    "Cannot read file %s:\n%s." % (self.fileName, file.errorString()))
            return False

        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.editor.append(instr.readAll())
        self.editor.setModified(False)
        QApplication.restoreOverrideCursor()
        
    def save(self, ):
        if self.mode == MODENEW:
            self.saveAs()
        else:
            self.saveIt()
 
    def saveAs(self, ):
        # first test to see if the file has changed
        
        # get filename to save as 
        #
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setDefaultSuffix("cyp")
        dlg.setNameFilters(["Cypher Query (*.cyp *.cypher)","Cypher Query (*.cyp)","Cypher Query (*.cypher)","all files (*.*)"])
        dlg.setDirectory(self.parent.settings.value("Default/ProjPath"))
        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            if fileNames:
                self.fileName = fileNames[0]
                # save the file
                self.saveIt()        
    
    def saveIt(self, ):
        file = QFile(self.fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "NodeEra",
                    "Cannot write file %s:\n%s." % (self.fileName, file.errorString()))
            return 

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.editor.text()
        head, tail = ntpath.split(QFileInfo(self.fileName).fileName())
        self.parent.tabCypher.setTabText(self.parent.tabCypher.currentIndex(), tail)
        self.mode = MODEEDIT
        QApplication.restoreOverrideCursor()
        
    def close(self, ):
#        print("editngrid close {}".format(self.fileName))
        # see if there is an open transaction and cancel the close
        self.checkOpenTxn()
        # see if text has changed and save the file if the user wants to
        if self.editor.isModified():
            # see if the user wants to save it
            if self.fileName is None:
                # these are unsaved cypher files so they have no filename yet
                displayName = self.parent.tabCypher.tabText(self.tabIndex)
            else:
                displayName = self.fileName
            if self.helper.saveChangedObject("Cypher File", displayName): 
                self.save()
        return True

##############################################################
# Button methods
##############################################################
    @pyqtSlot()
    def on_btnRun_clicked(self):
        """
        Run the query at the cursor.
        """
        self.runFileCursor()
        
    def runFileCursor(self):
        
        self.logMsg("User requests run Cypher in Cursor")
        # parse the text editor and get the index to the cypher command the cursor is pointing at
        currentCypherIndex = self.getSelectedCypher() 
        # check if cursor in a query
        if currentCypherIndex is None:
            self.helper.displayErrMsg("Run Query",  "You must position cursor within the Cypher query.")
            QApplication.restoreOverrideCursor()
            return
            
        # get the cypher statement to be executed
        startOffset = self.cypherList[currentCypherIndex][0]
        self.dataGrid.cypher =  self.cypherList[currentCypherIndex][1]
        
        # prompt the user for parameter values if any
        userCanceled = False
        if len(self.cypherParms[currentCypherIndex][1]) > 0:
#            print("Parms:{}".format(self.cypherParms[currentCypherIndex][1]))
            # display dialog to gather parms
            d = CypherParmEntryDlg(parent=self, parms=self.cypherParms[currentCypherIndex][1])
            if d.exec_():
                self.dataGrid.parmData = d.parmDict
            else:
                userCanceled = True
                self.dataGrid.parmData = None
#            print("Parm Dictionary:{}".format(self.dataGrid.parmData))
        else:
            self.dataGrid.parmData = None

        # see if the user canceled the query rather than enter parameters
        if userCanceled:
            self.helper.displayErrMsg("Run Query",  "User Canceled Query.")
            QApplication.restoreOverrideCursor()
            return
            
        # make sure the cypher is not just spaces, or nothing but a semicolon
        if (self.dataGrid.cypher.isspace() or 
            len(self.dataGrid.cypher) ==0 or 
            self.dataGrid.cypher.strip() == ";"):
            self.helper.displayErrMsg("Run Query",  "You must position cursor within the Cypher query.")
        else:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.dataGrid.refreshGrid()
            QApplication.restoreOverrideCursor()
        # see if there was a syntax error and position cursor
        try:
            offset = self.dataGrid.neoCon.cypherLogDict["offset"]
            if offset > -1:
                self.editor.SendScintilla(QsciScintilla.SCI_GOTOPOS, offset + startOffset)
        except:
            pass
        finally:
            ###  hack needed on mac os to force scintilla to show cursor and highlighted line
            self.helper.displayErrMsg("Run Query With Cursor",  "Query Complete")
    



    def getSelectedCypher(self):
        '''
        Build a list of cypher commands from the text in the editor
        '''
        # get position of cursor which is a zero based offset, it seems to return zero if editor hasn't been clicked on yet
        try:
            position = self.editor.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS, 0)
        except:
            position = 0
        # initialize cypherList
        self.cypherList = []    
        self.cypherParms = []
        parmList = []
        currentCypherIndex = None
        # get the full text from the editor
        text = self.editor.text()
        # make sure there is something in the text
        if len(text) < 1:
            return currentCypherIndex

        #	Walk through all the characters in text, and store start offset and end offset of each command
        startOffset = 0
        endOffset = 0
        foundCypher = False # tracks if we have found at least one character that is potentially a non-comment cypher command
        inComment = False  # tracks if we're looking at comment characters
        inParm = False        # tracks if we're looking at parameter characters
        inCypher = False     # tracks if we've found a non comment character while scanning
        newParm = ""
        for chrCtr in range (0,len(text)):
#            print("before: chrCtr:{} char: {} ord:{} inComment:{} inParm:{} inCypher:{}".format(chrCtr, text[chrCtr], ord(text[chrCtr]), inComment, inParm, inCypher))

            # see if we're in a comment ( this doesn't work for multiline comments)
            if chrCtr + 1 < len(text) and text[chrCtr] == '/' :
                inParm = False
                if text[chrCtr+1] == "/":
                    inComment = True
                    inCypher = False
            # see if end of line
            elif ord(text[chrCtr]) in [13, 10]:
                inParm = False
                if chrCtr + 1 < len(text):
                    if not text[chrCtr+1]  in [13, 10]:
                        # end of line ends the comment
                        inComment = False
                        
            elif text[chrCtr] == "$":
                if not inComment:
                    foundCypher = True
                    inParm = True
            elif text[chrCtr] == " ":
                if not inComment:
                    foundCypher = True
                inParm = False
            elif (text[chrCtr] == ";" and inComment == False):
                foundCypher = True
                inParm = False
                endOffset = chrCtr
                # save each command in the list
                self.cypherList.append([startOffset, text[startOffset:endOffset+1]])
                self.cypherParms.append([startOffset, parmList])
                parmList = []
                # HAPPY PATH - see if this is the command where the cursor is located
                if (position >= startOffset and position <= endOffset):
                    currentCypherIndex = len(self.cypherList)-1
                # set the next starting offset
                startOffset = chrCtr + 1
                endOffset = startOffset
            elif inComment == False:
                foundCypher = True
                inCypher = True
                
            if inParm:
                newParm = newParm + text[chrCtr]
            else:
                if len(newParm) > 0:
#                    print("Parameter: {}".format(newParm))
                    parmList.append(newParm)
                    newParm = ""
                    
#            print("after: chrCtr:{} char: {} ord:{} inComment:{} inParm:{} inCypher:{}".format(chrCtr, text[chrCtr], ord(text[chrCtr]), inComment, inParm, inCypher))
        
        # at this point all characters have been processed, must deal with edge cases, no final semicolon etc
        if len(self.cypherList) == 0:  # we never found a semi colon so the entire file is one cypher statement
            # return the entire text file
            self.cypherList.append([0, text])
            self.cypherParms.append([0, parmList])
            parmList = []

            currentCypherIndex = 0
        else:                                   # we found some characters after the last semi colon.  
            lastCypher = ""
            try:
                lastCypher = text[startOffset:len(text)]
                if lastCypher.isspace() == True:                           # if there is only whitespace after the last semicolon then return the last found cypher
                    if currentCypherIndex is None:
                        currentCypherIndex = len(self.cypherList)-1
                elif len(lastCypher) < 1:                    # there are no characters after the last semicolon, but cursor is positioned past it then return the last found cypher
                    if currentCypherIndex is None:
                        currentCypherIndex = len(self.cypherList)-1            
                elif inCypher == False and foundCypher == False:                      # none of the characters are outside a comment so return last found cypher
                    if currentCypherIndex is None:                          
                        currentCypherIndex = len(self.cypherList)-1                               
                else:
                    self.cypherList.append([startOffset, lastCypher])  # since some characters are present, add them as the last cypher command
                    self.cypherParms.append([startOffset, parmList])
                    parmList = []

                    if currentCypherIndex is None:                    
                        currentCypherIndex = len(self.cypherList)-1
            except:
                if currentCypherIndex is None:
                    currentCypherIndex = len(self.cypherList)-1            # return the last cypher command found if any error
        
#        print("cypher list: {}".format(self.cypherList))
        return currentCypherIndex
    
    @pyqtSlot()
    def on_btnRunScript_clicked(self):
        """
        this button will run all the cypher commands in the file one at a time.
        """

        self.runFileAsScript()


    def runFileAsScript(self, ):
        '''
        run each cypher command in the file one at a time.
        '''
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.logMsg("User requests run Cypher file as a script")
        # parse the text editor into cypher commands, we don't care which one the cursor is in
        self.getSelectedCypher()
        if len(self.cypherList) < 1:
            self.helper.displayErrMsg("Run File As Script",  "The file has no cypher commands in it.")            
        for cypherCmd in self.cypherList:
            # this is the starting offset of the cypher command in the entire file
            cypherOffset = cypherCmd[0]
            self.dataGrid.cypher = cypherCmd[1]
            # set editor selection to the cypher command
            self.editor.SendScintilla(QsciScintilla.SCI_SETSEL, cypherOffset, cypherOffset+len(self.dataGrid.cypher))
            # skip any cypher is not just spaces, or nothing but a semicolon
            if (self.dataGrid.cypher.isspace() or len(self.dataGrid.cypher) ==0 or self.dataGrid.cypher.strip() == ";"):
                #self.helper.displayErrMsg("Run Query",  "You must position cursor within the Cypher query.")
                pass
            else:
                self.dataGrid.refreshGrid()
                QApplication.processEvents()
            # see if there was a syntax error and position cursor
            try:
                offset = self.dataGrid.neoCon.cypherLogDict["offset"]
                if offset > -1:
                    self.editor.SendScintilla(QsciScintilla.SCI_GOTOPOS, offset + cypherOffset)
            except:
                pass
            # set editor selection to the end of the file
            self.editor.SendScintilla(QsciScintilla.SCI_SETSEL, len(self.editor.text()), len(self.editor.text()))

        QApplication.restoreOverrideCursor()    
                
    
    @pyqtSlot()
    def on_btnCommit_clicked(self):
        """
        User clicks on the Commit button.  Commit the TXN.
        """
        self.doCommit()
            
    def doCommit(self):
        self.logMsg("User request Commit the transaction")
        if not self.neoDriver is None:
            rc, msg = self.neoDriver.commitTxn()
            self.logMsg("Commit Complete - {}".format(msg))
            
    @pyqtSlot()
    def on_btnRollBack_clicked(self):
        """
        User clicks on the Rollback button.  Rollback the TXN.
        """
        self.doRollBack()

    def doRollBack(self):
        self.logMsg("User request Rollback the transaction")
        if not self.neoDriver is None:
            rc, msg = self.neoDriver.rollbackTxn()
            self.logMsg("Rollback Complete - {}".format(msg))
        
        

                
    def zoomIn(self, ):
        """
        increase Font Size
        """
#        self.editor.SendScintilla(QsciScintilla.SCI_ZOOMIN)
#        currentFontSize = self.editor.SendScintilla(QsciScintilla.SCI_STYLEGETSIZE, 0)
#        self.settings.setValue("Lexer/FontSize", currentFontSize)
        # get style 0 font size - all styles use same size
        currentFontSize = self.editor.SendScintilla(QsciScintilla.SCI_STYLEGETSIZE, 0)
        currentFontSize = currentFontSize + 2
        if currentFontSize < 24:
            self.settings.setValue("Lexer/FontSize", currentFontSize)
            for style in range(255):
                self.editor.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, style, currentFontSize)
#            self.editor.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, 34, currentFontSize)
#            self.editor.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, 35, currentFontSize)
            
    def zoomOut(self, ):
        """
        decrease font size
        """
#        self.editor.SendScintilla(QsciScintilla.SCI_ZOOMOUT)
#        currentFontSize = self.editor.SendScintilla(QsciScintilla.SCI_STYLEGETSIZE, 0)
#        self.settings.setValue("Lexer/FontSize", currentFontSize)
        
        # get style 0 font size - all styles use same size
        currentFontSize = self.editor.SendScintilla(QsciScintilla.SCI_STYLEGETSIZE, 0)
        currentFontSize = currentFontSize - 2
        if currentFontSize > 4:
            self.settings.setValue("Lexer/FontSize", currentFontSize)
            for style in range(255):  # was 5
                self.editor.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, style, currentFontSize)
#            self.editor.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, 34, currentFontSize)
#            self.editor.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, 35, currentFontSize)

    def checkOpenTxn(self):
        '''
        check if current txn is still open.  
        if autocommit is false then ask the user to commit or rollback
        if autocommit is true then do the commit
        '''
        if not (self.neoDriver is None):
            if not (self.neoDriver.tx is None):
                if self.neoDriver.tx.closed() is False:
                    if self.neoDriver.autoCommit is True:
                        self.doCommit()
                    else:
                        # prompt user to commit or rollback the current transaction
                        msgBox = QMessageBox()
                        msgBox.setIcon(QMessageBox.Warning)
                        msgBox.setText("You have an uncommitted transaction. Do you want to commit? (click Yes to commit, No to rollback")
                        msgBox.setWindowTitle("Commit or Rollback")
                        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        result = msgBox.exec_()
                        if result == QMessageBox.Yes:
                            self.doCommit()
                        else:
                            self.doRollBack()
                        
                        
    @pyqtSlot(int)
    def on_cmbAutoCommit_currentIndexChanged(self, index):
        """
        User has changed the auto commit dropdown.
        
        @param index DESCRIPTION
        @type int
        """
        self.logMsg("User request transaction mode changed to {}".format(self.cmbAutoCommit.currentText()))  
        if self.cmbAutoCommit.currentText() == "Auto Commit On":
            self.checkOpenTxn()
            if not (self.neoDriver is None):
                self.neoDriver.setAutoCommit(True)
            self.btnCommit.setEnabled(False)
            self.btnRollBack.setEnabled(False)
        if self.cmbAutoCommit.currentText() == "Auto Commit Off":  
            self.checkOpenTxn()
            if not (self.neoDriver is None):
                self.neoDriver.setAutoCommit(False) 
            self.btnCommit.setEnabled(True)
            self.btnRollBack.setEnabled(True)
    

