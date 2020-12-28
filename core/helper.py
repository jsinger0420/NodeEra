# -*- coding: utf-8 -*-

"""
Module implementing helper functions.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
import re
from cryptography.fernet import Fernet

from PyQt5.QtCore import QPoint, QRect, QEvent, QSettings, QItemSelectionModel
from PyQt5.QtWidgets import QMessageBox, QItemDelegate, QComboBox, QApplication, QStyle,  QStyledItemDelegate, QStyleOptionButton, QInputDialog, QLineEdit, QAbstractItemView
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.Qsci import QsciLexerCustom
from PyQt5.QtGui import QColor, QFont
# workaround to get Qt.xxx references to work.  this has to be after the import of QPrinter
from PyQt5.QtCore import Qt



from core.NeoTypeFunc import NeoTypeFunc

##########################################################
# classes used for page setup
##########################################################
class PageType():
    def __init__(self, name=None, height=None, width=None, qpagesizeEnum=None):
        self.name = name
        self.height = height
        self.width = width
        self.qpagesizeEnum = qpagesizeEnum

        
class PageSizes():
    def __init__(self):
        self.pageTypes = {}
        self.pageTypes['A0'] = PageType(name='A0',height=3370, width=2384, qpagesizeEnum=QPrinter.A0)
        self.pageTypes['A1'] = PageType(name='A1',height=2384, width=1684, qpagesizeEnum=QPrinter.A1)
        self.pageTypes['A2'] = PageType(name='A2',height=1684, width=1190, qpagesizeEnum=QPrinter.A2)
        self.pageTypes['A3'] = PageType(name='A3',height=1190, width=842, qpagesizeEnum=QPrinter.A3)
        self.pageTypes['A4'] = PageType(name='A4',height=842, width=595, qpagesizeEnum=QPrinter.A4)
        self.pageTypes['A5'] = PageType(name='A5',height=595, width=420, qpagesizeEnum=QPrinter.A5)
        self.pageTypes['A6'] = PageType(name='A6',height=420, width=298, qpagesizeEnum=QPrinter.A6)
        self.pageTypes['A7'] = PageType(name='A7',height=298, width=210, qpagesizeEnum=QPrinter.A7)
        self.pageTypes['A8'] = PageType(name='A8',height=210, width=148, qpagesizeEnum=QPrinter.A8)
        self.pageTypes['Letter (ANSI A)'] = PageType(name='Letter (ANSI A)',height=792, width=612, qpagesizeEnum=QPrinter.Letter)
        self.pageTypes['Legal'] = PageType(name='Legal',height=1008, width=612, qpagesizeEnum=QPrinter.Legal)
        self.pageTypes['Tabloid (ANSI B)'] = PageType(name='Tabloid (ANSI B)',height=1224, width=792, qpagesizeEnum=QPrinter.Tabloid)
        self.pageTypes['Executive'] = PageType(name='Executive',height=756, width=522, qpagesizeEnum=QPrinter.Executive)
        self.pageTypes['ANSI C'] = PageType(name='ANSI C',height=1224, width=1584, qpagesizeEnum=QPrinter.AnsiC)
        self.pageTypes['ANSI D'] = PageType(name='ANSI D',height=1584, width=2448, qpagesizeEnum=QPrinter.AnsiD)
        self.pageTypes['ANSI E'] = PageType(name='ANSI E',height=2448, width=3168, qpagesizeEnum=QPrinter.AnsiE)

    def loadDropDown(self, dropdown):
        dropdown.clear()
        keys = sorted(self.pageTypes.keys())
        for key in keys:
            dropdown.addItem(key)
            
class PageSetup():
    def __init__(self, objectDict=None):
        """
        Constructor
        """
        self.pageSizes = PageSizes()   
        # create an empty page settings dictionary
        self.objectDict = {} 
        
        # load values that are passed in
        if not objectDict is None:
            self.objectDict.update(objectDict)

        # if any keys are missing set them to the default
        self.objectDict.setdefault("pageOrientation", "Portrait")
        self.objectDict.setdefault("pageSize", self.pageSizes.pageTypes["Letter (ANSI A)"].name)
        self.objectDict.setdefault("pageRows", 3)
        self.objectDict.setdefault("pageCols", 3)
        self.objectDict.setdefault("pageWidth", self.pageSizes.pageTypes["Letter (ANSI A)"].width)
        self.objectDict.setdefault("pageHeight",  self.pageSizes.pageTypes["Letter (ANSI A)"].height)  
        
#        print(self.objectDict)
        
    def getHeightWidth(self, ):
        if self.objectDict["pageOrientation"] == "Portrait":
            return self.objectDict["pageHeight"], self.objectDict["pageWidth"]
        else:
            return self.objectDict["pageWidth"], self.objectDict["pageHeight"]
            





#####################################################################
# helper functions that don't seem to go anywhere else
#####################################################################
class Helper():
    """
    helper functions
    """  
    def __init__(self):
        self.neoTypeFunc = NeoTypeFunc()
        
    def putText(self, a):
        k = b'PSzt9FgcnwrpxIa6tt3HED-s-JyMPCHL0LlmXmjhX-4='
        doIt = Fernet(k)
        b = a.encode('utf-8')
        c = doIt.encrypt(b)
        return str(c,'utf-8')
#        return str(a)
        
    def getText(self, a):
        k = b'PSzt9FgcnwrpxIa6tt3HED-s-JyMPCHL0LlmXmjhX-4='
        doIt = Fernet(k)
        b = a.encode('utf-8')
        c = doIt.decrypt(b)
        return str(c,'utf-8')
#        return str(a)
        
    def slugify(self, aName):
        newName = "".join(x for x in aName if x.isalnum() )  + "_file"
        return newName

    def passwordPrompt(self, conName=None, conURL=None):
        '''if the connection is defined as prompt for password then prompt the user for a password and return what they enter.
          if the connection already has a password then return None
        '''
        self.settings = QSettings()
        # get the neocon dictionary from settings
        neoDict=self.settings.value("NeoCon/connection/{}".format(conName))
        if neoDict["prompt"] == "True":
            msgBox = QInputDialog()
            msgBox.setLabelText("Enter password for connection: {} URL:{}".format(str(conName), str(conURL)))
            msgBox.setInputMode(QInputDialog.TextInput) 
            msgBox.setTextEchoMode(QLineEdit.Password)
            msgBox.exec_()
            return msgBox.textValue()
        else:
            return None        

    def adjustGrid(self, grid=None):
        '''this function should be called after appending a row to the end of a grid
        '''
        # set current index to the first column of the row just added
        grid.setCurrentIndex(grid.model().createIndex(grid.model().rowCount(), 0))
        # set focus to that column
        grid.setFocus(Qt.MouseFocusReason)
        # force resize columns
#        grid.resizeColumnsToContents()
        # force last row to appear in the grid
        grid.scrollToBottom()   
        # force a repaint of the grid.  this is needed as a workaround for MAC OS
        grid.repaint()
        
    def genUpdateCypher(self, neoID = None, nodeInstanceDict = None, node = None):
        '''
        generate a match update cypher statement that updates a node in neo4j
        neoID is the node ID to update
        node is the node object that represents what the node is in the database
        nodeInstanceDict is the dictionary that represents what the user entered on the UI 
        The  goal is to remove all existing labels and properties and replace them with all the labels and properties from the UI.
        '''
        p1 = neoID
        # remove all labels
        p2 = self.genRemoveLblList("n", node)
        # remove propList from the db
        p3 = self.genRemovePropList("n", node)
        # set prop equal list
        p4 = self.genSetPropList("n", nodeInstanceDict)
        # set lbl list
        p5 = self.genSetLabelList("n", nodeInstanceDict)
        cypher = """match (n) 
                        where id(n) = {}   
                        {}  
                        {}
                        {}
                        {} 
                        return n """.format(p1, p2, p3, p4, p5)

#  this was commented out because return data after a constraint violation will cause the next cypher command to bomb                      
#                        return n """.format(p1, p2, p3, p4, p5)
        
        return cypher
        
    def genCreateRelCypher(self, relInstanceDict = None, rel = None, fromNeoID = None, toNeoID=None):
        '''
        generate a cypher statement that adds a relationship between two nodes in Neo4j
        
        rel is the relationship object that represents what the relationship is in the project
        relInstanceDict is the dictionary that represents what the user entered on the UI 
        fromNeoID is the id of the from node used for matching
        toNeoID is the id of the to node used for matching
        The  goal is to match the from and to nodes and add a new relationship between them
        '''
        p1 = fromNeoID
        p2 = toNeoID
        # the relationship name
        p3 = relInstanceDict.get("relName", "")
        # property set list
        p4 = self.genSetPropList("r", relInstanceDict)
        cypher = """match (f) \n 
                        where id(f) = {}  \n 
                        with f \n
                        match (t) \n
                        where id(t) = {}  \n 
                        with f,t
                        create (f)-[r:{}]->(t)
                        {}
                        return id(r), r
                                            """.format(p1, p2, p3, p4)
        return cypher
        
    def genUpdateRelCypher(self, relInstanceDict=None, relID=None, rel=None):
        '''
        generate a cypher statement that adds a relationship between two nodes in Neo4j
        
        rel is the relationship object that represents what the relationship is in the db
        relInstanceDict is the dictionary that represents what the user entered on the UI 
        The  goal is to match an existing relationship and update its properties
        '''
        p1 = str(relID)
        p2 = self.genRemovePropList("r", rel)
        p3 = self.genSetPropList("r", relInstanceDict)
        cypher = """match ()-[r]->() \n 
                        where id(r) = {}  \n 
                        {} \n
                        {} \n 
                        return id(r), r """.format(p1, p2, p3)
                        
