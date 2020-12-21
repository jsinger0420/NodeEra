# -*- coding: utf-8 -*-
'''
RelationTemplateItem manages a relationship on a Template Diagram
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software``
'''
import uuid

from PyQt5.QtCore import QPointF, QRectF, Qt, QLineF
from PyQt5.QtWidgets import QGraphicsItem,   QGraphicsTextItem, QGraphicsLineItem , QGraphicsEllipseItem
#from forms.IRelFormatDlg import  IRelFormat
from forms.TRelFormatDlg import TRelFormat

# enum for line type
ELBOW, STRAIGHT = range(2)

# enum for horizontal and vertical orientation - used by elbows line drawing
#LOWER, HIGHER, ALONGSIDE, RIGHT, LEFT, ABOVE, BELOW = range(7)
RIGHT, LEFT, LOWER, HIGHER, ALONGSIDE, ABOVE, BELOW = range(7)

# enum for node template side - used by straight line drawing
TOP, R, BOTTOM, L = range(4)
# enum for orientation - used by straight line drawing
#LEFT, ABOVE, RIGHT, BELOW = range(4)
RIGHT, LEFT, ABOVE, BELOW = range(4)

# enum for z value graphics item stacking - higher numbered items cover lower numbered items
PAGELAYER = 0
RELATIONLAYER = 1
NODELAYER = 2
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
RELINSTANCELINE = 6
RELTEMPLATETEXT = 7
RELTEMPLATELINE = 8

class RelationTemplateItem():
    ''' 
    This manages one relationship template on a diagram.
    '''    
    def __init__(self, scene, relationTemplateDict=None, NZID=None, startNodeItem=None, endNodeItem=None):
        '''
        NZID - the unique id of this relationtemplate on the diagram
        startNodeItem - the NodeTemplateItem object on the diagram that is the start node for this relationship
        endNodeItem   - the NodeTemplateItem object on the diagram that is the end node for this relationship
        relationTemplateDict - the object dictionary for the relation template this diagram item represents
        scene - the QGraphicsScene object that is displaying the diagram
        '''
        self.scene = scene
        self.model = self.scene.parent.model
        self.relationTemplateDict = relationTemplateDict
        self.startNodeItem = startNodeItem
        self.endNodeItem = endNodeItem        
        self.diagramType = "Relationship Template"
        self.logMsg = None

        # assign a unique key if it doesn't already have one
        if NZID == None:
            self.NZID = str(uuid.uuid4())
        else:
            self.NZID = NZID
        
        # create a relationTemplateDict if it's new
        if self.relationTemplateDict == None:
            self.relationTemplateDict = self.model.newRelTemplateDict()

        self.startNZID  = None      
        if not startNodeItem is None:
            self.startNZID = self.startNodeItem.NZID
            
        self.endNZID = None      
        if not endNodeItem is None:
            self.endNZID = self.endNodeItem.NZID

        # get the number that this relationship is in the list of all relationships between the start node and end node, i.e 1st, 2nd, 3rd
        self.relNum = self.scene.parent.addTRelationship(self)

        # initialize the qgraphicsitems needed to draw a relationship to None
#        self.bullet = None
        self.TRline1 = None
        self.TRline2 = None   
        self.TRline3 = None
        self.TRline4 = None
        self.TRtext = None
        self.TRFromCardinality = None
        self.TRToCardinality = None
        self.TAline1 = None
        self.TAline2 = None
        
        self.test1Line = None
        
        # track the inbound and outbound side and slot
        self.inboundSide = None
        self.inboundPoint = None
        self.outboundSide = None
        self.outboundPoint = None
        
        
    def getName(self, ):
        return self.relationTemplateDict.get("name", "")   
    
    def name(self, ):
        return self.relationTemplateDict.get("name", "")   
    
    def relname(self, ):
        return self.relationTemplateDict.get("relname", "")   
    
    def getFormat(self, ):
        '''
        determine if the Relationship Template  has a template format or should use the project default format
        '''
        # set the line type - for now this comes from project settings
        if self.model.modelData["TemplateLineType"] == "Straight":
            self.lineType =  STRAIGHT
        else:
            self.lineType =  ELBOW
            
        # get the rel Template custom format
        customFormat = self.relationTemplateDict.get("TRformat", None)
        if not customFormat is None:
            # get the template custom format
            self.relFormat = TRelFormat(formatDict=customFormat)
        else:
            # get the project default format
            self.relFormat = TRelFormat(formatDict=self.model.modelData["TRformat"])
                

    def getObjectDict(self, ):
        '''
        This function returns the object dictionary used to store this Relation Template Item in the diagram object dictionary list of items
        '''
        objectDict = {}
        objectDict["NZID"] = self.NZID
        objectDict["name"] = self.name()
        objectDict["relname"] = self.relname()
        objectDict["diagramType"] = self.diagramType
        objectDict["startNZID"] = self.startNZID
        objectDict["endNZID"] = self.endNZID
        return objectDict
        
    def moveRelationshipLine(self, ):
        self.drawIt2()        
    
    def clearItem(self, ):

        # if the line and text graphics items already exist on the scene then delete them
        if (not self.TRline1 is None  and not self.TRline1.scene() is None):
            self.TRline1.scene().removeItem(self.TRline1)
            self.TRline1 = None
        if (not self.TRline2 is None  and not self.TRline2.scene() is None):
            self.TRline2.scene().removeItem(self.TRline2)
            self.TRline2 = None
        if (not self.TRline3 is None  and not self.TRline3.scene() is None):
            self.TRline3.scene().removeItem(self.TRline3)
            self.TRline3 = None
        if (not self.TRline4 is None  and not self.TRline4.scene() is None):
            self.TRline4.scene().removeItem(self.TRline4)
            self.TRline4 = None            
        if (not self.TRtext is None  and not self.TRtext.scene() is None):
            self.TRtext.scene().removeItem(self.TRtext)   
            
        if (not self.TAline1 is None  and not self.TAline1.scene() is None):
            self.TAline1.scene().removeItem(self.TAline1)   
        if (not self.TAline2 is None  and not self.TAline2.scene() is None):
            self.TAline2.scene().removeItem(self.TAline2)   
            
        if (not self.TRFromCardinality is None  and not self.TRFromCardinality.scene() is None):
            self.TRFromCardinality.scene().removeItem(self.TRFromCardinality)        
        if (not self.TRToCardinality is None  and not self.TRToCardinality.scene() is None):
            self.TRToCardinality.scene().removeItem(self.TRToCardinality)   
       
        # debugging lines
        if (not self.test1Line is None  and not self.test1Line.scene() is None):
            self.test1Line.scene().removeItem(self.test1Line)                    

    def getOrientation(self, sN, eN):
# enum for orentiation LEFT, ABOVE, RIGHT, BELOW = range(4)
        aLine = QLineF(sN.x, sN.y, eN.x, eN.y)
        if aLine.angle() >= 0.0 and aLine.angle() <= 45.0 or aLine.angle() > 315.0 and aLine.angle() <= 360.0:
            return RIGHT
        if aLine.angle() > 45.0 and aLine.angle() <= 135.0:
            return ABOVE            
        if aLine.angle() > 135.0 and aLine.angle() <= 225.0:
            return LEFT
        if aLine.angle() > 225.0 and aLine.angle() <= 315.0:
            return BELOW
        # shouldn't happen 
