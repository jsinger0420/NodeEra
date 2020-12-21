# -*- coding: utf-8 -*-

"""
NodeTemplateItem.py provides a class to manage a NodeTemplate on a Template Diagram.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
import uuid
from math import sqrt
from PyQt5.QtCore import   QRectF, Qt, QPointF, QLineF
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem,  QGraphicsTextItem
from forms.TNodeFormatDlg import TNodeFormat

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

# enum for node template side
TOP, R, BOTTOM, L = range(4)

# enum for orientation
LEFT, ABOVE, RIGHT, BELOW = range(4)

LABEL, REQUIRED, NODEKEY = range(3)
PROPERTY, DATATYPE, PROPREQ, DEFAULT, EXISTS, UNIQUE, PROPNODEKEY = range(7)

def centerLine (sx, sy, ex, ey):
    ''' Find the center point of a line.
        Given two end points of a line, (sx,sy) and (ex,ey).
        Return the point (x,y) that is the center of the line.'''
    csx = sx * 1.0
    csy = sy * 1.0
    cex = ex * 1.0
    cey = ey * 1.0
    return (csx+cex)/2.0, (csy+cey)/2.0

def distanceLine (x1, y1, x2, y2):
    ''' Find the length of a line.
        Given two end points of a line, (sx,sy) and (ex,ey).
        Return the length of the line.'''
    distance = sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
    return distance
    

    

        

########################################################################
# represents a Node Template on the diagram
########################################################################
class NodeTemplateItem():
    ''' 
    This represents one node template on the diagram.  A node template can be on many diagrams
    This class creates the rectangle graphics item and the text graphics item and adds them to the scene.
    '''
    def __init__(self, scene, x, y, nodeTemplateDict = None, NZID = None):
        self.scene = scene
        self.logMsg = None
        self.x = x
        self.y = y
        self.nodeTemplateDict = nodeTemplateDict
#        self.name = self.nodeTemplateDict.get("name", "")   THIS HAS BEEN REPLACED BY THE name FUNCTION - SEE BELOW
        self.diagramType = "Node Template"
        self.displayText = None
        self.model = self.scene.parent.model
        self.gap = 100
        self.relList = []
        # assign a unique key if it doesn't already have one
        if NZID == None:
            self.NZID = str(uuid.uuid4())
        else:
            self.NZID = NZID
            
        # init graphics objects to none 
        self.TNode = None
        self.TNtext = None
        
        # draw the node template on the diagram
        self.drawIt()

    def name(self, ):
        return self.nodeTemplateDict.get("name", "")
    
    def getX(self, ):
        return self.TNode.boundingRect().x()
    def getY(self, ):
        return self.TNode.boundingRect().y()
    def getHeight(self, ):
        return self.TNode.boundingRect().height()
    def getWidth(self, ):
        return self.TNode.boundingRect().width()
        
    def getRelList(self, ):
        '''return a list of all relationitems that are inbound or outbound from this node template.
          do not include self referencing relationships
        '''
        return [diagramItem for key, diagramItem in self.scene.parent.itemDict.items() 
                      if diagramItem.diagramType == "Relationship Template"
                      and (diagramItem.startNZID == self.NZID or diagramItem.endNZID == self.NZID)]
    
    
    def getPoint(self, offset = None ):
        '''
        This function is used by the template diagram to calculate the location to drop a node template on the diagram
        '''
        if offset is None:
            return QPointF(self.x, self.y)
        else:
            return QPointF(self.x + offset, self.y + offset)

        
    def getFormat(self, ):
        '''
        determine if the Node Template  has a template format or should use the project default format
        '''
        # get the node Template custom format
        customFormat = self.nodeTemplateDict.get("TNformat", None)

        if not customFormat is None:
            # get the template custom format
            self.nodeFormat = TNodeFormat(formatDict=customFormat)
        else:
            # get the project default format
            self.nodeFormat = TNodeFormat(formatDict=self.model.modelData["TNformat"])            
        
    def clearItem(self, ):
        
        if (not self.TNode is None and not self.TNode.scene() is None):
            self.TNode.scene().removeItem(self.TNode)        
        if (not self.TNtext is None and not self.TNtext.scene() is None):
            self.TNtext.scene().removeItem(self.TNtext)        
            
    def drawIt(self, ):
        
        # get current format as it may have changed
        self.getFormat()

        # create the qgraphicsItems if they don't exist
        if self.TNode is None:
            # create the rectangle
            self.TNode = QGraphicsRectItem(QRectF(self.x,self.y,self.nodeFormat.formatDict["nodeWidth"],self.nodeFormat.formatDict["nodeHeight"]), parent=None)
            self.TNode.setZValue(NODELAYER)
            self.TNode.setFlag(QGraphicsItem.ItemIsMovable, True) 
            self.TNode.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True) 
            self.TNode.setFlag(QGraphicsItem.ItemIsSelectable, True) 
            self.TNode.setSelected(True)
            self.TNode.setData(1, self.NZID) # get with self.INode.data(1)
            self.TNode.setData(ITEMTYPE, NODETEMPLATE)     
            # create the text box
            self.TNtext = QGraphicsTextItem("", parent=None)
            self.TNtext.setPos(self.x, self.y)
            self.TNtext.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.TNtext.setFlag(QGraphicsItem.ItemIsSelectable, False)  
            self.TNtext.setData(NODEID, self.NZID) 
            self.TNtext.setData(ITEMTYPE, NODETEMPLATETEXT)
            self.TNtext.setZValue(NODELAYER)            
            # save the location
            self.x = self.TNode.sceneBoundingRect().x()
            self.y = self.TNode.sceneBoundingRect().y()
            # generate the html and resize the rectangle
            self.formatItem()
            # add the graphics items to the scene
            self.scene.addItem(self.TNode) 
            self.scene.addItem(self.TNtext) 
        else:
            # generate the html and resize the rectangle
            self.formatItem()




    def formatItem(self, ):

        # configure the formatting aspects of the qgraphics item
        pen = self.nodeFormat.pen()
        brush = self.nodeFormat.brush()
        self.TNode.setBrush(brush)
        self.TNode.setPen(pen)

        # generate the HTML 
        genHTML = self.generateHTML()   
        self.TNtext.prepareGeometryChange()
#        print("before html bounding rectangle width:{}".format(self.TNtext.boundingRect().width()))
#        print("before html text width:{}".format(self.TNtext.textWidth()))
        self.TNtext.setTextWidth(-1)  # reset the width to unkonwn so it will calculate a new width based on the new html
        self.TNtext.setHtml(genHTML)
#        print("after html bounding rectangle width:{}".format(self.TNtext.boundingRect().width()))
#        print("after html text width:{}".format(self.TNtext.textWidth()))

        # make sure minimum width of 120
        if self.TNtext.boundingRect().width() < 120:
            self.TNtext.setTextWidth(120)
        else:
            self.TNtext.setTextWidth(self.TNtext.boundingRect().width())  # you have to do a setTextWidth to get the html to render correctly.  

        # set the rectangle item to the same size as the formatted html
        self.TNode.prepareGeometryChange()
        currentRect = self.TNode.rect()
        # insure minimum height of 120
        if self.TNtext.boundingRect().height() < 120:
            currentRect.setHeight(120)
        else:
            currentRect.setHeight(self.TNtext.boundingRect().height())
        currentRect.setWidth(self.TNtext.boundingRect().width())
        self.TNode.setRect(currentRect)        


    def generateHTML(self, ):
        '''
        Generate the HTML that formats the node template data inside the rectangle
        '''
        # generate the html
        prefix = "<!DOCTYPE html><html><body>"
#        head = "<head><style>table, th, td {border: 1px solid black; border-collapse: collapse;}</style></head>"
        suffix = "</body></html>"
#        blankRow = "<tr><td><left>{}</left></td><td><left>{}</left></td><td><left>{}</left></td><td><left>{}</left></td></tr>".format("", "", "", "")

        name = "<center><b>{}</b></center>".format(self.nodeTemplateDict.get("name", ""))
        lbls = self.genLblHTML()
        props = self.genPropHTML()
        genHTML = "{}{}<hr>{}<br><hr>{}{}".format(prefix, name, lbls, props, suffix)
#        print("{} html: {}".format(self.name(), genHTML))
        
        return genHTML

    def genLblHTML(self):
#        html = '<table width="90%">'
        html = '<table style="width:90%;border:1px solid black;">'
        if len(self.nodeTemplateDict.get("labels", [])) > 0:
            for lbl in self.nodeTemplateDict.get("labels", []):
                if lbl[NODEKEY] == Qt.Checked:
                    nk = "NK"
                else:
                    nk = "&nbsp;&nbsp;"
                if lbl[REQUIRED] == Qt.Checked:
                    rq = "R"
                else:
                    rq = ""               

                html = html + '<tr align="left"><td width="15%"><left>{}</left></td><td width="65%"><left>{}</left></td><td width="10%"><left>{}</left></td><td width="10%"><left>{}</left></td></tr>'.format(nk, lbl[LABEL], "", rq)
            html = html + "</table>"
        else:
            html = '<tr align="left"><td width="15%"><left>{}</left></td><td  width="65%"><left>{}</left></td><td width="10%"><left>{}</left></td><td width="10%"><left>{}</left></td></tr>'.format("  ", "NO{}LABELS".format("&nbsp;"), "", "")
            html = html + "</table>"
        
        return html
        
        
    def genPropHTML(self):
#        PROPERTY, DATATYPE, PROPREQ, DEFAULT, EXISTS, UNIQUE, PROPNODEKEY
        html = '<table style="width:90%;border:1px solid black;">'
        if len(self.nodeTemplateDict.get("properties", [])) > 0:
            for prop in self.nodeTemplateDict.get("properties", []):
                if prop[PROPNODEKEY] == Qt.Checked:
                    nk = "NK"
                else:
                    nk = "&nbsp;&nbsp;"
                if prop[PROPREQ] == Qt.Checked:
                    rq = "R"
                else:
                    rq = ""           
                if prop[EXISTS] == Qt.Checked:
                    ex = "E"
                else:
                    ex = ""                
                if prop[UNIQUE] == Qt.Checked:
                    uq = "U"
                else:
                    uq = ""      
                html = html + '<tr align="left"><td width="15%"><left>{}</left></td><td width="65%"><left>{}</left></td><td width="10%"><left>{}</left></td><td width="10%"><left>{}</left></td><td width="10%"><left>{}</left></td></tr>'.format(nk, prop[PROPERTY], rq, ex, uq)
            html = html + "</table>"
        else:
            html = html + '<tr align="left"><td width="15%"><left>{}</left></td><td width="65%"><left>{}</left></td><td width="10%"><left>{}</left></td><td width="10%"><left>{}</left></td></tr>'.format("&nbsp;&nbsp;", "NO{}PROPERTIES".format("&nbsp;"), "","", "")
            html = html + "</table>"
        return html
        
        
    def moveIt(self, dx,dy):
        '''
        Move the node rectangle and the node textbox to the delta x,y coordinate.
        '''
#        print("before moveIt: sceneboundingrect {} ".format( self.INode.sceneBoundingRect()))

        self.TNode.moveBy(dx, dy)
        self.x = self.TNode.sceneBoundingRect().x()
        self.y = self.TNode.sceneBoundingRect().y()
        self.TNtext.moveBy(dx, dy)
#        print("after moveIt: sceneboundingrect {} ".format( self.INode.sceneBoundingRect()))
        # now redraw all the relationships
        self.drawRels()

 
    def drawRels(self, ):
        '''Redraw all the relationship lines connected to the Node Template Rectangle'''
        # get a list of the relationship items connected to this node template
        self.relList = self.getRelList()
        
        # assign the correct inbound/outbound side for the rel
        for rel in self.relList:
            if rel.endNodeItem.NZID != rel.startNodeItem.NZID:        # ignore bunny ears
                rel.assignSide()
        # get a set of all the nodes and sides involved
        nodeSet = set()
        for rel in self.relList:
            if rel.endNodeItem.NZID != rel.startNodeItem.NZID:        # ignore bunny ears
                nodeSet.add((rel.endNodeItem, rel.inboundSide))
                nodeSet.add((rel.startNodeItem, rel.outboundSide))
                
        # tell each node side to assign rel locations
        for nodeSide in nodeSet:
            nodeSide[0].assignPoint(nodeSide[1])
        
        ############################################
        
        # now tell them all to redraw
        for rel in self.relList:
            rel.drawIt2()
            

    def calcOffset(self, index, totRels):
        offset = [-60, -40, -20, 0, 20, 40, 60]
        offsetStart = [3, 2, 2, 1, 1, 0, 0]
        if totRels > 7:
            totRels = 7
        return offset[offsetStart[totRels-1]+index]
         
        
    def assignPoint(self, side):
        # go through all the rels on a side and assign their x,y coord for that side
        self.relList = self.getRelList()
        sideList = [rel for rel in self.relList if ((rel.startNZID == self.NZID and rel.outboundSide == side) or (rel.endNZID == self.NZID and rel.inboundSide == side))]
        totRels = len(sideList)
        if totRels > 0:
            if side == R:
                # calc center of the side
                x = self.x + self.getWidth()
                y = self.y + self.getHeight()/2 
                # sort the rels connected to this side by the y value
                sideList.sort(key=self.getSortY)
                # assign each of them a position on the side starting in the center and working out in both directions
                for index, rel in enumerate(sideList):
                    if rel.startNZID == self.NZID:
                        rel.outboundPoint = QPointF(x, y + (self.calcOffset(index, totRels))) 
                    if rel.endNZID == self.NZID:
                        rel.inboundPoint = QPointF(x, y + (self.calcOffset(index, totRels)))
            elif side == L:
                x = self.x
                y = self.y + self.getHeight()/2 
                sideList.sort(key=self.getSortY)
                for index, rel in enumerate(sideList):
                    if rel.startNZID == self.NZID:
                        rel.outboundPoint = QPointF(x, y + (self.calcOffset(index, totRels)))
                    if rel.endNZID == self.NZID:
                        rel.inboundPoint = QPointF(x, y + (self.calcOffset(index, totRels)))   
            elif side == TOP:
                x = self.x + self.getWidth()/2
                y = self.y
                sideList.sort(key=self.getSortX)
                for index, rel in enumerate(sideList):
                    if rel.startNZID == self.NZID:
                        rel.outboundPoint = QPointF(x + (self.calcOffset(index, totRels)), y)
                    if rel.endNZID == self.NZID:
                        rel.inboundPoint = QPointF(x + (self.calcOffset(index, totRels)), y)     
            elif side == BOTTOM:
                x = self.x + self.getWidth()/2
                y = self.y + self.getHeight()
                sideList.sort(key=self.getSortX)
                for index, rel in enumerate(sideList):
                    if rel.startNZID == self.NZID:
                        rel.outboundPoint = QPointF(x + (self.calcOffset(index, totRels)), y)
                    if rel.endNZID == self.NZID:
                        rel.inboundPoint = QPointF(x + (self.calcOffset(index, totRels)), y)    
            else:
                print("error, no side")
                

        
    def getSortY(self, rel):
        # if this node is the start node then return the end node's Y
        if rel.startNZID == self.NZID:
            return rel.endNodeItem.TNode.sceneBoundingRect().center().y()
        # if this node is the end node then return the start node's Y
        if rel.endNZID == self.NZID:
            return rel.startNodeItem.TNode.sceneBoundingRect().center().y()
        # this should never happen
        return 0
        
    def getSortX(self, rel):
        # if this node is the start node then return the end node's X
        if rel.startNZID == self.NZID:
            return rel.endNodeItem.TNode.sceneBoundingRect().center().x()
        # if this node is the end node then return the start node's X
        if rel.endNZID == self.NZID:
            return rel.startNodeItem.TNode.sceneBoundingRect().center().x()
        # this should never happen
        return 0        
        
    def getObjectDict(self, ):
        '''
        This function returns a dictionary with all the data that represents this node template item.  
        The dictionary is added to the Instance Diagram dictionary.'''
        objectDict = {}
        objectDict["NZID"] = self.NZID
        objectDict["name"] = self.nodeTemplateDict.get("name", "")
        objectDict["displayText"] = self.displayText
        objectDict["x"] = self.TNode.sceneBoundingRect().x()
        objectDict["y"] = self.TNode.sceneBoundingRect().y()
        objectDict["diagramType"] = self.diagramType
        objectDict["labels"] = self.nodeTemplateDict.get("labels", [])
        objectDict["properties"] = self.nodeTemplateDict.get("properties", [])
        
        return objectDict

    def setLogMethod(self, logMethod=None):
        if logMethod is None:
            if self.logMsg is None:
                self.logMsg = self.noLog
        else:
            self.logMsg = logMethod
            
    def noLog(self, msg):
        return
        


       