# if you return data after a constraint violation it will crash the system on the next cypher call
#                        return id(r), r """.format(p1, p2, p3)
                         
        return cypher   
        
    def genSetLabelList(self, nodeName, nodeInstanceDict):
        '''
        return all labels separated by : with a set statement or nothing if no labels
        '''
        lblList = ""
        if len(nodeInstanceDict["labels"]) > 0:
            lblList = "set " + nodeName + ":" + ":".join(lbl[0] for lbl in nodeInstanceDict["labels"] )
        return lblList   
        
    def genLabelList(self, nodeName, nodeInstanceDict):
        '''
        return all labels separated by :
        '''
        lblList = ""
        if len(nodeInstanceDict["labels"]) > 0:
            lblList = nodeName + ":" + ":".join(lbl[0] for lbl in nodeInstanceDict["labels"] )
        return lblList   

    def genPropValueList(self, nodeName, nodeInstanceDict):
        propList = ""
        if len(nodeInstanceDict["properties"]) > 0:
            propList = ",".join(nodeName + "." + prop[0] + " = " + self.genPropEqualTo(dataValue = prop[2], neoType=prop[1]) for prop in nodeInstanceDict["properties"] if prop[2] != "Null")
        return propList
        
    def genSetPropList(self, nodeName, objectDict):
        propList = ""
        if len(objectDict["properties"]) > 0:
            propList = ",".join(nodeName + "." + prop[0] + " = " + self.genPropEqualTo(dataValue = prop[2], neoType=prop[1]) for prop in objectDict["properties"] if prop[2] != "Null")
            if propList != "":
                return "set " + propList
        return propList
    
    def genPropList(self, nodeName, nodeInstanceDict):
        '''
        return all property names separated by a ,
        '''
        propList = ""
        if len(nodeInstanceDict["properties"]):
            propList = ",".join(nodeName + "." + prop[0] for prop in nodeInstanceDict["properties"] if prop[2] != "Null")
        return propList

    def genRemoveLblList(self, nodeName, object):
        '''
        return all label names separated by a ,
        '''
        lblList = ""
        if len(object.labels) > 0:
            lblList = "remove " + ",".join(nodeName + ":" + lbl for lbl in list(object.labels))
        return lblList  
        
    def genRemovePropList(self, nodeName, object):
        '''
        return all property names separated by a ,
        object - this works for both a node object and a relationship object
        '''
        propList = ""
        if len(dict(object).keys()) > 0:
            propList = "remove " + ",".join(nodeName + "." + propName for propName in dict(object).keys())
        return propList
        
    def genPropEqualTo(self, dataValue=None, neoType=None):
        
        return self.neoTypeFunc.genPropEqualTo(dataValue=dataValue, neoType=neoType)
        