#        print("error - can't determine orientation")
        return ABOVE
        
        
    def assignSide(self, ):
        '''
        assign the side of the node that this rel is connected to.
        enum for node template side TOP, R, BOTTOM, L = range(4)
        enum for orientation LEFT, ABOVE, RIGHT, BELOW = range(4)
        
        '''
        sN = self.startNodeItem
        eN = self.endNodeItem   
        orientation = self.getOrientation(sN, eN)
        
#        print("orientation:{}".format(orientation))
        
        if orientation == ABOVE:
            self.inboundSide = BOTTOM
            self.outboundSide = TOP
        elif orientation == LEFT:
            self.inboundSide = R
            self.outboundSide = L
        elif orientation == BELOW:
            self.inboundSide = TOP
            self.outboundSide = BOTTOM
        elif orientation == RIGHT:
            self.inboundSide = L
            self.outboundSide = R
        else:
            # shouldn't happen
#            print("error - can't assign side")
            self.inboundSide = L
            self.outboundSide = BOTTOM
            
#        print("inbound side:{} outbound side{}".format(self.inboundSide, self.outboundSide))    
            
#    def setLocation(self, moveNode = None):
#        return

    def generateHTML(self, ):
        '''
        Generate the HTML that displays the relationship name
        '''
        # generate the html
        prefix = '<!DOCTYPE html><html><body bgcolor="White">'
#        head = "<head><style>table, th, td {border: 1px solid black; border-collapse: collapse;}</style></head>"
        suffix = "</body></html>"
#        blankRow = "<tr><td><left>{}</left></td><td><left>{}</left></td><td><left>{}</left></td><td><left>{}</left></td></tr>".format("", "", "", "")

        name = "<center>{}</center>".format(self.relationTemplateDict.get("name", ""))
        genHTML = "{}{}{}".format(prefix, name, suffix)
#        print("{} html: {}".format(self.name(), genHTML))
        
        return genHTML

        
    def drawIt2(self, ):
        # get the format in case it changed
        self.getFormat()
        self.clearItem()
        # draw self referencing relationship
        if self.startNZID == self.endNZID:
#            print("draw bunny ears")  
            self.drawBunnyEars()
            return
        # draw straight or elbow relationship
        if self.lineType == STRAIGHT:   
#            print("draw straight")  
            self.drawStraight()
            return
        if self.lineType == ELBOW:
#            print("draw elbows")  
            self.drawElbows()

    def drawStraight(self):
        # draw a relationship line using the straight line logic
   
        # stop if missing any data
        if self.inboundSide is None or self.outboundSide is None:
            self.assignSide()
        if self.inboundPoint is None:
            self.endNodeItem.assignPoint(self.inboundSide)
        if self.outboundPoint is None:
            self.startNodeItem.assignPoint(self.outboundSide)        

        # if the two nodes overlap then don't draw the relationship
        if self.startNodeItem.TNode.collidesWithItem(self.endNodeItem.TNode):
            return
        
        
        # arrowhead size
        aLen = 7             # length of arrow head sides
        aAngle = 22         # for STRAIGHT        

        ex = self.inboundPoint.x()
        ey = self.inboundPoint.y()
        sx = self.outboundPoint.x()
        sy = self.outboundPoint.y()
        if sx == ex:
            ex = ex + .0001
        if sy == ey:
            ey = ey + .0001                            
        # get the center points of the start and end node templates
        scx = self.startNodeItem.TNode.sceneBoundingRect().center().x()
        scy = self.startNodeItem.TNode.sceneBoundingRect().center().y()
        ecx = self.endNodeItem.TNode.sceneBoundingRect().center().x()
        ecy = self.endNodeItem.TNode.sceneBoundingRect().center().y()
        if scx == ecx:
            ecx = ecx + .0001
        if scy == ecy:
            ecy = ecy + .0001                    
           
        self.TRline1 = QGraphicsLineItem(sx, sy, ex, ey, parent=None)       
#        print("line: start:{}-{} end:{}-{}".format(sx, sy, ex, ey))
        arrowLine = self.TRline1
        # text location 
        tx = self.TRline1.line().pointAt(.5).x()
        ty = self.TRline1.line().pointAt(.5).y()                   

        # draw the relationship line
        pen = self.relFormat.pen()      
        # configure the lines and add them to the scene
        self.TRline1.setPen(pen)
        self.TRline1.setZValue(RELATIONLAYER)   
        self.TRline1.setData(NODEID, self.NZID) 
        self.TRline1.setData(ITEMTYPE, RELTEMPLATELINE)
        self.TRline1.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.TRline1)   

        # line arrowhead
        aLine1 = QLineF(arrowLine.line().x2(), self.TRline1.line().y2(), self.TRline1.line().x1(), self.TRline1.line().y1())
        aLine1.setLength(aLen)
        aLine1.setAngle(arrowLine.line().angle()-aAngle-180)           
        self.TAline1 = QGraphicsLineItem (aLine1,  parent=None)
        aLine2 = QLineF(arrowLine.line().x2(), self.TRline1.line().y2(), self.TRline1.line().x1(), self.TRline1.line().y1())
        aLine2.setLength(aLen)
        aLine2.setAngle(arrowLine.line().angle()+aAngle-180)           
        self.TAline2 = QGraphicsLineItem (aLine2,  parent=None)                       
