# -*- coding: utf-8 -*-

"""
Module implementing ProjectHTMLDlg.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
import os
import shutil
import webbrowser

from mako.template import Template

from PyQt5.QtCore import pyqtSlot, QSettings, QByteArray, Qt, QFile, QTextStream
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication
from PyQt5.QtGui import QPixmap

from core.helper import Helper
from core.DiagramScene import DiagramScene

from .Ui_ProjectHTMLDlg import Ui_ProjectHTMLDlg


class ProjectHTMLDlg(QDialog, Ui_ProjectHTMLDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, schemaModel = None, model = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ProjectHTMLDlg, self).__init__(parent)
        self.setupUi(self)
        self.settings = QSettings()
        self.schemaModel = schemaModel
        self.model = model
        self.projectData = model.modelData
        self.helper = Helper()
        

        
        # initialize the header area
        dir = self.projectData["GenToDir"]
        self.lblOutputDir.setText(dir)
        self.lblOutputDir.setToolTip(dir)    
        
        # initialize the report generation fields
        self.txtTitle.setText(self.projectData["HeaderTitle"])  
        self.txtHomeTitle.setText(self.projectData["HomePageTitle"])  
        self.txtAuthor.setText(self.projectData["Author"])  
        self.txtFooter.setText(self.projectData["FooterTitle"])  
        self.txtImageFile.setText(self.projectData["IconFile"])  
        if len(self.projectData.get("IconFile", "")) > 0:
            self.loadImage()    

    def outputPath(self):
        return self.lblOutputDir.text()

    def fileFormat(self):
        '''only one file format for now
        '''
        return QByteArray(b'HTML')


    def fileExtension(self):
        '''Only one file extension for now
        '''
        return "HTML"

            
    def loadImage(self, ):
        '''load the image file into the frame
        '''
        try:
            fileName = self.txtImageFile.text()
            pixmap = QPixmap(fileName)
            self.frmImage.setPixmap(pixmap.scaled(self.frmImage.width(), self.frmImage.height(), aspectRatioMode = Qt.KeepAspectRatio))
        except Exception as e: 
            self.helper.displayErrMsg("Load Image", "Error loading {} image file. Error: {}".format(fileName, str(e)))
            return
            
    def getImage(self, ):
        '''return a QImage if valid image file is present
        '''
        try:
            fileName = self.txtImageFile.text()
            if len(fileName) > 0:
                if os.path.isfile(fileName) == True:
                    pixmap = QPixmap(fileName)
                    anImage = pixmap.toImage()
                    return fileName, anImage
                else:
                    self.helper.displayErrMsg("Load Image", "Image File: {} not a valid file.".format(fileName))
                    return fileName, None
            else:
                return fileName, None
        except Exception as e: 
            self.helper.displayErrMsg("Load Image", "Error loading {} image file. Error: {}".format(fileName, str(e)))
            return fileName, None
        
        # should never happen
        return None, None

    def saveSetupData(self):
        # save the report generation fields
        self.projectData["GenToDir"]= self.lblOutputDir.text()  
        self.projectData["HeaderTitle"]= self.txtTitle.text()  
        self.projectData["HomePageTitle"] = self.txtHomeTitle.text()  
        self.projectData["Author"] = self.txtAuthor.text()  
        self.projectData["FooterTitle"] = self.txtFooter.text()  
        self.projectData["IconFile"] = self.txtImageFile.text()          
        
    @pyqtSlot()
    def on_btnSelectDir_clicked(self):
        """
        User selects Path button to select an output path
        """
        curDir = self.lblOutputDir.text()
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setDirectory(curDir)
        file = str(dlg.getExistingDirectory(self, "Select Directory"))
        if file:
            self.lblOutputDir.setText(str(file))
            self.lblOutputDir.setToolTip(str(file))
    
    @pyqtSlot()
    def on_btnLoadImage_clicked(self):
        """
        User clicks on image file button.  They select an image file from disk.
        """
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setNameFilters(["Image Files (*.bmp *.gif *.jpg *.jpeg *.png)","all files (*.*)"])
        dlg.setDirectory(self.settings.value("Default/ProjPath"))
        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            if fileNames:
                fileName = fileNames[0]
                self.txtImageFile.setText(fileName)  
                if len(self.txtImageFile.text()) > 0:
                    self.loadImage()
    
    @pyqtSlot()
    def on_btnGenerate_clicked(self):
        """
        User clicks button to generate html using Mako
        """
        try:
            # setup folder structure, cancel html generation if error
            if self.createFolders():
                QApplication.setOverrideCursor(Qt.WaitCursor)
                # generate home page
                self.genIndexPage2()
                # generate object pages
                for objectType in self.projectData["TopLevel"]:
                    if objectType in ["Label","Property","Relationship","Node Template",  "Relationship Template", "Template Diagram", "Instance Diagram" ]:
                        objectList = self.model.instanceList(objectType)
                        objectPath = self.outputPath() + "/PAGES/{}".format(''.join(objectType.upper().split()) )
                        if len(objectList) > 0:
                            if os.path.exists(objectPath) == False:
                                os.mkdir(objectPath)
                            for objectName in objectList:
                                self.genObjectPage2(objectType=objectType, objectName=objectName)        
                # completed message
                QApplication.restoreOverrideCursor() 
                self.helper.displayErrMsg("Generate HTML", 'HTML generation complete! Click "View In Browser" button.')
                
        except Exception as e: 
            self.helper.displayErrMsg("Generate HTML", "Error clearing html folders. Error: {}".format(str(e)))
        finally:
            QApplication.restoreOverrideCursor() 
        
    @pyqtSlot()
    def on_btnViewBrowser_clicked(self):
        """
        user clicks on the view in browser button
        """
        genPath = self.outputPath()
        indexFileName = genPath + "/index.html"   
        if os.path.isfile(indexFileName) == True:
            webbrowser.open(indexFileName)
        else:
            self.helper.displayErrMsg("Open Browser", "Error - index.html file {} not found.")
    
    
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        User clicks the Close button
        """
        # save the report generation fields
        self.saveSetupData()

        QDialog.accept(self)