#        if neoType == DataType.STRING.value:
#            setEqualTo = "'{}'".format(dataValue)
#        elif neoType in (DataType.INT.value,  DataType.FLOAT.value):
#            setEqualTo = "{}".format(dataValue)
#        elif neoType == DataType.BOOLEAN.value:
#            setEqualTo = "toBoolean('{}')".format(dataValue)
#        elif neoType == ( DataType.DATE.value):
#            setEqualTo = "date('{}')".format(dataValue)        
#        elif neoType == ( DataType.DATETIME.value):
#            # create a qDateTime from the string in the cell
#            qDateTime = QDateTime.fromString( dataValue, "yyyy-MM-dd hh:mm:ss:zzz")
#            qDate = qDateTime.date()
#            qTime = qDateTime.time()
#            # the neodatetime takes one parm for seconds and milliseconds
#            seconds = qTime.second() + (qTime.msec() / 1000)
#            # create a neo date time from the components of the qdate and qtime
#            nDateTime = DateTime(qDate.year(), qDate.month(), qDate.day(), hour=qTime.hour(), minute=qTime.minute(), second=seconds)
#            # now generate the correct string representation for the cypher stmt
#            setEqualTo = "datetime('{}')".format(str(nDateTime))        
#        elif neoType == ( DataType.TIME.value):
#            setEqualTo = "time('{}')".format(dataValue)        
#        elif neoType == ( DataType.LOCALTIME.value):
#            setEqualTo = "localtime('{}')".format(dataValue)        
#        elif neoType == ( DataType.LOCALDATETIME.value):
#            setEqualTo = "localdatetime('{}')".format(dataValue)     
#        elif neoType == DataType.POINTCARTESIAN.value:
#            start = dataValue.find("(")  
#            end = dataValue.find(")")
#            data = dataValue[start+1:end].strip().split(" ")
#            if len(data) > 2:
#                setEqualTo = "point({}x:{}, y:{}, z:{}{})".format("{", data[0], data[1], data[2], "}") 
#            else:
#                setEqualTo = "point({}x:{}, y:{}{})".format("{", data[0], data[1], "}") 
#        elif neoType == DataType.POINTWGS84.value:
#            start = dataValue.find("(")  
#            end = dataValue.find(")")
#            data = dataValue[start+1:end].split(" ")
#            if len(data) > 2:
#                setEqualTo = "point({}longitude:{}, latitude:{}, height:{}{})".format("{", data[0], data[1], data[2], "}") 
#            else:
#                setEqualTo = "point({}longitude:{}, latitude:{}{})".format("{", data[0], data[1], "}") 
#        else:
#            setEqualTo = ""
#        
#        return setEqualTo
        
    def moveListItemUp(self, listWidget):
        '''
        this moves the current row in a qlistwidget up one
        the row selection moves as well
        error situations are ignored  by the try except block
        '''
        try:
            currentRow = listWidget.currentRow()
            currentItem = listWidget.takeItem(currentRow)
            listWidget.insertItem(currentRow - 1, currentItem)
            listWidget.setCurrentRow(currentRow - 1)
        except:
            pass  # lots of things could have gone wrong in the try block but we don't care.
        finally:
            listWidget.repaint()
            
    def moveListItemDown(self, listWidget):
        '''
        this moves the current row in a qlistwidget down one
        the row selection moves as well
        error situations are ignored  by the try except block
        '''
        try:
            currentRow = listWidget.currentRow()
            currentItem = listWidget.takeItem(currentRow)
            listWidget.insertItem(currentRow + 1, currentItem)
            listWidget.setCurrentRow(currentRow + 1)
        except:
            pass  # lots of things could have gone wrong in the try block but we don't car       
        finally:
            listWidget.repaint()
            
    def moveTableViewRowDown(self, tableView):
        '''
        this moves the current row in a qtableview down one
        the cell selection moves as well
        error situations are ignored  by the try except block
        '''
        try:
            indexes = tableView.selectionModel().selectedIndexes()
            if len(indexes) > 0:
                rowIndex = indexes[0]
                if rowIndex.row() == tableView.model().rowCount() - 1:
                    self.displayErrMsg("Move Row Down", "Can't move the last row down.")
                else:
