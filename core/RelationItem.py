# -*- coding: utf-8 -*-

"""
RelationItem.py provides two classes:
1. RelationItem - manages the qgraphicsItem on the Instance Diagram using a RelLIne.  
2. RelLine - an subtype of qGraphicsItem that draws an arc between two points.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from math import cos, sqrt, degrees, copysign, acos, sin, radians, atan, tan

from PyQt5.QtCore import QRectF, QPointF, Qt, QLineF
from PyQt5.QtGui import  QPainter, QColor, QPolygonF
from PyQt5.QtWidgets import QGraphicsItem,   QGraphicsTextItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsLineItem
from forms.IRelFormatDlg import IRelFormat

# enum for calculated points
DEGREES = 0
X = 1
Y = 2

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

# enum for z value graphics item stacking - higher numbered items cover lower numbered items
PAGELAYER = 0
RELATIONLAYER = 1
NODELAYER = 2

# enum for line type
STRAIGHT = 0
CURVE = 1

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
    
def define_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    if abs(det) < 1.0e-6:
#        return (None, np.inf)
        return (None, None)

    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

#    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    radius = sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    return [cx, cy], radius

    
class Ellipse:
    '''Class Ellipse provides handy functions for ellipses'''
    def __init__(self, mx, my, rh, rv):
        '''Ellipse Constructor - not sure of these, need to verify
        mx - center point x
        my - center point y
        rh - height of ellipse
        rv - width of ellipse'''
        self.mx = mx
        self.my = my
        self.rh = rh
        self.rv = rv

    def pointFromAngle(self, a):
        '''Return the point on an ellipse that is is at angle "a" from the origin.
            Given angle a in degrees, return the point (x,y) on the ellipse.'''
        c = cos(a)
        s = sin(a)
        ta = s / c  ## tan(a)
        tt = ta * self.rh / self.rv  ## tan(t)
        d = 1. / sqrt(1. + tt * tt)
        x = self.mx + copysign(self.rh * d, c)
        y = self.my + copysign(self.rv * tt * d, s)
        return x, y

class RelText(QGraphicsTextItem):
    def __init__(self, parent=None):
        super(RelText, self).__init__(parent)
        self.setZValue(RELATIONLAYER)
        self.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.setSelected(True)
        self.setAcceptHoverEvents(True)
        
    def hoverEnterEvent(self, event):
#        print("hoverEnterEvent")
        return        
        
class RelArc(QGraphicsItem):
    ''' RelArc extends QGraphicsItem to draw a relationship arc.'''
    def __init__(self, parent = None,  sx=None, sy=None, ex=None, ey=None, cx=None, cy=None,  pen=None, brush=None,  numRels=None):
        QGraphicsItem.__init__(self,parent)
        '''The constructor calculates all the values needed to draw the arc.
            The input is the start and end points on the line used to calculate with'''
        # set the "Z" layer to draw arcs on
        self.setZValue(RELATIONLAYER)
        # this is the centerpoint of the target ellipse
        self.ecx=cx
        self.ecy=cy

        #these are the points of the line segment to draw the arc through
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.pen = pen
        self.brush = brush
        # numrels is the number of this relationship is the list of all relationships between the two nodes, i.e. 1st, 2nd, 3rd
        self.numRels = numRels
        # computation for arc
        # get the centerpoint of the line
        self.cx, self.cy = centerLine(self.sx, self.sy, self.ex, self.ey)
        # get the distance of the line
        d = distanceLine(self.sx, self.sy, self.ex, self.ey)
        # use this distance as the radius of the circle being used to draw the arc
        self.r = d 
        # calculate the center of a circle with a given radius that passes through two points  
        self.circlex = self.cx + sqrt((d**2)-((d/2)**2)) * ((self.sy-self.ey)/d)
        self.circley = self.cy + sqrt((d**2)-((d/2)**2)) * ((self.ex-self.sx)/d)
        # calculate start angle for arc
        if self.ey > self.circley:
            a = distanceLine(self.circlex, self.circley, self.ex, self.ey)
            b = distanceLine(self.circlex, self.circley, self.circlex-self.r, self.circley)
            c = distanceLine(self.ex, self.ey, self.circlex-self.r, self.circley)
            self.startAngle = (angleDegrees(a, b, c) * 16) + (180 * 16)  # in 16ths of a degree
            self.startAngleR = radians(self.startAngle/16)            # in radians
        else:
            a = distanceLine(self.circlex, self.circley, self.ex, self.ey)
            b = distanceLine(self.circlex, self.circley, self.circlex+self.r, self.circley)
            c = distanceLine(self.ex, self.ey, self.circlex+self.r, self.circley)
            self.startAngle = (angleDegrees(a, b, c)) * 16      # in 16ths of a degree
            self.startAngleR = radians(self.startAngle/16)            # in radians
            
#        print("start angle 16 {}".format(self.startAngle))
#        print("start angle degrees {}".format(self.startAngle/16))
#        print("centery {} ey {}".format(self.circley, self.ey))
        # calculate sweep angle of the arc
        a1 = distanceLine(self.circlex,  self.circley, self.sx, self.sy)
        b1 = distanceLine(self.circlex, self.circley, self.ex, self.ey)
        c1 = d
        self.sweepAngle = (angleDegrees(a1, b1, c1) * 16)    # in 16ths of a degree
        self.sweepAngleR = radians(self.sweepAngle/16)   # in radians
        
#        print("sweep angle 16 {}".format(self.sweepAngle))
#        print("sweep angle deg {}".format(self.sweepAngle/16))
        
        # compute the mid point on the arc for the text 
        self.mx = self.circlex + (self.r * cos(self.startAngleR + (self.sweepAngleR/2) ))
        self.my = self.circley - (self.r * sin(self.startAngleR + (self.sweepAngleR/2) ))        

        # compute the arrow base center point 
        arrowLen = 5    # this is half the distance of the arrowhead base which determines how wide the arrow head is
        # compute a point on the arc that is a short distance away from the edge of the ellipse.  this is the base of the arrow head        
        aRadians = 10.0 / self.r    # this determines how long the arrow head is
        self.ax = self.circlex + (self.r * cos(self.startAngleR + aRadians ))
        self.ay = self.circley - (self.r * sin(self.startAngleR + aRadians ))      
        # compute the arrow base corners
        if self.ex == self.ax:
            self.ax = self.ax + .001
        # get the slope of the line from the ellipse to the arrowhead base
        slope = (self.ey - self.ay)/(self.ex - self.ax)
        if slope == 1.0:
            slope = 1.001
        # get the perpindicular slope
        perpSlope = -1.0 / slope
        perpSlopeSquared = perpSlope * perpSlope
        # get first arrowhead base corner
        ab1dx = (arrowLen / sqrt(1 + (perpSlopeSquared)))
        ab1dy = ab1dx * perpSlope
        self.b1x = self.ax + ab1dx
        self.b1y = self.ay + ab1dy
        # get 2nd arrowhead base corner
        ab2dx = (arrowLen / sqrt(1 + (perpSlopeSquared)))
        ab2dy = ab2dx * perpSlope
        self.b2x = self.ax - ab2dx
        self.b2y = self.ay - ab2dy        
        
        # this rectangle surrounds the entire ellipse used to draw the arc
        self.relRect = QRectF(self.circlex - (self.r), self.circley - (self.r), self.r*2, self.r*2)
        
        
    def paint(self, *args, **kwargs):
        '''Over-ride the paint method to draw the arc'''
        myPainter = args[0]
        myPainter.save()
        myPainter.setRenderHint(QPainter.Antialiasing, True)
        myPainter.setPen(self.pen)
        # force white, not sure how it got set to yellow
        self.brush.setColor(QColor(Qt.white))
        myPainter.setBrush(self.brush)
        # draw the connecting arc
        # drawArc is a method in the QPainter class, documented in the pyqt docs 
        # This takes the self.relRect argument which is the bounding rectangle
        # self.startAngle which is just where the arc starts, and self.sweepAngle which is how far the arc actually goes
        myPainter.drawArc(self.relRect, self.startAngle, self.sweepAngle)

        # draw the "arrow head base" which is just a circle for debugging
#        myPainter.drawEllipse(QPointF(self.ax, self.ay), 5.0, 5.0)
#        myPainter.drawEllipse(QPointF(self.b1x, self.b1y), 1.0, 1.0)
#        myPainter.drawEllipse(QPointF(self.b2x, self.b2y), 1.0, 1.0)
#        myPainter.drawEllipse(QPointF(self.ax, self.ay), 1.0, 1.0)

        # draw the  midpoint circle where text will go
#        myPainter.drawEllipse(QPointF(self.mx, self.my), 5.0, 5.0)
        
        # for debugging, draw the bounding rect and full ellipse
#        myPainter.drawRect(self.relRect)
#        myPainter.drawEllipse(self.circlex - (self.r), self.circley - (self.r),self.r*2, self.r *2)
#        myPainter.drawEllipse(QPointF(self.circlex, self.circley), 5, 5)
        
        if self.isSelected():
#            print("rel selected")
            pass
            
        myPainter.restore()
    
    def boundingRect(self, ):
        '''Over-ride the boundingRect method to provide the QRectF that describes the boundary of the qGraphicsItem '''
        return self.relRect
    


class RelationItem():
    ''' This represents one relationship on the diagram.
        This class creates the arc graphics item and the text graphics item and draws them on the scene.
        The RelationInstance class manages reading and writing the relationship to Neo4j
        '''    
    def __init__(self, scene, relationInstance=None):
        
        self.scene = scene
        self.model = self.scene.parent.model
        self.diagramType = "Instance Relationship"
        self.logMsg = None
        # self.relationInstance should have been called self.itemInstance to be consistent
        # with NodeItem.  so we'll set it to none and someday fix this.
        self.itemInstance = None 
        self.relationInstance = relationInstance
        self.startNZID = self.relationInstance.startNZID
        self.endNZID = self.relationInstance.endNZID
        # get the NodeItem objects for the start and end nodes
        self.startNode = self.scene.parent.itemDict[self.startNZID]
        self.endNode = self.scene.parent.itemDict[self.endNZID]

        self.numRels = self.scene.parent.numRels(self.relationInstance.startNZID, self.relationInstance.endNZID)
#        print("numRels:{}".format(self.numRels))
        self.lineType = None
#        print("num rels{}".format(str(self.numRels)))
        # initialize the two qgraphicsitems needed to draw a relationship to None
        self.IRel = None
        self.IRtext = None  
        self.bunnyEar = None
        self.endDot = None
        self.arrowHead = None
        self.TAline1 = None
        self.TAline2 = None
        self.debugTriangle = None
        self.drawRelationship()

        
    def name(self, ):
        return self.relationInstance.NZID 
        
    def NZID(self, ):
        return self.relationInstance.NZID      
        
    def getFormat(self, ):
        '''
        determine if the rel instance has a template format or should use the project default format
        '''
        # get the default
        self.relFormat = IRelFormat(formatDict=self.model.modelData["IRformat"])
        # get a custom template format if there is one
        if not self.relationInstance.relTemplate is None:
            index, relTemplateDict = self.model.getDictByName(topLevel="Relationship Template",objectName=self.relationInstance.relTemplate)
            if not relTemplateDict is None:
                self.instanceRelFormatDict = relTemplateDict.get("IRformat", None)
                if not self.instanceRelFormatDict is None:
                    self.relFormat = IRelFormat(formatDict=self.instanceRelFormatDict) 

    def getNodeId(self):
        '''return the rel id for the relationship from the IREL or bunnyear graphic item - which ever it is
        '''
        if not self.IRel is None:
            nodeID = self.IRel.data(NODEID)
        elif not self.bunnyEar is None:
            nodeID = self.bunnyEar.data(NODEID)
        else:
            nodeID = None
        return nodeID
        
    def clearItem(self, ):

        if (not self.IRel is None and not self.IRel.scene() is None):
            self.IRel.scene().removeItem(self.IRel)        
        if (not self.IRtext is None and not self.IRtext.scene() is None):
            self.IRtext.scene().removeItem(self.IRtext)     
        if (not self.bunnyEar is None and not self.bunnyEar.scene() is None):
            self.bunnyEar.scene().removeItem(self.bunnyEar)                
        if (not self.endDot is None and not self.endDot.scene() is None):
            self.endDot.scene().removeItem(self.endDot)        
        if (not self.arrowHead is None and not self.arrowHead.scene() is None):
            self.arrowHead.scene().removeItem(self.arrowHead)  
        if (not self.TAline2 is None and not self.TAline2.scene() is None):
            self.TAline2.scene().removeItem(self.TAline2)  
        if (not self.TAline1 is None and not self.TAline1.scene() is None):
            self.TAline1.scene().removeItem(self.TAline1)  
#        if (not self.debugTriangle is None and not self.debugTriangle.scene() is None):
#            self.debugTriangle.scene().removeItem(self.debugTriangle)                

    def drawIt(self, ):
        '''
        for consistency, drawIt should be used instead of drawRelationship
        '''
        self.drawRelationship()
        
    def drawRelationship(self, ):
        # relationship is between two different nodes
        if self.startNZID != self.endNZID:
            #  set the line type if it hasn't been determined yet.  This happens on first draw
            if self.lineType is None:
                if self.scene.parent.anyRels(self.relationInstance.startNZID, self.relationInstance.endNZID):
                    self.lineType = CURVE
                else:
                    self.lineType = STRAIGHT
            # now draw the line or arc
            if self.lineType == CURVE:
                self.drawRel()
            else:
                self.drawStraightRel()
        # relationship is between the same node
        if self.startNZID == self.endNZID:
            self.drawBunnyEars()        
        
    def drawBunnyEars(self, ):
        # force the rel instance to update its values in case it has been updated from another diagram or the tree view
        self.relationInstance.reloadDictValues()
        # get the format in case it changed
        self.getFormat()
        # if the arc and text graphics items already exist on the scene then delete them
        self.clearItem()
        # draw the relationship arc
        pen = self.relFormat.pen()
        brush = self.relFormat.brush()
        brush.setColor(QColor(Qt.white))
        # create an ellipse like the startNode
        x = self.startNode.INode.sceneBoundingRect().center().x()
        y = self.startNode.INode.sceneBoundingRect().center().y()
        w = self.startNode.INode.sceneBoundingRect().width()/2.0
        h = self.startNode.INode.sceneBoundingRect().height()/2.0
        myEllipse = Ellipse(x, y, w, h)    
        # move the bunny ears around the ellipse until we run out of room
        startDegree = 360 - (self.numRels * 40)
        if startDegree < 40:
            startDegree = 40
            
        startPoint = myEllipse.pointFromAngle(radians(startDegree))
        endPoint = myEllipse.pointFromAngle(radians(startDegree-35))
        lineMidPoint = centerLine (startPoint[0], startPoint[1], endPoint[0], endPoint[1])
        lineDist = distanceLine (startPoint[0], startPoint[1], endPoint[0], endPoint[1])
        circleRad = lineDist/2.0

        self.bunnyEar = QGraphicsEllipseItem(QRectF(lineMidPoint[0]-circleRad,lineMidPoint[1]-circleRad,circleRad*2,circleRad*2), parent=None)
        self.bunnyEar.setZValue(RELATIONLAYER)
        self.bunnyEar.setBrush(brush)
        self.bunnyEar.setPen(pen)
        self.bunnyEar.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.bunnyEar.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True) 
        self.bunnyEar.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.bunnyEar.setSelected(False)
        
        # create arrowhead
        self.circlex = lineMidPoint[0]
        self.circley = lineMidPoint[1]
        
#        self.circleDot = QGraphicsEllipseItem(QRectF(self.circlex-1.5,self.circley-1.5,3, 3), parent=None)
#        self.circleDot.setZValue(NODELAYER)
#        self.scene.addItem(self.circleDot) 
#        self.pointDot = QGraphicsEllipseItem(QRectF(endPoint[0]-1.5,endPoint[1]-1.5,3, 3), parent=None)
#        self.pointDot.setZValue(NODELAYER)
#        self.scene.addItem(self.pointDot) 
        
        # compute the arrow base center point 
        arrowLen = 5    # this is half the distance of the arrowhead base which determines how wide the arrow head is
        # compute a point on the arc that is a short distance away from the edge of the ellipse.  this is the base of the arrow head        

        # get the slope of the line from the start point to the end point on the node ellipse
        if endPoint[0] == startPoint[0]:
            startPoint[0] = startPoint[0] + .001
#        slope1 = (startPoint[1] - endPoint[1])/(startPoint[0] - endPoint[0])
        slope1 = (endPoint[1] - startPoint[1] )/(endPoint[0] - startPoint[0])
        if slope1 == 1.0:
            slope1 = 1.001
        slope1Squared = slope1 * slope1
        perpSlope1 =  -1.0 / slope1
        perpSlope1Squared = perpSlope1 * perpSlope1
#        print("numrels:{} startDegree:{} radius:{} slope:{} perpslope:{}".format(self.numRels, startDegree, circleRad, slope1,  perpSlope1))
        # now find a point on the line tangent to the point on the bunny ear circle.  This is the base of the arrow
#        ax = (arrowLen / sqrt(1 + (perpSlope1Squared)))
#        ay = ax * perpSlope1   
        if lineMidPoint[0] < x:
            baseX = endPoint[0] - (arrowLen / sqrt(1 + (perpSlope1Squared)))
            baseY = endPoint[1] - ((arrowLen / sqrt(1 + (perpSlope1Squared))) * perpSlope1 )
        else:
            baseX = endPoint[0] + (arrowLen / sqrt(1 + (perpSlope1Squared)))
            baseY = endPoint[1] + ((arrowLen / sqrt(1 + (perpSlope1Squared))) * perpSlope1 )
#        print("ax:{} ay:{} slope1:{} perslope1:{}".format(ax, ay, slope1, perpSlope1))
#        self.anchorDot = QGraphicsEllipseItem(QRectF(baseX-1.5,baseY-1.5,3, 3), parent=None)
#        self.anchorDot.setZValue(NODELAYER)
#        self.scene.addItem(self.anchorDot) 
        
        # get first arrowhead base corner
        ab1dx = (arrowLen / sqrt(1 + (slope1Squared)))
        ab1dy = ab1dx * slope1
        self.b1x = baseX + ab1dx
        self.b1y = baseY + ab1dy
        # get 2nd arrowhead base corner
        ab2dx = (arrowLen / sqrt(1 + (slope1Squared)))
        ab2dy = ab2dx * slope1
        self.b2x = baseX - ab2dx
        self.b2y = baseY - ab2dy        

        
#        # calculate the arrowhead points
#        cx = self.endNode.INode.sceneBoundingRect().center().x()
#        cy = self.endNode.INode.sceneBoundingRect().center().y()
#        self.calcArrowHead(QPointF(cx, cy), QPointF( endPoint[0], endPoint[1]), bunnyEars=True)


        #create an empty polygon
        arrowPolygon = QPolygonF()
#        # add arrowhead points
#        arrowPolygon.append(QPointF(self.ah1x, self.ah1y))
#        arrowPolygon.append(QPointF(endPoint[0], endPoint[1]))
#        arrowPolygon.append(QPointF(self.ah2x, self.ah2y))
        # add arrowhead points
        arrowPolygon.append(QPointF(self.b1x, self.b1y))
        arrowPolygon.append(QPointF(endPoint[0], endPoint[1]))
        arrowPolygon.append(QPointF(self.b2x, self.b2y))        
        
        self.arrowHead = QGraphicsPolygonItem(arrowPolygon, parent=None, )
        self.arrowHead.setZValue(RELATIONLAYER)
        self.arrowHead.setBrush(brush)
        self.arrowHead.setPen(pen)
        self.arrowHead.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.arrowHead.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True) 
        self.arrowHead.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.arrowHead.setSelected(False)
        
        # set data in the bunnyEar object
        self.bunnyEar.setData(NODEID, self.relationInstance.NZID) 
        self.bunnyEar.setData(ITEMTYPE, RELINSTANCEARC)
        self.scene.addItem(self.bunnyEar) 
        self.scene.addItem(self.arrowHead) 

        # calculate position  of text
        bunnyEllipse = Ellipse(lineMidPoint[0],lineMidPoint[1],circleRad,circleRad)  
        # use the same midpoint angle as the bunny ear start and end point
        bunnyMidPoint = bunnyEllipse.pointFromAngle(radians(startDegree-17.5))
        # draw the text
        self.drawText(bunnyMidPoint[0], bunnyMidPoint[1], startPoint[0], startPoint[1], endPoint[0], endPoint[1])
#        self.anchorDot = QGraphicsEllipseItem(QRectF(bunnyMidPoint[0]-1.5,bunnyMidPoint[1]-1.5,3, 3), parent=None)
#        self.anchorDot.setZValue(NODELAYER)
#        self.scene.addItem(self.anchorDot) 

    def drawStraightRel(self):
#        print("draw straight rel")
        # force the rel instance to update its values in case it has been updated from another diagram or the tree view
        self.relationInstance.reloadDictValues()
        # get the format in case it changed
        self.getFormat()
        # if the arc and text graphics items already exist on the scene then delete them
        self.clearItem()
        # draw the relationship arc
        pen = self.relFormat.pen()
        brush = self.relFormat.brush()
    
        # get the centerpoint of the end node
        cx = self.endNode.INode.sceneBoundingRect().center().x()
        cy = self.endNode.INode.sceneBoundingRect().center().y()
        
        # get the start and end points of the line
        esx, esy, eex, eey = self.calcLine3()
        # create the arc qgraphicsitem
        self.IRel = QGraphicsLineItem(esx, esy, eex, eey, parent=None) 
        arrowLine = self.IRel
        # text location 
        tx = self.IRel.line().pointAt(.5).x()
        ty = self.IRel.line().pointAt(.5).y()                   

        # draw the relationship line
        pen = self.relFormat.pen()      
        # configure the lines and add them to the scene
        self.IRel.setPen(pen)
        self.IRel.setZValue(RELATIONLAYER)   
        self.IRel.setData(NODEID, self.relationInstance.NZID) 
        self.IRel.setData(ITEMTYPE, RELINSTANCEARC)
        self.IRel.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.IRel)   

        # line arrowhead
        # compute the arrow base center point 
        arrowLen = 5    # this is half the distance of the arrowhead base which determines how wide the arrow head is
        # compute a point on the arc that is a short distance away from the edge of the ellipse.  this is the base of the arrow head        


        ax =  self.IRel.line().pointAt(1-(10.0/self.IRel.line().length())).x()
        ay = self.IRel.line().pointAt(1-(10.0/self.IRel.line().length())).y()
        # compute the arrow base corners
        if eex == ax:
            ax = ax + .001
        # get the slope of the line from the ellipse to the arrowhead base
        slope = (eey - ay)/(eex - ax)
        if slope == 1.0:
            slope = 1.001
        # get the perpindicular slope
        perpSlope = -1.0 / slope
        perpSlopeSquared = perpSlope * perpSlope
        # get first arrowhead base corner
        ab1dx = (arrowLen / sqrt(1 + (perpSlopeSquared)))
        ab1dy = ab1dx * perpSlope
        self.b1x = ax + ab1dx
        self.b1y = ay + ab1dy
        # get 2nd arrowhead base corner
        ab2dx = (arrowLen / sqrt(1 + (perpSlopeSquared)))
        ab2dy = ab2dx * perpSlope
        self.b2x = ax - ab2dx
        self.b2y = ay - ab2dy        


        #create an empty polygon
        arrowPolygon = QPolygonF()
        # add arrowhead points
        arrowPolygon.append(QPointF(self.b1x, self.b1y))
        arrowPolygon.append(QPointF(eex, eey))
        arrowPolygon.append(QPointF(self.b2x, self.b2y))
        
        self.arrowHead = QGraphicsPolygonItem(arrowPolygon, parent=None, )
        self.arrowHead.setZValue(RELATIONLAYER)
        self.arrowHead.setBrush(brush)
        self.arrowHead.setPen(pen)
        self.arrowHead.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.arrowHead.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True) 
        self.arrowHead.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.arrowHead.setSelected(False)        
        self.scene.addItem(self.arrowHead) 
        
        # draw the text
        self.drawText(tx, ty, esx, esy, eex, eey)
        
    def drawRel(self, ):
        # draw the curved relationship line
#        print("draw curve rel")
        # force the rel instance to update its values in case it has been updated from another diagram or the tree view
        self.relationInstance.reloadDictValues()
        # get the format in case it changed
        self.getFormat()
        # if the arc and text graphics items already exist on the scene then delete them
        self.clearItem()
        # draw the relationship arc
        pen = self.relFormat.pen()
        brush = self.relFormat.brush()
        
        # METHOD 1 use ellipse center points
#        # get the center points of the qgraphicellipses
#        sx = self.startNode.INode.sceneBoundingRect().center().x()
#        sy = self.startNode.INode.sceneBoundingRect().center().y()
#        ex = self.endNode.INode.sceneBoundingRect().center().x()
#        ey = self.endNode.INode.sceneBoundingRect().center().y()
#        # if the x's or y's are equal offset one slightly to avoid divide by zero errors
#        if sx == ex:
#            ex = ex + .001
#        if sy == ey:
#            ey = ey + .001        
#        self.IRel = RelArc(parent=None, sx=sx, sy=sy, ex=ex, ey=ey, pen=pen, brush=brush, numRels=self.numRels)
        
        # METHOD 2 use points on the ellipse
#        esx, esy, eex, eey = self.calcLine()
#        self.IRel = RelArc(parent=None, sx=esx, sy=esy, ex=eex, ey=eey, pen=pen, brush=brush, numRels=self.numRels)

        # METHOD 3 use regularly spaced endpoints on the ellipse
        # get the centerpoint of the end node
        cx = self.endNode.INode.sceneBoundingRect().center().x()
        cy = self.endNode.INode.sceneBoundingRect().center().y()
        

        # get the start and end points of the arc 
        esx, esy, eex, eey = self.calcLine2()
        # create the arc qgraphicsitem
        self.IRel = RelArc(parent=None, sx=esx, sy=esy, ex=eex, ey=eey, cx=cx, cy=cy, pen=pen, brush=brush, numRels=self.numRels)

        #create an empty polygon
        arrowPolygon = QPolygonF()
        # add arrowhead points
        arrowPolygon.append(QPointF(self.IRel.b1x, self.IRel.b1y))
        arrowPolygon.append(QPointF(eex, eey))
        arrowPolygon.append(QPointF(self.IRel.b2x, self.IRel.b2y))
        
        self.arrowHead = QGraphicsPolygonItem(arrowPolygon, parent=None, )
        self.arrowHead.setZValue(RELATIONLAYER)
        self.arrowHead.setBrush(brush)
        self.arrowHead.setPen(pen)
        self.arrowHead.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.arrowHead.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True) 
        self.arrowHead.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.arrowHead.setSelected(False)
        
        # set data in the RelLine object
        self.IRel.setData(NODEID, self.relationInstance.NZID) 
        self.IRel.setData(ITEMTYPE, RELINSTANCEARC)
        # add the RelLine object to the scene
        self.scene.addItem(self.IRel) 
        # add arrowhead to the scene
        self.scene.addItem(self.arrowHead) 
        # draw the text
        self.drawText(self.IRel.mx, self.IRel.my, esx, esy, eex, eey)

        
    def drawText(self, mx, my, esx, esy, eex, eey):
        # mx,my is the center point of the arc
        # esx,esy is the start point of the arc
        # eex,eey is the end point of the arc
        
        # get the center points of the node qgraphicellipses
        sx = self.startNode.INode.sceneBoundingRect().center().x()
        sy = self.startNode.INode.sceneBoundingRect().center().y()
        sh = self.startNode.INode.sceneBoundingRect().height()
        ex = self.endNode.INode.sceneBoundingRect().center().x()
        ey = self.endNode.INode.sceneBoundingRect().center().y()
        eh = self.endNode.INode.sceneBoundingRect().height()
        # if the x's or y's are equal offset one slightly to avoid divide by zero errors
        if sx == ex:
            ex = ex + .001
        if sy == ey:
            ey = ey + .001        
        # draw the text 
#        self.IRtext = QGraphicsTextItem(self.relationInstance.relName, parent=None)
        self.IRtext = RelText(parent=None)
#        self.IRtext.setZValue(RELATIONLAYER)
#        self.IRtext.setFlag(QGraphicsItem.ItemIsMovable, True) 
#        self.IRtext.setFlag(QGraphicsItem.ItemIsSelectable, True) 
#        self.IRtext.setSelected(True)
#        self.IRtext.setAcceptHoverEvents(True)
        self.IRtext.setData(NODEID, self.relationInstance.NZID) 
        self.IRtext.setData(ITEMTYPE, RELINSTANCETEXT)
        self.IRtext.setHtml(self.genRelHTML())
        
        #calculate rotation angle
        adj = abs(esx-eex)
        opp = abs(esy-eey)
        OOA = opp/adj
        rotateAnglerad = (atan(OOA))
        rotateAngledeg = degrees(atan(OOA))
        
        # get the height and width of the text graphics item
        th = self.IRtext.boundingRect().height()
        tw  = self.IRtext.boundingRect().width()
        
        # position the relation name text centered on the arc centerpoint
        if self.startNZID != self.endNZID:
#            esx, esy, eex, eey
            if esy >= eey and esx <= eex:
                # end node is above and to the right 
                self.IRtext.setRotation((360 - rotateAngledeg))
                xoffset = (tw/2) * cos(rotateAnglerad)
                yoffset = (tw/2) * sin(rotateAnglerad)                
                self.IRtext.setPos(QPointF(mx - xoffset, my + yoffset ))
            
            elif esy <= eey and esx <= eex:
                # end node is below and to the right
                self.IRtext.setRotation(rotateAngledeg)
                xoffset = (tw/2) * (cos(rotateAnglerad))
                yoffset = (tw/2) * (sin(rotateAnglerad))
                self.IRtext.setPos(QPointF(mx - xoffset, my - yoffset ))
            
            elif esy >= eey and esx >= eex:
                # end node is above and to the left
                self.IRtext.setRotation(rotateAngledeg)
                xoffset = (tw/2) * (cos(rotateAnglerad))
                yoffset = (tw/2) * (sin(rotateAnglerad))
                self.IRtext.setPos(QPointF(mx - xoffset, my - yoffset ))       
                
            elif esy <= eey and esx >= eex:
                # end node is below and to the left
                self.IRtext.setRotation((360 - rotateAngledeg))
                xoffset = (tw/2) * cos(rotateAnglerad)
                yoffset = (tw/2) * sin(rotateAnglerad)                
                self.IRtext.setPos(QPointF(mx - xoffset, my + yoffset ))
                
            # this shouldn't happen      
            else:
                xoffset = (tw/2)
                yoffset = (tw/2)             
                self.IRtext.setPos(QPointF(mx, my ))
                
#            print("tw {} xoffset {} yoffset {} angle {}".format(tw,  xoffset, yoffset, rotateAngledeg)) 
            
        elif self.startNZID == self.endNZID:
            if mx > sx:
                self.IRtext.setPos(QPointF(mx, my - (th) ))
            if mx < sx:
                self.IRtext.setPos(QPointF(mx - tw, my - (th) ))
        else:
            # this shouldn't happen
            self.IRtext.setPos(QPointF(mx, my ))   

        self.scene.addItem(self.IRtext) 
        
    def updateText(self, ):
        # force the node instance to update its values in case it has been updated from another diagram or the tree view
        self.relationInstance.reloadDictValues()
#        self.IRtext.setPlainText(self.relationInstance.relName)
        self.IRtext.setHtml(self.genRelHTML())
    
    def genRelHTML(self):
        '''generate html to display the relationship type
        '''
        prefix = '<html><body>'
        suffix = "</body></html>"
        myHTML = ('{}<p><font size="1"> [{}]</font></p>{}'.format(prefix, self.relationInstance.relName, suffix))
        return myHTML
        
#    def calcLine(self, ):
#        '''calculate the points on the two ellipses to draw a straight line through their centers'''
#        self.startNodeX = self.startNode.INode.sceneBoundingRect().center().x()
#        self.startNodeY = self.startNode.INode.sceneBoundingRect().center().y()
#        self.endNodeX = self.endNode.INode.sceneBoundingRect().center().x()
#        self.endNodeY = self.endNode.INode.sceneBoundingRect().center().y()   
#        
#        self.distanceX = abs(self.startNodeX - self.endNodeX) + .001
#        self.distanceY = abs(self.startNodeY - self.endNodeY) + .001
#        temp = (pow(self.distanceX,2) + pow(self.distanceY,2)) - (2 * self.distanceX * self.distanceY * cos(radians(90)))
#        self.distanceXY = sqrt(temp)
#        a = self.distanceX
#        b = self.distanceY
#        c = self.distanceXY
##        angA = angle(a,b,c)
##        angB = angle(b,c,a)
#        angC = angleDegrees(c,a,b)
#        
#        if self.endNodeX == self.startNodeX:
#            self.endNodeX = self.endNodeX + .001
#        if self.endNodeY == self.startNodeY:
#            self.endNodeY = self.endNodeY + .001
#        
#        if self.endNodeX > self.startNodeX and self.endNodeY > self.startNodeY:
#                startangle = angC
#                endangle = 180 + angC
#        elif self.endNodeX < self.startNodeX and self.endNodeY > self.startNodeY:
#                startangle = 180 - angC
#                endangle = 360 - angC
#        elif self.endNodeX < self.startNodeX and self.endNodeY < self.startNodeY:
#                startangle = 180 + angC
#                endangle = angC
#        elif self.endNodeX > self.startNodeX and self.endNodeY < self.startNodeY:
#                startangle = 360 - angC
#                endangle = 180 - angC
#                
#        #print("angA: {} angleB: {} angleC: {} startangle: {}".format(angA, angB, angC, startangle))
#        aa = self.startNode.INode.boundingRect().width()/2.0
#        bb = self.startNode.INode.boundingRect().height()/2.0        
#        sn = Ellipse(self.startNodeX, self.startNodeY, aa, bb)
#        sx, sy = sn.pointFromAngle(radians(startangle))
#        cc = self.endNode.INode.boundingRect().width()/2.0
#        dd = self.endNode.INode.boundingRect().height()/2.0                
#        en = Ellipse(self.endNodeX, self.endNodeY, cc, dd)  #need to calc width/height of end node.
#        ex, ey = en.pointFromAngle(radians(endangle))
#        #print("sx {} - sy {} - ex {} - ey {}".format(sx,sy,ex,sy))
#        return sx, sy, ex, ey

    def calcLine2(self, ):
        '''calculate the point on the start and end node ellipse for an arc
        '''
        # get centerpoints of the two nodes
        self.startNodeX = self.startNode.INode.sceneBoundingRect().center().x()
        self.startNodeY = self.startNode.INode.sceneBoundingRect().center().y()
        self.endNodeX = self.endNode.INode.sceneBoundingRect().center().x()
        self.endNodeY = self.endNode.INode.sceneBoundingRect().center().y()   
        
        self.distanceX = abs(self.startNodeX - self.endNodeX) + .001
        self.distanceY = abs(self.startNodeY - self.endNodeY) + .001
        temp = (pow(self.distanceX,2) + pow(self.distanceY,2)) - (2 * self.distanceX * self.distanceY * cos(radians(90)))
        self.distanceXY = sqrt(temp)
        a = self.distanceX
        b = self.distanceY
        c = self.distanceXY
#        angA = angle(a,b,c)
#        angB = angle(b,c,a)
        angC = angleDegrees(c,a,b)
#        print("angC {}".format(angC))
        
        if self.endNodeX == self.startNodeX:
            self.endNodeX = self.endNodeX + .001
        if self.endNodeY == self.startNodeY:
            self.endNodeY = self.endNodeY + .001
        
        # adjust starting and ending points based on the number of rels between the node, if more than 7 in the same direction just start stacking them one on top of the other.
        if self.numRels > 6:
            adjustDegree = (7) * 10
        else:
            adjustDegree = (self.numRels+1) * 10
            
        if self.endNodeX > self.startNodeX and self.endNodeY > self.startNodeY:
                startangle = angC - adjustDegree
                endangle = 180 + angC + adjustDegree
        elif self.endNodeX < self.startNodeX and self.endNodeY > self.startNodeY:
                startangle = 180 - angC - adjustDegree
                endangle = 360 - angC + adjustDegree
        elif self.endNodeX < self.startNodeX and self.endNodeY < self.startNodeY:
                startangle = 180 + angC - adjustDegree
                endangle = angC + adjustDegree
        elif self.endNodeX > self.startNodeX and self.endNodeY < self.startNodeY:
                startangle = 360 - angC - adjustDegree
                endangle = 180 - angC + adjustDegree
                
#        print("adjust: {}startangle: {} endangle: {}".format(adjustDegree, startangle, endangle))
        aa = self.startNode.INode.boundingRect().width()/2.0
        bb = self.startNode.INode.boundingRect().height()/2.0        
        sn = Ellipse(self.startNodeX, self.startNodeY, aa, bb)
        sx, sy = sn.pointFromAngle(radians(startangle))
        cc = self.endNode.INode.boundingRect().width()/2.0
        dd = self.endNode.INode.boundingRect().height()/2.0                
        en = Ellipse(self.endNodeX, self.endNodeY, cc, dd)  #need to calc width/height of end node.
        ex, ey = en.pointFromAngle(radians(endangle))
        #print("sx {} - sy {} - ex {} - ey {}".format(sx,sy,ex,sy))
        return sx, sy, ex, ey
        
    def calcLine3(self, ):
        '''calculate the point on the start and end node ellipse for a straight line
        '''
        # get centerpoints of the two nodes
        self.startNodeX = self.startNode.INode.sceneBoundingRect().center().x()
        self.startNodeY = self.startNode.INode.sceneBoundingRect().center().y()
        self.endNodeX = self.endNode.INode.sceneBoundingRect().center().x()
        self.endNodeY = self.endNode.INode.sceneBoundingRect().center().y()   
        
        self.distanceX = abs(self.startNodeX - self.endNodeX) + .001
        self.distanceY = abs(self.startNodeY - self.endNodeY) + .001
        temp = (pow(self.distanceX,2) + pow(self.distanceY,2)) - (2 * self.distanceX * self.distanceY * cos(radians(90)))
        self.distanceXY = sqrt(temp)
        a = self.distanceX
        b = self.distanceY
        c = self.distanceXY
#        angA = angle(a,b,c)
#        angB = angle(b,c,a)
        angC = angleDegrees(c,a,b)
#        print("angC {}".format(angC))
        
        if self.endNodeX == self.startNodeX:
            self.endNodeX = self.endNodeX + .001
        if self.endNodeY == self.startNodeY:
            self.endNodeY = self.endNodeY + .001
        
#        # adjust starting and ending points based on the number of rels between the node, if more than 7 in the same direction just start stacking them one on top of the other.
#        if self.numRels > 6:
#            adjustDegree = (7) * 10
#        else:
#            adjustDegree = (self.numRels+1) * 10

        adjustDegree = 0    
        if self.endNodeX > self.startNodeX and self.endNodeY > self.startNodeY:
                startangle = angC - adjustDegree
                endangle = 180 + angC + adjustDegree
        elif self.endNodeX < self.startNodeX and self.endNodeY > self.startNodeY:
                startangle = 180 - angC - adjustDegree
                endangle = 360 - angC + adjustDegree
        elif self.endNodeX < self.startNodeX and self.endNodeY < self.startNodeY:
                startangle = 180 + angC - adjustDegree
                endangle = angC + adjustDegree
        elif self.endNodeX > self.startNodeX and self.endNodeY < self.startNodeY:
                startangle = 360 - angC - adjustDegree
                endangle = 180 - angC + adjustDegree
                
#        print("adjust: {}startangle: {} endangle: {}".format(adjustDegree, startangle, endangle))
        aa = self.startNode.INode.boundingRect().width()/2.0
        bb = self.startNode.INode.boundingRect().height()/2.0        
        sn = Ellipse(self.startNodeX, self.startNodeY, aa, bb)
        sx, sy = sn.pointFromAngle(radians(startangle))
        cc = self.endNode.INode.boundingRect().width()/2.0
        dd = self.endNode.INode.boundingRect().height()/2.0                
        en = Ellipse(self.endNodeX, self.endNodeY, cc, dd)  #need to calc width/height of end node.
        ex, ey = en.pointFromAngle(radians(endangle))
        #print("sx {} - sy {} - ex {} - ey {}".format(sx,sy,ex,sy))
        return sx, sy, ex, ey
                
#    def moveRelationshipLine(self, ):
#        self.drawRelationship()

    def getObjectDict(self, ):
        objectDict = {}
        objectDict["NZID"] = self.relationInstance.NZID
        objectDict["diagramType"] = self.diagramType
        return objectDict
        