############################################################
## diagram render methods
############################################################
    def renderDiagram(self, diagramType=None, diagramName=None, fileName=None):
        # the parent of the scene needs to maintain these dictionaries 
        self.itemDict = {}   # dictionary of graphic items rendered on the scene
        self.relIRPair = {}
        self.relTRPair = {} 
        # create the scene
        self.scene = DiagramScene(self)
        # render the diagram
        self.scene.renderDiagram(diagramType=diagramType, diagramName=diagramName)
        # save the image
        self.scene.saveImage(fileName=fileName)


    # these functions need to be in the parent of the scene.  This needs to be refactored so the scene handles this
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
        
############################################################
    def createFolders(self, ):
        # create directories
        indexFileName = self.outputPath() + "/index.html"
        pagePath = self.outputPath() + "/PAGES"
        imagePath = self.outputPath() + "/IMAGES"
        try:
            # first delete existing content if the user says ok
            if (os.path.isfile(indexFileName) == True or os.path.exists(pagePath) == True or os.path.exists(imagePath) == True):
                if self.helper.delObjectPrompt("Generated HTML files in {}".format(self.outputPath())):
                    # delete existing content and re-add the needed folders
                    if os.path.isfile(indexFileName) == True:
                        os.remove(indexFileName)
                    if os.path.exists(pagePath) == True:
                        shutil.rmtree(pagePath)
                    if os.path.exists(imagePath) == True:
                        shutil.rmtree(imagePath)
                else:
                    return False
            # now create the two needed folders if they don't exist
            if os.path.exists(pagePath) == False:
                os.mkdir(pagePath)
            if os.path.exists(imagePath) == False:
                os.mkdir(imagePath)
                    
        except Exception as e: 
            self.helper.displayErrMsg("Generate HTML", "Error checking {} for existing html folders, html generation cancelled. Error: {}".format(self.outputPath(), str(e)))
            return False
        
        # create the icon image file in the /images directory
        try:
            self.logoImage = None
            self.logoFile = None
            fileName, anImage = self.getImage()
            if not anImage is None:
                self.logoImage = anImage
                self.logoFile = imagePath + "/" + os.path.basename(fileName)
                anImage.save (self.logoFile)
        except Exception as e: 
            self.helper.displayErrMsg("Generate HTML", "Error saving {} to {}. Error: {}".format(fileName, self.logoFile, str(e)))
            return False
        
        return True
            
    def genIndexPage2(self, ):
        try:
            genPath = self.outputPath()
            indexFileName = genPath + "/index.html"   
            # make sur current generation settings are in the project model so template can see them
            self.saveSetupData()
            # get the template for the index page
            mytemplate = self.indexPageTemplate()
            # validate the file to write to
            file = QFile(indexFileName)
            if not file.open(QFile.WriteOnly | QFile.Text):
                self.helper.displayErrMsg("Generate HTML", "Cannot write file %s:\n%s." % (self.indexFileName, file.errorString()))
                return 
            # generate the html page
            outstr = QTextStream(file)
            outstr << mytemplate.render(model=self.model, outputPath= self.outputPath())
        except Exception as e: 
            self.helper.displayErrMsg("Generate HTML", "Error saving {}. Error: {}".format(indexFileName, str(e)))
            
        
    def genObjectPage2(self, objectType=None, objectName=None ):
        try:
            # get the object dictionary
            index, objectDict = self.model.getDictByName(objectType, objectName)
            objectPath = self.outputPath() + "/PAGES/{}".format(''.join(objectType.upper().split()) )
            objName = objectDict.get("name", "NoName")
    #        goodObjName = self.helper.slugify(objName)
            goodObjName = "".join(x for x in objName if x.isalpha() or x.isnumeric() )  + "_file"
            objFileName = objectPath + "/{}.html".format(goodObjName)
            # get the template for the page
            mytemplate = self.objectPageTemplate(objectDict = objectDict)
            # validate the file to write to
            file = QFile(objFileName)
            if not file.open(QFile.WriteOnly | QFile.Text):
                self.helper.displayErrMsg("Generate HTML", "Cannot write file %s:\n%s." % (self.indexFileName, file.errorString()))
                return 
            # generate the html page
            outstr = QTextStream(file)
            outstr << mytemplate.render(objectDict=objectDict, model=self.model, outputPath= self.outputPath(), genObjectType=objectType, genObjectName=objectName)
        except Exception as e: 
            self.helper.displayErrMsg("Generate HTML", "Error saving {}. Error: {}".format(objFileName, str(e)))            
        
        try:
            # for diagrams, also generate the PNG file and save it
            if objectType in ("Template Diagram", "Instance Diagram"):
                goodImgName = "".join(x for x in objName if x.isalpha() or x.isnumeric() )  + "_image"
                imgFileName = objectPath + "/{}.png".format(goodImgName)
                self.renderDiagram(diagramType=objectType, diagramName=objectName)
                # save the image
                self.scene.saveImage(fileName=imgFileName)
        except Exception as e: 
            self.helper.displayErrMsg("Generate HTML", "Error saving {}. Error: {}".format(imgFileName, str(e)))            
            
    def indexPageTemplate(self):
        aTemplate = Template(self.htmlHead() + self.htmlHeader() + self.htmlAside() + self.htmlIndexArticle() + self.htmlFooter() + self.htmlEnd())
        return aTemplate
        
    def objectPageTemplate(self, objectDict = None):
        aTemplate = Template(self.htmlHead() + self.htmlHeader() + self.htmlAside() + self.htmlObjectArticle(objectDict = objectDict) + self.htmlFooter() + self.htmlEnd())
        return aTemplate    

    def htmlHead(self, ):
        html = '''
<!DOCTYPE html>
<html>
    <head>
        <title>NodeEra Generated Web Page</title>
        <meta charset="UTF-8">
        <style type="text/css">''' + self.htmlCSS() + '''      </style>
    </head>
    <body>
        <div class="wrapper">'''
        return html
        
    def htmlHeader(self, ):
        html = '''
            <header class="header">
                <table>
                    <tbody>
                        <tr>
                            <h1><p>
                                <img src="${model.modelData["IconFile"]}" />
                                <span>${model.modelData["HeaderTitle"]}</span>
                            </p></h1>
                        </tr>
                    </tbody>
                </table>
            </header>'''
        return html
        
    def htmlAside(self, ):
        '''
        this is the object list of links on the left hand side of the screen
        '''
        html = '''
            <aside class="aside">
            <%
                homeURL = outputPath + "/index.html"
            %>     
            <a href="${homeURL}">
                <span>Home</span>
            </a>
            <h2><p>Model Objects</p></h2>
            % for objectType in ["Label","Property","Relationship","Node Template",  "Relationship Template", "Template Diagram", "Instance Diagram" ]:
            <%
                objectPath = outputPath + "/PAGES/{}".format(''.join(objectType.upper().split()) )
            %>            
                <h3><p>${objectType}</p></h3>
                <ul>
                % for objectName in model.instanceList(objectType):
                        <li>
                        <%
                            goodObjName = "".join(x for x in objectName if x.isalpha() or x.isnumeric() )  + "_file"
                            objFile = "/{}.html".format(goodObjName)
                        %>
                            <a href="${objectPath}${objFile}">
                                <span>${objectName}</span>
                            </a>
                        </li>
                % endfor
                </ul>
            % endfor
            </aside>
            '''
        return html        

    def htmlIndexArticle(self, ):
        html = '''
            <article class="content">
                <table>
                    <tbody>
                        <tr>
                            <h2><p>${model.modelData["HomePageTitle"]}</p></h2>
                            <p>Project File: ${model.modelFileName}</p>
                            <p>Author: ${model.modelData["Author"]}</p>
                            <p>Description: ${model.modelData["Description"]}</p>
                        </tr>
                    </tbody>
                </table>
            </article>'''
        return html    
        
    def htmlObjectArticle(self, objectDict = None):
        html = '''
            <article class="content">
                ## generic header for all object types
                <h1>${genObjectType}: ${genObjectName}</h1>
                <p>Description: ${objectDict.get("desc","No Description")}</p>
                ## generate object specific stuff

                % if genObjectType == "Instance Diagram":
                <%
                    diagramImgFile = "".join(x for x in objectDict.get("name", "") if x.isalpha() or x.isnumeric() )  + "_image"
                    diagramImgURL = "{}/PAGES/INSTANCEDIAGRAM/{}.png".format(outputPath, diagramImgFile)
                %>    
                    <p>Diagram Image:</p>
                    <p>
                        <img src="${diagramImgURL}" />
                    </p>
                % endif
                
                % if genObjectType == "Template Diagram":
                <%
                    diagramImgFile = "".join(x for x in objectDict.get("name", "") if x.isalpha() or x.isnumeric() )  + "_image"
                    diagramImgURL = "{}/PAGES/TEMPLATEDIAGRAM/{}.png".format(outputPath, diagramImgFile)
                %>    
                    <p>Diagram Image:</p>
                    <p>
                        <img src="${diagramImgURL}" />
                    </p>
                % endif
                
                % if genObjectType == "Node Template":
                    ## label grid
                    <p>Labels:</p>
                    ''' + self.htmlTable(listName="labels", dict=objectDict) + '''
                    <p></p>
                    ## property grid
                    <p>Properties:</p>
                    ''' + self.htmlTable(listName="properties", dict=objectDict) + '''
                    <p></p>
                    ## constraint grid
                    <p>Constraints:</p>
                    ''' + self.htmlTable(listName="constraints", dict=objectDict) + '''
                    <p></p>
                    ## index grid
                    <p>Indexes:</p>
                    ''' + self.htmlTable(listName="indexes", dict=objectDict) + '''
                    <p></p>
                % endif
                
                % if genObjectType == "Relationship Template":
                <%
                    relNameFile = "".join(x for x in objectDict.get("relname", "") if x.isalpha() or x.isnumeric() )  + "_file"
                    relNameURL = "{}/PAGES/RELATIONSHIP/{}.html".format(outputPath, relNameFile)
                    toNodeFile = "".join(x for x in objectDict.get("toTemplate", "") if x.isalpha() or x.isnumeric() )  + "_file"
                    toNodeURL = "{}/PAGES/NODETEMPLATE/{}.html".format(outputPath, toNodeFile)
                    fromNodeFile = "".join(x for x in objectDict.get("fromTemplate", "") if x.isalpha() or x.isnumeric() )  + "_file"
                    fromNodeURL = "{}/PAGES/NODETEMPLATE/{}.html".format(outputPath, fromNodeFile)
                %>
                <p>Relationship Type:                
                    <a href="${relNameURL}">
                        <span>${objectDict.get("relname", "")}</span>
                    </a>
                </p> 
                <p>From node template: 
                    <a href="${fromNodeURL}">
                        <span>${objectDict.get("fromTemplate", "")}</span>
                    </a> has ${objectDict.get("fromCardinality", "")} node template: ${objectDict.get("toTemplate", "")}
                </p> 
                <p>To  node template: 
                    <a href="${toNodeURL}">
                        <span>${objectDict.get("toTemplate", "")}</span>
                    </a> has ${objectDict.get("toCardinality", "")} node template: ${objectDict.get("fromTemplate", "")}                    
                </p> 
                
                <p>Properties:</p>
                ''' + self.htmlTable(listName="properties", dict=objectDict) + '''
                <p></p>
                <p>Constraints:</p>
                ''' + self.htmlTable(listName="constraints", dict=objectDict) + '''
                <p></p>
                % endif
                
                % if genObjectType == "Property":
                    <p>Data Type: ${objectDict.get("dataType", "")} </p>                  
                % endif
                
                ## generate the where used section                
                <p>Where Used:</p>
                <% 
                    hitList = model.scanForObjectUse(genObjectType, genObjectName)
                %>
                % if not hitList is None:
                    % if len(hitList) > 0:
                    <ul>
                        % for hit in hitList:
                            % if hit[0] in ["Label","Property","Node Template",  "Relationship Template", "Template Diagram", "Instance Diagram"]:
                                <%
                                    goodObjName = "".join(x for x in hit[1] if x.isalpha() or x.isnumeric() )  + "_file"
                                    objURL = "../{}/{}.html".format(''.join(hit[0].upper().split()), goodObjName)
                                    ##text = "{} - {} ({})".format(hit[0], hit[1], hit[2])
                                %>
                                <li>
                                    <p>${hit[0]} - 
                                        <a href="${objURL}">
                                            <span>${hit[1]}</span>
                                        </a>
                                        (${hit[2]})
                                    </p>
                                </li>
                            % endif
                        % endfor
                    </ul>
                    % endif
                % endif
                
                
            </article>'''
        return html       

    def htmlTable(self, listName=None, dict=None ):
        '''generate a table from the list in the dictionary
        '''