#                    print("{}-{}".format(rowIndex.row(), rowIndex.column()))
                    # delete the row from current position but save the items in the row
                    rowItemList = tableView.model().takeRow(rowIndex.row())
                    # add the row below next row
                    tableView.model().insertRow(rowIndex.row()+1, rowItemList)
                    # set selection to the moved row
                    tableView.selectionModel().select(rowIndex.sibling(rowIndex.row()+1, rowIndex.column()), QItemSelectionModel.ClearAndSelect)
                    # scroll to the newly inserted row to insure it is visible
                    tableView.scrollTo (tableView.selectionModel().selectedIndexes()[0], hint = QAbstractItemView.EnsureVisible)

            else:
                self.displayErrMsg("Move Row Down", "You must select a row to move down.")
        except:
            self.displayErrMsg("Move Row Down", "Unknown error attempting to move row down.")  
        finally:
            tableView.repaint()
    
    def moveTableViewRowUp(self, tableView):
        '''
        this moves the current row in a qtableview up one
        the cell selection moves as well
        error situations are ignored  by the try except block
        '''
        try:
            indexes = tableView.selectionModel().selectedIndexes()
            if len(indexes) > 0:
                rowIndex = indexes[0]
                if rowIndex.row() == 0:
                    self.displayErrMsg("Move Row Up", "Can't move the first row up.")
                else:
                    # delete the row from current position but save the items in the row
                    rowItemList = tableView.model().takeRow(rowIndex.row())
                    # add the row above next row
                    tableView.model().insertRow(rowIndex.row()-1, rowItemList)
                    # set selection to the moved row and cell
                    tableView.selectionModel().select(rowIndex.sibling(rowIndex.row()-1, rowIndex.column()), QItemSelectionModel.ClearAndSelect)
                    # scroll to the newly inserted row to insure it is visible
                    tableView.scrollTo (tableView.selectionModel().selectedIndexes()[0], hint = QAbstractItemView.EnsureVisible)
            else:
                self.displayErrMsg("Move Row Up", "You must select a row to move up.")
        except:
            self.displayErrMsg("Move Row Up", "Unknown error attempting to move row up.") 
        finally:
            tableView.repaint()

    def delObjectPrompt(self, objectType):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Do you want to Delete {} ?".format(objectType))
        msgBox.setWindowTitle("CONFIRM {} DELETE".format(objectType))
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msgBox.exec_()
        if result == QMessageBox.Yes:
            return True
        else:
            return False
            
    def removeObjectPrompt(self, objectType):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Do you want to remove the {} from the diagram?".format(objectType))
        msgBox.setWindowTitle("CONFIRM {} REMOVE".format(objectType))
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msgBox.exec_()
        if result == QMessageBox.Yes:
            return True
        else:
            return False
            
    def delRowsPrompt(self, startRow=None, endRow=None):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        if (startRow is not None and (endRow is None or endRow == startRow)):
            msgBox.setText("Do you want to Delete Row {} ?".format(startRow))
            msgBox.setWindowTitle("CONFIRM DELETE")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msgBox.exec_()
            if result == QMessageBox.Yes:
                return True
            else:
                return False        
        if (endRow is not None and startRow is not None):
            msgBox.setText("Do you want to Delete Rows {} - {} ?".format(startRow, endRow))
            msgBox.setWindowTitle("CONFIRM DELETE")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msgBox.exec_()
            if result == QMessageBox.Yes:
                return True
            else:
                return False        
        
        return False

    def saveChangedObject(self, objectType, objectName):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("{}: {} has changed.  Do you want to Save?".format(objectType, objectName))
        msgBox.setWindowTitle("{} Has Changed".format(objectType))
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msgBox.exec_()
        if result == QMessageBox.Yes:
            return True
        else:
            return False
        
    def displayErrMsg(self, errTitle, errMsg): 
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(errMsg)
        msgBox.setWindowTitle(errTitle)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()  

    def  textBadLengthError(self, var, min, max, errmsg):
        if len(var) < min:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(errmsg)
            msgBox.setWindowTitle("Error - Value too short")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            return True            
        if len(var) > max:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(errmsg)
            msgBox.setWindowTitle("Error - Value too long")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            return True
        
        return False

    def NoComboBoxSelectionError(self, comboBox, errmsg):
        '''
        if the combobox selection index is 0 that means the user hasn't selected anything yet
        if the selected text is a zero length string that is also an error
        '''
        if (comboBox.currentIndex() == 0 or len(comboBox.currentText()) == 0):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(errmsg)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            return True        
    
    def  NoTextValueError(self, var, errmsg):
        '''
        check var to see that it has a text value
        QListWidget should have len > 0
        '''
        if type(var) == "QListWidget":
            if len(var) == 0:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText(errmsg)
                msgBox.setWindowTitle("Warning")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()
                return True

        elif type(var) == "String":
            if len(var.strip()) == 0:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText(errmsg)
                msgBox.setWindowTitle("Warning")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()
                return True

        else:
            if len(var) == 0:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText(errmsg)
                msgBox.setWindowTitle("Warning")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()
                return True
        return False
        
    def DupObjectError(self, designModel = None, objName=None, topLevel = None, txtMsg = None):
        '''
        Check to see if an object name has already been used for a top level object in the design model.
        The function returns True if the duplicate exists.
        '''
        if designModel.objectExists(topLevel=topLevel, objectName=objName):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(txtMsg)
            msgBox.setWindowTitle("Duplicate Object Name Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            return True
        else:
            return False  

    def gridNoEntryError(self, grid=None, txtMsg=None):
        'check to see that the grid has at least one row'
        model=grid.model()
        numrows = model.rowCount()
        if numrows > 0:
            return False
        self.displayErrMsg("Validate Label", txtMsg)
        return True
    
    def gridAtLeastOneRequired(self, grid=None, col=None, txtMsg=None):
        'check each row in the grid and make sure at least one of the rows has the checkbox checked for the given column'
        model = grid.model()
        numrows = model.rowCount()
        foundOne = False
        for row in range(0,numrows):
            checkIt = model.item(row,col).checkState()
            if checkIt == 2:
                foundOne = True
        if foundOne == False:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(txtMsg)
            msgBox.setWindowTitle("At Lease One Required")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            return True
        else:
            return False            
        
    def gridNoNameError(self, grid=None, col=None, txtMsg=None):
        '''
        Check each row in the grid and make sure the specified column has a text value
        '''
        model = grid.model()
        numrows = model.rowCount()
        for row in range(0,numrows):
            checkIt = model.item(row,col).data(Qt.EditRole)
            if len(checkIt) == 0:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("Row: {} - {}".format(str(row+1), txtMsg))
                msgBox.setWindowTitle("Mising Label Name")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()
                return True
        return False    

    def gridNoSelectionError(self, designModel=None, grid=None, col=None, lookup=None, txtMsg=None):
        '''
        Check each row in the grid and make sure the specified column has a valid designmodel object name value
        '''
        model = grid.model()
        numrows = model.rowCount()
        rc = False
        for row in range(0,numrows):    
            checkIt = model.item(row,col).data(Qt.EditRole)  
            if not(designModel.objectExists(topLevel=lookup,objectName=checkIt )):
                self.displayErrMsg("Validate Selection", txtMsg)
                rc = True
        return rc
    
    def gridDupEntryError(self, grid=None, col=None, txtMsg=None):
        '''
        Check each row in the grid and make sure the value in the specified column is only used once in all rows
        '''
        model = grid.model()
        numrows = model.rowCount()
        rc = False
        checkList = []
        for row in range(0,numrows):  
            if model.item(row,col).data(Qt.EditRole) in checkList:
                self.displayErrMsg("Validate No Duplicates", "Value: {} - {}".format(model.item(row,col).data(Qt.EditRole), txtMsg))
                rc = True
            else:
                checkList.append(model.item(row,col).data(Qt.EditRole))
        return rc

    def csvNumItemsError(self, value=None, min=None, max=None, msg=None):
        rc = False
        if value is None:
            value = ""
        if min is None:
            min=0
        if max is None:
            max=0
        valueList = value.split(",")
        if len(valueList) < min:
                self.displayErrMsg("Check Number Of Items", msg)
                rc = True
        elif len(valueList) > max:
                self.displayErrMsg("Check Number of Items", msg)
                rc = True
        return rc    
        
        
########################################################
# combobox delegate for grid
########################################################
class CBDelegate(QItemDelegate):
    def __init__(self, owner, items, setEditable=None):
        super(CBDelegate, self).__init__(owner)
        self.items = items
        if setEditable is None:
            self.setEditable = True
        else:
            self.setEditable = setEditable
        
    def createEditor(self, parent, option, index):
#        print("createEditor. editable={}".format(self.setEditable))
        self.editor = QComboBox(parent)
        self.editor.setEditable(self.setEditable)
        self.editor.addItems(self.items)
        return self.editor
        
    def setEditorData(self, editor, index):
        value = index.data(Qt.DisplayRole)
        try:
            num = self.items.index(value)
            editor.setCurrentIndex(num)
        except:
            editor.setCurrentIndex(0)
        
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        if value == '':
            model.setData(index, self.items[0], Qt.DisplayRole) # show default unselected value
        else:
            model.setData(index, value, Qt.DisplayRole)
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)   

