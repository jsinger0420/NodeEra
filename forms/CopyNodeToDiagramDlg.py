# -*- coding: utf-8 -*-

"""
Module implementing CopyNodeToDiagramDlg.
    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
from PyQt5.QtCore import pyqtSlot, Qt, QSettings, QPointF
from PyQt5.QtWidgets import QDialog, QAbstractButton,  QApplication, QVBoxLayout
from .Ui_CopyNodeToDiagramdlg import Ui_CopyNodeToDiagramDlg
from forms.DataGridWidget import DataGridWidget
from core.helper import Helper
#from core.neocon import NeoCon
from core.NeoDriver import NeoDriver
from core.AddNodeCypher import AddNodeCypher
from core.NeoTypeFunc import NeoTypeFunc

# NodeEra managed nodes grid columns
DIAGRAMITEM, ITEMKEY = range(2)
# Project diagram nodes grid columns
LABELS, PROPERTIES, NODEERAKEY = range(3)
# tab names
INSTANCENODES, DATABASENODES = range(2)

class CopyNodeToDiagramDlg(QDialog, Ui_CopyNodeToDiagramDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, rightClickPos=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(CopyNodeToDiagramDlg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.settings = QSettings()
        self.rightClickPos = rightClickPos
        self.designModel = self.parent.model
        self.syncNeoCon = self.designModel.modelNeoCon
        self.itemDict = self.parent.itemDict
        self.helper = Helper()
        self.neoTypeFunc = NeoTypeFunc()
        self.nodeGrid = None
        
        # header area
        self.txtDiagramName.setText(self.parent.diagramName)  
        self.txtNeoCon.setText("{} - {}".format( self.syncNeoCon.name, self.syncNeoCon.neoDict["URL"]))

        # load  node template dropdown and disable it
        dropdownList = []
        dropdownList.append("No Template Selected")
        dropdownList.extend(sorted(self.designModel.instanceList("Node Template")))
        self.cboNodeTemplates.addItems(dropdownList)
        self.rbFilterTemplate.setChecked(True) 
        
        # get neocon object for this project page
        self.neoCon = NeoDriver(name=self.parent.parent.pageItem.neoConName, promptPW=self.parent.parent.pageItem.promptPW)
        
        # add the data grid widget.  
        self.addNodeCypher = AddNodeCypher()

        self.nodeGrid = DataGridWidget(self, neoCon=self.neoCon, genCypher=self.addNodeCypher)
        self.nodeGridLayout = QVBoxLayout(self.frmDataGrid)
        self.nodeGridLayout.setObjectName("nodeGridLayout")
        self.nodeGridLayout.addWidget(self.nodeGrid)    
        


    def refreshDatabaseNodeGrid(self, ):
        # first make sure the node grid has been created.
        if self.nodeGrid is None:
            return
            
        nodeTemplate = self.cboNodeTemplates.currentText()
        index, nodeTemplateDict = self.designModel.getDictByName(topLevel="Node Template",objectName=nodeTemplate)
        if self.rbFilterTemplate.isChecked() == True:
            useTemplate  = True
        else:
            useTemplate = False
        
        self.nodeGrid.refreshGrid(useTemplate=useTemplate, nodeTemplate=nodeTemplate, nodeTemplateDict=nodeTemplateDict)        
 
    def getNodeRels(self, nodeID, nodeIDList):
        '''
        Run a query that retrieves all relationships between one node and all other nodes on a diagram
        '''
        try:
            msg = None
            p1 = str(nodeID)
            p2 = str(nodeIDList)
            cypher = '''match (f)-[r]->(t)
                            where ((id(f) = {} and id(t) in {}) or (id(t) = {} and id(f) in {}))
                            return id(f),
                                    f.NZID,
                                    f, 
                                    id(r), 
                                    type(r),
                                    r.NZID,
                                    r,
                                    id(t),
                                    t.NZID,
                                    t
                            '''.format(p1, p2, p1, p2)
#            print(cypher)
            #run the query
            rc1, msg1 = self.syncNeoCon.runCypherAuto(cypher)

        except BaseException as e:
            msg = "{} - Get Relationships failed.".format(repr(e))
        finally: 
            QApplication.restoreOverrideCursor()
            if not msg is None:
                self.helper.displayErrMsg("Error Retrieving Relationships.", msg ) 
                
                
#####################################################################################
# dialog buttons
#####################################################################################
    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        Slot documentation goes here.
        
        @param button DESCRIPTION
        @type QAbstractButton
        """

                
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        
        """
        QDialog.accept(self)
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        QDialog.reject(self)
    

    @pyqtSlot()
    def on_rbAllNodes_clicked(self):
        """
        User selects all Nodes option, so configure UI and refresh the grid
        """
        self.cboNodeTemplates.setEnabled(False)
        self.refreshDatabaseNodeGrid()
        
    @pyqtSlot()
    def on_rbFilterTemplate_clicked(self):
        """
        User selects filter on template option
        """
        self.cboNodeTemplates.setEnabled(True)
        self.refreshDatabaseNodeGrid()
    
    @pyqtSlot(int)
    def on_cboNodeTemplates_currentIndexChanged(self, index):
        """
        User changes the node template selection so refresh the grid
        
        @param index DESCRIPTION
        @type int
        """
        self.refreshDatabaseNodeGrid()
    
    @pyqtSlot()
    def on_btnAdd_clicked(self):
        """
        User clicks the add button so add the selected nodes to the diagram
        """

        applyX = self.rightClickPos.x()
        applyY = self.rightClickPos.y()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if self.rbAllNodes.isChecked() == True:
            ID, LBLS, PROPS, NODE = range(4)
        else:
            ID, NODE = range(2)
        # get the selected node template
        if self.rbFilterTemplate.isChecked() == True:    
            nodeTemplate = self.cboNodeTemplates.currentText()
        else:
            nodeTemplate = None

        # make sure there is data in the grid
        if self.nodeGrid.gridCypherData.selectionModel() is None:
            self.helper.displayErrMsg("Copy Node", "Select a Node Template or All Nodes.")
            QApplication.restoreOverrideCursor() 
            return
            
        # check if any rows selected
        if len(self.nodeGrid.gridCypherData.selectionModel().selectedRows(column=0)) > 0:
            # looking at nodes in the database
            for itemIndex in self.nodeGrid.gridCypherData.selectionModel().selectedRows(column=0):
                # get the Neo4j node id from the result set
                instanceNodeID = self.nodeGrid.gridCypherData.model().item(itemIndex.row(), ID).data(Qt.EditRole)
                # see if it's already an instance node in the model
                instanceNZID = self.designModel.lookupNZID(neoID = instanceNodeID, topLevel="Instance Node")
                # get the node object
                n = self.nodeGrid.gridCypherData.model().item(itemIndex.row(),NODE).data(Qt.UserRole)
                # get the list of labels from the node object
                lbls = [[lbl] for lbl in n.labels]  
                # get the dictionary of properties from the node object  and convert it to a list
                props = []
                for key, val in dict(n).items():
                    props.append( [key, self.neoTypeFunc.getNeo4jDataType(value=val),self.neoTypeFunc.convertTypeToString(dataValue=val) ])
                # create a new node instance dictionary
                newNodeInstanceDict = self.designModel.newNodeInstance(nodeID = instanceNodeID, templateName=nodeTemplate, labelList=lbls, propList=props,  NZID=instanceNZID)
                NZID = self.parent.scene.dropINode(point=QPointF(applyX, applyY), nodeInstanceDict=newNodeInstanceDict, NZID=instanceNZID)

                if not NZID is None:
                    applyX = applyX + 200

            QApplication.restoreOverrideCursor() 
            self.helper.displayErrMsg("Copy Node", "Selected Node(s) were added to diagram.")
            # update project model
            self.parent.model.setModelDirty()
            self.parent.model.updateTV()
        else:
            QApplication.restoreOverrideCursor() 
            self.helper.displayErrMsg("Copy Node", "You must select a node to add to the diagram.")   
                
        QApplication.restoreOverrideCursor() 