#        # make arrowhead red for debugging
#        pen.setColor(Qt.red)
        self.TAline1.setPen(pen)
        self.TAline1.setZValue(RELATIONLAYER)        
        self.TAline1.setData(NODEID, self.NZID) 
        self.TAline1.setData(ITEMTYPE, RELTEMPLATELINE)
        self.TAline1.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.TAline1)       
        self.TAline2.setPen(pen)
        self.TAline2.setZValue(RELATIONLAYER)        
        self.TAline2.setData(NODEID, self.NZID) 
        self.TAline2.setData(ITEMTYPE, RELTEMPLATELINE)
        self.TAline2.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.TAline2)        

        # draw text
        self.TRtext = QGraphicsTextItem("", parent=None)
        self.TRtext.setHtml(self.generateHTML())
        self.TRtext.setZValue(RELATIONLAYER)
        self.TRtext.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.TRtext.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.TRtext.setSelected(True)
        self.TRtext.setData(NODEID, self.NZID) 
        self.TRtext.setData(ITEMTYPE, RELTEMPLATETEXT)
        
        # draw the cardinalities
        # create the text items
        self.TRFromCardinality = QGraphicsTextItem(self.relationTemplateDict.get("fromCardinality", ""), parent=None)
        self.TRFromCardinality.setZValue(RELATIONLAYER)
        self.TRFromCardinality.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.TRFromCardinality.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.TRFromCardinality.setSelected(True)
        self.TRFromCardinality.setData(NODEID, self.NZID) 
        self.TRFromCardinality.setData(ITEMTYPE, RELTEMPLATETEXT)
        
        self.TRToCardinality = QGraphicsTextItem(self.relationTemplateDict.get("toCardinality", ""), parent=None)
        self.TRToCardinality.setZValue(RELATIONLAYER)
        self.TRToCardinality.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.TRToCardinality.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.TRToCardinality.setSelected(True)
        self.TRToCardinality.setData(NODEID, self.NZID) 
        self.TRToCardinality.setData(ITEMTYPE, RELTEMPLATETEXT)      

        # calculate text position on the relationship line
        # get the height and width of the text graphics item
        th = self.TRtext.boundingRect().height() / 2.0  # this is half the height
        tw  = self.TRtext.boundingRect().width()
        # get height and width of the cardinalities
        cFw = self.TRFromCardinality.boundingRect().width()
        cFh = self.TRFromCardinality.boundingRect().height() / 2.0             
        cTw = self.TRToCardinality.boundingRect().width() * 1.2  #  add a little distance to move it away from the arrow head
        cTh = self.TRToCardinality.boundingRect().height() / 2.0  
        
        relLine = self.TRline1.line()  
        lineLen = relLine.length() 
        if tw == lineLen:
            lineLen = lineLen + .001
        tlr = tw / lineLen  # text length to line length ratio
        perpLine = relLine.normalVector()                  
        perpLine.setLength(th)
        cardPerpLine = relLine.normalVector()
        cardPerpLine.setLength(cFh)  
        
        if sx <= ex:
            tx = relLine.pointAt(.5-(tlr/2.0)).x()
            ty = relLine.pointAt(.5-(tlr/2.0)).y()                                
            if sy >= ey:
                # compute rel text pos
                dx = abs(tx - relLine.p1().x())
                dy = abs(ty - relLine.p1().y()) * -1   
                perpLine.translate(dx, dy) 
                self.TRtext.setPos(perpLine.p2())
                # compute  Cardinality text pos
                cFx = cardPerpLine.p2().x()
                cFy = cardPerpLine.p2().y()
                dx = abs(relLine.pointAt(1.0-(cTw/lineLen)).x() - relLine.p1().x())
                dy = abs(relLine.pointAt(1.0-(cTw/lineLen)).y() - relLine.p1().y()) * -1   
                cardPerpLine.translate(dx, dy) 
                cTx = cardPerpLine.p2().x()
                cTy = cardPerpLine.p2().y()
            else:
                dx = abs(tx - relLine.p1().x())
                dy = abs(ty - relLine.p1().y())        
                perpLine.translate(dx, dy) 
                self.TRtext.setPos(perpLine.p2())     
                # compute  Cardinality text pos
                cFx = cardPerpLine.p2().x()
                cFy = cardPerpLine.p2().y()
                dx = abs(relLine.pointAt(1.0-(cTw/lineLen)).x() - relLine.p1().x())
                dy = abs(relLine.pointAt(1.0-(cTw/lineLen)).y() - relLine.p1().y())  
                cardPerpLine.translate(dx, dy) 
                cTx = cardPerpLine.p2().x()
                cTy = cardPerpLine.p2().y()
        else:
            tx = relLine.pointAt(.5+(tlr/2.0)).x()
            ty = relLine.pointAt(.5+(tlr/2.0)).y()      
            if sy <= ey:
                dx = (abs(tx - relLine.p1().x())) * -1
                dy = abs(ty - relLine.p1().y())
                perpLine.translate(dx, dy) 
                dx = abs(perpLine.dx()) * -1
                dy = abs(perpLine.dy()) * -1
                perpLine.translate(dx, dy)             
                self.TRtext.setPos(perpLine.p1())
                # compute  from Cardinality text pos
                dx = abs(relLine.pointAt((cFw/lineLen)).x() - relLine.p1().x()) * -1
                dy = abs(relLine.pointAt((cFw/lineLen)).y()    - relLine.p1().y())  
                cardPerpLine.translate(dx, dy) 
                dx = abs(cardPerpLine.dx()) * -1
                dy = abs(cardPerpLine.dy()) * -1
                cardPerpLine.translate(dx, dy)                                 
                cFx = cardPerpLine.p1().x()
                cFy = cardPerpLine.p1().y()
                # compute  To Cardinality text pos
                dx = abs(relLine.pointAt(1.0-((cTw * .3)/lineLen)).x() - cardPerpLine.p2().x()) * -1
                dy = abs(relLine.pointAt(1.0-((cTw * .3)/lineLen)).y()   - cardPerpLine.p2().y())    
                cardPerpLine.translate(dx, dy)                                 
                cTx = cardPerpLine.p1().x()
                cTy = cardPerpLine.p1().y()                    
            else:
                dx = abs(tx - relLine.p1().x()) * -1
                dy = abs(ty - relLine.p1().y()) * -1
                perpLine.translate(dx, dy)     
                dx = abs(perpLine.dx()) 
                dy = abs(perpLine.dy()) * -1
                perpLine.translate(dx, dy)             
                self.TRtext.setPos(perpLine.p1())                        
                # compute  From Cardinality text pos
                dx = abs(relLine.pointAt((cFw/lineLen)).x() - relLine.p1().x()) * -1
                dy = abs(relLine.pointAt((cFw/lineLen)).y() - relLine.p1().y()) * -1  
                cardPerpLine.translate(dx, dy) 
                dx = abs(cardPerpLine.dx())
                dy = abs(cardPerpLine.dy()) * -1
                cardPerpLine.translate(dx, dy)                                 
                cFx = cardPerpLine.p1().x()
                cFy = cardPerpLine.p1().y()
                # compute  To Cardinality text pos
                dx = abs(relLine.pointAt(1.0-((cTw * .3)/lineLen)).x() - cardPerpLine.p2().x()) * -1
                dy = abs(relLine.pointAt(1.0-((cTw * .3)/lineLen)).y()  - cardPerpLine.p2().y()) * -1  
                cardPerpLine.translate(dx, dy)                                 
                cTx = cardPerpLine.p1().x()
                cTy = cardPerpLine.p1().y()                    
                