#########################################################
## combobox subclass that provides checkboxes
#########################################################
#class CheckableComboBox(QComboBox):
#    # once there is a checkState set, it is rendered
#    # here we assume default Unchecked
#    def addItem(self, item):
#        super(CheckableComboBox, self).addItem(item)
#        item = self.model().item(self.count()-1,0)
#        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
#        item.setCheckState(Qt.Unchecked)
#
#    def itemChecked(self, index):
#        item = self.model().item(index,0)
#        return item.checkState() == Qt.Checked
#        
#########################################################
## checkable combobox delegate for grid
#########################################################
#class CCBDelegate(QItemDelegate):
#    def __init__(self, owner, items, setEditable=None):
#        super(CCBDelegate, self).__init__(owner)
#        self.items = items
#        self.setEditable = setEditable
#        
#    def createEditor(self, parent, option, index):
#        self.editor = CheckableComboBox(parent)
#        if self.setEditable:
#            self.editor.setEditable(self.setEditable)
##        self.editor.addItems(self.items)
#            for item in self.items:
#                self.editor.addItem(item)
#        return self.editor
#        
#    def setEditorData(self, editor, index):
#        value = index.data(Qt.DisplayRole)
#        try:
#            num = self.items.index(value)
#            editor.setCurrentIndex(num)
#        except:
#            editor.setCurrentIndex(0)
#        
#    def setModelData(self, editor, model, index):
#        value = editor.currentText()
#        if value == '':
#            model.setData(index, self.items[0], Qt.DisplayRole) # show default unselected value
#        else:
#            model.setData(index, value, Qt.DisplayRole)
#        
#    def updateEditorGeometry(self, editor, option, index):
#        editor.setGeometry(option.rect)      
########################################################
# checkbox delegate for grid
########################################################
class CheckBoxDelegateQt(QStyledItemDelegate):
    """ Delegate for editing bool values via a checkbox with no label centered in its cell.
    Does not actually create a QCheckBox, but instead overrides the paint() method to draw the checkbox directly.
    Mouse events are handled by the editorEvent() method which updates the model's bool value.
    """
    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        """ Important, otherwise an editor is created if the user clicks in this cell.
        """
        return None

    def paint(self, painter, option, index):
        """ Paint a checkbox without the label.
        """
        checked = bool(index.model().data(index, Qt.DisplayRole))
        opts = QStyleOptionButton()
        opts.state |= QStyle.State_Active
        if index.flags() & Qt.ItemIsEditable:
            opts.state |= QStyle.State_Enabled
        else:
            opts.state |= QStyle.State_ReadOnly
        if checked:
            opts.state |= QStyle.State_On
        else:
            opts.state |= QStyle.State_Off
        opts.rect = self.getCheckBoxRect(option)
        QApplication.style().drawControl(QStyle.CE_CheckBox, opts, painter)

    def editorEvent(self, event, model, option, index):
        """ Change the data in the model and the state of the checkbox if the
        user presses the left mouse button and this cell is editable. Otherwise do nothing.
        """
        if not (index.flags() & Qt.ItemIsEditable):
            return False
        if event.button() == Qt.LeftButton:
            if event.type() == QEvent.MouseButtonRelease:
                if self.getCheckBoxRect(option).contains(event.pos()):
                    self.setModelData(None, model, index)
                    return True
            elif event.type() == QEvent.MouseButtonDblClick:
                if self.getCheckBoxRect(option).contains(event.pos()):
                    return True
        return False

    def setModelData(self, editor, model, index):
        """ Toggle the boolean state in the model.
        """
        checked = not bool(index.model().data(index, Qt.DisplayRole))
        model.setData(index, checked, Qt.EditRole)

    def getCheckBoxRect(self, option):
        """ Get rect for checkbox centered in option.rect.
        """
        # Get size of a standard checkbox.
        opts = QStyleOptionButton()
        checkBoxRect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, opts, None)
        # Center checkbox in option.rect.
        x = option.rect.x()
        y = option.rect.y()
        w = option.rect.width()
        h = option.rect.height()
        checkBoxTopLeftCorner = QPoint(x + w / 2 - checkBoxRect.width() / 2, y + h / 2 - checkBoxRect.height() / 2)
        return QRect(checkBoxTopLeftCorner, checkBoxRect.size())
    

        

        
