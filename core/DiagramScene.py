#!/usr/bin/python
''' 
    Author: John Singer
    The DiagramScene class is used to render diagrams with no UI so they can be saved as image files

Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
    

'''
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import  QPainter, QImage
from PyQt5.QtWidgets import QGraphicsScene
#from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

# this has to follow the previous import so references to Qt.xxx will work
from PyQt5.QtCore import Qt

from core.helper import Helper
from core.RelationInstance import RelationInstance
from core.RelationItem import RelationItem
from core.RelationTemplateItem import RelationTemplateItem
from core.NodeInstance import NodeInstance
from core.NodeItem import NodeItem
from core.NodeTemplateItem import NodeTemplateItem

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

class DiagramScene(QGraphicsScene):
    
    def __init__(self,  parent=None):
        super(DiagramScene,  self).__init__(parent)
        self.parent = parent
        self.model = self.parent.model       
        self.helper = Helper() 
        
    def addIRelToScene(self, NZID=None, startNode=None, endNode=None, mode=None):
        '''
        called by drawDiagram to initially draw an existing diagram
        '''
        try:
            # get required data, if any of this errors out then skip adding this to the diagram
#            startNZID = startNode.data(NODEID)
#            endNZID = endNode.data(NODEID)
            relationInstanceDict=None
            index,  relationInstanceDict = self.model.getDictByName(topLevel="Instance Relationship", objectName=NZID)
            startNZID = relationInstanceDict["startNZID"]
            endNZID = relationInstanceDict["endNZID"]
            # create a new relation instance object
            relInstance = RelationInstance(parent=self, model=self.model, relationInstanceDict=relationInstanceDict, startNode=self.parent.itemDict[startNZID].itemInstance, endNode=self.parent.itemDict[endNZID].itemInstance)
            # create a new relation item object
            relItem = RelationItem(self, relationInstance=relInstance)
            # add the relation item object to the diagram item dictionary
            self.parent.itemDict[relInstance.NZID] = relItem
            # this counts how many relationships exist between two nodes
            self.parent.addRelationship(relInstance)
        except:
            print("error adding instance rel")

        
    def addInode(self, point, nodeInstance=None):
        '''
        Add a Node Instance to the diagram
        '''
        try:
            nodeItem = NodeItem(self, point.x(),point.y(),nodeInstance=nodeInstance)
            # add it to the diagramEditor's list of node/rels
            self.parent.itemDict[nodeInstance.NZID] = nodeItem
        except:
            print("error adding Instance Node")
            
        return nodeInstance.NZID
        
    def addTNode(self, point, nodeTemplateDict=None, NZID=None):
        '''
        Add a Node template to the diagram at the given point.
        Used by the drawdiagram function
        '''
        try:
            # create a NodeTemplateItem
            nodeTemplateItem = NodeTemplateItem(self, point.x(), point.y(), nodeTemplateDict=nodeTemplateDict, NZID=NZID)
            # add it to the diagramEditor's list of node/rels
            self.parent.itemDict[nodeTemplateItem.NZID] = nodeTemplateItem
        except:
            print("error adding template Node")
        
    def addTRelToScene(self, relTemplateName=None, NZID=None, startNZID=None, endNZID=None, mode=None):
        # if adding a relationship template while initially loading the diagram or while dropping arelationship template, you will get the name of the relationship template
        
        try:

            index,  relationTemplateDict = self.model.getDictByName(topLevel="Relationship Template", objectName=relTemplateName)
            # create a new RelationTemplateItem object
            relationTemplateItem = RelationTemplateItem(scene = self, NZID=NZID,  relationTemplateDict=relationTemplateDict, startNodeItem=self.parent.itemDict[startNZID], endNodeItem=self.parent.itemDict[endNZID])
            # add the relation item object to the diagram item dictionary
            self.parent.itemDict[relationTemplateItem.NZID] = relationTemplateItem 
            # tell the relationship to set it's loation and draw itself
            # for some reason, rel template doesn't draw itself when the object is created.  You have to tell it to draw
            relationTemplateItem.drawIt2()
        except:
            print("error adding template Relationship")

###########################################################
# diagram render methods
###########################################################
    def renderDiagram(self, diagramType=None, diagramName=None):
        try:
            self.diagramName = diagramName
            saveIndex, diagramDict = self.model.getDictByName(topLevel=diagramType,objectName=diagramName)
            self.diagramDict = diagramDict  # this is all the diagram data and contains the saved diagram items
            self.itemDict = {}   # dictionary of graphic items rendered on the scene
            self.drawDiagram()  
            self.setSceneRect(self.itemsBoundingRect())
            self.clearSelection()
        except Exception as e: 
            self.helper.displayErrMsg("Render Diagram", "Error rendering diagram {}. Error: {}".format(self.diagramName, str(e)))            


    def saveImage(self, fileName=None):
        try:
            self.image = QImage(self.sceneRect().size().toSize(), QImage.Format_ARGB32_Premultiplied)
            self.image.fill(Qt.white)
            self.painter = QPainter(self.image)
            self.render(self.painter)
            self.painter.end()
            self.image.save(fileName)
        except Exception as e: 
            self.helper.displayErrMsg("Save Image", "Error saving diagram image file: {}. Error: {}".format(fileName, str(e)))            

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
                self.addInode(QPointF(diagramItem["x"],diagramItem["y"] ),nodeInstance=nodeInstance )
            elif diagramItem["diagramType"] == "Instance Relationship":
                self.addIRelToScene(NZID=diagramItem["NZID"] ) 
            elif diagramItem["diagramType"] == "Node Template":
                # get the node template 
                saveIndex, nodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=diagramItem["name"])
                self.addTNode(QPointF(diagramItem["x"],diagramItem["y"] ), nodeTemplateDict=nodeTemplateDict, NZID = diagramItem["NZID"] )       
            elif diagramItem["diagramType"] == "Relationship Template":    
                self.addTRelToScene(relTemplateName=diagramItem["name"], NZID= diagramItem["NZID"], startNZID=diagramItem["startNZID"], endNZID=diagramItem["endNZID"] ) 
            