#            self.test1Line = QGraphicsLineItem (perpLine, parent=None)            
#            self.test1Line.setPen(pen)                                        
        
        lineAngle = self.TRline1.line().angle()
        if (lineAngle < 180.0 and lineAngle >= 90.0):
            rotateAngle = 180-lineAngle
        elif (lineAngle < 360.0 and lineAngle >= 270.0):
            rotateAngle = 180-(lineAngle-180)
        elif (lineAngle < 270.0 and lineAngle >= 180.0):
            rotateAngle = 180-lineAngle
        elif (lineAngle < 90.0 and lineAngle >= 0.0):
            rotateAngle = 360-lineAngle
        else:
            # shouldn't happen
            return
        # rotate
        self.TRtext.setRotation(rotateAngle)    
        # display the text
        self.scene.addItem(self.TRtext) 
        
        if not self.test1Line is None:
            self.scene.addItem(self.test1Line)


        # draw the cardinalities - THE TO AND FROM LOCATION CALCULATIONS ARE MIXED UP
        self.TRToCardinality.setPos(QPointF(cFx, cFy))      
        self.TRToCardinality.setRotation(rotateAngle)    
        
        self.TRFromCardinality.setPos(QPointF(cTx, cTy))  
        self.TRFromCardinality.setRotation(rotateAngle)   
        
        self.scene.addItem(self.TRFromCardinality) 
        self.scene.addItem(self.TRToCardinality)                 

    def drawBunnyEars(self, ):
        ''' draw a relationship line that is self referencing
        '''
        # get the center points of the start and end node templates
        scx = self.startNodeItem.TNode.sceneBoundingRect().center().x()
        scy = self.startNodeItem.TNode.sceneBoundingRect().center().y()
        ecx = self.endNodeItem.TNode.sceneBoundingRect().center().x()
        ecy = self.endNodeItem.TNode.sceneBoundingRect().center().y()
        if scx == ecx:
            ecx = ecx + .0001
        if scy == ecy:
            ecy = ecy + .0001            
        # get the centerpoint of the line
        cx, cy = self.centerLine(scx, scy, ecx, ecy)
        
        # set offset
        if self.relNum > 5:
            offSet = (14) * 5 # once you get past 5 relationships they just start stacking on top of each other 
        else:
            offSet = (14) * self.relNum 
            
        # set cardinality offset
        cardOffset = 25
        
        # arrowhead size
        aLen = 7             # length of arrow head sides
        aSpread = 7         # for ELBOW and self referencing
        
        
        sx = self.startNodeItem.TNode.sceneBoundingRect().x()
        sy = self.startNodeItem.TNode.sceneBoundingRect().y()
        sh = self.startNodeItem.TNode.sceneBoundingRect().height()
        sw = self.startNodeItem.TNode.sceneBoundingRect().width()

        
        # self referencing relationship
        self.TRline1 = QGraphicsLineItem (sx+sw, sy+offSet, sx+sw+offSet, sy+offSet, parent=None)
        self.TRline2 = QGraphicsLineItem (sx+sw+offSet, sy+offSet, sx+sw+offSet, sy-offSet, parent=None)       
        self.TRline3 = QGraphicsLineItem (sx+sw+offSet, sy-offSet, sx+sw-offSet, sy-offSet, parent=None) 
        self.TRline4 = QGraphicsLineItem (sx+sw-offSet, sy-offSet, sx+sw-offSet, sy, parent=None) 
        tx = self.TRline2.line().pointAt(1).x()
        ty = self.TRline2.line().pointAt(1).y()   
        cTx = sx+sw
        cTy = scy-sy+offSet
        cFx =sx+sw-offSet - cardOffset
        cFy = sy - cardOffset                 
        # arrow head
        a1x = (sx+sw-offSet) + (aSpread/2) 
        a1y = sy - aLen
        a2x = (sx+sw-offSet)  - (aSpread/2)
        a2y = sy - aLen        
        a3x = sx+sw-offSet
        a3y = sy                            
    
        # draw the relationship line
        pen = self.relFormat.pen()      
        # configure the lines and add them to the scene
        self.TRline1.setPen(pen)
        self.TRline1.setZValue(RELATIONLAYER)   
        self.TRline1.setData(NODEID, self.NZID) 
        self.TRline1.setData(ITEMTYPE, RELTEMPLATELINE)
        self.TRline1.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.TRline1)   

        if self.TRline2 is not None:        
            self.TRline2.setPen(pen)
            self.TRline2.setZValue(RELATIONLAYER)        
            self.TRline2.setData(NODEID, self.NZID) 
            self.TRline2.setData(ITEMTYPE, RELTEMPLATELINE)
            self.TRline2.setFlag(QGraphicsItem.ItemIsSelectable, True) 
            self.scene.addItem(self.TRline2)   
        
        if self.TRline3 is not None:
            self.TRline3.setPen(pen)
            self.TRline3.setZValue(RELATIONLAYER)        
            self.TRline3.setData(NODEID, self.NZID) 
            self.TRline3.setData(ITEMTYPE, RELTEMPLATELINE)
            self.TRline3.setFlag(QGraphicsItem.ItemIsSelectable, True) 
            self.scene.addItem(self.TRline3)   
            
        if self.TRline4 is not None:
            self.TRline4.setPen(pen)
            self.TRline4.setZValue(RELATIONLAYER)        
            self.TRline4.setData(NODEID, self.NZID) 
            self.TRline4.setData(ITEMTYPE, RELTEMPLATELINE)
            self.TRline4.setFlag(QGraphicsItem.ItemIsSelectable, True) 
            self.scene.addItem(self.TRline4)   
        
        # line arrowhead
        self.TAline1 = QGraphicsLineItem (a3x, a3y, a1x, a1y, parent=None)
        self.TAline2 = QGraphicsLineItem (a3x, a3y, a2x, a2y, parent=None)  

            
#        # make arrowhead red for debugging
#        pen.setColor(Qt.red)
        self.TAline1.setPen(pen)
        self.TAline1.setZValue(RELATIONLAYER)        
        self.TAline1.setData(NODEID, self.NZID) 
        self.TAline1.setData(ITEMTYPE, RELTEMPLATELINE)
        self.TAline1.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.TAline1)       
        self.TAline2.setPen(pen)
        self.TAline2.setZValue(RELATIONLAYER)        
        self.TAline2.setData(NODEID, self.NZID) 
        self.TAline2.setData(ITEMTYPE, RELTEMPLATELINE)
        self.TAline2.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.TAline2)        
        
        # draw the text 
        
        self.TRtext = QGraphicsTextItem(self.relationTemplateDict.get("name", ""), parent=None)
        self.TRtext.setZValue(RELATIONLAYER)
        self.TRtext.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.TRtext.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.TRtext.setSelected(True)
        self.TRtext.setData(NODEID, self.NZID) 
        self.TRtext.setData(ITEMTYPE, RELTEMPLATETEXT)
        self.TRtext.setPos(QPointF(tx, ty))
        
        if not self.test1Line is None:
            self.scene.addItem(self.test1Line)
            
        self.scene.addItem(self.TRtext) 

        # draw the from cardinality only on self referencing rels
        self.TRFromCardinality = QGraphicsTextItem(self.relationTemplateDict.get("fromCardinality", ""), parent=None)
        self.TRFromCardinality.setZValue(RELATIONLAYER)
        self.TRFromCardinality.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.TRFromCardinality.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.TRFromCardinality.setSelected(True)
        self.TRFromCardinality.setData(NODEID, self.NZID) 
        self.TRFromCardinality.setData(ITEMTYPE, RELTEMPLATETEXT)
        self.TRFromCardinality.setPos(QPointF(cFx, cFy))
        self.scene.addItem(self.TRFromCardinality) 
        
#        self.TRToCardinality = QGraphicsTextItem(self.relationTemplateDict.get("toCardinality", ""), parent=None)
#        self.TRToCardinality.setZValue(RELATIONLAYER)
#        self.TRToCardinality.setFlag(QGraphicsItem.ItemIsMovable, True) 
#        self.TRToCardinality.setFlag(QGraphicsItem.ItemIsSelectable, False) 
#        self.TRToCardinality.setSelected(True)
#        self.TRToCardinality.setData(NODEID, self.NZID) 
#        self.TRToCardinality.setData(ITEMTYPE, RELTEMPLATETEXT)
#        self.TRToCardinality.setPos(QPointF(cTx, cTy))
#        self.scene.addItem(self.TRToCardinality)             
    
    def drawIt(self, ):
        self.drawIt2()
        return

    def drawElbows(self, ):
        
#        # get the format in case it changed
#        self.getFormat()
#        self.clearItem()
        
        # stop if missing any data
        if self.inboundSide is None:
            return
        if self.outboundSide is None:
            return
        if self.inboundPoint is None:
            return
        if self.outboundPoint is None:
            return
            