################################################################################################################
# Qscintilla lexers
################################################################################################################
class CypherLexer(QsciLexerCustom):

    def __init__(self, parent):
        super(CypherLexer, self).__init__(parent)

        self.settings = QSettings()
        # this causes an error
        try:
            self.curFontSize = int(self.settings.value("Lexer/FontSize", "10"))
        except:
            self.curFontSize = 10
            
        self.curFontSize = 10
        
        self.multiLineComment = False
        self.lineComment = False      
        
        self.initSettings()
#        self.setFonts()
        self.cypher_keywords = [
            "AS",
            "ASC",
            "ASCENDING",
            "ASSERT",
            "ASSERT EXISTS",
            "EXISTS", 
            "CALL",
            "CONSTRAINT ON",
            "ON", 
            "CREATE",
            "CREATE UNIQUE",
            "UNIQUE", 
            "CYPHER",
            "DELETE",
            "DESC",
            "DESCENDING",
            "DETACH DELETE",
            "DO",
            "DROP",
            "EXPLAIN",
            "FIELDTERMINATOR",
            "FOREACH",
            "FROM",
            "GRAPH",
            "GRAPH AT",
            "GRAPH OF",
            "INDEX ON",
            "AT",  "OF",  "ON", 
            "INTO",
            "IS", "NODE", "KEY", 
            "IS NODE KEY",
            "UNIQUE", 
            "IS UNIQUE",
            "LIMIT",
            "LOAD",
            "LOAD CSV",
            "CSV", 
            "MATCH",
            "MERGE",
            "ON CREATE SET",
            "ON MATCH SET",
            "OPTIONAL", 
            "OPTIONAL MATCH",
            "ORDER BY",
            "ORDER", 
            "BY", 
            "PERSIST",
            "_PRAGMA",
            "PROFILE",
            "REMOVE",
            "RELOCATE",
            "RETURN",
            "RETURN DISTINCT",
            "DISTINCT", 
            "SET",
            "SKIP",
            "SNAPSHOT",
            "SOURCE",
            "START",
            "TARGET",
            "UNION",
            "UNION ALL",
            "ALL", 
            "UNWIND",
            "USING", 
            "USING INDEX",
            "JOIN", 
            "USING JOIN ON",
            "PERIODIC", "COMMIT"
            "USING PERIODIC COMMIT",
            "USING SCAN", "SCAN"
            "WHERE",
            "WITH",
            "WITH DISTINCT",
            "WITH HEADERS", "HEADERS"
            "YIELD",
            ">>",
        ]
        self.cypher_pseudo_keywords = [
            "BEGIN",
            "COMMIT",
            "ROLLBACK",
        ]
        self.cypher_operator_symbols = [
            "!=",
            "%",
            "*",
            "+",
            "+=",
            "-",
            ".",
            "/",
            "<",
            "<=",
            "<>",
            "=",
            "=~",
            ">",
            ">=",
            "^",
        ]
        self.cypher_operator_words = [
            'AND',
            'CASE',
            'CONTAINS',
            'DISTINCT',
            'ELSE',
            'END',
            'ENDS WITH',
            'IN',
            'IS NOT NULL', 'IS', 'NULL', 
            'IS NULL',
            'NOT',
            'OR',
            'STARTS WITH','STARTS', 'WITH'
            'THEN',
            'WHEN',
            'XOR',
        ]
        self.cypher_constants = [
            'null',
            'true',
            'false',
        ]

        self.neo4j_built_in_functions = [
            "abs",
            "acos",
            "all",
            "allShortestPaths",
            "any",
            "asin",
            "atan",
            "atan2",
            "avg",
            "ceil",
            "coalesce",
            "collect",
            "cos",
            "cot",
            "count",
            "degrees",
            "e",
            "endNode",
            "exists",
            "exp",
            "extract",
            "filter",
            "floor",
            "haversin",
            "head",
            "id",
            "keys",
            "labels",
            "last",
            "left",
            "length",
            "log",
            "log10",
            "lTrim",
            "max",
            "min",
            "nodes",
            "none",
            "percentileCont",
            "percentileDisc",
            "pi",
            "distance",
            "point",
            "radians",
            "rand",
            "range",
            "reduce",
            "relationships",
            "replace",
            "reverse",
            "right",
            "round",
            "rTrim",
            "shortestPath",
            "sign",
            "sin",
            "single",
            "size",
            "split",
            "sqrt",
            "startNode",
            "stdDev",
            "stdDevP",
            "substring",
            "sum",
            "tail",
            "tan",
            "timestamp",
            "toBoolean",
            "toFloat",
            "toInteger",
            "toLower",
            "toString",
            "toUpper",
            "properties",
            "trim",
            "type",
        ]

        self.neo4j_user_defined_functions = [
            "date",
            "date.realtime",
            "date.statement",
            "date.transaction",
            "date.truncate",
            "datetime",
            "datetime.fromepoch",
            "datetime.fromepochmillis",
            "datetime.realtime",
            "datetime.statement",
            "datetime.transaction",
            "datetime.truncate",
            "duration",
            "duration.between",
            "duration.inDays",
            "duration.inMonths",
            "duration.inSeconds",
            "localdatetime",
            "localdatetime.realtime",
            "localdatetime.statement",
            "localdatetime.transaction",
            "localdatetime.truncate",
            "localtime",
            "localtime.realtime",
            "localtime.statement",
            "localtime.transaction",
            "localtime.truncate",
            "randomUUID",
            "time",
            "time.realtime",
            "time.statement",
            "time.transaction",
            "time.truncate"
        ]        
        # create the keywork list
        self.keyword_list = (self.cypher_keywords
                                + self.neo4j_user_defined_functions 
                                + self.neo4j_built_in_functions 
                                + self.cypher_constants 
                                + self.cypher_operator_words 
                                )
        self.keyWordList = []
        for l in self.keyword_list:
            self.keyWordList.append(l.title())
            self.keyWordList.append(l.upper())
            self.keyWordList.append(l.lower())
