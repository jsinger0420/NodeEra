# -*- coding: utf-8 -*-

"""
UC-07 Instance Diagram Tab
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
import uuid
from PyQt5.QtCore import pyqtSlot,  QRectF, QPointF,  pyqtSignal, QModelIndex, QObject
from PyQt5.QtGui import  QColor,  QPen, QPainter, QCursor, QPainterPath, QStandardItemModel
from PyQt5.QtWidgets import QWidget,  QGraphicsView,  QGraphicsScene, QMenu, QGraphicsRectItem,  QApplication
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

# this has to follow the previous import so references to Qt.xxx will work
from PyQt5.QtCore import Qt

from forms.Ui_InstanceDiagramTab import Ui_InstanceDiagramTab
from forms.NodePropertyBox import NodePropertyBox
from forms.INPropertyBox import INPropertyBox
from forms.IRPropertyBox  import IRPropertyBox
from forms.TRPropertyBox import TRPropertyBox
from forms.PageSetupDlg import dlgPageSetup
from forms.SyncToDBDlg import SyncToDBDlg
from forms.CopyNodeToDiagramDlg import CopyNodeToDiagramDlg
from forms.ObjectRenameDlg import ObjectRenameDlg
from core.helper import PageSetup, PageSizes, Helper
#from core.InstanceRel import RelationInstance
from core.RelationInstance import RelationInstance
from core.RelationItem import RelationItem
from core.RelationTemplateItem import RelationTemplateItem
#from core.InstanceNode import NodeInstance
from core.NodeInstance import NodeInstance
from core.NodeItem import NodeItem
from core.NodeTemplateItem import NodeTemplateItem
from core.NeoTypeFunc import NeoTypeFunc

# enum for editor modes
POINT = 1
SHOVE = 2
INODE = 3
IREL = 4
TNODE = 5
TREL = 6

# enum for graphic item user data types
NODEID = 1
ITEMTYPE = 2
# enum for graphic item types
PAGEGRID = 0
NODEINSTANCE = 1
RELINSTANCEARC = 2
NODETEMPLATE = 3
RELTEMPLATE = 4
RELINSTANCETEXT = 5
NODEINSTANCETEXT = 6
RELTEMPLATETEXT = 7
RELTEMPLATELINE = 8
NODETEMPLATETEXT = 9

# enum for z value graphics item stacking - higher numbered items cover lower numbered items
PAGELAYER = 0
RELATIONLAYER = 1
NODELAYER = 2

class GraphicsView(QGraphicsView):
    ''' The Graphics View is the widgit that maps a portion of the Graphics Scene to the UI.
        See the constructor of class InstanceDiagramTab.
    '''
    def __init__(self,  parent=None):
        super(GraphicsView,  self).__init__(parent)
        self.parent = parent

        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setAcceptDrops(True)
        
    def hoverEnterEvent(self, e):
#        print ("view hoverEnterEvent {}".format(e))
        # let the scene do the work
        super(GraphicsView, self).hoverEnterEvent(e)    
        
    def dragEnterEvent(self, e):
#        print ("view dragEnterEvent {}".format(e))
        # let the scene do the work
        super(GraphicsView, self).dragEnterEvent(e)

    def dragMoveEvent(self, e):
#        print ("view dragMoveEvent".format(e))
        super(GraphicsView, self).dragMoveEvent(e)
    
    def dropEvent(self, e):
#        print ("view dropEvent {}".format(e))
        # let the scene do the work
        super(GraphicsView, self).dropEvent(e)
        
    def wheelEvent(self, event):
        
        factor = 1.4 ** (-event.angleDelta().y() / 240.0)
        if factor > 1:
            self.parent.on_btnZoomOut_clicked()
        else:
            self.parent.on_btnZoomIn_clicked()
#        print("angledelta: {} factor:{}".format(event.angleDelta(), factor))


class GraphicsScene(QGraphicsScene):
    ''' The Graphics Scene is where objects are drawn and can be larger than what is displayed.
        The Graphics Scene responds to mouse events.
        What happens on a mouse click depends on which mode button is selected. 
        When the mouse is double-clicked the selected object editor will be displayed.
        '''
    treeViewUpdate = pyqtSignal()
    def __init__(self,  parent=None):
        super(GraphicsScene,  self).__init__(parent)
        
        self.parent = parent
        self.model = self.parent.model
        self.neoTypeFunc = NeoTypeFunc()
        self.editMode = POINT
        self.RelStartMode = False
        self.RelEndMode = False
        self.RelStartItem = None
        self.RelEndItem = None    
        self.oldX = None
        self.oldY = None
        self.rubberBandRect = None
        self.helper = Helper()
        self.rubberBand = False
        self.rubberBandSelections = False

        
    def dragEnterEvent(self, e):
        '''
        A new dragging operation has started.  The dragged object has entered the scene.
        - Capture the object type and object key of the dragged object
        - Accept the drag operation if the object type is ok to drop on the diagram type
        - Otherwise, ignore the drag operation
        '''
        formats = e.mimeData().formats()
        if 'application/x-qabstractitemmodeldatalist' in formats:
#            e.accept()
            # create an empty item model to add the dragged item to.
            model = QStandardItemModel()
            model.dropMimeData(e.mimeData(), Qt.CopyAction, 0,0, QModelIndex())
            # get the dragged qstandarditem and it's data
            self.dragItem = model.itemFromIndex(QStandardItemModel.index(model, 0, 0))
            self.dragDataType = self.dragItem.data(Qt.UserRole)
            # the nzid for instances is in qt.userrole+1
            if self.dragDataType in ["Instance Node", "Instance Relationship"]:
                self.dragDataKey = self.dragItem.data(Qt.UserRole+1)
            else:
                self.dragDataKey = self.dragItem.data(Qt.DisplayRole)
            
#            print("Drag Object Type: {} Key: {}".format(self.dragDataType,self.dragDataKey ))
            # make sure the dragged object type is comapible with the diagram type
            if (self.parent.tabType == "Instance Diagram" and self.dragDataType in ["Instance Node", "Instance Relationship"]):
                e.accept()
            else:
                if (self.parent.tabType == "Template Diagram" and self.dragDataType in ["Node Template", "Relationship Template"]):
                    e.accept()
                else:
                    e.ignore()
                    
    def dragMoveEvent(self, e):
#        print ("scene dragMoveEvent {}".format(e))
        e.accept()
    
    def dropEvent(self, e):
        '''
        A dragged object has been dropped on the scene.  
        - call the appropriate add function to add the object to the diagram
        '''
        # get the QpointF where the drop occurred
        self.scenePos = e.scenePos() 
        # see if the dragged object was dropped on another object
        items = self.items(e.scenePos())
        droppedOnItem = None
        for item in items:
            if item.data(ITEMTYPE) in [NODETEMPLATE]:
                droppedOnItem = self.parent.itemDict[item.data(NODEID)]
        if self.dragDataType == "Instance Node":
            saveIndex, nodeDict = self.model.getDictByName(topLevel="Instance Node",objectName=self.dragDataKey)
            # add it    
            self.dropINode(e.scenePos(), nodeInstanceDict=nodeDict)

        if self.dragDataType == "Instance Relationship":
            # make sure it's not already on the diagram
            if self.dragDataKey in [key for key, value in self.parent.itemDict.items()]:
                self.helper.displayErrMsg("Drop Instance Relationship", "This Relationship already exists on this diagram.  An Instance Relationship can only be on a diagram once")                 
                return

            # add it
            self.addIRelationship(NZID=self.dragDataKey, mode="Drop" ) 

            
        if self.dragDataType == "Node Template":
            saveIndex, nodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=self.dragDataKey)
            # add it    
            self.dropTNode(e.scenePos(), nodeTemplateDict=nodeTemplateDict )   

            
        if self.dragDataType == "Relationship Template":
            saveIndex, relTemplateDict = self.model.getDictByName(topLevel="Relationship Template",objectName=self.dragDataKey)
            self.dropTRel(e.scenePos(), relTemplateDict = relTemplateDict, nodeTemplateItem=droppedOnItem )
            

        
    def mousePressEvent(self, event):
        position = QPointF(event.scenePos())
        self.savePosition = QPointF(event.scenePos())
        '''
        Process left button clicks
        '''
        if event.button()==Qt.LeftButton:
#            print ("scenePos LB pressed here: " + str(position.x()) + ", " + str(position.y()))
            '''
            in POINT mode, the user can select items on the diagram
            - when the user clicks, all selected items are deselected, and the current item (if there is one} is selected.  
            - when the user control clicks, all selected items remain selected, and the current item is selected
            ''' 
            if self.editMode == POINT:
                self.oldX = position.x()
                self.oldY = position.y()
                items = self.items(event.scenePos())
                # if there is no rubberband selections, then select the first selectable item under the mouse
                if self.rubberBandSelections == False:
                    self.clearSelection()
                    if len(items) > 0:
                        for item in items:
                            if item.data(ITEMTYPE) in [NODEINSTANCE,NODETEMPLATE, RELTEMPLATE, RELINSTANCETEXT, RELTEMPLATELINE, RELTEMPLATETEXT ]:
                                item.setSelected(True)
                                if item.data(ITEMTYPE)  in [RELTEMPLATELINE, RELTEMPLATETEXT]:
                                    relTemplateItem = self.parent.itemDict[item.data(NODEID)]
                                    if not relTemplateItem is None:
                                        relTemplateItem.selectItems()
                                return                
                    # did not find a dragable item so turn on rubberbanding
                    self.rubberBand = True
                    aPen = QPen()
                    aPen.setWidth(1)
                    aPen.setStyle(Qt.DotLine)
                    self.rubberBandRect = QGraphicsRectItem(QRectF(position.x(),position.y(),1, 1))
                    self.rubberBandRect.setPen(aPen)
                    self.rubberBandRect.setZValue(NODELAYER)
                    self.addItem(self.rubberBandRect) 
                else:
                    # if there are rubber band selections, is the current mouse press on one of them?
                    if any(item in self.selectedItems() for item in items):
                        self.rubberBandSelections = True
                    else:
                        # user clicked outside the items selected via the rubberband selection so clear all selections
                        self.rubberBandSelections = False
                        self.clearSelection()
                
                return
                
            if self.editMode == SHOVE:
                '''
                In SHOVE mode, the cursor turns to a hand, 
                - when the mouse is depressed, the user will drag the diagram around
                
                This functionality is provided entirely by the QT framework, no logic needed here
                '''
                return
                
            if self.editMode == TNODE:
                '''
                In TNODE mode:
                - when the user clicks the mouse, a new Node Template will be drawn on the diagram
                '''
                self.addNewNodeTemplate(position)
                return
            
            if self.editMode == TREL:
                '''
                In TREL mode:
                -  the user must select a start and and end node Template to create a relationship
                - if no selections have been made - when the user clicks a start node template will be selected
                - if a start node has been selected - when the user clicks an end node template will be selected
                '''
                if self.RelStartMode:
                    # no selection has been made so select the start node
                    self.clearSelection()
                    items = self.items(event.scenePos())
                    if len(items) > 0:
                        clickItem = items[0]
                        # must click on a node template
                        if clickItem.data(ITEMTYPE) in [NODETEMPLATE, NODETEMPLATETEXT]:
                            clickItem.setSelected(True)
                            self.RelStartItem = clickItem
                            self.RelStartMode = False
                            self.RelEndMode = True
                            self.parent.updateMsgBar("Click on relationship end node template.")
                        else:
                            self.helper.displayErrMsg("Add Relationship Template", "Click on a Node Template to select start node template for the relationship.")
                    return
                if self.RelEndMode:
                    # the start node has been selected so select the end node
                    items = self.items(event.scenePos())
                    if len(items) > 0:
                        clickItem = items[0]
                        # must click on a node template
                        if clickItem.data(ITEMTYPE) in [NODETEMPLATE, NODETEMPLATETEXT]:
                            clickItem.setSelected(True)
                            self.RelEndItem = clickItem
                            self.addNewRelationshipTemplate(startNode=self.RelStartItem, endNode=self.RelEndItem)
                        else:
                            self.helper.displayErrMsg("Add Relationship Template", "Click on a Node Template to select end node template for the relationship.")

            
            if self.editMode == INODE:
                '''
                In INODE mode:
                - when the user clicks the mouse, a new Node Instance will be drawn on the diagram
                '''
                self.addNewInstanceNode(position)
                
            if self.editMode == IREL:
                '''
                In IREL mode:
                -  the user must select a start and and end node to create a relationship
                - if no selections have been made - when the user clicks a start node will be selected
                - if a start node has been selected - when the user clicks an end node will be selected
                '''
                if self.RelStartMode:
                    # no selection has been made so select the start node
                    self.clearSelection()
                    items = self.items(event.scenePos())
                    if len(items) > 0:
                        if items[0].data(ITEMTYPE) in [NODEINSTANCE, NODEINSTANCETEXT]:
                            items[0].setSelected(True)
                            self.RelStartItem = items[0]
                            self.RelStartMode = False
                            self.RelEndMode = True
                            self.parent.updateMsgBar("Click on relationship end node.")
                        else:
                            self.helper.displayErrMsg("Add Relationship Instance", "Click on a Node Instance to select the start node for the relationship.")
                    return
                if self.RelEndMode:
                    # the start node has been selected so select the end node
                    items = self.items(event.scenePos())
                    if len(items) > 0:
                        if items[0].data(ITEMTYPE) in [NODEINSTANCE, NODEINSTANCETEXT]:
                            items[0].setSelected(True)
                            self.RelEndItem = items[0]
                            self.addNewRelationship(startNode=self.RelStartItem, endNode=self.RelEndItem)
                        else:
                            self.helper.displayErrMsg("Add Relationship Instance", "Click on a Node Instance to select the end node for the relationship.")
                    return
        '''
        Process right button clicks
        '''
        if event.button()==Qt.RightButton:
            position = QPointF(event.scenePos())
            self.rightClickPos = position 
            # clear any previously made selections
            self.clearSelection()
            # get all items under the mouse
            items = self.items(position)                       
            if len(items) > 0:
                # scan items until we find the first one that has a right click menu.
                for item in items:
#                    print("item selected-{},{}".format(item.data(NODEID), item.data(ITEMTYPE))) 
                    item.setSelected(True)
                    # generate right click menu based on item type, then exit function
                    if item.data(ITEMTYPE) in [NODEINSTANCE, NODEINSTANCETEXT]:
                        menu = QMenu()
                        editNodeAction = menu.addAction("Properties...")
                        editNodeAction.triggered.connect(self.editSelectedNodeInstance)
                        delNodeAction = menu.addAction("Remove From Diagram...")
                        delNodeAction.triggered.connect(self.removeSelectedNodeInstance)
                        wuNodeAction = menu.addAction("Where Used...")
                        wuNodeAction.triggered.connect(self.whereUsed) 
                        QApplication.setOverrideCursor(Qt.WaitCursor)
                        subInMenu = QMenu("In Bound Relationships", parent=menu)
                        # generate inboundrel menu items
                        nodeInstanceItem = self.parent.itemDict[item.data(NODEID)]
                        inBoundList = self.getInstanceNodeRels(nodeID=nodeInstanceItem.itemInstance.neoID, direction="Inbound")
                        for relInstance in inBoundList:
                            aSubAction = subInMenu.addAction(str(relInstance["r"]))
                            aSubAction.setData(relInstance)
                            aSubAction.triggered.connect(self.addInboundRelInstance)
                        if len(inBoundList) == 0:
                            aSubAction = subInMenu.addAction("No Inbound Relationship Instances")
                        menu.addMenu(subInMenu)
                        subOutMenu = QMenu("Out Bound Relationships", parent=menu)
                        # generate inboundrel menu items
                        nodeInstanceItem = self.parent.itemDict[item.data(NODEID)]
                        outBoundList = self.getInstanceNodeRels(nodeID=nodeInstanceItem.itemInstance.neoID, direction="Outbound")
                        for relInstance in outBoundList:
                            aSubAction = subOutMenu.addAction(str(relInstance["r"]))
                            aSubAction.setData(relInstance)
                            aSubAction.triggered.connect(self.addOutboundRelInstance)
                        if len(outBoundList) == 0:
                            aSubAction = subOutMenu.addAction("No Outbound Relationship Instances")
                        menu.addMenu(subOutMenu)     
                        QApplication.restoreOverrideCursor()
                        menu.exec_(QCursor.pos())
                        return
                    elif item.data(ITEMTYPE) in [NODETEMPLATE, NODETEMPLATETEXT]:
                            menu = QMenu()
                            propNodeAction = menu.addAction("Properties...")
                            propNodeAction.triggered.connect(self.editSelectedNodeInstance)
                            renameNodeAction = menu.addAction("Rename...")
                            renameNodeAction.triggered.connect(self.renameObject)
                            delNodeAction = menu.addAction("Remove From Diagram...")
                            delNodeAction.triggered.connect(self.removeSelectedNodeInstance)
                            wuNodeAction = menu.addAction("Where Used...")
                            wuNodeAction.triggered.connect(self.whereUsed) 
                            subInMenu = QMenu("In Bound Relationships", parent=menu)
                            # generate inboundrel menu items
                            nodeTemplateItem = self.parent.itemDict[item.data(NODEID)]
                            inBoundList = self.parent.model.getInboundRelTemplates(nodeTemplateName = nodeTemplateItem.name())
                            for relTemplate in inBoundList:
                                aSubAction = subInMenu.addAction(relTemplate["name"])
                                aSubAction.setData(relTemplate)
                                aSubAction.triggered.connect(self.addInboundRel)
                            if len(inBoundList) == 0:
                                aSubAction = subInMenu.addAction("No Inbound Relationship Templates")
                            menu.addMenu(subInMenu)
                            subOutMenu = QMenu("Out Bound Relationships", parent=menu)
                            # generate outboundrel menu items
                            outBoundList = self.parent.model.getOutboundRelTemplates(nodeTemplateName = nodeTemplateItem.name())
                            for relTemplate in outBoundList:
                                aSubAction = subOutMenu.addAction(relTemplate["name"])
                                aSubAction.setData(relTemplate)
                                aSubAction.triggered.connect(self.addOutboundRel)
                            if len(outBoundList) == 0:
                                aSubAction = subOutMenu.addAction("No Outbound Relationship Templates")

                            menu.addMenu(subOutMenu)

                            genNodeAction1 = menu.addAction("Generate Cypher Match")
                            genNodeAction1.triggered.connect(self.genMatch)  
                            menu.exec_(QCursor.pos())
                            return                            
                    elif item.data(ITEMTYPE) in [RELINSTANCETEXT]: 
#                            print("rel text hover {}".format(item.acceptHoverEvents()))
                            menu = QMenu()
                            addNodeAction = menu.addAction("Properties...")
                            addNodeAction.triggered.connect(self.editSelectedRelInstance)
                            addNodeAction = menu.addAction("Remove From Diagram...")
                            addNodeAction.triggered.connect(self.removeSelectedRelInstance)
                            wuNodeAction = menu.addAction("Where Used...")
                            wuNodeAction.triggered.connect(self.whereUsed)                    
                            menu.exec_(QCursor.pos())
                            return
                    elif item.data(ITEMTYPE) in [RELTEMPLATETEXT]:
                            menu = QMenu()
                            propNodeAction = menu.addAction("Properties...")
                            propNodeAction.triggered.connect(self.editSelectedRelInstance)
                            renameNodeAction = menu.addAction("Rename...")
                            renameNodeAction.triggered.connect(self.renameObject)
                            delNodeAction = menu.addAction("Remove From Diagram...")
                            delNodeAction.triggered.connect(self.removeSelectedRelInstance)
                            wuNodeAction = menu.addAction("Where Used...")
                            wuNodeAction.triggered.connect(self.whereUsed)                    
                            genNodeAction1 = menu.addAction("Generate Cypher Match")
                            genNodeAction1.triggered.connect(self.genMatch)  
                            menu.exec_(QCursor.pos())
                            return
                    else:
                        if self.parent.tabType == "Instance Diagram":
                            menu = QMenu()
                            addNodeAction = menu.addAction("Add Existing Node")
                            addNodeAction.triggered.connect(self.addExistingInstanceNode)
                            addNodeAction = menu.addAction("Sync Diagram to Graph")
                            addNodeAction.triggered.connect(self.parent.on_btnSyncDB_clicked)
                            menu.exec_(QCursor.pos())
                        elif self.parent.tabType == "Template Diagram":
                            # no right click menus on background of Template Diagram
                            pass                
           
    def notYet(self):
        return
        
    def genMatch(self, ):

        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [NODETEMPLATE]:
                nodeTemplateItem = self.parent.itemDict[item.data(NODEID)]  
                objectName=nodeTemplateItem.name()
                self.parent.parent.matchNode(nodeName=objectName)
                return
            if item.data(ITEMTYPE) in [RELTEMPLATE, RELTEMPLATETEXT]:
                relTemplateItem = self.parent.itemDict[item.data(NODEID)]  
                objectName=relTemplateItem.name()
                self.parent.parent.matchRelationship(relName=objectName)    
                return
                
    def renameObject(self):

        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [NODETEMPLATE]:
                nodeTemplateItem = self.parent.itemDict[item.data(NODEID)]  
                objectName=nodeTemplateItem.name()
                objectType = "Node Template"
                d = ObjectRenameDlg(self.parent, mode="RENAME", objectType = objectType, objectName = objectName, designModel = self.model)
                if d.exec_():
                    # tell all open diagrams to redraw
                    self.parent.parent.redrawInstanceDiagrams()            
                    self.parent.parent.redrawTemplateDiagrams() 
                    self.parent.parent.populateTree()
                return
            if item.data(ITEMTYPE) in [RELTEMPLATETEXT]:
                relTemplateItem = self.parent.itemDict[item.data(NODEID)]  
                objectName=relTemplateItem.getName()
                objectType = "Relationship Template"
                d = ObjectRenameDlg(self.parent, mode="RENAME", objectType = objectType, objectName = objectName, designModel = self.model)
                if d.exec_():
                    # tell all open diagrams to redraw
                    self.parent.parent.redrawInstanceDiagrams()            
                    self.parent.parent.redrawTemplateDiagrams() 
                    self.parent.parent.populateTree()
                return
        
    def whereUsed(self):

        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [NODEINSTANCE]:
                nodeInstanceItem = self.parent.itemDict[item.data(NODEID)]  
                objectName=nodeInstanceItem.name()
                objectType = "Instance Node"
                d = ObjectRenameDlg(self.parent, mode="VIEW", objectType = objectType, objectName = objectName, designModel = self.model)
                d.exec_()
                return
            if item.data(ITEMTYPE) in [RELINSTANCETEXT]:
                relInstanceItem = self.parent.itemDict[item.data(NODEID)]  
                objectName=relInstanceItem.name()
                objectType = "Instance Relationship"
                d = ObjectRenameDlg(self.parent, mode="VIEW", objectType = objectType, objectName = objectName, designModel = self.model)
                d.exec_()
                return
            if item.data(ITEMTYPE) in [NODETEMPLATE]:
                nodeTemplateItem = self.parent.itemDict[item.data(NODEID)]  
                objectName=nodeTemplateItem.name()
                objectType = "Node Template"
                d = ObjectRenameDlg(self.parent, mode="VIEW", objectType = objectType, objectName = objectName, designModel = self.model)
                d.exec_()
                return
            if item.data(ITEMTYPE) in [RELTEMPLATETEXT]:
                relTemplateItem = self.parent.itemDict[item.data(NODEID)]  
                objectName=relTemplateItem.name()
                objectType = "Relationship Template"
                d = ObjectRenameDlg(self.parent, mode="VIEW", objectType = objectType, objectName = objectName, designModel = self.model)
                d.exec_()
                return
                
        return
        
    def mouseMoveEvent(self, event):
        '''
        Move a Node Instance Item or a Node Template Item
        '''
        position = QPointF(event.scenePos())
        if self.editMode == POINT:
#        print ("scene mouse event moved here: " + str(position.x()) + ", " + str(position.y()))
            if not (self.oldX is None):
                deltaX = position.x() - self.oldX
                deltaY = position.y() - self.oldY
                self.oldX = position.x()
                self.oldY = position.y()
                for item in self.selectedItems():
                    if self.parent.itemDict[item.data(NODEID)].diagramType in ["Instance Node", "Node Template"]:  
                        # this calls the moveIt method on the selected item
                        self.parent.itemDict[item.data(NODEID)].moveIt(deltaX, deltaY) 

                if not self.rubberBandRect is None:
                    currentRect = self.rubberBandRect.rect()
                    currentRect.setHeight(currentRect.height() + deltaY)
                    currentRect.setWidth(currentRect.width() + deltaX)
                    self.rubberBandRect.prepareGeometryChange()
                    self.rubberBandRect.setRect(currentRect)
                
    def mouseReleaseEvent(self, event):
        self.oldX = None
        self.oldY = None
        if self.editMode == POINT:
            if not self.rubberBandRect is None:
                if self.rubberBandRect.boundingRect().width() > 2:
                    # select all the items that intersect with the rubberband rectangle
                    currentRect = self.rubberBandRect.rect()
                    myQPainterPath = QPainterPath()
                    myQPainterPath.addRect(currentRect)
                    self.setSelectionArea(myQPainterPath)
                    if len(self.selectedItems()) > 0:
                        self.rubberBandSelections = True
                    else:
                        self.rubberBandSelections = False
                self.removeItem(self.rubberBandRect)
                self.rubberBandRect = None

            self.rubberBand = False

#        position = QPointF(event.scenePos())
#        print ("scene released here: " + str(position.x()) + ", " + str(position.y()))
 
    def mouseDoubleClickEvent(self, event):       
        position = QPointF(event.scenePos())
#        print ("scene doubleclicked here: " + str(position.x()) + ", " + str(position.y()))
        if self.editMode == POINT:
            self.clearSelection()
            items = self.items(position)
    #        print("items under mouse {}".format(str(items))) 
            doubleClickedItem = None
            if len(items) > 0:
                for item in items:
                    if item.data(ITEMTYPE) in [NODEINSTANCE,NODETEMPLATE, RELTEMPLATETEXT, RELINSTANCETEXT ]:
                        item.setSelected(True)
                        doubleClickedItem = item
                        break
                if doubleClickedItem is None:
                    self.helper.displayErrMsg("Double Click", "You aren't pointing at anything that can be double clicked.")
                    return
#            print("item doubleclicked-{},{}".format(doubleClickedItem.data(NODEID), doubleClickedItem.data(ITEMTYPE)))
                if doubleClickedItem.data(ITEMTYPE) == NODEINSTANCE:
                    self.editNodeInstance(doubleClickedItem)
                    return
                if doubleClickedItem.data(ITEMTYPE) == RELINSTANCETEXT:
                    relItem = self.parent.itemDict[doubleClickedItem.data(NODEID)]
                    self.editRelInstance(relItem)
                    return                
                if doubleClickedItem.data(ITEMTYPE) == NODETEMPLATE:
                    self.editNodeTemplate(doubleClickedItem)
                    return                            
                if doubleClickedItem.data(ITEMTYPE) == RELTEMPLATETEXT:
                    relItem = self.parent.itemDict[doubleClickedItem.data(NODEID)]
                    self.editRelTemplate(relItem)
                    return             

########################################################
# Node Template Functions
########################################################
    def addTNode(self, point, nodeTemplateDict=None, NZID=None):
        '''
        Add a Node template to the diagram at the given point.
        Used by the drawdiagram function
        '''
        self.clearSelection()
        # create a NodeTemplateItem
        nodeTemplateItem = NodeTemplateItem(self, point.x(), point.y(), nodeTemplateDict=nodeTemplateDict, NZID=NZID)
        # add it to the diagramEditor's list of node/rels
        self.parent.itemDict[nodeTemplateItem.NZID] = nodeTemplateItem
        
        # reset the editor mode to "point"
        self.parent.checkModeButton(self.parent.btnPoint)    
        
    def dropTNode(self, point, nodeTemplateDict=None, NZID=None):
        '''
        Add a Node template to the diagram at the given point.
        Used by the dropEvent function 
        '''
        self.clearSelection()
        # create a NodeTemplateItem
        nodeTemplateItem = NodeTemplateItem(self, point.x(), point.y(), nodeTemplateDict=nodeTemplateDict, NZID=NZID)
        # add it to the diagramEditor's list of node/rels
        self.parent.itemDict[nodeTemplateItem.NZID] = nodeTemplateItem
        # save it to the diagram list of item dictionaries in the project model
        self.parent.diagramDict["items"].append(nodeTemplateItem.getObjectDict())        
        self.model.setModelDirty()        
        # reset the editor mode to "point"
        self.parent.checkModeButton(self.parent.btnPoint)
        
    def addNewNodeTemplate(self, point):
        '''
        Add a new node template via the user clicking on the diagram.
        ''' 
        # bring up the editor
        d = NodePropertyBox(mode="NEW", parent=self.parent.parent, objectDict= None, designModel = self.model)
        if d.exec_():
            # save the node template dictionary from the editor
            self.model.modelData["Node Template"].append(d.objectDict) 
            # get the index to the newly appended dictionary
            objectIndex = self.model.instanceTopLevelIndex("Node Template", d.objectDict["name"])
            # create a NodeTemplateItem
            nodeTemplateItem = NodeTemplateItem(self, point.x(), point.y(), nodeTemplateDict=self.model.modelData["Node Template"][objectIndex], NZID=None)
            # add it to the diagramEditor's list of node/rels
            self.parent.itemDict[nodeTemplateItem.NZID] = nodeTemplateItem
            # save it to the diagram list of item dictionaries in the project model
            self.parent.diagramDict["items"].append(nodeTemplateItem.getObjectDict())
            self.model.setModelDirty()
            self.model.updateTV()   
        # set the edit mode back to pointer
        self.parent.checkModeButton(self.parent.btnPoint)       
        
    def editNodeTemplate(self, item):

        nodeTemplateItem = self.parent.itemDict[item.data(NODEID)]
        # get the index for the Node Instance so we can resave it after the dialog box
        saveIndex, nodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=nodeTemplateItem.name())
        
        if nodeTemplateDict is None:
            mode = "NEW"
        else:
            mode = "UPDATE"

        d = NodePropertyBox(mode=mode, parent=self.parent.parent, objectDict= nodeTemplateDict, designModel = self.model)
        if d.exec_():
            if d.objectDict is not None:
                if saveIndex is None:
                    # tell the nodeTemplateItem it's name
                    nodeTemplateItem.name = d.editName.text()
                    self.model.modelData["Node Template"].append(d.objectDict)
                else:
                    self.model.modelData["Node Template"][saveIndex]=d.objectDict
            
            #redraw all open  diagrams - this should be smart enough to only redraw diagrams with this node template
            self.parent.parent.redrawTemplateDiagrams()
            self.parent.parent.redrawInstanceDiagrams()            
            self.model.setModelDirty()
            self.model.updateTV()
        # set the edit mode back to pointer
        self.parent.checkModeButton(self.parent.btnPoint)     
        
############################################################
# Instance Node Functions
############################################################

    def addExistingInstanceNode(self, ):
#        print("add node at {}".format(str(self.rightClickPos)))
        self.parent.addExistingInstanceNode(self.rightClickPos)
    

    def addNewInstanceNode(self, point):
        '''
        Add a new instance node  via the user clicking on the diagram.
        ''' 
        # bring up the editor
        nodeDict = None
        nodeInstance = NodeInstance(model=self.model, nodeInstanceDict=nodeDict)
        d = INPropertyBox(parent=self.parent.parent, diagramInstance = nodeInstance, model = self.model)
        if d.exec_():
            self.model.setModelDirty()
            if d.diagramInstance is not None:
                    self.model.modelData["Instance Node"].append(d.diagramInstance.getObjectDict())
#                    self.parent.parent.populateTree()
                    # put it on the diagram
                    self.clearSelection()
                    nodeItem = NodeItem(self, point.x(),point.y(),nodeInstance=nodeInstance)
                    # add it to the diagramEditor's list of node/rels
                    self.parent.itemDict[nodeInstance.NZID] = nodeItem
                    # save it to the diagram list of item dictionaries in the project model
                    self.parent.diagramDict["items"].append(nodeItem.getObjectDict())  
                    self.model.updateTV()         
                    self.model.setModelDirty()       
        # reset the editor mode to "point"
        self.parent.checkModeButton(self.parent.btnPoint)
        
    def dropINode(self, point, nodeInstanceDict=None, NZID=None):
        '''
        Add a Node instance to the diagram at the given point.
        called by dropevent, addinboundrelinstance, addirelationship
        '''
        self.clearSelection()
        nodeInstance = NodeInstance(model=self.model, nodeInstanceDict=nodeInstanceDict)
        # make sure it's not already on the diagram
        if nodeInstance.NZID in [key for key, value in self.parent.itemDict.items()]:
            self.helper.displayErrMsg("Instance Node", "This node already exists on this diagram.  An Instance Node can only be on a diagram once") 
            return None
            
        nodeItem = NodeItem(self, point.x(),point.y(),nodeInstance=nodeInstance)
        # add it to the diagramEditor's list of node/rels
        self.parent.itemDict[nodeInstance.NZID] = nodeItem
        # save it to the diagram list of item dictionaries in the project model
        self.parent.diagramDict["items"].append(nodeItem.getObjectDict())       
       
        # save or update the node instance item
        # sync to db - not sure why this is needed
        nodeInstance.syncToDB() 
        # add or update in the project model
        saveIndex, nodeDict = self.parent.model.getDictByName(topLevel="Instance Node",objectName=nodeInstance.NZID)
        if saveIndex is None:
            self.parent.model.modelData["Instance Node"].append(nodeInstance.getObjectDict())
        else:
            self.parent.model.modelData["Instance Node"][saveIndex]=nodeInstance.getObjectDict()

        # mark the model changed
        self.model.setModelDirty()       
        # reset the editor mode to "point"
        self.parent.checkModeButton(self.parent.btnPoint)        
        return nodeInstance.NZID
        
    def addInode(self, point, nodeInstance=None):
        '''
        Add a Node Instance to the diagram
        called by drawdiagram, copynodetodiagram
        '''
        self.clearSelection()
        # create new blank node instance if none provided
        if nodeInstance == None:
            nodeDict = None
            nodeInstance = NodeInstance(model=self.model, nodeInstanceDict=nodeDict)
        # make sure it's not already on the diagram
        if nodeInstance.NZID in [key for key, value in self.parent.itemDict.items()]:
            self.helper.displayErrMsg("Instance Node", "This node already exists on this diagram.  An Instance Node can only be on a diagram once") 
            return None
            
        self.model.setModelDirty()           
        nodeItem = NodeItem(self, point.x(),point.y(),nodeInstance=nodeInstance)
        # add it to the diagramEditor's list of node/rels
        self.parent.itemDict[nodeInstance.NZID] = nodeItem

        # reset the editor mode to "point"
        self.parent.checkModeButton(self.parent.btnPoint)
        return nodeInstance.NZID
        
    def fillRels(self, nodeNZID):
        '''
        if the instance node nodeNZID has any relationships to other instance nodes on this diagram,
        then add those relationships
        '''
        diagramNodeNZIDSet = set([key for key,diagramItem in self.parent.itemDict.items()])
        # see if the dropped node has any Instance relationships to already existing Instance nodes
        for iRel in self.model.modelData["Instance Relationship"]:
                # is the newly dropped node in an instance relationship in this project
                if nodeNZID in [iRel["startNZID"], iRel["endNZID"]]  :
                    # are both the start and end node on the diagram
                    if set([iRel["startNZID"], iRel["endNZID"]]).issubset(diagramNodeNZIDSet):
                            # add the instance relationship
                            self.addIRelationship(NZID=iRel["NZID"], startNode=None, endNode=None, mode="Drop")        
        
    def removeSelectedNodeInstance(self, ):
#        items = self.selectedItems()                       
#        if len(items) > 0:
#            item = items[0]
        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [NODEINSTANCE]:
                if self.helper.removeObjectPrompt("Node Instance") == True:
                    i = self.parent.itemDict[item.data(NODEID)]
                    # clear the items from the scene
                    i.clearItem()
                    # remove the item from the diagrams list of items
                    del self.parent.itemDict[item.data(NODEID)]
                    # remove the item from the diagram dictionary as well
                    index = self.parent.model.diagramItemIndex(diagramType="Instance Diagram", diagramName=self.parent.diagramName, itemType="Instance Node", NZID = i.itemInstance.NZID)
                    if not index is None:
                        del self.parent.diagramDict["items"][index]
#                    print("del node - {},{}".format(rc, msg))
                    # remove all the relationships for this node
                    keyList = []
                    for key,diagramInstance in self.parent.itemDict.items():
                        if diagramInstance.diagramType == "Instance Relationship":
                            if diagramInstance.startNZID == diagramInstance.endNZID:
                                keyList.append(diagramInstance.getNodeId())
                                diagramInstance.clearItem()
                                
                            elif diagramInstance.startNZID == i.itemInstance.NZID:
                                keyList.append(diagramInstance.getNodeId())
                                diagramInstance.clearItem()
#                                self.removeItem(diagramInstance.IRel)
#                                self.removeItem(diagramInstance.IRtext)
#                                keyList.append(diagramInstance.IRel.data(NODEID))
                                
                            elif diagramInstance.endNZID == i.itemInstance.NZID:
                                keyList.append(diagramInstance.getNodeId())
                                diagramInstance.clearItem()
#                                self.removeItem(diagramInstance.IRel)
#                                self.removeItem(diagramInstance.IRtext)
#                                keyList.append(diagramInstance.IRel.data(NODEID))
                                
                    for key in keyList:
                        del self.parent.itemDict[key]
                        index = self.parent.model.diagramItemIndex(diagramType="Instance Diagram", diagramName=self.parent.diagramName, itemType="Instance Relationship", NZID = key)
                        if not index is None:
                            del self.parent.diagramDict["items"][index]                        
                return
            else:
                if item.data(ITEMTYPE) in [NODETEMPLATE]:
                    if self.helper.removeObjectPrompt("Node Template") == True:
                        i = self.parent.itemDict[item.data(NODEID)]
                        # remove the qgraphics items from the scene
                        i.clearItem()
                        # remove the item from the item dictionary
                        del self.parent.itemDict[item.data(NODEID)]
                        # remove the item from the diagram dictionary as well
                        index = self.parent.model.diagramItemIndex(diagramType="Template Diagram", diagramName=self.parent.diagramName, itemType="Node Template", NZID = i.NZID)
                        if not index is None:
                            del self.parent.diagramDict["items"][index]
                        # remove any connected rel templates from the diagram item dictionary
                        keyList = []
                        for key,diagramInstance in self.parent.itemDict.items():
                            if diagramInstance.diagramType == "Relationship Template":
                                if (diagramInstance.startNZID == i.NZID or diagramInstance.endNZID == i.NZID) :
                                    diagramInstance.clearItem()
                                    keyList.append(key)
                                    index = self.parent.model.diagramItemIndex(diagramType="Template Diagram", diagramName=self.parent.diagramName, itemType="Relationship Template", NZID = diagramInstance.NZID)
                                    if not index is None:
                                        del self.parent.diagramDict["items"][index]
                        for key in keyList:
                            del self.parent.itemDict[key]
                            index = self.parent.model.diagramItemIndex(diagramType="Template Diagram", diagramName=self.parent.diagramName, itemType="Relationship Template", NZID = key)
                            if not index is None:
                                del self.parent.diagramDict["items"][index]
                    return
                
    def editSelectedNodeInstance(self, ):

        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [NODEINSTANCE]:
                self.editNodeInstance(item)
                return
            elif item.data(ITEMTYPE) in [NODETEMPLATE]:
                self.editNodeTemplate(item)                
                return
        
    def editNodeInstance(self, item):

        nodeItem = self.parent.itemDict[item.data(NODEID)]
        nodeInstance = nodeItem.itemInstance
        # get the index for the Node Instance so we can resave it after the dialog box
        saveIndex, nodeDict = self.model.getDictByName(topLevel="Instance Node",objectName=nodeInstance.NZID)
        d = INPropertyBox(parent=self.parent, diagramInstance=nodeInstance, model = self.model)
        if d.exec_():
            if d.diagramInstance is not None:
                if saveIndex is None:
                    self.model.modelData["Instance Node"].append(d.diagramInstance.getObjectDict())
                else:
                    self.model.modelData["Instance Node"][saveIndex]=d.diagramInstance.getObjectDict()

                #redraw all open  diagrams - this should be smart enough to only redraw diagrams with this node instance
                self.parent.parent.redrawInstanceDiagrams()   
                
#            self.parent.updateSyncModeMsg(msg=d.msg)
            self.model.setModelDirty()
            self.model.updateTV()
        
    def getInstanceNodeRels(self, nodeID=None, direction=None):
        '''
        Run a query that retrieves all relationships between one node and all other nodes in the db
        '''
        if direction == "Inbound":
            p1 = str(nodeID)
            cypher = '''match (f)-[r]->(t)
                            where (id(t) = {} )
                            return id(f),
                                    f, 
                                    id(r), 
                                    type(r),
                                    r,
                                    id(t),
                                    t
                            '''.format(p1)
        if direction == "Outbound":
            p1 = str(nodeID)
            cypher = '''match (f)-[r]->(t)
                            where (id(f) = {} )
                            return id(f),
                                    f, 
                                    id(r), 
                                    type(r),
                                    r,
                                    id(t),
                                    t
                            '''.format(p1)
        #run the query
        rc1, msg1 = self.parent.model.modelNeoCon.runCypherAuto(cypher)
        if rc1 is True:
            # return list of rels and instance nodes
            return self.parent.model.modelNeoCon.resultSet
        else:
            return []
            
        

############################################################
# Relationship Template Functions
############################################################
    def addInboundRel(self):      
        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [NODETEMPLATE]:
                nodeTemplateItem = self.parent.itemDict[item.data(NODEID)]
                aSubAction = QObject.sender(self)
                relTemplateDict = aSubAction.data()
                if not relTemplateDict is None:
                    self.dropTRel(nodeTemplateItem.getPoint(), relTemplateDict=relTemplateDict, nodeTemplateItem=nodeTemplateItem)
           
    def addOutboundRel(self):
        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [NODETEMPLATE]:
                nodeTemplateItem = self.parent.itemDict[item.data(NODEID)]
                aSubAction = QObject.sender(self)
                relTemplateDict = aSubAction.data()
                if not relTemplateDict is None:
                    self.dropTRel(nodeTemplateItem.getPoint(offset=200), relTemplateDict=relTemplateDict, nodeTemplateItem=nodeTemplateItem)
                
        
    
    def addNewRelationshipTemplate(self, startNode=None, endNode=None):
        '''
        Add a new relationship template via the user selecting a start and end node template on the diagram.
        startNode, endNode = QGraphicsRect object the user selected
        ''' 
        # get the start and end node items
        startNZID = startNode.data(NODEID)
        endNZID = endNode.data(NODEID) 
        startNode=self.parent.itemDict[startNZID]
        endNode=self.parent.itemDict[endNZID]
        # create a new rel template dictionary
        objectDict = self.parent.model.newRelTemplateDict()
        objectDict["fromTemplate"] = startNode.name()
        objectDict["toTemplate"] = endNode.name() 
        
        # bring up the editor as the user must supply a name
        d = TRPropertyBox(self.parent.parent, mode="NEW",   objectDict=objectDict,  designModel = self.model)
        if d.exec_():
            # save the rel template to the project model
            self.model.modelData["Relationship Template"].append(d.objectDict)
            # get the index to the newly appended dictionary
            objectIndex = self.model.instanceTopLevelIndex("Relationship Template", d.objectDict["name"])
            # create a new relation template item object
            relationTemplateItem = RelationTemplateItem(scene = self, relationTemplateDict=self.model.modelData["Relationship Template"][objectIndex], startNodeItem=startNode, endNodeItem=endNode)
            # add the relation item object to the diagram item dictionary
            self.parent.itemDict[relationTemplateItem.NZID] = relationTemplateItem    
            # save it to the diagram list of item dictionaries in the project model           
            self.parent.diagramDict["items"].append(relationTemplateItem.getObjectDict())
            # tell the relationship to set it's loation and draw itself
            relationTemplateItem.drawIt2()
            self.model.setModelDirty()
            self.model.updateTV()   
            #redraw all open template diagrams - SHOULD BE SMART ENOUGH TO ONLY REDRAW THIS REL
            self.parent.parent.redrawTemplateDiagrams()
            self.parent.parent.redrawInstanceDiagrams() 

        # set the edit mode back to pointer
        self.parent.checkModeButton(self.parent.btnPoint)    
        
    def editRelTemplate(self, item):
        '''
        item = RelationTemplateItem object
        '''
        #get the index for this relation template so we can save it later
        saveIndex, relDict = self.model.getDictByName(topLevel="Relationship Template",objectName=item.name())
        d = TRPropertyBox(self.parent.parent, objectDict = relDict, designModel = self.model, mode="UPDATE")

        if d.exec_():
            #save the object dictionary to the model object
            self.model.modelData["Relationship Template"][saveIndex]=d.objectDict
            self.model.setModelDirty()
            #redraw all open  diagrams - this should be smart enough to only redraw diagrams with this node template
            self.parent.parent.redrawTemplateDiagrams()   
            self.model.updateTV()
            
        # set the edit mode back to pointer
        self.parent.checkModeButton(self.parent.btnPoint)    
        
    def addTRelationship(self, relTemplateName=None, NZID=None, startNZID=None, endNZID=None, mode=None):
        # if adding a relationship template while initially loading the diagram or while dropping arelationship template, you will get the name of the relationship template
        relationTemplateDict=None
        if not relTemplateName is None:
            index,  relationTemplateDict = self.model.getDictByName(topLevel="Relationship Template", objectName=relTemplateName)
        # verify it has a from and to node template.  
        if (relationTemplateDict["fromTemplate"] == '' or relationTemplateDict["toTemplate"] == ''):
            self.helper.displayErrMsg("Add Relationship Template", "Invalid Relationship Template {} - missing To or From Node Template.".format(relationTemplateDict["name"]))
        else:
            # create a new RelationTemplateItem object
            relationTemplateItem = RelationTemplateItem(scene = self, NZID=NZID,  relationTemplateDict=relationTemplateDict, startNodeItem=self.parent.itemDict[startNZID], endNodeItem=self.parent.itemDict[endNZID])
            # verify it has a from and to node template.  
            if (relationTemplateItem.startNZID is None or relationTemplateItem.endNZID is None):
                self.helper.displayErrMsg("Add Relationship Template", "Invalid Relationship Template {} - missing To or From Node Template.".format(relationTemplateItem.name()))
            else:
                # add the relation item object to the diagram item dictionary
                self.parent.itemDict[relationTemplateItem.NZID] = relationTemplateItem 
                # tell the relationship to set it's loation and draw itself
                relationTemplateItem.drawIt2()

    def dropTRel(self, point, relTemplateDict=None, nodeTemplateItem=None ):
            if not relTemplateDict is None:
                fromTemplate = relTemplateDict["fromTemplate"]
                toTemplate = relTemplateDict["toTemplate"]
                # verify it has a from and to node template.  
                if (fromTemplate == '' or toTemplate == ''):
                    self.helper.displayErrMsg("Add Relationship Template", "Invalid Relationship Template {} - missing To or From Node Template.".format(relTemplateDict["name"]))
                else:
                    endNodeItem = None
                    startNodeItem = None
                    fromTemplateItems = self.parent.findNodeTemplatesOnDiagram(nodeTemplateName=fromTemplate)
                    toTemplateItems = self.parent.findNodeTemplatesOnDiagram(nodeTemplateName=toTemplate)
                    toNodeTemplateDict=None
                    fromNodeTemplateDict=None
                    if len(toTemplateItems) == 0:
                        # add the to node template to the diagram
                        saveIndex, toNodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=toTemplate)
                        if not toNodeTemplateDict is None:
                            self.dropTNode(point, nodeTemplateDict=toNodeTemplateDict )   
                            toTemplateItems = self.parent.findNodeTemplatesOnDiagram(nodeTemplateName=toTemplate)
                    if len(fromTemplateItems) == 0:
                        # add the from node template to the diagram
                        saveIndex, fromNodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=fromTemplate)
                        if not fromNodeTemplateDict is None:
                            self.dropTNode(QPointF(point.x() + 150 , point.y()+150), nodeTemplateDict=fromNodeTemplateDict )  
                            fromTemplateItems = self.parent.findNodeTemplatesOnDiagram(nodeTemplateName=fromTemplate)
     
                    if len(toTemplateItems) == 1:
                        # node template already on the diagram
                        saveIndex, toNodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=toTemplate)
                    if len(fromTemplateItems) == 1:
                        # node template already on the diagram
                        saveIndex, fromNodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=fromTemplate)

                    if len(toTemplateItems) > 1:
                        # see if one of the to templates is the one right clicked on - only applies if coming from add inbount/outbound submenu
                        if not nodeTemplateItem is None:
                            for item in toTemplateItems:
                                if item.NZID == nodeTemplateItem.NZID:
                                    endNodeItem = item
                        
                        # multiple to templates on the diagram, so pick the first one - this needs to be improved to where the user controls which one
                        if endNodeItem == None:
                            endNodeItem = toTemplateItems[0]
                        
                    if len(fromTemplateItems) > 1:
                        # see if one of the to templates is the one right clicked on - only applies if coming from add inbount/outbound submenu
                        if not nodeTemplateItem is None:
                            for item in fromTemplateItems:
                                if item.NZID == nodeTemplateItem.NZID:
                                    startNodeItem = item
                        # multiple to templates on the diagram, so pick the first one - this needs to be improved to where the user controls which one
                        if startNodeItem == None:
                            startNodeItem = fromTemplateItems[0]
       
                    if startNodeItem == None:
                        startNodeItem = self.parent.itemDict[fromTemplateItems[0].NZID]
                    if endNodeItem == None:
                        endNodeItem = self.parent.itemDict[toTemplateItems[0].NZID]
                        
                    if (toNodeTemplateDict or endNodeItem) and (fromNodeTemplateDict or startNodeItem):
                        # create a new RelationTemplateItem object
#                        relationTemplateItem = RelationTemplateItem(scene = self, relationTemplateDict=relTemplateDict, startNodeItem=self.parent.itemDict[fromTemplateItems[0].NZID], endNodeItem=self.parent.itemDict[toTemplateItems[0].NZID])
                        relationTemplateItem = RelationTemplateItem(scene = self, relationTemplateDict=relTemplateDict, startNodeItem=startNodeItem, endNodeItem=endNodeItem)                        
                        # add the relation item object to the diagram item dictionary
                        self.parent.itemDict[relationTemplateItem.NZID] = relationTemplateItem   
                        # save it to the diagram list of item dictionaries in the project model           
                        self.parent.diagramDict["items"].append(relationTemplateItem.getObjectDict())
                        # tell the relationship to set it's loation and draw itself
                        relationTemplateItem.drawIt2()
                
###########################################################
# Instance Relationship functions
###########################################################
    def addInboundRelInstance(self):      
        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [NODEINSTANCE]:
                # drop the from node on the diagram
                aSubAction = QObject.sender(self)
                result = aSubAction.data()
                fromNodeObject = result["f"]
                fromNodeNeoID = result["id(f)"]
                toNodeNeoID = result["id(t)"]
                # lookup the NZID based on the neoID retrieved from the database
                fromNZID = self.model.lookupNZID(neoID = fromNodeNeoID, topLevel="Instance Node")
                toNZID = self.model.lookupNZID(neoID = toNodeNeoID, topLevel="Instance Node")
                
                if fromNZID is None:
                    # get the list of labels from the node object
                    lbls = [[lbl] for lbl in fromNodeObject.labels]  
                    # get the dictionary of properties from the node object  and convert it to a list
                    props = [[key, val] for key, val in dict(fromNodeObject).items() if key !="NZID"]
                    # see if there is a matching node template
                    nodeTemplateName = self.model.matchNodeTemplate(fromNodeObject)
                    # create a new node instance dictionary and add the node
                    fromNodeInstanceDict = self.model.newNodeInstance(nodeID = str(result["id(f)"]), templateName=nodeTemplateName, labelList=lbls, propList=props,  NZID=None)
                    fromNZID = self.dropINode(QPointF(self.savePosition.x()+150,self.savePosition.y()+150),  nodeInstanceDict=fromNodeInstanceDict, NZID= None)
                else:
                    # check to see if the from node is on the diagram, if not then drop it on the diagram
                    if not fromNZID in [key for key, value in self.parent.itemDict.items()]:
                        index, fromNodeInstanceDict = self.model.getDictByName(topLevel="Instance Node",objectName=fromNZID)
                        # the instance node is already in the project so just drop it like a drag'n'drop
                        self.dropINode(QPointF(self.savePosition.x()+150,self.savePosition.y()+150),  nodeInstanceDict=fromNodeInstanceDict, NZID=fromNZID)

                # create a relation instance dict based on the relationship retrieved from the graph db
                startNode = [ value for key, value in self.parent.itemDict.items() if (value.diagramType == "Instance Node" and value.itemInstance.NZID == fromNZID )][0]
                endNode = [ value for key, value in self.parent.itemDict.items() if (value.diagramType == "Instance Node" and value.itemInstance.NZID == toNZID) ][0]
                
                relNeoID = result["id(r)"]
                # get the relationship NZID if it exists
                relNZID = self.model.lookupNZID(neoID = relNeoID, topLevel="Instance Relationship")                   
                if relNZID is None:
                    relNZID = str(uuid.uuid4())
                # see if the relationship is already in the project model
                relIndex, instanceRelationDict = self.model.getDictByName(topLevel="Instance Relationship",objectName=relNZID)
                # if the instance rel wasn't found in the model, then create it and add it
                if instanceRelationDict is None:
                    # see if there is a matching relationship template
                    relTemplateName = self.model.matchRelTemplate(startNodeTemplate=startNode.itemInstance.nodeTemplate, endNodeTemplate=endNode.itemInstance.nodeTemplate, relName = result['type(r)'] )
                    relObjectDict = {}
                    relObjectDict["NZID"] = relNZID
                    relObjectDict["name"] = relNZID
                    relObjectDict["neoID"] = result['id(r)']
                    relObjectDict["diagramType"] = "Instance Relationship"
                    relObjectDict["relName"] = result['type(r)']    

                    # get the dictionary of properties from the rel object  and convert it to a list
                    props = []
                    for key, val in dict(result["r"]).items():
#                        print("key:{} val:{} type:{}".format(key, val, type(val)))
                        props.append( [key, self.neoTypeFunc.getNeo4jDataType(value=val),self.neoTypeFunc.convertTypeToString(dataValue=val) ])
                    relObjectDict["properties"] = props
                    
                    relObjectDict["startNZID"] = startNode.itemInstance.NZID
                    relObjectDict["endNZID"] = endNode.itemInstance.NZID
                    relObjectDict["relTemplate"] = relTemplateName  
                    # this should really call a function to do this
                    propList = self.helper.genPropValueList("n", relObjectDict)
                    signature = "({})-[{}:{} {}{}{}]->({})".format(str(startNode.itemInstance.neoID), str(relObjectDict["neoID"]), relObjectDict["relName"], "{", propList, "}", str(endNode.itemInstance.neoID))
                    relObjectDict["displayName"] =  signature   

                    # 
                    self.model.modelData["Instance Relationship"].append(relObjectDict)                
                    self.addIRelationship(NZID=relNZID, startNode=startNode.INode, endNode=endNode.INode, mode="Drop")
                else:
                    # make sure the relationship isn't already on the diagram
                    if not relNZID in [key for key, value in self.parent.itemDict.items()]:
                        self.addIRelationship(NZID=relNZID, startNode=startNode.INode, endNode=endNode.INode, mode="Drop")
                    else:
                        self.helper.displayErrMsg("Add Relationship", "This relationship is already on the diagram.")
                        
                
        self.model.updateTV()
        # set the edit mode back to pointer
        self.parent.checkModeButton(self.parent.btnPoint)                    
           
    def addOutboundRelInstance(self):

        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [NODEINSTANCE]:
                # add rel to this node
                aSubAction = QObject.sender(self)
                result = aSubAction.data()
                toNodeObject = result["t"]
                toNodeNeoID = result["id(t)"]
                fromNodeNeoID  = result["id(f)"]
                # lookup the NZID based on the neoID retrieved from the database
                toNZID = self.model.lookupNZID(neoID = toNodeNeoID, topLevel="Instance Node")    
                fromNZID  = self.model.lookupNZID(neoID = fromNodeNeoID, topLevel="Instance Node")    
                if toNZID is None:
                    # get the list of labels from the node object
                    lbls = [[lbl] for lbl in toNodeObject.labels]  
                    # get the dictionary of properties from the node object  and convert it to a list
                    props = [[key, val] for key, val in dict(toNodeObject).items() if key !="NZID"]
                    # see if there is a matching node template
                    nodeTemplateName = self.model.matchNodeTemplate(toNodeObject)
                    # create a new node instance dictionary and add the node
                    toNodeInstanceDict = self.model.newNodeInstance(nodeID = str(result["id(t)"]), templateName=nodeTemplateName, labelList=lbls, propList=props,  NZID=None)
                    toNZID = self.dropINode(QPointF(self.savePosition.x()+150,self.savePosition.y()+150),  nodeInstanceDict=toNodeInstanceDict, NZID=None)
                else:
                    # check to see if the to node is on the diagram, if not then drop it on the diagram
                    if not toNZID in [key for key, value in self.parent.itemDict.items()]:
                        index, fromNodeInstanceDict = self.model.getDictByName(topLevel="Instance Node",objectName=toNZID)
                        # the instance node is already in the project so just drop it like a drag'n'drop
                        self.dropINode(QPointF(self.savePosition.x()+150,self.savePosition.y()+150),  nodeInstanceDict=fromNodeInstanceDict, NZID=toNZID)

                # create a relation instance dict based on the relationship retrieved from the graph db
                startNode = [ value for key, value in self.parent.itemDict.items() if (value.diagramType == "Instance Node" and value.itemInstance.NZID == fromNZID) ][0]
                endNode = [ value for key, value in self.parent.itemDict.items() if (value.diagramType == "Instance Node" and value.itemInstance.NZID == toNZID) ][0]
                
                relNeoID = result["id(r)"]
                # get the relationship NZID if it exists
                relNZID = self.model.lookupNZID(neoID = relNeoID, topLevel="Instance Relationship")    
                if relNZID is None:
                    relNZID = str(uuid.uuid4())
                
                relIndex, instanceRelationDict = self.model.getDictByName(topLevel="Instance Relationship",objectName=relNZID)
                # if the instance rel wasn't found in the model, then create it and add it
                if instanceRelationDict is None:
                    relTemplateName = self.model.matchRelTemplate(startNodeTemplate=startNode.itemInstance.nodeTemplate, endNodeTemplate=endNode.itemInstance.nodeTemplate, relName = result['type(r)'] )
                    relObjectDict = {}
                    relObjectDict["NZID"] = relNZID
                    relObjectDict["name"] = relNZID
                    relObjectDict["neoID"] = result['id(r)']
                    relObjectDict["diagramType"] = "Instance Relationship"
                    relObjectDict["relName"] = result['type(r)']  
                    
                    # get the dictionary of properties from the rel object  and convert it to a list
                    props = []
                    for key, val in dict(result["r"]).items():
#                        print("key:{} val:{} type:{}".format(key, val, type(val)))
                        props.append( [key, self.neoTypeFunc.getNeo4jDataType(value=val),self.neoTypeFunc.convertTypeToString(dataValue=val) ])

                    relObjectDict["properties"] = props
                    
                    relObjectDict["startNZID"] = startNode.itemInstance.NZID
                    relObjectDict["endNZID"] = endNode.itemInstance.NZID
                    relObjectDict["relTemplate"] = relTemplateName 
                    
                    # this should really call a function to do this
                    propList = self.helper.genPropValueList("n", relObjectDict)

                    signature = "({})-[{}:{} {}{}{}]->({})".format(str(startNode.itemInstance.neoID), str(relObjectDict["neoID"]), relObjectDict["relName"], "{", propList, "}", str(endNode.itemInstance.neoID))
                    relObjectDict["displayName"] =  signature   

                    self.model.modelData["Instance Relationship"].append(relObjectDict)                
                    self.addIRelationship(NZID=relNZID, startNode=startNode.INode, endNode=endNode.INode, mode="Drop")
                else:
                    # make sure the relationship isn't already on the diagram
                    if not relNZID in [key for key, value in self.parent.itemDict.items()]:
                        self.addIRelationship(NZID=relNZID, startNode=startNode.INode, endNode=endNode.INode, mode="Drop")
                    else:
                        self.helper.displayErrMsg("Add Relationship", "This relationship is already on the diagram.")
                
        self.model.updateTV()
        # set the edit mode back to pointer
        self.parent.checkModeButton(self.parent.btnPoint)                    

    
    def addNewRelationship(self, startNode=None, endNode=None):
        '''
        Add a new Instance relationship via the user selecting a start and end node on the diagram.
        startNode = NodeItem object
        '''
        startNZID = startNode.data(NODEID)
        endNZID = endNode.data(NODEID) 
        relationInstanceDict = None
        # create a new relation instance object
        relInstance = RelationInstance(parent=self, model=self.model, relationInstanceDict=relationInstanceDict, startNode=self.parent.itemDict[startNZID].itemInstance, endNode=self.parent.itemDict[endNZID].itemInstance)
        d = IRPropertyBox(self.parent, diagramInstance=relInstance,  model = self.model)
        if d.exec_():
            self.model.setModelDirty()
            self.model.modelData["Instance Relationship"].append(d.diagramInstance.getObjectDict())
            self.model.updateTV()
            # create a new relation item object
            relItem = RelationItem(self, relationInstance=relInstance)
            # add the relation item object to the diagram item dictionary
            self.parent.itemDict[relInstance.NZID] = relItem
            # this counts how many relationships exist between two nodes
            self.parent.addRelationship(relInstance)
            # save it to the diagram list of item dictionaries in the project model           
            self.parent.diagramDict["items"].append(relItem.getObjectDict())
            
        # set the edit mode back to pointer
        self.parent.checkModeButton(self.parent.btnPoint)        


    def addIRelationship(self, NZID=None, startNode=None, endNode=None, mode=None):
        '''
        called by drawDiagram to initially draw an existing diagram
        called by dropEvent to drop an existing instance relationship on a diagram
        '''
        # SHOULD REALLY SPLIT THIS UP AND ADD A dropIRelationship function
        
        # you get the NZID of the relationship in  the following situations:
        # - adding an Instance relationship while initially loading the diagram 
        # - dropping an Instance relationship
        # - adding an IR from the copy node dialog and the node you've added is pulling in a relationship that has an NZID from another project.

        if not startNode is None:
            startNZID = startNode.data(NODEID)
        if not endNode is None:
            endNZID = endNode.data(NODEID)
        
        relationInstanceDict=None
        if not NZID is None:
            index,  relationInstanceDict = self.model.getDictByName(topLevel="Instance Relationship", objectName=NZID)
            
            if not relationInstanceDict is None:
                startNZID = relationInstanceDict["startNZID"]
                endNZID = relationInstanceDict["endNZID"]

        # if dropping a relationship, first make sure the nodes are on the diagram, if not then add them
        if mode == "Drop":
            # get the object dictionary for the start node
            saveIndex, nodeDict = self.model.getDictByName(topLevel="Instance Node",objectName=startNZID)
            # if it's not on the diagram then add it
            if not startNZID in [key for key, value in self.parent.itemDict.items()]:
#                nodeInstance = NodeInstance(model=self.model, nodeInstanceDict=nodeDict)
                self.dropINode(self.scenePos, nodeInstanceDict=nodeDict, NZID=startNZID ) 
            # get the object dictionary for the end node
            saveIndex, nodeDict = self.model.getDictByName(topLevel="Instance Node",objectName=endNZID)
            # if it's not on the diagram then add it
            if not endNZID in [key for key, value in self.parent.itemDict.items()]:
#                nodeInstance = NodeInstance(model=self.model, nodeInstanceDict=nodeDict)
                self.dropINode(QPointF(self.scenePos.x() + 200,self.scenePos.y() + 200), nodeInstanceDict=nodeDict, NZID=endNZID ) 
        # create a new relation instance object
        relInstance = RelationInstance(parent=self, model=self.model, relationInstanceDict=relationInstanceDict, startNode=self.parent.itemDict[startNZID].itemInstance, endNode=self.parent.itemDict[endNZID].itemInstance)
        # create a new relation item object
        relItem = RelationItem(self, relationInstance=relInstance)
        # add the relation item object to the diagram item dictionary
        self.parent.itemDict[relInstance.NZID] = relItem
        # this counts how many relationships exist between two nodes
        self.parent.addRelationship(relInstance)
        # bring up the editor if this is adding a new relationship
        if mode == "AddNew":
            self.editRelInstance(relItem)
        if mode == "Drop":
    #        # save it to the diagram list of item dictionaries in the project model           
            self.parent.diagramDict["items"].append(relItem.getObjectDict())
            # sync to db
            relInstance.syncToDB() 
            
        # set the edit mode back to pointer
        self.parent.checkModeButton(self.parent.btnPoint)        

            

    def removeSelectedRelInstance(self, ):

        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [RELINSTANCETEXT]:
                if self.helper.removeObjectPrompt("Relationship Instance") == True:
                    i = self.parent.itemDict[item.data(NODEID)]
#                    rc,  msg = i.relationInstance.deleteRel()  #need to pass a log method
                    # clear the items from the scene
                    i.clearItem()
                    # remove the item from the diagrams list of items
                    del self.parent.itemDict[item.data(NODEID)]
                    # remove the item from the diagram dictionary as well
                    index = self.parent.model.diagramItemIndex(diagramType="Instance Diagram", diagramName=self.parent.diagramName, itemType="Instance Relationship", NZID = i.relationInstance.NZID)
                    if not index is None:
                        del self.parent.diagramDict["items"][index]

#                    # remove qgraphic items from the scene
#                    self.removeItem(i.IRel)
#                    self.removeItem(i.IRtext)
#                    del self.parent.itemDict[item.data(NODEID)]

                return
            if item.data(ITEMTYPE) in [RELTEMPLATETEXT]:
                if self.helper.removeObjectPrompt("Relationship Template") == True:
                    i = self.parent.itemDict[item.data(NODEID)]
                    # remove qgraphic items from the scene
                    i.clearItem()
                    # remove rel template item from the diagram list of items
                    del self.parent.itemDict[item.data(NODEID)]
                    # remove rel template item from the diagram dictionary list of items
                    index = self.parent.model.diagramItemIndex(diagramType="Template Diagram", diagramName=self.parent.diagramName, itemType="Relationship Template", NZID = i.NZID)
                    if not index is None:
                        del self.parent.diagramDict["items"][index]
                return
                    
                    
    def editSelectedRelInstance(self, ):
#        items = self.selectedItems()                       
#        if len(items) > 0:
#            item = items[0]
        items=self.items(self.savePosition)
        for item in items:
            if item.data(ITEMTYPE) in [RELINSTANCETEXT]:
                relItem = self.parent.itemDict[item.data(NODEID)]
                self.editRelInstance(relItem)
                return
            if item.data(ITEMTYPE) in [RELTEMPLATETEXT]:
                relItem = self.parent.itemDict[item.data(NODEID)]
                self.editRelTemplate(relItem)    
                return
                
    def editRelInstance(self, item):
        '''
        item = RelationItem object
        '''
        #get the index for this relation instance so we can save it later
        saveIndex, relDict = self.model.getDictByName(topLevel="Instance Relationship",objectName=item.relationInstance.NZID)
        d = IRPropertyBox(self.parent, diagramInstance=item.relationInstance,  model = self.model)
        if d.exec_():
            #save the object dictionary to the model object
            self.model.modelData["Instance Relationship"][saveIndex]=d.diagramInstance.getObjectDict()
            item.updateText()  #update the relationship name
#            self.parent.updateSyncModeMsg(msg=d.msg)
            self.model.setModelDirty()
        
        self.model.updateTV()
        


        
class InstanceDiagramTab(QWidget, Ui_InstanceDiagramTab):
    """
    UC-07 Instance Diagram Editing tab.
    This class sets up the Scene and View for graphics drawing and sets 
    appropriate values when the user clicks on the drawing mode buttons.
    """

    
    def __init__(self, parent=None, model=None, name=None, tabType=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(InstanceDiagramTab, self).__init__(parent)
        self.parent = parent
        self.schemaTab = self.parent.schemaTab
        self.schemaObject = self.parent.schemaObject
        self.model=model
        self.tabType = tabType
        self.tabName = name
        self.diagramName = name
        saveIndex, diagramDict = self.model.getDictByName(topLevel=self.tabType,objectName=name)
        self.diagramDict = diagramDict  # this is all the diagram data and contains the saved diagram items
        self.helper = Helper()
        
# if you need syncmode get it from self.model.modelData["SyncMode"]
#        self.syncMode = True  # default sync to neo4j to ON

        self.pages = []
        self.modeBtns= []
        self.itemDict = {}   # dictionary of graphic items displayed on the view.  
        self.relIRPair = {}
        self.relTRPair = {} 
        self.setupUi(self)
        
        # show and hide buttons based on diagram type
        if self.tabType == "Instance Diagram":
            self.btnTNode.hide()
            self.btnTRel.hide()
        if self.tabType == "Template Diagram":
            self.btnNode.hide()
            self.btnRel.hide()    
            self.btnSyncDB.hide()
            self.btnCopyNode.hide()
        # complete ui setups
        self.graphicsView = GraphicsView(parent=self)
        self.horizontalLayout.addWidget(self.graphicsView)
        self.graphicsView.setCursor(QCursor(Qt.ArrowCursor))
        
        self.scene = GraphicsScene(self)
        self.drawPageGrid()
        self.drawDiagram()
        self.graphicsView.setScene(self.scene)

        self.lastSliderValue = self.zoomSlider.value()
        
        # set the mode buttons
        self.modeBtns.append(self.btnPoint)
        self.modeBtns.append(self.btnShove)
        self.modeBtns.append(self.btnNode)
        self.modeBtns.append(self.btnRel)
        self.modeBtns.append(self.btnTNode)
        self.modeBtns.append(self.btnTRel)          
        self.checkModeButton(self.btnPoint)
#        self.updateSyncModeMsg()
            
    def checkModeButton(self, checkBtn):
        '''This function is called when a mode button is clicked.
           The actual button object is passed to the function.
           The function sets tracking variables appropriately 
           and determines which message to display. '''
        # reset relationship tracking variables
        self.scene.RelStartMode = False
        self.scene.RelEndMode = False            
        # make sure only the one button is checked
        for btn in self.modeBtns:
            btn.setChecked(False)
            if btn == checkBtn:
                btn.setChecked(True)
        # set the edit mode
        if checkBtn == self.btnShove:
            self.scene.editMode = SHOVE
            self.updateMsgBar("Use the mouse to move the diagram around")
        if checkBtn == self.btnPoint:
            self.scene.editMode = POINT
            self.updateMsgBar("Left click - select item. Doubleclick - edit item. Right click - more options.")
        if checkBtn == self.btnNode:
            self.scene.editMode = INODE
            self.updateMsgBar("Click on diagram to add a Node instance.")
        if checkBtn == self.btnRel:
            self.scene.editMode = IREL
            self.scene.RelStartMode = True
            self.updateMsgBar("Click on relationship start node.")
        if checkBtn == self.btnTNode:
            self.scene.editMode = TNODE
            self.updateMsgBar("Click on the diagram to add a Node Template") 
        if checkBtn == self.btnTRel:
            self.scene.editMode = TREL
            self.scene.RelStartMode = True    
            self.updateMsgBar("Click on the diagram to add a Relationship Template") 

    def pagePen(self, ):
        ''' this function returns a QPen used to draw the page grid. '''
        aPen = QPen()
        aColor = QColor(Qt.black)
        aPen.setColor(aColor)
        aPen.setWidth(1)
        aPen.setStyle(Qt.DotLine)
        return aPen   
        
    def drawPageGrid(self, ):
        '''Draw the page grid on the scene.'''
        # remove existing page borders
        self.removePages()
        # get the page setup data
        pageSetup = PageSetup(self.diagramDict["pageSetup"])
        objectDict = pageSetup.objectDict
        rows=objectDict["pageRows"]
        cols=objectDict["pageCols"]
        pageHeight, pageWidth = pageSetup.getHeightWidth()
        self.scene.setSceneRect(0, 0, pageWidth * cols, pageHeight * rows)
        currow=1
        self.pages = []
        while currow <= rows:
            upperY = (currow * pageHeight) - pageHeight
            curcol=1
            while curcol <= cols:
                upperX = (curcol * pageWidth) - pageWidth
#                print("x:{}, y:{}, h:{}, w:{}".format(upperX, upperY, pageWidth, pageHeight))
                rect = QRectF(upperX, upperY, pageWidth, pageHeight)
                self.pages.append(self.scene.addRect(rect, pen=self.pagePen()))
                curcol = curcol + 1
            currow = currow + 1
        
    def removePages(self, ):
        ''' remove all the page rectangles from the scene. '''
        if not (self.pages is None):
            while self.pages:
                item = self.pages.pop()
                self.scene.removeItem(item)
                del item
            
    def addRelationship(self, relItem):
        '''Track how many relationship instances exist
           between any pair of node instances.
        '''
        key=relItem.startNZID + relItem.endNZID
        x = self.relIRPair.setdefault(key, 0)
        self.relIRPair[key] = x + 1
        
    def numRels(self, startNZID, endNZID):  
        return self.relIRPair.setdefault(startNZID + endNZID, 0)
    
    def anyRels(self, startNZID, endNZID):
        ''' return True if there are any instance relationships between these two nodes'''
        for key, value in self.itemDict.items():
            if value.diagramType == "Instance Relationship":
                if value.startNZID in [startNZID, endNZID] and value.endNZID in [startNZID, endNZID]:
                    return True
        return False
        
    def addTRelationship(self, relItem):
        '''Track how many relationship templates exist
           between any pair of node templates.
        '''
        key=relItem.startNZID + relItem.endNZID
        # add the from/to key to the dictionary if it's not there, then return the current total which is initialized to zero (see next step)
        x = self.relTRPair.setdefault(key, 0)
        # increment the count and save it as the new total
        self.relTRPair[key] = x + 1
        return self.relTRPair[key]
        
        
    def reDrawDiagram(self, ):

        if self.tabType == "Template Diagram":

            delKeyList = []
            # delete  node templates no longer on diagram
            for key, value in self.itemDict.items():
                if value.diagramType == "Node Template":
                    # does the node template still exist?
                    if self.model.objectExists(topLevel=value.diagramType, objectName=value.name() ) :
                        # does this node still exist on the diagram?
                        if not self.model.diagramItemIndex(diagramType=self.tabType, diagramName = self.diagramName, itemType = "Node Template", NZID = value.NZID) is None:
                            pass 
#                            value.drawIt()
                        else:
                            # clear this item from the diagram as it no longer exists on this diagram
                            value.clearItem()
                            # remember to delete this one from the diagram item list
                            delKeyList.append(key)
                    else:
                        # clear this item from the diagram as it no longer exists on this diagram
                        value.clearItem()
                        # remember to delete this one from the diagram item list
                        delKeyList.append(key)     
                        
            # delete relationshp templates
            for key, value in self.itemDict.items():
                if value.diagramType == "Relationship Template":
                    # does the relationship template still exist?
                    if self.model.objectExists(topLevel=value.diagramType, objectName=value.name() ):                    
                        # does this relationship still exist on the diagram?
                        if not self.model.diagramItemIndex(diagramType=self.tabType, diagramName = self.diagramName, itemType = "Relationship Template", NZID = value.NZID) is None:
                            pass
#                            value.drawIt()
                        else:
                            # clear this item from the diagram as it no longer exists on this diagram
                            value.clearItem()
                            # remember to delete this one from the diagram item list
                            delKeyList.append(key)
                    else:
                        # clear this item from the diagram as it no longer exists on this diagram
                        value.clearItem()
                        # remember to delete this one from the diagram item list
                        delKeyList.append(key)   
                        
            # now get rid of all the node and rel templates that are no longer on this diagram        
            for key in delKeyList:
                del self.itemDict[key]   
                
            # draw all the nodes
            for key, value in self.itemDict.items():
                if value.diagramType == "Node Template":
                    value.drawIt()            
            # tell all the nodes to redraw their relationships
            for key, value in self.itemDict.items():
                if value.diagramType == "Node Template":
                    value.drawRels()                        
            
        if self.tabType == "Instance Diagram":
            
            delKeyList = []
            # draw instance node s
            for key, value in self.itemDict.items():
                if value.diagramType == "Instance Node":
                    # does the Instance Node still exist?
                    if self.model.objectExists(topLevel=value.diagramType, objectName=value.name() ) :
                        # does this Instance Node still exist on the diagram?
                        if not self.model.diagramItemIndex(diagramType=self.tabType, diagramName = self.diagramName, itemType = "Instance Node", NZID = value.NZID()) is None:
                            value.drawIt()
                        else:
                            # clear this item from the diagram as it no longer exists on this diagram
                            value.clearItem()
                            # remember to delete this one from the diagram item list
                            delKeyList.append(key)
                    else:
                        # clear this item from the diagram as it no longer exists on this diagram
                        value.clearItem()
                        # remember to delete this one from the diagram item list
                        delKeyList.append(key)     
                        
            # draw Instance Relationships
            for key, value in self.itemDict.items():
                if value.diagramType == "Instance Relationship":
                    # does the Instance Relationship still exist?
                    if self.model.objectExists(topLevel=value.diagramType, objectName=value.name() ):                    
                        # does this Instance Relationship still exist on the diagram?
                        if not self.model.diagramItemIndex(diagramType=self.tabType, diagramName = self.diagramName, itemType = "Instance Relationship", NZID = value.NZID()) is None:
                            value.drawIt()
                        else:
                            # clear this item from the diagram as it no longer exists on this diagram
                            value.clearItem()
                            # remember to delete this one from the diagram item list
                            delKeyList.append(key)
                    else:
                        # clear this item from the diagram as it no longer exists on this diagram
                        value.clearItem()
                        # remember to delete this one from the diagram item list
                        delKeyList.append(key)   
                        
            # now get rid of all the node and rel templates that are no longer on this diagram        
            for key in delKeyList:
                del self.itemDict[key]   
            
    def drawDiagram(self, ):
        '''get saved diagram object data and create diagram objects on the scene''' 
#        print("loaded diagramDict {}".format(self.diagramDict))
        #generate all the node instances
        for diagramItem in self.diagramDict["items"]:
#            print(str(diagramItem))
            if diagramItem["diagramType"] == "Instance Node":
                # get the node instance object
                saveIndex, nodeDict = self.model.getDictByName(topLevel="Instance Node",objectName=diagramItem["NZID"])
                nodeInstance = NodeInstance(model=self.model, nodeInstanceDict=nodeDict)
                self.scene.addInode(QPointF(diagramItem["x"],diagramItem["y"] ),nodeInstance=nodeInstance )
                                    
        #generate the relationship instances
        for diagramItem in self.diagramDict["items"]:
            if diagramItem["diagramType"] == "Instance Relationship":
#                index, relationInstanceDict = self.model.getDictByName(topLevel="Instance Relationship", objectName=diagramItem["NZID"])
                self.scene.addIRelationship(NZID=diagramItem["NZID"], ) 
        
        #generate all the node templates
        for diagramItem in self.diagramDict["items"]:
            if diagramItem["diagramType"] == "Node Template":
                # get the node template 
                saveIndex, nodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=diagramItem["name"])
                self.scene.addTNode(QPointF(diagramItem["x"],diagramItem["y"] ), nodeTemplateDict=nodeTemplateDict, NZID = diagramItem["NZID"] )       
                
        #generate all the relationship templates
        for diagramItem in self.diagramDict["items"]:
            if diagramItem["diagramType"] == "Relationship Template":    
                self.scene.addTRelationship(relTemplateName=diagramItem["name"], NZID= diagramItem["NZID"], startNZID=diagramItem["startNZID"], endNZID=diagramItem["endNZID"] ) 
                
            # last items are selected so clear selections
            self.scene.clearSelection()
        
        # for straight line template diagrams must redraw diagram to get rel point assignments right - this is really lame
        if self.tabType == "Template Diagram":
            self.reDrawDiagram()
        
    def findNodeTemplatesOnDiagram(self, nodeTemplateName=None):
        nodeTemplateItems = []
        for key, nodeTemplateItem in self.itemDict.items():
            if nodeTemplateItem.diagramType == "Node Template":
                if nodeTemplateItem.name() == nodeTemplateName:
                    nodeTemplateItems.append(nodeTemplateItem)
        return nodeTemplateItems

  
    def relModeClick(self):
        if self.RelMode:
            if self.relStartMode:
                self.relStartMode = False
                self.relEndMode = True

    @pyqtSlot()
    def on_btnPrint_clicked(self):
        """
        print the diagram using the standard print dialog.
        """
        # get page setup data
        self.pageSizes = PageSizes()
        pageSetup = PageSetup(self.diagramDict["pageSetup"])
        objectDict = pageSetup.objectDict
        rows=objectDict["pageRows"]
        cols=objectDict["pageCols"]
        pageHeight, pageWidth = pageSetup.getHeightWidth()
        # configure the printer
        self.printer = QPrinter(QPrinter.HighResolution)
        if objectDict["pageOrientation"] == "Landscape":
            self.printer.setOrientation(QPrinter.Landscape)
        else:
            self.printer.setOrientation(QPrinter.Portrait)
        # bring up the print dialog
        form = QPrintDialog(self.printer)
        if form.exec_():
            try:
#                print("from:{} to:{}".format(self.printer.fromPage(), self.printer.toPage()))
                if self.printer.fromPage() == 0:
                    fromPage = 1
                else:
                    fromPage = self.printer.fromPage()
                if self.printer.toPage() == 0:
                    toPage = rows * cols
                else:
                    toPage = self.printer.toPage()
                self.painter = QPainter()
                self.painter.begin(self.printer)
                for r in range(1, rows+1):
                    for c in range(1, cols+1):
                        currentPage = c + ((r-1)*cols)
                        if currentPage  >= fromPage and currentPage <= toPage:
                            self.scene.render(self.painter, source=QRectF((pageWidth * c)-pageWidth, (pageHeight * r)-pageHeight, pageWidth, pageHeight))
                            if currentPage < toPage:
                                self.printer.newPage()
                self.painter.end()
            except:
                self.printer.abort()
                
    @pyqtSlot()
    def on_btnPageSetup_clicked(self):
        """
        Display the page setup dialog.  This allows the user to define page size etc.
        """
        form = dlgPageSetup(objectDict=self.diagramDict["pageSetup"])
        if form.exec_():
            self.diagramDict["pageSetup"] = form.pageSetup.objectDict
            self.drawPageGrid()
            
    @pyqtSlot()
    def on_btnShove_clicked(self):
        """
        This button toggles on/off the shove mode
        The user can use the mouse to move the diagram around
        """
        self.graphicsView.setDragMode (QGraphicsView.ScrollHandDrag)
        self.graphicsView.setCursor(QCursor(Qt.OpenHandCursor))
        self.checkModeButton(self.btnShove)
        
    @pyqtSlot()
    def on_btnPoint_clicked(self):
        """
        This button toggles on/off the point mode
        The user can use the mouse to select items on the diagram
        """
        self.graphicsView.setDragMode (QGraphicsView.NoDrag)
        self.graphicsView.setCursor(QCursor(Qt.ArrowCursor))
        self.checkModeButton(self.btnPoint)
        
    @pyqtSlot()
    def on_btnNode_clicked(self):
        """
        This button toggles on/off the Node Instance editing mode.
        Turn on Node Instance editing mode if it is not already turned on.
        Turn off Node Instance editing mode if it is already turned on.
        """
        self.checkModeButton(self.btnNode)
#        print("bntNodeClick - start - {}".format(self.scene.editMode))
            
    
    @pyqtSlot()
    def on_btnRel_clicked(self):
        """
        This button toggles on/off the Relationship Instance editing mode
        Turn on Instance Relationship editing mode if it is not already turned on.
        The user must select a start node and an end node to complete an Relationship Instance.
        Turn off Instance Relationship editing mode if it is already turned on.
        """
        self.checkModeButton(self.btnRel)
        
    def save(self, ):

        self.diagramDict.pop("items",0)
        itemList = []
        for key, value in self.itemDict.items():
            # make sure it still exists before saving it
            if self.model.objectExists(topLevel=value.diagramType, objectName=value.name() ):
                objectDict = value.getObjectDict()
                itemList.append(objectDict)
        self.diagramDict["items"] = itemList
        self.model.setModelDirty()  

    def updateMsgBar(self, msg):
        self.lblMessage.setText(msg)

    def addExistingInstanceNode(self, rightClickPos):
        d = CopyNodeToDiagramDlg(self, rightClickPos=rightClickPos)
        d.exec_()
        return None
        
    @pyqtSlot()
    def on_btnSyncDB_clicked(self):
        """
        Slot documentation goes here.
        """
        # should check to see if sync is on before running dialog
#        self.on_btnSyncOn_clicked()
        if self.model.modelData["SyncMode"] == "On":
            d = SyncToDBDlg(self, )
            d.exec_()
            self.parent.redrawInstanceDiagrams()            
            self.model.setModelDirty()
            self.model.updateTV()            
        else:
            self.helper.displayErrMsg("Sync DB Error", "You must turn Sync Mode On before you can synchronize to the Neo4j Instance")
    
    @pyqtSlot()
    def on_pbRedraw_clicked(self):
        """
        Slot documentation goes here.
        """
        self.reDrawDiagram()
    
    @pyqtSlot()
    def on_btnTNode_clicked(self):
        """
        This button toggles on/off the Node template editing mode.
        Turn on Node Template editing mode if it is not already turned on.
        Turn off Node Template editing mode if it is already turned on.
        """
        self.checkModeButton(self.btnTNode)
    
    @pyqtSlot()
    def on_btnTRel_clicked(self):
        """
        This button toggles on/off the Relationship Template editing mode
        Turn on Template Relationship editing mode if it is not already turned on.
        The user must select a start node and an end node to complete an Relationship Template.
        Turn off Template Relationship editing mode if it is already turned on.
        """
        self.checkModeButton(self.btnTRel)
    
    @pyqtSlot()
    def on_btnCopyNode_clicked(self):
        """
        user clicks the button to bring up the copy node dialog box
        """
        self.addExistingInstanceNode(self.scene.sceneRect().center())
    
    @pyqtSlot()
    def on_btnZoomOut_clicked(self):
        """
        User clicks the zoom out button
        """
        # change slider value and let it do the zooming
        self.zoomSlider.setValue(self.lastSliderValue - 1)
    
    @pyqtSlot(int)
    def on_zoomSlider_valueChanged(self, value):
        """
        User slides the slider
        
        @param value DESCRIPTION
        @type int
        """
#        print("current value: {} slider value:{}".format(self.lastSliderValue, value))
        if value < self.lastSliderValue:
            for x in range(value, self.lastSliderValue):
#                print("slide:{}".format(x))
                self.graphicsView.scale(.84, .84)
        elif value > self.lastSliderValue:
            for x in range(self.lastSliderValue, value):
#                print("slide:{}".format(x))
                self.graphicsView.scale(1.16, 1.16)
        
        # save slider value for next time
        self.lastSliderValue = value
    
    @pyqtSlot()
    def on_btnZoomIn_clicked(self):
        """
        User clicks the zoom in button
        """
        # change the slider value and let it do the zooming
        self.zoomSlider.setValue(self.lastSliderValue + 1)