#        ex = self.inboundPoint.x()
#        ey = self.inboundPoint.y()
#        sx = self.outboundPoint.x()
#        sy = self.outboundPoint.y()
#        if sx == ex:
#            ex = ex + .0001
#        if sy == ey:
#            ey = ey + .0001     
            
        # get the center points of the start and end node templates
        scx = self.startNodeItem.TNode.sceneBoundingRect().center().x()
        scy = self.startNodeItem.TNode.sceneBoundingRect().center().y()
        ecx = self.endNodeItem.TNode.sceneBoundingRect().center().x()
        ecy = self.endNodeItem.TNode.sceneBoundingRect().center().y()
        if scx == ecx:
            ecx = ecx + .0001
        if scy == ecy:
            ecy = ecy + .0001            
        # get the centerpoint of the line
        cx, cy = self.centerLine(scx, scy, ecx, ecy)
        
        sx = self.startNodeItem.TNode.sceneBoundingRect().x()
        sy = self.startNodeItem.TNode.sceneBoundingRect().y()
        ex = self.endNodeItem.TNode.sceneBoundingRect().x()
        ey = self.endNodeItem.TNode.sceneBoundingRect().y()
        sh = self.startNodeItem.TNode.sceneBoundingRect().height()
        sw = self.startNodeItem.TNode.sceneBoundingRect().width()
        eh = self.endNodeItem.TNode.sceneBoundingRect().height()
        ew = self.endNodeItem.TNode.sceneBoundingRect().width() 
        
        # determine orientation of the startNode when compared to the endNode
        if sy + sh < ey:
            self.verticalOrientation = HIGHER
        elif sy > ey + eh:
            self.verticalOrientation = LOWER
        else:
            self.verticalOrientation = ALONGSIDE
        
        if ex > sx + sw:
            self.horizontalOrientation = LEFT
        elif sx > ex + ew:
            self.horizontalOrientation = RIGHT
        else:
            self.horizontalOrientation = ALONGSIDE
           
        a1x = None
        a1y = None
        a2x = None
        a2y = None
        a3x = None
        a3y = None       
        
        # set bullet size 
        bulletSize = 10

        # set offset
        if self.relNum > 5:
            offSet = (bulletSize + 4) * 5 # once you get past 5 relationships they just start stacking on top of each other 
        else:
            offSet = (bulletSize + 4) * self.relNum 
            
        # set cardinality offset
        cardOffset = 25
        
        # arrowhead size
        aLen = 7             # length of arrow head sides
        aSpread = 7         # for ELBOW and self referencing
        aAngle = 22         # for STRAIGHT
        
        # create the qgraphicsline objects based on the relative positions of the start and end nodes
        if (self.horizontalOrientation == LEFT and self.verticalOrientation == HIGHER):
            self.TRline1 = QGraphicsLineItem (sx+sw, scy+offSet, ex+(ew/2)-offSet, scy+offSet, parent=None)
            self.TRline2 = QGraphicsLineItem (ex+(ew/2)-offSet, scy+offSet, ex+(ew/2)-offSet, ey, parent=None)
            # arrow head line1 end 
            a1x = (ex+(ew/2)-offSet) + (aSpread/2)
            a1y = ey - aLen
            # arrow head line2 end 
            a2x = (ex+(ew/2)-offSet) - (aSpread/2)
            a2y = ey - aLen    
            # arrow point
            a3x = ex+(ew/2)-offSet
            a3y = ey                    
            tx = ex+(ew/2)-offSet
            ty = scy+offSet                    
#            elif self.lineType == STRAIGHT:
#                self.inboundSide = L
#                self.outboundSide = R
#                self.inboundSlot = self.endNodeItem.nextRelSide(self.inboundSide)
#                self.outboundSlot = self.startNodeItem.nextRelSide(self.outboundSide)
#                inboundOffSet = (bulletSize + 4) * self.inboundSlot  * self.updown(self.inboundSlot)    
#                outboundOffSet = (bulletSize + 4) * self.outboundSlot * self.updown(self.outboundSlot) 
#                self.TRline1 = QGraphicsLineItem (sx+sw, scy+outboundOffSet, ex+(ew/2)+inboundOffSet, ey, parent=None)       
#                # arrow point
#                a3x = self.TRline1.line().x2()
#                a3y = self.TRline1.line().y2()   
#                # text location 
#                tx = self.TRline1.line().pointAt(.5).x()
#                ty = self.TRline1.line().pointAt(.5).y()                
            

            cTx = sx+sw
            cTy = scy+offSet
            cFx = ex+(ew/2)-offSet
            cFy = ey - cardOffset
            

        elif (self.horizontalOrientation == RIGHT and self.verticalOrientation == HIGHER) :
            self.TRline1 = QGraphicsLineItem (sx, scy+offSet, ecx+offSet, scy+offSet, parent=None)
            self.TRline2 = QGraphicsLineItem (ecx+offSet, scy+offSet, ecx+offSet, ey, parent=None)     
            tx = ecx+offSet
            ty = scy+offSet     
            # arrow head
            a1x = (ecx+offSet) + (aSpread/2)
            a1y = ey - aLen
            a2x = (ecx+offSet) - (aSpread/2)
            a2y = ey - aLen        
            a3x = ecx+offSet
            a3y = ey
                
#            elif self.lineType == STRAIGHT:
#                self.inboundSide = R
#                self.outboundSide = L
#                self.inboundSlot = self.endNodeItem.nextRelSide(self.inboundSide)
#                self.outboundSlot = self.startNodeItem.nextRelSide(self.outboundSide)
#                inboundOffSet = (bulletSize + 4) * self.inboundSlot  * self.updown(self.inboundSlot)      
#                outboundOffSet = (bulletSize + 4) * self.outboundSlot * self.updown(self.outboundSlot)                
#                self.TRline1 = QGraphicsLineItem (sx, scy+outboundOffSet, ecx+inboundOffSet, ey, parent=None)                    
#                # text location 
#                tx = self.TRline1.line().pointAt(.5).x()
#                ty = self.TRline1.line().pointAt(.5).y() 
                
  
            cTx = sx - cardOffset
            cTy = scy+offSet - cardOffset
            cFx = ecx+offSet
            cFy = ey - cardOffset      

        elif (self.horizontalOrientation == ALONGSIDE and self.verticalOrientation == HIGHER) :
            if scx < ecx + .001:
                self.TRline1 = QGraphicsLineItem (scx+offSet, sy+sh, scx+offSet, sy+sh+((ey-(sy+sh))/2)-offSet, parent=None)
                self.TRline2 = QGraphicsLineItem (scx+offSet, sy+sh+((ey-(sy+sh))/2)-offSet, ecx+offSet, sy+sh+((ey-(sy+sh))/2)-offSet, parent=None)       
                self.TRline3 = QGraphicsLineItem (ecx+offSet, sy+sh+((ey-(sy+sh))/2)-offSet, ecx+offSet, ey, parent=None) 
            else:
                self.TRline1 = QGraphicsLineItem (scx+offSet, sy+sh, scx+offSet, sy+sh+((ey-(sy+sh))/2)+offSet, parent=None)
                self.TRline2 = QGraphicsLineItem (scx+offSet, sy+sh+((ey-(sy+sh))/2)+offSet, ecx+offSet, sy+sh+((ey-(sy+sh))/2)+offSet, parent=None)       
                self.TRline3 = QGraphicsLineItem (ecx+offSet, sy+sh+((ey-(sy+sh))/2)+offSet, ecx+offSet, ey, parent=None) 
            tx = self.TRline2.line().pointAt(.5).x() #+ offSet    
            ty = self.TRline2.line().pointAt(.5).y() #- offSet    
            # arrow head
            a1x = (ecx+offSet) + (aSpread/2)
            a1y = ey - aLen
            a2x = (ecx+offSet) - (aSpread/2)
            a2y = ey - aLen             
            a3x = ecx+offSet
            a3y = ey                    