#        print(self.keyWordList)
        
    def initSettings(self):
        # Default text settings
        # ----------------------
        self.setDefaultColor(QColor("#ff000000"))
        self.setDefaultPaper(QColor("#ffffffff"))
        self.setDefaultFont(QFont("Consolas", 10))

        # Initialize colors per style
        # ----------------------------
        self.setColor(QColor("#ff000000"), 0)   # Style 0 (defualt): black
        self.setColor(QColor("#ff7f0000"), 1)   # Style 1 (keyword) : red
        self.setColor(QColor("#ff0000bf"), 2)   # Style 2 : blue
        self.setColor(QColor("#ff007f00"), 3)   # Style 3 (comment): green
        self.setColor(QColor("#ff007f00"), 4)   # Style 4 (multiline comment): green
        # Initialize paper colors per style
        # ----------------------------------
        self.setPaper(QColor("#ffffffff"), 0)   # Style 0: white
        self.setPaper(QColor("#ffffffff"), 1)   # Style 1: white
        self.setPaper(QColor("#ffffffff"), 2)   # Style 2: white
        self.setPaper(QColor("#ffffffff"), 3)   # Style 3: white
        self.setPaper(QColor("#ffffffff"), 4)   # Style 3: white

#    def setFonts(self, ):
#        # setup fonts per style
#        self.setFont(QFont("Consolas", self.curFontSize, weight=QFont.Normal), 0)   # Style 0
#        self.setFont(QFont("Consolas", self.curFontSize, weight=QFont.Normal), 1)   # Style 1
#        self.setFont(QFont("Consolas", self.curFontSize, weight=QFont.Normal), 2)   # Style 2
#        self.setFont(QFont("Consolas", self.curFontSize, weight=QFont.Normal), 3)   # Style 3

    def language(self):
        return "Cypher"

    def description(self, style):
        if style == 0:
            return "Default"
        elif style == 1:
            return "Keywords"
        elif style == 2:
            return "multiline comment"
        elif style == 3:
            return "Comment"
        elif style == 4:
            return "MultiLine Comment"
        ###
        return ""
    ''''''

    def styleText(self, start, end):
        # 1. Initialize the styling procedure
        self.startStyling(start)

        # 2. Slice out a part from the text
        text = self.parent().text()[start:end]

        # 3. Tokenize the text
        p = re.compile(r"[*]\/|\/[*]|\s+|\w+|\W")

        # 'token_list' is a list of tuples: (token_name, token_len)
        token_list = [ (token, len(bytearray(token, "utf-8"))) for token in p.findall(text)]

