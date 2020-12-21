# -*- coding: utf-8 -*-

"""
CallOut.py
Provides a qgraphicsitem that displays text surrounded by a "callout" shape
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import  QPolygonF
from PyQt5.QtWidgets import QGraphicsItem,   QGraphicsTextItem, QGraphicsPolygonItem

# enum for z value graphics item stacking - higher numbered items cover lower numbered items
PAGELAYER = 0
RELATIONLAYER = 1
NODELAYER = 2
CALLOUTLAYER = 3

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
CALLOUT = 6

## handy geometry functions
#def angleDegrees (a, b, c):
#    ''' Return the angle in degrees between 3 sides of a triangle.
#        Given three sides a, b, c
#        Return the angle between sides a and b in degrees'''
#    return degrees(acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))
#
#def angleRadians(a, b, c):
#    ''' Return the angle in radians between 3 sides of a triangle.
#        Given three sides a, b, c
#        Return the angle between sides a and b in radians'''
#    return (acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))
#
#def centerLine (sx, sy, ex, ey):
#    ''' Find the center point of a line.
#        Given two end points of a line, (sx,sy) and (ex,ey).
#        Return the point (x,y) that is the center of the line.'''
#    csx = sx * 1.0
#    csy = sy * 1.0
#    cex = ex * 1.0
#    cey = ey * 1.0
#    return (csx+cex)/2.0, (csy+cey)/2.0
#
#def distanceLine (x1, y1, x2, y2):
#    ''' Find the length of a line.
#        Given two end points of a line, (sx,sy) and (ex,ey).
#        Return the length of the line.'''
#    distance = sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
#    return distance
#    
#def define_circle(p1, p2, p3):
#    """
#    Returns the center and radius of the circle passing the given 3 points.
#    In case the 3 points form a line, returns (None, infinity).
#    """
#    temp = p2[0] * p2[0] + p2[1] * p2[1]
#    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
#    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
#    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
#
#    if abs(det) < 1.0e-6:
##        return (None, np.inf)
#        return (None, None)
#
#    # Center of circle
#    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
#    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
#
##    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
#    radius = sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
#    return [cx, cy], radius
#

    
class CallOut():
    ''' This represents a callouton the diagram
        This class creates a text item and then surrounds it with a polygon that is a rectangle
        with a pointer to another object on the diagram.
        This can be used by hover over functions or be displayed as a part of a node or relationship
        '''    
    def __init__(self, scene, text, anchorPoint, diagramType, format ):
        
        self.scene = scene
        self.model = self.scene.parent.model
        self.text = text
        self.anchorPoint = anchorPoint
        self.diagramType = diagramType  
        self.format = format  

        # initialize the two qgraphicsitems needed to draw a relationship to None
        self.itemText = None
        self.itemPolygon = None  
        self.drawIt

    def name(self, ):
        return "no name"
        
    def NZID(self, ):
        return None  
        
    def clearItem(self, ):

        if (not self.itemText is None and not self.itemText.scene() is None):
            self.itemText.scene().removeItem(self.itemText)        
        if (not self.itemPolygon is None and not self.itemPolygon.scene() is None):
            self.itemPolygon.scene().removeItem(self.itemPolygon)     

    def drawIt(self, ):
        '''
        draw the callout
        '''

        # if the polygon and text graphics items already exist on the scene then delete them
        self.clearItem()
        
        # draw the relationship arc
        pen = self.format.pen()
        brush = self.format.brush()
        
        # create text box
        # draw the text 
        self.itemText = QGraphicsTextItem(self.relationInstance.relName, parent=None)
        self.itemText.setZValue(CALLOUTLAYER)
        self.itemText.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.itemText.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.itemText.setSelected(False)
        self.itemText.setData(NODEID, self.relationInstance.NZID) 
        self.itemText.setData(ITEMTYPE, CALLOUT)
        self.itemText.setHtml(self.genTextHTML())
        # set the position of the text
        self.itemText.setPos(self.anchorPoint)   
        
        # get the height and width of the text graphics item
        th = self.IRtext.boundingRect().height()
        tw  = self.IRtext.boundingRect().width()
        
        #create an empty polygon
        arrowPolygon = QPolygonF()
        # add callout points
        arrowPolygon.append(self.anchorPoint)
        arrowPolygon.append(QPointF(self.anchorPoint.x()+tw, self.anchorPoint.y()))
        arrowPolygon.append(QPointF(self.anchorPoint.x()+tw, self.anchorPoint.y()))
        arrowPolygon.append(QPointF(self.anchorPoint.x()+tw, self.anchorPoint.y()+th))
        arrowPolygon.append(QPointF(self.anchorPoint.x(), self.anchorPoint.y()+th))
        self.itemPolygon = QGraphicsPolygonItem(arrowPolygon, parent=None, )
        self.itemPolygon.setZValue(CALLOUTLAYER)
        self.itemPolygon.setBrush(brush)
        self.itemPolygon.setPen(pen)
        self.itemPolygon.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.itemPolygon.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True) 
        self.itemPolygon.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.itemPolygon.setSelected(False)
        
        # set data in the RelLine object
        self.IRel.setData(NODEID, self.relationInstance.NZID) 
        self.IRel.setData(ITEMTYPE, RELINSTANCEARC)
        # add the polygon object to the scene
        self.scene.addItem(self.itemPolygon) 
        # add text to the scene
        self.scene.addItem(self.itemText) 
        
    def updateText(self, ):
#        # force the node instance to update its values in case it has been updated from another diagram or the tree view
#        self.relationInstance.reloadDictValues()
#        self.IRtext.setPlainText(self.relationInstance.relName)
        self.itemText.setHtml(self.genTextHTML())
    
    def genTextHTML(self):
        '''generate html to display the text
        '''
        prefix = '<html><body>'
        suffix = "</body></html>"
        myHTML = ('{}<p><font size="1"> [{}]</font></p>{}'.format(prefix, self.text, suffix))
        return myHTML
        

        
    def moveIt(self, ):
        self.drawIt()