#        print(objectType, objectName, listName, dict)

        html = '''
                    <%
                        aList = objectDict.get("{}", [])  ## labels
                    %>
                    % if not aList is None:
                        % if (len(aList) > 0 ):
                            <%    
                                rows = len(aList)+1
                                columns = len(aList[0])
                                colMetaDataList = model.getHeaderList(objectType=genObjectType, listName="{}")  ## labels
                            %>
                            <table id=object-section>
                            % if not colMetaDataList is None:
                                <%
                                    colHeaderList = colMetaDataList[0]
                                    colLinkList  = colMetaDataList[1]
                                %>
                                <thead>
                                <tr>
                                % for header in colHeaderList:
                                    <th>${{header}}</td>
                                % endfor
                                </tr>
                                </thead>
                            % endif
                            <tbody>
                            % for indexObject, listObject in enumerate(aList):
                                <tr>
                                % for indexItem, listItem in enumerate(listObject):
                                    % if isinstance(listItem, int):
                                        % if listItem == 0:
                                            <% displayText = "False" %>
                                        % else:
                                            <% displayText = "True" %>
                                        % endif
                                    % else:
                                        <% displayText = str(listItem) %>
                                    % endif
                                    ##<td>${{displayText}}</td>
                                    % if len(colLinkList[indexItem]) > 0:   
                                        <% linkItemList = displayText.split(",") %>
                                        <td>
                                        % for linkItem in linkItemList:
                                            <%
                                                goodObjName = "".join(x for x in linkItem if x.isalpha() or x.isnumeric() )  + "_file"
                                                objURL = "../{{}}/{{}}.html".format(''.join(colLinkList[indexItem].upper().split()), goodObjName)
                                            %>                
                                                <a href="${{objURL}}">
                                                    <span>${{linkItem}} </span>
                                                </a>
                                        % endfor
                                        </td>
                                    % else:
                                        <td>${{displayText}}</td>
                                    % endif
                                % endfor
                                </tr>
                            % endfor
                            </tbody>
                        % endif
                            </table>
                    % endif
        '''.format(listName, listName)
        
        return html

    def htmlFooter(self, ):

        html = '''
            <footer class="footer">
                <table>
                    <tbody>
                        <tr>
                            <p>${model.modelData["FooterTitle"]}</p>
                        </tr>
                    </tbody>
                </table>
            </footer>'''
        return html

        
    def htmlEnd(self, ):
        html = '''
        </div>
    </body>
</html>'''
        return html      

    def htmlCSS(self, ):
        html = '''
*, *:before, *:after {
  box-sizing: border-box;
}

body {
  margin: 40px;
  font-family: 'Open Sans', 'sans-serif';
  background-color: #fff;
  color: #444;
}

h1, p {
  margin: 0 0 1em 0;
}

.wrapper {
  max-width: 1100px;
  margin: 0 20px;
  display: grid;
  grid-gap: 10px;
}

@media screen and (min-width: 500px) {

  /* no grid support? */
  .sidebar {
    float: left;
    width: 19.1489%;
  }

  .content {
    float: right;
    width: 79.7872%;
  }

  .wrapper {
    margin: 0 auto;
    grid-template-columns: 1fr 3fr;
  }
  
  .header, .footer {
    grid-column: 1 / -1;
    /* needed for the floated layout */
    clear: both;
  }

}

.wrapper > * {
  background-color: AliceBlue;
  color: Black;
  border-radius: 5px;
  padding: 10px;
  font-size: 100%;
  /* needed for the floated layout*/
  margin-bottom: 10px;
}

/* We need to set the widths used on floated items back to auto, and remove the bottom margin as when we have grid we have gaps. */
@supports (display: grid) {
  .wrapper > * {
    width: auto;
    margin: 0;
  }
}

#object-section {font-family:lucida sans unicode,lucida grande,Sans-Serif;font-size:12px;width:480px;text-align:left;border-collapse:collapse;margin:20px}

#object-section th{font-size:13px;font-weight:400;background:#b9c9fe;border-top:4px solid #aabcfe;border-bottom:1px solid #fff;color:#039;padding:8px}

#object-section td{background:#e8edff;border-bottom:1px solid #fff;color:#669;border-top:1px solid transparent;padding:8px}

#object-section tr:hover td{background:#d0dafd;color:#339}'''
        
        return html
        