#        print("start token list")
#        print("[{}]".format(text))
#        print("comment status: single:{} multi:{}".format(self.lineComment, self.multiLineComment))
#        print(token_list)
        
        # 4. Style the text

#        editor = self.parent()
#        if start > 0:
#            previous_style_nr = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
#            if previous_style_nr == 4:
#                self.multiLineComment = True

        # 4.2 Style the text in a loop
        for i, token in enumerate(token_list):

            # if it's a linefeed then stop single line comment styling
            if token[0] in [ "/r/n", "/n", "/n/n", " \n", "\n", "\r\n", " \r\n", " \n\n"]:
                self.lineComment = False
                self.setStyling(token[1], 0)

            # if we're in a line comment then keep the comment style
            elif self.lineComment:
                self.setStyling(token[1], 3)
                
            # is this the end of a multiline comment?
            elif token[0] == "*/":
                self.multiLineComment = False
                self.setStyling(token[1], 4)
                
            # if we're in a multiline comment then keep the comment style
            elif self.multiLineComment:
                self.setStyling(token[1], 4)
                
            # is this the start of an inline comment?
            elif token[0] == "/":
                if i > 0 and token_list[i-1][0] == "/" and self.lineComment == False:
                    self.lineComment = True
                    self.setStyling(token_list[i-1][1], 3)
                    self.setStyling(token[1], 3)
                    
            # is this the start of a multiline comment?
            elif token[0] == "/*":
                self.multiLineComment = True
                self.setStyling(token[1], 4)   
                
            # style keywords
            elif token[0] in self.keyWordList:
                self.setStyling(token[1], 1)
            
            # style brackets
            elif token[0] in ["(", ")", "{", "}", "[", "]"]:
                self.setStyling(token[1], 2)
                
            # style other special characters
            elif token[0] in self.cypher_operator_symbols:
                self.setStyling(token[1], 2)

            else:
                # Default style
                self.setStyling(token[1], 0)
            
        # always reset single line comment flag to false
        self.lineComment = False