#            elif self.lineType == STRAIGHT:
#                self.inboundSide = TOP
#                self.outboundSide = BOTTOM
#                self.inboundSlot = self.endNodeItem.nextRelSide(self.inboundSide)
#                self.outboundSlot = self.startNodeItem.nextRelSide(self.outboundSide)
#                inboundOffSet = (bulletSize + 4) * self.inboundSlot   * self.updown(self.inboundSlot)     
#                outboundOffSet = (bulletSize + 4) * self.outboundSlot * self.updown(self.outboundSlot)                
#                
#                self.TRline1 = QGraphicsLineItem (scx+outboundOffSet, sy+sh,ecx+inboundOffSet, ey, parent=None)
#                tx = self.TRline1.line().pointAt(.5).x()
#                ty = self.TRline1.line().pointAt(.5).y()                      


            cTx = scx+offSet
            cTy = sy+sh
            cFx = ecx+offSet
            cFy = ey - cardOffset    

          
        elif (self.horizontalOrientation == LEFT and self.verticalOrientation == LOWER) :
            self.TRline1 = QGraphicsLineItem (sx+sw, scy-offSet, ex+(ew/2)-offSet, scy-offSet, parent=None)
            self.TRline2 = QGraphicsLineItem (ex+(ew/2)-offSet, scy-offSet, ex+(ew/2)-offSet, ey+eh, parent=None)
            tx = ex+(ew/2) - offSet
            ty = scy - offSet                             
            # arrow head
            a1x = (ex+(ew/2)-offSet) + (aSpread/2)
            a1y = ey+eh + aLen
            a2x = (ex+(ew/2)-offSet)  - (aSpread/2)     
            a2y = ey+eh + aLen     
            a3x = ex+(ew/2)-offSet
            a3y = ey+eh                    
#            elif self.lineType == STRAIGHT:
#                self.inboundSide = L
#                self.outboundSide = R
#                self.inboundSlot = self.endNodeItem.nextRelSide(self.inboundSide)
#                self.outboundSlot = self.startNodeItem.nextRelSide(self.outboundSide)
#                inboundOffSet = (bulletSize + 4) * self.inboundSlot  * self.updown(self.inboundSlot)      
#                outboundOffSet = (bulletSize + 4) * self.outboundSlot * self.updown(self.outboundSlot)                
#                self.TRline1 = QGraphicsLineItem (sx+sw, scy-outboundOffSet, ex+(ew/2)-inboundOffSet, ey+eh, parent=None)
#                tx = self.TRline1.line().pointAt(.5).x()
#                ty = self.TRline1.line().pointAt(.5).y()                        
                

            cTx = sx+sw 
            cTy = scy-offSet 
            cFx = ex+(ew/2)-offSet 
            cFy = ey+eh       


        elif (self.horizontalOrientation == RIGHT and self.verticalOrientation == LOWER) :
            self.TRline1 = QGraphicsLineItem (sx, scy-offSet, ecx+offSet, scy-offSet, parent=None)
            self.TRline2 = QGraphicsLineItem (ecx+offSet, scy-offSet, ecx+offSet, ey+eh, parent=None)  
            tx = ex+(ew/2)+offSet
            ty = scy-offSet    
            # arrow head
            a1x = (ecx+offSet) + (aSpread/2)
            a1y = ey+eh + aLen
            a2x = (ecx+offSet)  - (aSpread/2)     
            a2y = ey+eh + aLen     
            a3x = ecx+offSet
            a3y = ey+eh                                 
#            elif self.lineType == STRAIGHT:
#                self.inboundSide = R
#                self.outboundSide = L
#                self.inboundSlot = self.endNodeItem.nextRelSide(self.inboundSide)
#                self.outboundSlot = self.startNodeItem.nextRelSide(self.outboundSide)
#                inboundOffSet = (bulletSize + 4) * self.inboundSlot   * self.updown(self.inboundSlot)     
#                outboundOffSet = (bulletSize + 4) * self.outboundSlot * self.updown(self.outboundSlot)                
#                self.TRline1 = QGraphicsLineItem (sx, scy-outboundOffSet, ecx+inboundOffSet, ey+eh, parent=None)     
#                tx = self.TRline1.line().pointAt(.5).x()
#                ty = self.TRline1.line().pointAt(.5).y()    
                
            cTx = sx - cardOffset
            cTy = scy-offSet
            cFx = ecx+offSet
            cFy = ey+eh        


        elif (self.horizontalOrientation == ALONGSIDE and self.verticalOrientation == LOWER) :
            if ecx > scx + .001:
                self.TRline1 = QGraphicsLineItem (scx-offSet, sy, scx-offSet, (sy-((sy-(ey+eh))/2))-offSet, parent=None)
                self.TRline2 = QGraphicsLineItem (scx-offSet, (sy-((sy-(ey+eh))/2))-offSet, ecx-offSet, (sy-((sy-(ey+eh))/2))-offSet, parent=None)       
                self.TRline3 = QGraphicsLineItem (ecx-offSet, (sy-((sy-(ey+eh))/2))-offSet, ecx-offSet, ey+eh, parent=None)    
            else:
                self.TRline1 = QGraphicsLineItem (scx-offSet, sy, scx-offSet, (sy-((sy-(ey+eh))/2))+offSet, parent=None)
                self.TRline2 = QGraphicsLineItem (scx-offSet, (sy-((sy-(ey+eh))/2))+offSet, ecx-offSet, (sy-((sy-(ey+eh))/2))+offSet, parent=None)       
                self.TRline3 = QGraphicsLineItem (ecx-offSet, (sy-((sy-(ey+eh))/2))+offSet, ecx-offSet, ey+eh, parent=None)    
            tx = self.TRline2.line().pointAt(.5).x()
            ty = self.TRline2.line().pointAt(.5).y()
            # arrow head
            a1x = (ecx-offSet) + (aSpread/2)
            a1y = ey+eh + aLen
            a2x = (ecx-offSet)  - (aSpread/2)     
            a2y = ey+eh + aLen     
            a3x = ecx-offSet
            a3y = ey+eh                
            
#            elif self.lineType == STRAIGHT:
#                self.inboundSide = BOTTOM
#                self.outboundSide = TOP
#                self.inboundSlot = self.endNodeItem.nextRelSide(self.inboundSide)
#                self.outboundSlot = self.startNodeItem.nextRelSide(self.outboundSide)
#                inboundOffSet = (bulletSize + 4) * self.inboundSlot * self.updown(self.inboundSlot)       
#                outboundOffSet = (bulletSize + 4) * self.outboundSlot  * self.updown(self.outboundSlot)               
##                    if ecx > scx + .001:
##                        self.TRline1 = QGraphicsLineItem (scx-offSet, sy, ecx-offSet, ey+eh, parent=None)
##                    else:
##                        self.TRline1 = QGraphicsLineItem (scx-offSet, sy, ecx-offSet, ey+eh, parent=None)
#                self.TRline1 = QGraphicsLineItem (scx-outboundOffSet, sy, ecx-inboundOffSet, ey+eh, parent=None)
#                tx = self.TRline1.line().pointAt(.5).x()
#                ty = self.TRline1.line().pointAt(.5).y()     
                
            cTx = scx-offSet
            cTy = sy - cardOffset
            cFx = ecx-offSet
            cFy = ey+eh        

        elif (self.horizontalOrientation == LEFT and self.verticalOrientation == ALONGSIDE) :
            if scy < ecy + .001:
                self.TRline1 = QGraphicsLineItem (sx+sw, scy-offSet, sx+sw+((ex-(sx+sw))/2)+offSet, scy-offSet, parent=None)
                self.TRline2 = QGraphicsLineItem (sx+sw+((ex-(sx+sw))/2)+offSet, scy-offSet, sx+sw+((ex-(sx+sw))/2)+offSet, ecy-offSet, parent=None)       
                self.TRline3 = QGraphicsLineItem (sx+sw+((ex-(sx+sw))/2)+offSet, ecy-offSet, ex, ecy-offSet, parent=None) 
                tx = self.TRline2.line().pointAt(.5).x()
                ty = self.TRline2.line().pointAt(.5).y()  
                cTx = sx+sw
                cTy = scy-offSet
                cFx =ex- cardOffset
                cFy = ecy-offSet - cardOffset  
                # arrow head
                a1x = (ex) - aLen
                a1y = ecy-offSet + (aSpread/2) 
                a2x = (ex) - aLen       
                a2y = ecy-offSet  - (aSpread/2)
                a3x = ex
                a3y = ecy-offSet                                         
                
            else:
                self.TRline1 = QGraphicsLineItem (sx+sw, scy+offSet, sx+sw+((ex-(sx+sw))/2)+offSet, scy+offSet, parent=None)
                self.TRline2 = QGraphicsLineItem (sx+sw+((ex-(sx+sw))/2)+offSet, scy+offSet, sx+sw+((ex-(sx+sw))/2)+offSet, ecy+offSet, parent=None)       
                self.TRline3 = QGraphicsLineItem (sx+sw+((ex-(sx+sw))/2)+offSet, ecy+offSet, ex, ecy+offSet, parent=None) 
                tx = self.TRline2.line().pointAt(.5).x()
                ty = self.TRline2.line().pointAt(.5).y()    
                cTx = sx+sw
                cTy = scy+offSet
                cFx =ex- cardOffset
                cFy = ecy+offSet - cardOffset        
                # arrow head
                a1x = (ex) - aLen
                a1y = ecy+offSet + (aSpread/2) 
                a2x = (ex) - aLen       
                a2y = ecy+offSet  - (aSpread/2)
                a3x = ex
                a3y = ecy+offSet                                         
         
