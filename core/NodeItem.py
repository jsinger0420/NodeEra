# -*- coding: utf-8 -*-

"""
NodeItem.py provides a class to manage a NodeInstance on an Instance Diagram.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""
from math import sqrt, degrees, acos
from PyQt5.QtCore import   QRectF
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem,  QGraphicsTextItem
from forms.INodeFormatDlg import INodeFormat

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

# enum for z value graphics item stacking - higher numbered items cover lower numbered items
PAGELAYER = 0
RELATIONLAYER = 1
NODELAYER = 2

# ENUM for property grid
PROPERTY, DATATYPE, VALUE = range(3)

# handy geometry functions
def angleDegrees (a, b, c):
    ''' Return the angle in degrees between 3 sides of a triangle.
        Given three sides a, b, c
        Return the angle between sides a and b in degrees'''
    return degrees(acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))

def angleRadians(a, b, c):
    ''' Return the angle in radians between 3 sides of a triangle.
        Given three sides a, b, c
        Return the angle between sides a and b in radians'''
    return (acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))

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
# NodeItem combined with NodeInstance represents an actual node in Neo4j on the diagram
########################################################################
class NodeItem():
    ''' 
    This represents one node on the diagram.
    This class creates the ellipse graphics item and the text graphics item and adds them to the scene.
    '''
    def __init__(self, scene, x, y, nodeInstance=None):
        self.scene = scene
        self.logMsg = None
        
        self.x = x
        self.y = y
        self.itemInstance = nodeInstance
        self.diagramType = self.itemInstance.diagramType
        self.displayText = None
        self.model = self.scene.parent.model
        self.neoCon = self.scene.parent.model.modelNeoCon
        self.getFormat()
        # remember current width and height
        self.oldNodeWidth = 0
        self.oldNodeHeight = 0
        # init graphics objects to none 
        self.INode = None
        self.INtext = None
#        # init list of qgrapphicellipseitems to none
#        self.ellipsePoints = []
#        self.ellipseGraphicItems = []
        # draw the ellipse
        self.drawIt()
        
        
        
    def name(self, ):
        return self.itemInstance.NZID
    
    def NZID(self, ):
        return self.itemInstance.NZID
        
    def getFormat(self, ):
        '''
        determine the format to use to draw the instance node
        - start with the project default
        - if the instance node has a template then use the instance format defined on the template
        '''
        # get the default
        self.nodeFormat = INodeFormat(formatDict=self.model.modelData["INformat"])
        # get a custom template format if there is one
        if not self.itemInstance.nodeTemplate is None:
            index, nodeTemplateDict = self.model.getDictByName(topLevel="Node Template",objectName=self.itemInstance.nodeTemplate)
            if not nodeTemplateDict is None:
                self.instanceNodeFormatDict = nodeTemplateDict.get("INformat", None)
                if not self.instanceNodeFormatDict is None:
                    self.nodeFormat = INodeFormat(formatDict=self.instanceNodeFormatDict) 

    def clearItem(self, ):
        
        if (not self.INode is None and not self.INode.scene() is None):
            self.INode.scene().removeItem(self.INode)        
        if (not self.INtext is None and not self.INtext.scene() is None):
            self.INtext.scene().removeItem(self.INtext)    
            
#        # remove the points on the ellipse - this code is only for debugging
#        for point in self.ellipseGraphicItems:
#            if (not point is None and not point.scene() is None):
#                point.scene().removeItem(point)    
        
    def drawIt(self, ):
        # force the node instance to update its values in case it has been updated from another diagram or the tree view
        self.itemInstance.reloadDictValues()
        # get current format as it may have changed
        self.getFormat()
        if self.oldNodeWidth != self.nodeFormat.formatDict["nodeWidth"] or self.oldNodeHeight != self.nodeFormat.formatDict["nodeHeight"]:
            # remove graphic items that already exist
            self.clearItem()
            # create the node ellipse
            self.INode = QGraphicsEllipseItem(QRectF(self.x,self.y,self.nodeFormat.formatDict["nodeWidth"],self.nodeFormat.formatDict["nodeHeight"]), parent=None)
            # create the node text
            self.INtext = QGraphicsTextItem("", parent=None)
            self.INtext.setPos(self.x, self.y)
            self.x = self.INode.sceneBoundingRect().x()
            self.y = self.INode.sceneBoundingRect().y()
#            print("after create items before drawIt: sceneboundingrect {} ".format( self.INode.sceneBoundingRect()))
#            print("x:{} y:{}".format(self.x, self.y))
            self.formatItem()
            self.scene.addItem(self.INode) 
            self.scene.addItem(self.INtext) 
#            # add points
#            for point in self.ellipseGraphicItems:
#                self.scene.addItem(point) 
            
            # redraw all the rels associated to this node.
            self.moveRels()
        else:
#            print("before drawIt: sceneboundingrect {} ".format( self.INode.sceneBoundingRect()))
#            print("x:{} y:{}".format(self.x, self.y))
            self.formatItem()
        # remember current width and height
        self.oldNodeWidth = self.nodeFormat.formatDict["nodeWidth"]
        self.oldNodeHeight = self.nodeFormat.formatDict["nodeHeight"]
#        print("after drawIt: sceneboundingrect {} ".format( self.INode.sceneBoundingRect()))
#        print("x:{} y:{}".format(self.x, self.y))

#    def genPoints(self, ):
#        '''Ellipse Constructor - not sure of these, need to verify
#        def __init__(self, mx, my, rh, rv):
#        mx - center point x
#        my - center point y
#        rh - height of ellipse
#        rv - width of ellipse'''
#        x = self.INode.sceneBoundingRect().center().x()
#        y = self.INode.sceneBoundingRect().center().y()
#        w = self.INode.sceneBoundingRect().width()/2.0
#        h = self.INode.sceneBoundingRect().height()/2.0
#        myEllipse = Ellipse(x, y, w, h)
#        for d in range(0, 360, 10):
#            x, y = myEllipse.pointFromAngle(radians(d))
#            self.ellipsePoints.append([d, x, y])
#            aPoint = QGraphicsEllipseItem(QRectF(x-2.5,y-2.5,5, 5), parent=None)
#            self.ellipseGraphicItems.append(aPoint)
##        print(self.ellipsePoints)
        
        
    def formatItem(self, ):
        # configure the formatting aspects of the qgraphics item
        pen = self.nodeFormat.pen()
        brush = self.nodeFormat.brush()
        self.INode.setZValue(NODELAYER)
        self.INode.setBrush(brush)
        self.INode.setPen(pen)
        self.INode.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.INode.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True) 
        self.INode.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.INode.setSelected(True)
        self.INode.setData(1, self.itemInstance.NZID) # get with self.INode.data(1)
        self.INode.setData(ITEMTYPE, NODEINSTANCE)
        # draw the text 
        self.updateText()
        self.INtext.setZValue(NODELAYER)
        self.INtext.setTextWidth(self.INode.boundingRect().width())
        self.INtext.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.INtext.setFlag(QGraphicsItem.ItemIsSelectable, False)  
        self.INtext.setData(NODEID, self.itemInstance.NZID) 
        self.INtext.setData(ITEMTYPE, NODEINSTANCETEXT)


    def updateText(self, ):
        '''
        Generate the HTML that formats the node  data inside the ellipse
        '''
        # generate the html
        prefix = "<!DOCTYPE html><html><body>"
        suffix = "</body></html>"
        try:
            Lbl = str(self.itemInstance.labelList[0][0])
        except:
            Lbl = "No Labels"
        firstLbl = "<center><b>{}</b></center>".format(Lbl)        
        try:
            propName = str(self.itemInstance.propList[0][PROPERTY])
            propVal = str(self.itemInstance.propList[0][VALUE])
            prop = "{}: {}".format(propName, propVal)
        except:
            prop = "No Properties"              
        firstProp = "<center>{}</center>".format(prop)        
        genHTML = '{}{}<hr width="75%">{}{}'.format(prefix, firstLbl, firstProp, suffix)        
        self.INtext.setHtml(genHTML)
        
        
    def moveIt(self, dx,dy):
        '''Move the node ellipse and the node textbox to the delta x,y coordinate.'''
#        print("before moveIt: sceneboundingrect {} ".format( self.INode.sceneBoundingRect()))

        self.INode.moveBy(dx, dy)
        self.x = self.INode.sceneBoundingRect().x()
        self.y = self.INode.sceneBoundingRect().y()
        self.INtext.moveBy(dx, dy)
#        print("after moveIt: sceneboundingrect {} ".format( self.INode.sceneBoundingRect()))
        
#        # recalc points
#        self.genPoints()
        
#        for point in self.ellipseGraphicItems:
#            point.moveBy(dx, dy)
                
        self.moveRels()


    def moveRels(self, ):
        '''Redraw all the relationship arcs connected to the Node ellipse.'''
#        print("moveRels")
        for key,diagramItem in self.scene.parent.itemDict.items():
            if diagramItem.diagramType == "Instance Relationship":
                if self.itemInstance.NZID in [diagramItem.relationInstance.startNZID, diagramItem.relationInstance.endNZID]:
                    diagramItem.drawRelationship()
#                if diagramItem.relationInstance.startNZID == self.itemInstance.NZID:
#                    diagramItem.moveRelationshipLine()
##                    print("move startnode {}-{}".format(self.x, self.y))
#                if diagramItem.relationInstance.endNZID == self.itemInstance.NZID:
#                    diagramItem.moveRelationshipLine()
##                    print("move endnode {}-{}".format(self.x, self.y))
        
    def getObjectDict(self, ):
        '''
        This function returns a dictionary with all the data that represents this node item.  
        The dictionary is added to the Instance Diagram dictionary.'''
        objectDict = {}
        objectDict["NZID"] = self.itemInstance.NZID
        objectDict["x"] = self.INode.sceneBoundingRect().x()
        objectDict["y"] = self.INode.sceneBoundingRect().y()
        objectDict["diagramType"] = self.diagramType
        return objectDict

    def setLogMethod(self, logMethod=None):
        if logMethod is None:
            if self.logMsg is None:
                self.logMsg = self.noLog
        else:
            self.logMsg = logMethod
            
    def noLog(self, msg):
        return
        


       