#            elif self.lineType == STRAIGHT:
#                self.inboundSide = L
#                self.outboundSide = R
#                self.inboundSlot = self.endNodeItem.nextRelSide(self.inboundSide)
#                self.outboundSlot = self.startNodeItem.nextRelSide(self.outboundSide)
#                inboundOffSet = (bulletSize + 4) * self.inboundSlot  * self.updown(self.inboundSlot)      
#                outboundOffSet = (bulletSize + 4) * self.outboundSlot  * self.updown(self.outboundSlot)               
#                if scy < ecy + .001:
#                    self.TRline1 = QGraphicsLineItem (sx+sw, scy-outboundOffSet, ex, ecy-inboundOffSet, parent=None)
#                    tx = self.TRline1.line().pointAt(.5).x()
#                    ty = self.TRline1.line().pointAt(.5).y()      
#                    cTx = sx+sw
#                    cTy = scy-offSet
#                    cFx =ex- cardOffset
#                    cFy = ecy-offSet - cardOffset                    
#                    
#                else:
#                    self.TRline1 = QGraphicsLineItem (sx+sw, scy+outboundOffSet, ex, ecy+inboundOffSet, parent=None)
#                    tx = self.TRline1.line().pointAt(.5).x()   
#                    ty = self.TRline1.line().pointAt(.5).y()         
#                    cTx = sx+sw
#                    cTy = scy+offSet
#                    cFx =ex- cardOffset
#                    cFy = ecy+offSet - cardOffset                                   
                
                
        elif (self.horizontalOrientation == RIGHT and self.verticalOrientation == ALONGSIDE) :
            if scy > ecy + .001:
                self.TRline1 = QGraphicsLineItem (sx, scy+offSet, ex+ew+(((sx-(ex+ew))+.001)/2)-offSet, scy+offSet, parent=None)
                self.TRline2 = QGraphicsLineItem (ex+ew+(((sx-(ex+ew))+.001)/2)-offSet, scy+offSet, ex+ew+(((sx-(ex+ew))+.001)/2)-offSet, ecy+offSet, parent=None)       
                self.TRline3 = QGraphicsLineItem (ex+ew+(((sx-(ex+ew))+.001)/2)-offSet, ecy+offSet, ex+ew, ecy+offSet, parent=None) 
                tx = self.TRline2.line().pointAt(.5).x()
                ty = self.TRline2.line().pointAt(.5).y()   
                cTx = sx - cardOffset
                cTy = scy+offSet - cardOffset
                cFx =ex+ew  
                cFy = ecy+offSet - cardOffset 
                # arrow head
                a1x = (ex+ew) + aLen
                a1y = ecy+offSet + (aSpread/2) 
                a2x = (ex+ew) + aLen       
                a2y = ecy+offSet  - (aSpread/2)
                a3x = ex+ew
                a3y = ecy+offSet                                         
            else:
                self.TRline1 = QGraphicsLineItem (sx, scy-offSet, ex+ew+(((sx-(ex+ew))+.001)/2)-offSet, scy-offSet, parent=None)
                self.TRline2 = QGraphicsLineItem (ex+ew+(((sx-(ex+ew))+.001)/2)-offSet, scy-offSet, ex+ew+(((sx-(ex+ew))+.001)/2)-offSet, ecy-offSet, parent=None)       
                self.TRline3 = QGraphicsLineItem (ex+ew+(((sx-(ex+ew))+.001)/2)-offSet, ecy-offSet, ex+ew, ecy-offSet, parent=None)                     
                tx = self.TRline2.line().pointAt(.5).x()
                ty = self.TRline2.line().pointAt(.5).y()   
                cTx = sx - cardOffset
                cTy = scy-offSet - cardOffset
                cFx =ex+ew
                cFy = ecy-offSet - cardOffset                
                # arrow head
                a1x = (ex+ew) + aLen
                a1y = ecy-offSet + (aSpread/2) 
                a2x = (ex+ew) + aLen       
                a2y = ecy-offSet  - (aSpread/2)
                a3x = ex+ew
                a3y = ecy-offSet                         
        else:
            # from and to nodes are overlapping in some fashion so we aren't going to draw the relationship line
            return
        
#        print("inboundSide: {} outboundSide: {} ".format(self.inboundSide, self.outboundSide))
        # draw the relationship line
        pen = self.relFormat.pen()      
        # configure the lines and add them to the scene
        self.TRline1.setPen(pen)
        self.TRline1.setZValue(RELATIONLAYER)   
        self.TRline1.setData(NODEID, self.NZID) 
        self.TRline1.setData(ITEMTYPE, RELTEMPLATELINE)
        self.TRline1.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.TRline1)   

        if self.TRline2 is not None:        
            self.TRline2.setPen(pen)
            self.TRline2.setZValue(RELATIONLAYER)        
            self.TRline2.setData(NODEID, self.NZID) 
            self.TRline2.setData(ITEMTYPE, RELTEMPLATELINE)
            self.TRline2.setFlag(QGraphicsItem.ItemIsSelectable, True) 
            self.scene.addItem(self.TRline2)   
        
        if self.TRline3 is not None:
            self.TRline3.setPen(pen)
            self.TRline3.setZValue(RELATIONLAYER)        
            self.TRline3.setData(NODEID, self.NZID) 
            self.TRline3.setData(ITEMTYPE, RELTEMPLATELINE)
            self.TRline3.setFlag(QGraphicsItem.ItemIsSelectable, True) 
            self.scene.addItem(self.TRline3)   
            
        if self.TRline4 is not None:
            self.TRline4.setPen(pen)
            self.TRline4.setZValue(RELATIONLAYER)        
            self.TRline4.setData(NODEID, self.NZID) 
            self.TRline4.setData(ITEMTYPE, RELTEMPLATELINE)
            self.TRline4.setFlag(QGraphicsItem.ItemIsSelectable, True) 
            self.scene.addItem(self.TRline4)   
        
        # line arrowhead
        self.TAline1 = QGraphicsLineItem (a3x, a3y, a1x, a1y, parent=None)
        self.TAline2 = QGraphicsLineItem (a3x, a3y, a2x, a2y, parent=None)  
            
#        # make arrowhead red for debugging
#        pen.setColor(Qt.red)
        self.TAline1.setPen(pen)
        self.TAline1.setZValue(RELATIONLAYER)        
        self.TAline1.setData(NODEID, self.NZID) 
        self.TAline1.setData(ITEMTYPE, RELTEMPLATELINE)
        self.TAline1.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.TAline1)       
        self.TAline2.setPen(pen)
        self.TAline2.setZValue(RELATIONLAYER)        
        self.TAline2.setData(NODEID, self.NZID) 
        self.TAline2.setData(ITEMTYPE, RELTEMPLATELINE)
        self.TAline2.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.scene.addItem(self.TAline2)        
        
        # draw the text 
        
        self.TRtext = QGraphicsTextItem(self.relationTemplateDict.get("name", ""), parent=None)
        self.TRtext.setZValue(RELATIONLAYER)
        self.TRtext.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.TRtext.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.TRtext.setSelected(True)
        self.TRtext.setData(NODEID, self.NZID) 
        self.TRtext.setData(ITEMTYPE, RELTEMPLATETEXT)
        
#        # if STRAIGHT then rotate the text to match the relationship line
#        if self.lineType == STRAIGHT:
#            # calculate text position on the relationship line
#            # get the height and width of the text graphics item
#            th = self.TRtext.boundingRect().height()
#            tw  = self.TRtext.boundingRect().width()
#            relLine = self.TRline1.line()
#            lineLen = relLine.length() 
#            tlr = tw / lineLen  # text length to line length rati
#            perpLine = relLine.normalVector()     
##            tx = relLine.pointAt(.5-(tlr/2.0)).x()
##            ty = relLine.pointAt(.5-(tlr/2.0)).y()                
#            perpLine.setLength(th)            
#            if scx <= ecx:        
#                tx = relLine.pointAt(.5-(tlr/2.0)).x()
#                ty = relLine.pointAt(.5-(tlr/2.0)).y()                                
#                if scy >= ecy:
#                    dx = abs(tx - relLine.p1().x())
#                    dy = abs(ty - relLine.p1().y()) * -1   
#                    perpLine.translate(dx, dy) 
#                    self.TRtext.setPos(perpLine.p2())
#                else:
#                    dx = abs(tx - relLine.p1().x())
#                    dy = abs(ty - relLine.p1().y())        
#                    perpLine.translate(dx, dy) 
#                    self.TRtext.setPos(perpLine.p2())                        
#            else:
#                tx = relLine.pointAt(.5+(tlr/2.0)).x()
#                ty = relLine.pointAt(.5+(tlr/2.0)).y()                
#                if scy <= ecy:
#                    dx = (abs(tx - relLine.p1().x())) * -1
#                    dy = abs(ty - relLine.p1().y())
#                    perpLine.translate(dx, dy) 
#                    dx = abs(perpLine.dx()) * -1
#                    dy = abs(perpLine.dy()) * -1
#                    perpLine.translate(dx, dy)             
#                    self.TRtext.setPos(perpLine.p1())
#                else:
#                    dx = (abs(tx - relLine.p1().x())) * -1
#                    dy = abs(ty - relLine.p1().y()) * -1
#                    perpLine.translate(dx, dy)     
#                    dx = abs(perpLine.dx()) #* -1
#                    dy = abs(perpLine.dy()) * -1
#                    perpLine.translate(dx, dy)             
#                    self.TRtext.setPos(perpLine.p1())                        
#                    
##            self.test1Line = QGraphicsLineItem (perpLine, parent=None)            
##            self.test1Line.setPen(pen)                                        
#            
#            lineAngle = self.TRline1.line().angle()
#            if (lineAngle < 180.0 and lineAngle >= 90.0):
#                rotateAngle = 180-lineAngle
#            elif (lineAngle < 360.0 and lineAngle >= 270.0):
#                rotateAngle = 180-(lineAngle-180)
#            elif (lineAngle < 270.0 and lineAngle >= 180.0):
#                rotateAngle = 180-lineAngle
#            elif (lineAngle < 90.0 and lineAngle >= 0.0):
#                rotateAngle = 360-lineAngle
#            else:
#                rotateAngle = lineAngle
#            # rotate
#            self.TRtext.setRotation(rotateAngle)    
#            
#
##            print("{} line angle:{} deltay: {}".format(self.relationTemplateDict.get("name", ""), self.TRline1.line().angle(), dy))
##            print("text width {} line len {} ratio {} pointat {}".format(tw,lineLen, tlr, (1.0-(tlr/2.0)) ))
##            print("scene pos {}".format(self.TRtext.scenePos()))
##            print("topleft {} bottomleft {}".format(self.TRtext.sceneBoundingRect().bottomLeft(), self.TRtext.sceneBoundingRect().topLeft()))
##            print("topright {} bottomright {}".format(self.TRtext.sceneBoundingRect().bottomRight(), self.TRtext.sceneBoundingRect().topRight()))
##            print("move by x {} y {}".format(dx, dy))
#            
#        else:
        # ELBOW text position is already calculated 
        self.TRtext.setPos(QPointF(tx, ty))
        
        if not self.test1Line is None:
            self.scene.addItem(self.test1Line)
            
        self.scene.addItem(self.TRtext) 

        # draw the cardinalities
        self.TRFromCardinality = QGraphicsTextItem(self.relationTemplateDict.get("fromCardinality", ""), parent=None)
        self.TRFromCardinality.setZValue(RELATIONLAYER)
        self.TRFromCardinality.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.TRFromCardinality.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.TRFromCardinality.setSelected(True)
        self.TRFromCardinality.setData(NODEID, self.NZID) 
        self.TRFromCardinality.setData(ITEMTYPE, RELTEMPLATETEXT)
        self.TRFromCardinality.setPos(QPointF(cFx, cFy))
        self.scene.addItem(self.TRFromCardinality) 
        
        self.TRToCardinality = QGraphicsTextItem(self.relationTemplateDict.get("toCardinality", ""), parent=None)
        self.TRToCardinality.setZValue(RELATIONLAYER)
        self.TRToCardinality.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.TRToCardinality.setFlag(QGraphicsItem.ItemIsSelectable, False) 
        self.TRToCardinality.setSelected(True)
        self.TRToCardinality.setData(NODEID, self.NZID) 
        self.TRToCardinality.setData(ITEMTYPE, RELTEMPLATETEXT)
        self.TRToCardinality.setPos(QPointF(cTx, cTy))
        self.scene.addItem(self.TRToCardinality)         
        
    def selectItems(self):
        '''
        cause all components of the relationline to be selected
        '''
        if self.TRToCardinality is not None:
            self.TRToCardinality.setSelected(True)
        if self.TRFromCardinality is not None:
            self.TRFromCardinality.setSelected(True)
        if self.TRtext is not None:   
            self.TRtext.setSelected(True)
        if self.TRtext is not None:   
            self.TRline1.setSelected(True)
        if self.TRline2 is not None:
            self.TRline2.setSelected(True)
        if self.TRline3 is not None:
            self.TRline3.setSelected(True)
        if self.TRline4 is not None:
            self.TRline4.setSelected(True)   
            
    def centerLine (self, sx, sy, ex, ey):
        ''' Find the center point of a line.
            Given two end points of a line, (sx,sy) and (ex,ey).
            Return the point (x,y) that is the center of the line.'''
        csx = sx * 1.0
        csy = sy * 1.0
        cex = ex * 1.0
        cey = ey * 1.0
        return (csx+cex)/2.0, (csy+cey)/2.0
