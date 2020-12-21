#!/usr/bin/env python3
'''
    Copyright: SingerLinks Consulting LLC 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
'''
import sys
import os
from operator import itemgetter
import json
from json import JSONDecodeError
from PyQt5.QtCore import QSettings, Qt

#from core.Enums import DataType
from core.NeoTypeFunc import NeoTypeFunc
from core.helper import Helper

LABEL, REQUIRED, NODEKEY = range(3)
PROPERTY, REQUIRED, PK = range(3)
SOURCENODE, CARDINALITY, TARGETNODE  = range(3)
# node template properties
PROPERTY, DATATYPE, PROPREQ, PROPDEF, EXISTS, UNIQUE, PROPNODEKEY = range(7)
# constraints in node template
CONTYPE, CONLBL, CONPROPLIST = range(3)
# constraints in REL template
CONTYPE, CONPROP, RELNAME = range(3)
# indexes in node template
AUTOINDEX, IDXLBL, IDXPROPLIST = range(3)


class JSONFile():
    def __init__(self, ):
        # the decoded json data from disk
        self.modelData = None    
        # the filename that contains the json data
        self.modelFileName = None    
    #
    # load the model file
    #
    def readFile(self,filename=None):
        self.modelData = None
        rc = True
        msg = "Read File {} OK".format(filename)
        try:
            self.modelData = json.load(open(filename))
            self.modelFileName = filename
        except JSONDecodeError as inst:
            msg =   "Read file: {} - JSON Decode Error: {}".format(filename, inst.args[0])
            rc = False
        except BaseException as e:
            msg =   "Read file: {} - Error: {}".format(filename, str(sys.exc_info()[0]))
            rc = False
        finally:
            return rc, msg
        
    def writeFile(self, ):
        if self.modelData is not None:
            rc = True
            msg = "Write File {} OK".format(self.modelFileName)
            try:
                with open(self.modelFileName, 'w') as outfile:
                    json.dump(self.modelData, outfile, separators=(',', ':'))
                self.setModelClean()
            except BaseException as e:
                msg =   "write file: {} - Error: {}".format(self.modelFileName, str(sys.exc_info()[0]))
                rc = False
        else:
            rc = False
            msg = "Error - No model data to write."
            
        return rc, msg    
        
    def setModelDirty(self, ):
        self.dirty = True
    def setModelClean(self, ):
        self.dirty = False     
        
            
class ProjectModel(JSONFile):
    def __init__(self, neoCon = None ):
        super(ProjectModel, self).__init__()
        self.settings = QSettings()
        self.helper = Helper()
        self.modelNeoCon = neoCon
        self.neoTypeFunc = NeoTypeFunc()
        # model defaults
        self.modelDefaultIDPropertyName = "NZID"
        self.setModelClean()
        # the treeview refresh method from the gui class that should be called whenever some action changes the treeview
        self.updateTreeView = None

        # impact search objects - list of top level objects that might reference an object
        self.objectSearch = {}
        self.objectSearch["Label"] = ["Node Template", "Instance Node"]
        self.objectSearch["Property"] = ["Node Template", "Relationship Template","Instance Node", "Instance Relationship"]
        self.objectSearch["Relationship"] = ["Relationship Template", "Instance Relationship"]
        self.objectSearch["Node Template"] = ["Relationship Template", "Instance Node", "Template Diagram"]
        self.objectSearch["Relationship Template"] = ["Instance Relationship", "Template Diagram"]
        self.objectSearch["Instance Node"] = ["Instance Diagram", "Instance Relationship"]
        self.objectSearch["Instance Relationship"] = ["Instance Diagram"]    
        self.objectSearch["Instance Diagram"] = [] 
        self.objectSearch["Template Diagram"]=[]
        self.objectSearch["Path Template"]=[]
        self.objectSearch["Form"]=[]
        
    def initModel(self, ):
        '''
        Initialize an empty project model data structure
        '''
        self.modelData = {}
        # the top level objects in the model file
        self.modelData["TopLevel"] = ["Instance Diagram","Instance Node","Instance Relationship","Template Diagram","Node Template","Relationship Template","Path Template","Label","Property", "Relationship", "Form"]
        
        # the filename this model is stored as
        self.modelData["ModelName"] = self.modelFileName
        
        # general metadata
        self.modelData["Author"] = "Author name"
        self.modelData["Description"] = ""
        
        # html generation field defaults
        self.modelData["GenToDir"] = str(self.settings.value("Default/ProjPath"))
        self.modelData["HeaderTitle"] = "Enter a title for the page header."
        self.modelData["HomePageTitle"] = "Enter a title for the home page."
        
        self.modelData["FooterTitle"] = "Enter a copyright/classification notice for the page footer"
        self.modelData["IconFile"] = ""                        
        
        # template diagram settings
        self.modelData["TemplateLineType"] = "Straight"

            
        # set sync mode to True
        self.modelData["SyncMode"] = "On"
        
        # create initial project properties from system settings    
        self.modelData["INformat"] = self.settings.value("Default/Format/InstanceNode")
        self.modelData["IRformat"] = self.settings.value("Default/Format/InstanceRelation")
        self.modelData["TNformat"] = self.settings.value("Default/Format/TemplateNode")
        self.modelData["TRformat"] = self.settings.value("Default/Format/TemplateRelation")
        self.modelData["pageSetup"] = self.settings.value("Default/PageSetup")
        
        #create an empty list for each top level model category
        for x in self.modelData["TopLevel"]:
            self.modelData[x] = []        
        
        self.setModelDirty()

    def shortName(self):
        '''return the base part of the filename
        '''
        if os.path.isfile(self.modelFileName) == True:
            return os.path.basename(self.modelFileName)
        else:
            return "invalid filename"
            
    def upgradeModel(self):
        '''
        upgradeModel should be called whenever a model file is first opened.
        This function will perform upgrades on the model file data if it is an older model file
        '''
        if not self.modelData is None:
            # fix the model if its older than current version
            # report generation fields
            if "GenToDir" not in self.modelData:
                self.modelData["GenToDir"] = str(self.settings.value("Default/ProjPath"))
            if "HeaderTitle" not in self.modelData:
                self.modelData["HeaderTitle"] = "Enter a title for the page header."
            if "HomePageTitle" not in self.modelData:    
                self.modelData["HomePageTitle"] = "Enter a title for the home page."
            if "Author" not in self.modelData:    
                self.modelData["Author"] = "Author name"
            if "FooterTitle" not in self.modelData:     
                self.modelData["FooterTitle"] = "Enter a copyright/classification notice for the page footer"
            if "IconFile" not in self.modelData:
                self.modelData["IconFile"] = ""                   
            # add datatype to the property definition dictionary and default to unknown
            for index, property in enumerate(self.modelData["Property"]):
                if not "dataType" in property:
                    property["dataType"] = "Unknown"     

            # add datatype to the node template properties
            for index, nodeTemplate in enumerate(self.modelData["Node Template"]):
                for prop in nodeTemplate["properties"]:
                    # insert blank datatype into the property list if needed
                    if len(prop) == 4:
                        dataType = self.getPropertyDataType(propName=prop[0])
                        prop.insert(1,dataType)
                    if len(prop) in [4, 5]:
                        prop.insert(2, "n")
                        prop.insert(3, "")
            # add datatype to the node instance properties
            for index, nodeInstance in enumerate(self.modelData["Instance Node"]):
                for prop in nodeInstance["properties"]:
                    # insert blank datatype into the property list if needed
                    if len(prop) == 2:
                        dataType = self.getPropertyDataType(propName=prop[0])
                        prop.insert(1,dataType)                  
            # add datatype to the relationship instance properties
            for index, relInstance in enumerate(self.modelData["Instance Node"]):
                for prop in relInstance["properties"]:
                    # insert blank datatype into the property list if needed
                    if len(prop) == 2:
                        dataType = self.getPropertyDataType(propName=prop[0])
                        prop.insert(1,dataType)              
            # add datatype to the rel template properties
            for index, relTemplate in enumerate(self.modelData["Relationship Template"]):
                if not "constraints" in relTemplate:
                    relTemplate["constraints"] = []
                if not "fromCardinality" in relTemplate:
                    relTemplate["fromCardinality"] = "0:M"
                if not "toCardinality" in relTemplate:
                    relTemplate["toCardinality"] = "0:M"
                for prop in relTemplate["properties"]:
                    # insert blank datatype into the property list if needed
                    if len(prop) == 2:
                        dataType = self.getPropertyDataType(propName=prop[0])
                        prop.insert(1,dataType)
                    if len(prop) in [2, 3]:
                        prop.insert(2, "N")
                        prop.insert(3, "")            
            # add top level relationship object - 1.04
            if "Relationship" not in self.modelData:
                self.modelData["TopLevel"].append("Relationship")
                self.modelData["Relationship"] = []         
                self.setModelDirty()
            # add top level PATH TEMPLATE object - 1.05
            if "Path Template" not in self.modelData:
                # insert after Relationship Template
                self.modelData["TopLevel"] = ["Instance Diagram","Instance Node","Instance Relationship","Template Diagram","Node Template","Relationship Template","Path Template","Label","Property", "Relationship"]
                self.modelData["Path Template"] = []         
                self.setModelDirty()
        
            if "TemplateLineType" not in self.modelData:
                self.modelData["TemplateLineType"] = "Elbows"      
             
            # gemeral settings
            if "Author" not in self.modelData:
                self.modelData["Author"] = "Author name"
            if "Description" not in self.modelData:
                self.modelData["Description"] = ""

            # add top level Form object - 1.08
            if "Form" not in self.modelData:
                # insert after Relationship Template
                self.modelData["TopLevel"] = ["Instance Diagram","Instance Node","Instance Relationship","Template Diagram","Node Template","Relationship Template","Path Template","Label","Property", "Relationship", "Form"]
                self.modelData["Form"] = []         
                self.setModelDirty()
                
        return
        
        
    def setUpdateTreeViewMethod(self, method=None):
        if not (method is None):
            self.updateTreeView = method
            
    def updateTV(self, ):
        if not (self.updateTreeView is None):
            self.updateTreeView()

        
################################################################################################
# object type generic functions
################################################################################################

    def loadComboBox(self, topLevel=None, objectName=None, selectMsg=None ):
        '''
        return a list of top level object names prepended with an "instruction" item to load to a combobox
        '''
        # provide default select message if none given
        if selectMsg is None:
            addMsg = "No {} Selected".format(topLevel)
        else:
            addMsg = selectMsg
        objectList = None
        if topLevel is not None:
            #generate the list
            dropdownList = []   
            dropdownList.append(addMsg)
            objectList = dropdownList + self.instanceList(topLevel)
        return objectList
                    
    def objectExists(self, topLevel=None,objectName=None ):
        if topLevel is not None and objectName is not None:
            for index, listObject in enumerate(self.modelData[topLevel]):
                if listObject["name"] == objectName:            
                    return True
        return False
        
    def getObjectDesc(self, topLevel=None, objectName=None):
        desc = "no description"
        if topLevel is not None and objectName is not None:
            for index, listObject in enumerate(self.modelData[topLevel]):
                if listObject["name"] == objectName: 
                    try:
                        desc =  listObject["desc"]
                    except:
                        pass
        return desc  

    def getDictByName(self, topLevel=None,objectName=None):
        if topLevel is not None and objectName is not None:
            for index, listObject in enumerate(self.modelData[topLevel]):
                if listObject["name"] == objectName:            
                    return index, listObject
        return None, None
        
    def deleteTopLevelObject(self, topLevel=None, objectName=None):
        hitList = None
        if topLevel is not None and objectName is not None:
            for index, listObject in enumerate(self.modelData[topLevel]):
                if listObject["name"] == objectName:
                    hitList = self.scanForObjectUse(topLevel, objectName)
                    # remove any reference to the top level object being deleted
                    for hit in hitList:
                        if hit[0] == "Node Template":
                            self.removeFromNodeTemplate(hit)
                        if hit[0] == "Relationship Template":
                            self.removeFromRelationshipTemplate(hit)
                        if hit[0] == "Instance Diagram":
                            self.removeFromInstanceDiagram(hit)
                        if hit[0] == "Template Diagram":
                            self.removeFromTemplateDiagram(hit)
                        if hit[0] == "Instance Node":
                            self.removeFromInstanceNode(hit)
                        if hit[0] == "Instance Relationship":
                            self.removeFromInstanceRelationship(hit)
                    # this removes the top level object from the model
                    del self.modelData[topLevel][index]    
                    self.setModelDirty()
        return hitList                    

    def renameTopLevelObject(self, topLevel = None, objectName=None, newName=None):
        hitList = None
        if topLevel is not None and objectName is not None and newName is not None:
            for index, listObject in enumerate(self.modelData[topLevel]):
                if listObject["name"] == objectName:
                    hitList = self.scanForObjectUse(topLevel, objectName)
                    listObject["name"] = newName
                    for hit in hitList:
#                        if hit[0] == "Instance Diagram":
#                            self.updateInstanceDiagram(hit)
                        if hit[0] == "Template Diagram":
                            self.updateTemplateDiagram(hit, newName)
                        if hit[0] == "Node Template":
                            self.updateNodeTemplate(hit, newName)
                        if hit[0] == "Relationship Template":
                            self.updateRelationshipTemplate(hit, newName)
                        if hit[0] == "Instance Node":
                            self.updateInstanceNode(hit, newName)
                        if hit[0] == "Instance Relationship":
                            self.updateInstanceRelationship(hit, newName)
                    self.setModelDirty()
                    
        return hitList

######################################################################################
#  impact analysis functions 
# - update functions handle "rename" operations
# - remove functions handle "delete" operations
######################################################################################

    def updateTemplateDiagram(self, hit, newName):
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        if hit[2] == "Node Template":
            dict['items'][int(hit[3])]["name"] = newName
        if hit[2] == "Relationship Template":
            dict['items'][int(hit[3])]["name"] = newName
            
#    def updateInstanceDiagram(self, hit, newName):
#        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        
    def removeFromInstanceDiagram(self, hit):
        # get dictionary for the diagram
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        # remove an instance relationship from the diagram
        if hit[2] == "Instance Relationship":
            for index, item in enumerate(dict['items']):
                if item['NZID'] == hit[4]:
                    del dict['items'][index]
                    break
        # remove an instance node from the diagram            
        if hit[2]  == "Instance Node":
            keepList = []
            dropNZID = None
            # scan all items on the diagram
            for index, item in enumerate(dict['items']):
                # find the instance node being deleted
                if (item["diagramType"] == "Instance Node" and item['NZID'] == hit[4]):
                    # don't keep this one
                    dropNZID = item['NZID']

                # keep all other instance nodes
                elif (item["diagramType"] == "Instance Node"):
                    keepList.append(item)
            # scan all items on the diagram again
            for index, relitem in enumerate(dict['items']):                    
                if relitem["diagramType"] == "Instance Relationship":
                    index, relDict = self.getDictByName(topLevel="Instance Relationship", objectName=relitem["NZID"])
                    if (relDict['startNZID'] == dropNZID or relDict['endNZID'] == dropNZID) :
                        # don't keep relations connected to the node template being dropped
                        pass
                    else:
                        keepList.append(relitem)                    
            # save the ones we want to keep
            dict['items']=keepList
            
        
    def removeFromTemplateDiagram(self, hit):
        # get dictionary for the diagram
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        # remove a relationship template from the diagram
        if hit[2] == "Relationship Template":
            for index, item in enumerate(dict['items']):
                if item['NZID'] == hit[4]:
                    del dict['items'][index]
                    break
        # remove a node template from the diagram            
        if hit[2]  == "Node Template":
            keepList = []
            dropNZID = None
            # scan all items on the diagram
            for index, item in enumerate(dict['items']):
                # find the node template being deleted
                if (item["diagramType"] == "Node Template" and item['NZID'] == hit[4]):
                    # don't keep this one
                    dropNZID = item['NZID']

                # keep all other node templates
                elif (item["diagramType"] == "Node Template"):
                    keepList.append(item)
            # scan all items on the diagram again
            for index, relitem in enumerate(dict['items']):                    
                if relitem["diagramType"] == "Relationship Template":
                    if (relitem['startNZID'] == dropNZID or relitem['endNZID'] == dropNZID) :
                        # don't keep relations connected to the node template being dropped
                        pass
                    else:
                        keepList.append(relitem)                    
            # save the ones we want to keep
            dict['items']=keepList
            
    def updateNodeTemplate(self, hit, newName):
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        #this updates the labels or properties list in the node template dictionary
        if hit[2] in ["properties", "labels"]:
            dict[hit[2]][int(hit[3])][0] = newName
        # only constraint or index updates have the 5th item in hit 
        if len(hit)  > 4:
            if hit[4] == "Label":
                #update constraint label
                if hit[2] in ["constraints"]:
                    dict[hit[2]][int(hit[3])][1] = newName
                #update index label
                if hit[2] in ["indexes"]:
                    dict[hit[2]][int(hit[3])][1] = newName
            if hit[4] == "Property":
                #update constraint property
                if hit[2] in ["constraints"]:
                    oldVal = dict[hit[2]][int(hit[3])][2]
                    # turn the comma sep string into a list of props
                    propList = oldVal.split(", ")
                    # substitute the new prop name for the old prop name in the list
                    newPropList = [newName if prop ==hit[5] else prop for prop in propList]
                    # turn the list back into the string
                    newPropString = ", ".join(prop for prop in newPropList)
                    dict[hit[2]][int(hit[3])][2] = newPropString
                #update index property
                if hit[2] in ["indexes"]:
                    oldVal = dict[hit[2]][int(hit[3])][2]
                    # turn the comma sep string into a list of props
                    propList = oldVal.split(", ")
                    # substitute the new prop name for the old prop name in the list
                    newPropList = [newName if prop ==hit[5] else prop for prop in propList]
                    # turn the list back into the string
                    newPropString = ", ".join(prop for prop in newPropList)
                    dict[hit[2]][int(hit[3])][2] = newPropString                    
        
        
    def removeFromNodeTemplate(self, hit):
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        if hit[2] in ["properties", "labels"]:
            del dict[hit[2]][int(hit[3])]
        # only constraint or index updates have the 5th item in hit 
        if len(hit)  > 4:
            if hit[4] == "Label":
                #remove constraint label
                if hit[2] in ["constraints"]:
                    dict[hit[2]][int(hit[3])][1] = ""
                #update index label
                if hit[2] in ["indexes"]:
                    dict[hit[2]][int(hit[3])][1] = ""       
            if hit[4] == "Property":
                #update constraint property
                if hit[2] in ["constraints"]:
                    if dict[hit[2]][int(hit[3])][0] == "Node Key":
                        oldVal = dict[hit[2]][int(hit[3])][2]
                        propList = oldVal.split(", ")
                        if len(propList) > 1:
                            newPropList = [prop for prop in propList if prop != hit[5]]
                            newPropString = ", ".join(prop for prop in newPropList)
                            dict[hit[2]][int(hit[3])][2] = newPropString
                        else:
                            # for nodekey constraints with just one property delete the entire constraint
                            del dict[hit[2]][int(hit[3])]                            
                    else:
                        # for constraints with just one property delete the entire constraint
                        del dict[hit[2]][int(hit[3])]
                #update index property
                if hit[2] in ["indexes"]:
                    oldVal = dict[hit[2]][int(hit[3])][2]
                    propList = oldVal.split(", ")
                    if len(propList) > 1:
                        newPropList = [prop for prop in propList if prop != hit[5]]
                        newPropString = ", ".join(prop for prop in newPropList)
                        dict[hit[2]][int(hit[3])][2] = newPropString
                    else:
                        # for indexes with just one property delete the entire index
                        del dict[hit[2]][int(hit[3])]                            

                    
    def updateInstanceNode(self, hit, newName):
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        #this updates the label or property list in the instance node  dictionary
        if hit[2] == "properties" or hit[2] == "labels":        
            dict[hit[2]][int(hit[3])][0] = newName
            # update the instance node signature
            self.genNodeSignature(dict)
        if hit[2] == "nodeTemplate":
            dict[hit[2]] = newName
        return
        
    def removeFromInstanceNode(self, hit):     
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        #this removes the label or property from the instance node  dictionary
        if hit[2] == "properties" or hit[2] == "labels":        
            del dict[hit[2]][int(hit[3])]
        if hit[2] == "nodeTemplate":        
            dict[hit[2]]=None

        
    def updateInstanceRelationship(self, hit, newName):
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        #this updates the property list in the instance node  dictionary
        if hit[2] == "properties":        
            dict[hit[2]][int(hit[3])][0] = newName
            # update the instance rel signature
            self.genRelSignature(dict)
        if hit[2] == "relTemplate":
            dict[hit[2]] = newName
        # relationship type
        if hit[2] == "relName":
            dict[hit[2]] = newName        
        return   
        
    def removeFromInstanceRelationship(self, hit):     
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        #this removes the property from the instance node  dictionary
        if hit[2] == "properties":        
            del dict[hit[2]][int(hit[3])]
        if hit[2] in ["endNZID", "startNZID"]:
            # delete the instance relationship itself because one of the nodes is being deleted
            try:
                del self.modelData["Instance Relationship"][index]
            except:
                pass
        if hit[2] in ["relName"]:
            # delete the instance relationship itself because the relationship type is being deleted
            try:
                del self.modelData["Instance Relationship"][index]
            except:
                pass     
                
    def updateRelationshipTemplate(self, hit, newName):
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        # update the relname itself
        if hit[2] == "relname":
            dict[hit[2]]= newName        
        #this updates the properties list in the rel template dictionary
        if hit[2] == "properties":
            dict[hit[2]][int(hit[3])][0] = newName
        
        # this updates the source or target node template name
        if hit[2] == "from node template":
            dict['fromTemplate'] = newName
        if hit[2] == "to node template":
            dict['toTemplate'] = newName   
            
        # only constraint updates have the 5th item in hit 
        if len(hit)  > 4:
            if hit[4] == "Property":
                #update constraint property
                if hit[2] in ["constraints"]:
                    dict[hit[2]][int(hit[3])][1] = newName
    
        
    def removeFromRelationshipTemplate(self, hit):     
        index, dict = self.getDictByName(topLevel=hit[0],objectName=hit[1])
        if hit[2] in ["properties"]:
            del dict[hit[2]][int(hit[3])]
        if hit[2] in ["from node template"]:
            dict["fromTemplate"] = ''
        if hit[2] in ["to node template"]:
            dict["toTemplate"] = ''
        # only constraint or index updates have the 5th item in hit 
        if len(hit)  > 4:
            if hit[4] == "Property":
                #update constraint property
                if hit[2] in ["constraints"]:
                    del dict[hit[2]][int(hit[3])]
        if hit[2] in ["relname"]:
            # this removes the top level object from the model
            del self.modelData[hit[0]][index]    
        
    def diagramItemIndex(self, diagramType=None, diagramName=None, itemType=None, NZID=None):
        '''
        return the index of a given Item in the diagram item dictionary based on it's NZID
        '''
        if diagramType == "Instance Diagram":
            try:
                for index, item in enumerate(self.modelData[diagramType][self.instanceDiagramIndex(diagramName)]["items"]):
                    if ( item["NZID"] == NZID and item["diagramType"] == itemType):
                        return index
            except:
                return None
            return None
            
        if diagramType == "Template Diagram":            
            try:
                for index, item in enumerate(self.modelData[diagramType][self.templateDiagramIndex(diagramName)]["items"]):
                    if ( item["NZID"] == NZID and item["diagramType"] == itemType):
                        return index
            except:
                return None
            return None
        
    def templateDiagramIndex(self, name):
        for index, diagram in enumerate(self.modelData["Template Diagram"]):
            if diagram["name"] == name:
                return index
        return None       
        
    def instanceDiagramIndex(self, name):
        for index, diagram in enumerate(self.modelData["Instance Diagram"]):
            if diagram["name"] == name:
                return index
        return None
        
    def instanceList(self, listName):
        '''
        Return a List of name properties from the toplevel dictionary listName
        if listName = "Node Template" you will get back a list of all the node template names
        ''' 
        try:
            returnList = []
            searchDict = self.modelData[listName]
            for index, object in enumerate(searchDict):
                returnList.append(object["name"])
        except:
            pass
        return returnList
        
    def instanceDisplayNameList(self, listName):
        '''
        Return a List of displayName properties from the toplevel dictionary listName
        if listName = "Instance Node" you will get back a list of all the instance node display names
        ''' 
        try:
            returnList = []
            searchDict = self.modelData[listName]
            for index, object in enumerate(searchDict):
                returnList.append(object.get("displayName", object.get("name", "no name")))
        except:
            pass
        return returnList   
        
    def instanceTopLevelIndex(self, listName, objectName):
        try:
            searchDict = self.modelData[listName]
            for index, object in enumerate(searchDict):
                if object["name"] == objectName:
                    return index
        except:
            return None
        return None

    def getHeaderList(self, objectType=None, listName=None):
        '''metadata for grid columns, used by html generation
        '''
        if objectType == "Node Template":
            if listName == "labels":
                return [["Label Name", "Required", "Node Key"], ["Label", "", ""]]
            elif listName == "properties":
                return [["Property Name", "Data Type", "Required","Default","Exists", "Unique", "Node Key"], ["Property", "","","", "", "", ""]]
            elif listName == "constraints":
                return [["Constraint Type", "LABEL", "Property List"], ["", "Label", "Property"]]
            elif listName == "indexes":
                return [["Auto Generated", "LABEL", "Property List"], ["", "Label", "Property"]]
            else:
                return None
        if objectType == "Relationship Template":
            if listName == "properties":
                return [["Property Name", "Data Type", "Required","Default",  "Exists"], ["Property", "", "", "", ""]]
            elif listName == "constraints":
                return [["Constraint Type", "LABEL", "Property List"], ["", "Label", "Property"]]
            else:
                return None
        else:
            return None
            
###################################################################################################
# the following methods are used for where-used analysis.  
# they determine which top level objects use another top level object.
# for example: find everthing that uses a certain property
###################################################################################################
    def scanForObjectUse(self, findObjectType, findObjectName):
        '''Search the project model for references to this objectType and objectName.'''
        hitList = []
        # get the top level objects that might contain findObjectTypes
        for topLevel in self.objectSearch[findObjectType]:
            if topLevel == "Node Template":
                self.scanNodeTemplate(hitList, findObjectType, findObjectName)
            if topLevel == "Relationship Template":
                self.scanRelationshipTemplate(hitList, findObjectType, findObjectName)
            if topLevel == "Template Diagram":
                self.scanTemplateDiagram(hitList, findObjectType, findObjectName)    
            if topLevel == "Instance Diagram":
                self.scanInstanceDiagram(hitList, findObjectType, findObjectName)    
            if topLevel == "Instance Node":
                self.scanInstanceNode(hitList, findObjectType, findObjectName)                           
            if topLevel == "Instance Relationship":
                self.scanInstanceRelationship(hitList, findObjectType, findObjectName)                           
        
#        for hit in hitList:
#            print("hit: {}".format(hit))
        return hitList
        
    def scanNodeTemplate(self, hitList, findObjectType, findObjectName):
        nodeTemplateList = self.instanceList("Node Template")
        for nodeTemplateName in nodeTemplateList:
            index, nodeTemplateDict = self.getDictByName(topLevel="Node Template", objectName = nodeTemplateName)
            if findObjectType == "Label":
                for index, label in enumerate(nodeTemplateDict["labels"]):
                    if label[0] == findObjectName:
                       hitList.append(["Node Template", nodeTemplateDict["name"], "labels", str(index)]) 
                for index, constraint in enumerate(nodeTemplateDict["constraints"]):
                    if findObjectName in constraint[1]:
                       hitList.append(["Node Template", nodeTemplateDict["name"], "constraints", str(index), findObjectType])      
                for index, constraint in enumerate(nodeTemplateDict["indexes"]):
                    if findObjectName in constraint[1]:
                       hitList.append(["Node Template", nodeTemplateDict["name"], "indexes", str(index), findObjectType])                             
            if findObjectType == "Property":
                for index, property in enumerate(nodeTemplateDict["properties"]):
                    if property[0] == findObjectName:
                       hitList.append(["Node Template", nodeTemplateDict["name"], "properties", str(index)]) 
                for index, constraint in enumerate(nodeTemplateDict["constraints"]):
                    propList = (constraint[2].replace("(", "").replace(")", "")).split(", ")
                    if findObjectName in propList: 
#                    if findObjectName in constraint[2]:
                       hitList.append(["Node Template", nodeTemplateDict["name"], "constraints", str(index), findObjectType, findObjectName])      
                for index, constraint in enumerate(nodeTemplateDict["indexes"]):
                    propList = (constraint[2].replace("(", "").replace(")", "")).split(", ")
                    if findObjectName in propList: 
#                    if findObjectName in constraint[2]:
                       hitList.append(["Node Template", nodeTemplateDict["name"], "indexes", str(index), findObjectType, findObjectName])      
        return

    def scanInstanceNode(self, hitList, findObjectType, findObjectName):
        instanceNodeList = self.instanceList("Instance Node")
        for instanceNodeName in instanceNodeList:
            index, instanceNodeDict = self.getDictByName(topLevel="Instance Node", objectName = instanceNodeName)
            if findObjectType == "Label":
                for index, label in enumerate(instanceNodeDict["labels"]):
                    if label[0] == findObjectName:
                       hitList.append(["Instance Node", instanceNodeDict["name"], "labels", str(index)]) 
            if findObjectType == "Property":
                for index, property in enumerate(instanceNodeDict["properties"]):
                    if property[0] == findObjectName:
                       hitList.append(["Instance Node", instanceNodeDict["name"], "properties", str(index)]) 
            if findObjectType == "Node Template":   
                if instanceNodeDict["nodeTemplate"] == findObjectName:
                    hitList.append(["Instance Node", instanceNodeDict["name"], "nodeTemplate"]) 
            
        return


    def scanRelationshipTemplate(self, hitList, findObjectType, findObjectName):
        relTemplateList = self.instanceList("Relationship Template")
        for relTemplateName in relTemplateList:
            index, relTemplateDict = self.getDictByName(topLevel="Relationship Template", objectName = relTemplateName)
            if findObjectType == "Relationship":
                if findObjectName == relTemplateDict["relname"]:
                    hitList.append(["Relationship Template", relTemplateDict["name"], "relname" ]) 
            if findObjectType == "Property":
                for index, property in enumerate(relTemplateDict["properties"]):
                    if property[0] == findObjectName:
                       hitList.append(["Relationship Template", relTemplateDict["name"], "properties", str(index)]) 
                for index, property in enumerate(relTemplateDict["constraints"]):
                    propList = (property[1].replace("(", "").replace(")", "")).split(",")
                    if findObjectName in propList: 
                       hitList.append(["Relationship Template", relTemplateDict["name"], "constraints", str(index), findObjectType, findObjectName])      
            if findObjectType == "Node Template":
                if findObjectName == relTemplateDict["fromTemplate"]:
                    hitList.append(["Relationship Template", relTemplateDict["name"], "from node template", str(index)]) 
                if findObjectName == relTemplateDict["toTemplate"]:
                    hitList.append(["Relationship Template", relTemplateDict["name"], "to node template", str(index)]) 

        return   
        
    def scanInstanceRelationship(self, hitList, findObjectType, findObjectName):
        instanceRelationshipList = self.instanceList("Instance Relationship")
        for instanceRelationshipName in instanceRelationshipList:
            index, instanceRelationshipDict = self.getDictByName(topLevel="Instance Relationship", objectName = instanceRelationshipName)
            if findObjectType == "Relationship":
                if findObjectName == instanceRelationshipDict["relName"]:
                    hitList.append(["Instance Relationship", instanceRelationshipDict["name"], "relName"]) 
            if findObjectType == "Property":
                for index, property in enumerate(instanceRelationshipDict["properties"]):
                    if property[0] == findObjectName:
                       hitList.append(["Instance Relationship", instanceRelationshipDict["name"], "properties", str(index)]) 
            if findObjectType == "Relationship Template":   
                if instanceRelationshipDict["relTemplate"] == findObjectName:
                    hitList.append(["Instance Relationship", instanceRelationshipDict["name"], "relTemplate"]) 
            if findObjectType == "Instance Node":   
                if instanceRelationshipDict["startNZID"] == findObjectName:
                    hitList.append(["Instance Relationship", instanceRelationshipDict["name"], "startNZID"]) 
            if findObjectType == "Instance Node":   
                if instanceRelationshipDict["endNZID"] == findObjectName:
                    hitList.append(["Instance Relationship", instanceRelationshipDict["name"], "endNZID"]) 
        
        return
        
    def scanInstanceDiagram(self, hitList, findObjectType, findObjectName):
        instanceDiagramList = self.instanceList("Instance Diagram")
        for instanceDiagramName in instanceDiagramList:
            index, instanceDiagramDict = self.getDictByName(topLevel="Instance Diagram", objectName = instanceDiagramName)
            for itemIndex, item in enumerate(instanceDiagramDict["items"]):
                if findObjectType == "Instance Node":
                    if item["NZID"] == findObjectName:
                        hitList.append(["Instance Diagram", instanceDiagramDict["name"], item["diagramType"], str(itemIndex), item["NZID"] ])
                        break
                if findObjectType == "Instance Relationship":
                    if item["NZID"] == findObjectName:
                        hitList.append(["Instance Diagram", instanceDiagramDict["name"], item["diagramType"], str(itemIndex), item["NZID"] ])
                        break
                # check the  nodes on the diagram
                if item["diagramType"] == "Node":
                    index, instanceDict = self.getDictByName(topLevel="Instance Node", objectName = item["NZID"])


                    if findObjectType == "Property":   
                        for index, property in enumerate(instanceDict["properties"]):
                            if property[0] == findObjectName:
                               hitList.append(["Instance Diagram", instanceDiagramDict["name"], item["diagramType"], str(itemIndex),"properties", str(index)]) 

                    if findObjectType == "Label":   
                        for index, label in enumerate(instanceDict["labels"]):
                            if label[0] == findObjectName:
                               hitList.append(["Instance Diagram", instanceDiagramDict["name"], item["diagramType"], str(itemIndex),"labels", str(index)]) 
                    
                    if findObjectType == "Node Template":   
                        if item["nodeTemplate"] == findObjectName:
                            hitList.append(["Instance Diagram", instanceDiagramDict["name"], item["diagramType"], str(itemIndex),"nodeTemplate"]) 

                # check the relationships on the diagram
                if item["diagramType"] == "Instance Relationship":
                    if findObjectType == "Relationship Template":   
                        if item["relTemplate"] == findObjectName:
                            hitList.append(["Instance Diagram", instanceDiagramDict["name"], item["diagramType"], str(itemIndex),"relTemplate"]) 
                    
                    index, instanceDict = self.getDictByName(topLevel="Instance Relationship", objectName = item["NZID"])
                    if findObjectType == "Property":   
                        for index, property in enumerate(instanceDict["properties"]):
                            if property[0] == findObjectName:
                               hitList.append(["Instance Diagram", instanceDiagramDict["name"], item["diagramType"], str(itemIndex),"properties", str(index)]) 

        return       
              
    def scanTemplateDiagram(self, hitList, findObjectType, findObjectName):
        templateDiagramList = self.instanceList("Template Diagram")
        for templateDiagramName in templateDiagramList:
            index, templateDiagramDict = self.getDictByName(topLevel="Template Diagram", objectName = templateDiagramName)
            for itemIndex, item in enumerate(templateDiagramDict["items"]):
                if  (item.get("diagramType", "") == findObjectType
                    and item.get("name", "") == findObjectName):
                        hitList.append(["Template Diagram", templateDiagramDict["name"], item["diagramType"], str(itemIndex),item["NZID"] ])

                # check the  nodes on the diagram for labels and properties
                if item["diagramType"] == "Node Template":
                    index, instanceDict = self.getDictByName(topLevel="Node Template", objectName = item["NZID"])
                    if findObjectType == "Property":   
                        for index, property in enumerate(instanceDict["properties"]):
                            if property[0] == findObjectName:
                               hitList.append(["Template Diagram", templateDiagramDict["name"], item["diagramType"], str(itemIndex),"properties", str(index)]) 

                    if findObjectType == "Label":   
                        for index, label in enumerate(instanceDict["labels"]):
                            if label[0] == findObjectName:
                               hitList.append(["Template Diagram", templateDiagramDict["name"], item["diagramType"], str(itemIndex),"labels", str(index)]) 
                    
                # check the relationships on the diagram for properties
                if (item["diagramType"] == "Relationship Template" and findObjectType == "Property") :
                    index, instanceDict = self.getDictByName(topLevel="Relationship Template", objectName = item["NZID"])
                    if findObjectType == "Property":   
                        for index, property in enumerate(instanceDict["properties"]):
                            if property[0] == findObjectName:
                               hitList.append(["Template Diagram", templateDiagramDict["name"], item["diagramType"], str(itemIndex),"properties", str(index)]) 

        return       

##################################################################################
# Node Template Specific Methods
##################################################################################
    def getNodeDescription(self, nodeName=None):
        '''generate the description for the node'''
        descList = []
        if self.objectExists("Node Template", nodeName):
            nodeDict = self.getDictByName("Node Template", nodeName)
            descList.append("Generated Description for Node Template: {} \r\n".format(nodeName))
            descList.append("\r\n")
            descList.append("{} \r\n".format(nodeDict[1]["desc"]))
            descList.append("\r\n")
            descList.append("Labels:\r\n")
            descList += ([label[LABEL] + " - " + self.getObjectDesc(topLevel="Label", objectName=label[LABEL]) + "\r\n" for label in nodeDict[1]["labels"]])
            descList.append("\r\n")
            descList.append("Properties:\r\n")
            descList += ([prop[PROPERTY] + " - " + self.getObjectDesc(topLevel="Property", objectName=prop[PROPERTY]) + "\r\n" for prop in nodeDict[1]["properties"]])
            descList.append("\r\n")
            descList.append("Outbound relationships:\r\n")
            listRels = sorted(self.getOutboundRelTemplates(nodeTemplateName = nodeName), key=itemgetter('relname'))
            descList += (["({}) - [{}] -> ({}) - {} \r\n".format(nodeName, outbound["relname"], outbound["toTemplate"], outbound["desc"]) for outbound in listRels])
            descList.append("\r\n")
            descList.append("Inbound relationships:\r\n")
            listRels = sorted(self.getInboundRelTemplates(nodeTemplateName = nodeName), key=itemgetter('relname'))
            descList += (["({}) - [{}] -> ({}) - {} \r\n".format(outbound["fromTemplate"], outbound["relname"], outbound["toTemplate"], outbound["desc"]) for outbound in listRels])
           
        else:
            descList.append("Node {} not found.".format(nodeName))
        
        descText = ''.join(descList)
        return descText

    def newNodeTemplate(self, name=None, labelList=None, propList=None, conList = None, idxList=None, desc=None):
        '''
        labelList is a list of lists.  each sublist contains two entries, name and required
        propList is a list of lists.  each sublist contains 3 entries, name, PK, and required
        '''
        if name is None:
            return
        if len(name) == 0:
            return
        nodeDict = {}
        nodeDict["name"] = name
        if desc is not None:
            nodeDict["desc"] = desc

        #save the labels
        nodeDict["labels"] = labelList
        #save the properties
        nodeDict["properties"] = propList
        
        
        #save the constraints
        nodeDict["constraints"] = conList
        #save the indexes
        nodeDict["indexes"] = idxList
        
        return nodeDict

    def getNodeLabels(self, objectName=None, requiredOnly=False):
        index, objectDict = self.getDictByName("Node Template",objectName)
        labels = objectDict["labels"]
        lblList = ":".join(label[LABEL] for label in labels)
        return lblList
        

                
########################################################################
    def genNodeSignature(self, nodeDict):
        # this code is also in NodeInstance
        nodeID = nodeDict.get("neoID", "")
        if nodeID == "":
            nodeID = nodeDict.get("NZID", "no ID")
        lblList = self.helper.genLabelList("n", nodeDict)
        propList = self.helper.genPropValueList("n", nodeDict)
        signature = "({} {} {}{}{} )".format(str(nodeID), lblList, "{", propList, "}")
        nodeDict["displayName"] =  signature        
        

    def genRelSignature(self, relDict):
        '''generate the display name for a relationship instance
        '''
        relID = relDict.get("neoID", "")
        if relID == "":
            relID = relDict.get("NZID", "no ID")
        
        startNZID = relDict.get("startNZID", "")
        fromID = self.lookupNeoID(startNZID)
        endNZID = relDict.get("endNZID", "")
        toID = self.lookupNeoID(endNZID)

        propList = self.helper.genPropValueList("n", relDict)
        signature = "({})-[{}:{} {}{}{}]->({})".format(str(fromID), str(relID), relDict["relname"], "{", propList, "}", str(toID))
        relDict["displayName"] =  signature   
        
    def getInstanceItemDict(self, diagramName, NodeEraKey):
        '''
        this function returns the dictionary for an instance diagram item.
        the input is the diagram name and the NZID which is unique across all items 
        in all diagrams.
        '''
        index, diagramDict = self.getDictByName("Instance Diagram", diagramName)
        if diagramDict:
            itemList = diagramDict.get("items", None)
            if itemList:
                for itemDict in itemList:
                    if itemDict["NZID"] == NodeEraKey:
                        return itemDict
        return None
        
    def lookupNeoID(self, NZID=None):
        '''find the neoID based on the NZID
        '''
        for instance in self.instanceList("Instance Node"):
            instanceIndex, instanceDict = self.getDictByName(topLevel="Instance Node", objectName=instance)
            if str(instanceDict.get("NZID", None)) == str(NZID):
                return instanceDict.get("neoID", None)        
        return None
        
    def lookupNZID(self, neoID=None, topLevel=None):
        '''
        find the NZID based on a neoID
        '''
        for instance in self.instanceList(topLevel):
            instanceIndex, instanceDict = self.getDictByName(topLevel=topLevel, objectName=instance)
            if str(instanceDict.get("neoID", None)) == str(neoID):
                return instanceDict.get("NZID", None)
                
        return None
        
    def lookupNZIDfromDisplayName(self, displayName=None, topLevel=None):
        '''
        find the NZID based  on the display  name for an Instance Node or Instance Rel
        '''
        for instance in self.instanceList(topLevel):
            instanceIndex, instanceDict = self.getDictByName(topLevel=topLevel, objectName=instance)
            if str(instanceDict.get("displayName", "")) == str(displayName):
                return instanceDict.get("NZID", None)
                
        return None
    
    def matchNodeTemplate(self, nodeObject=None):
        '''
        nodeObject is a neo4j node data type returned from a query.
        this function looks for a node template that matches the labels and properties in the node.
        It picks the first template it founds where the required labels are present 
        future - should also match on required properties
        '''
        nodeLblSet = set([lbl for lbl in nodeObject.labels]  )
        for nodeTemplate in self.instanceList("Node Template"):
            nodeIndex, nodeDict = self.getDictByName(topLevel="Node Template", objectName=nodeTemplate) 
            reqLabels = set([label[LABEL] for label in nodeDict["labels"] if label[REQUIRED] == Qt.Checked])
            if (len(reqLabels) > 0 and reqLabels.issubset(nodeLblSet)):
                return nodeTemplate
        
        return None
            
    def matchRelTemplate(self, startNodeTemplate=None, endNodeTemplate=None, relName = None ):
        '''
        see if a relationship template has the given start and end node template and the relationshipn name.
        This returns the first matching template it finds
        '''
        for relTemplate in self.instanceList("Relationship Template"):
            relIndex, relDict = self.getDictByName(topLevel="Relationship Template", objectName=relTemplate) 
            if relDict["relname"] == relName and relDict["fromTemplate"] == startNodeTemplate and relDict["toTemplate"] == endNodeTemplate:
                return relTemplate
    
        return None

    def matchAllRelTemplates(self, startNodeTemplate=None, endNodeTemplate=None, relName = None ):
        '''
        see if a relationship template has the given start and end node template and the relationshipn name.
        This returns all matching templates in a list
        '''
        relTemplateList = []
        for relTemplate in self.instanceList("Relationship Template"):
            relIndex, relDict = self.getDictByName(topLevel="Relationship Template", objectName=relTemplate) 
            # a relationship type has been selected
            if not relName in ["NoRelationshipName", "Enter or Select Relationship Type"]:
                if relDict["relname"] == relName:
                    if (((relDict["fromTemplate"] == startNodeTemplate) and (relDict["toTemplate"] == endNodeTemplate))
                        or
                        ((relDict["fromTemplate"] == startNodeTemplate) and (endNodeTemplate in ["No Template Selected", ""]))
                        or
                        ((startNodeTemplate in ["No Template Selected", ""]) and (relDict["toTemplate"] == endNodeTemplate))
                        or
                        ((startNodeTemplate in ["No Template Selected", ""]) and (endNodeTemplate in ["No Template Selected", ""]))
                        ):
                        relTemplateList.append(relTemplate)
            # no relationship type has been selected yet so only look at node templates to make a match
            else:
                if (((relDict["fromTemplate"] == startNodeTemplate) and (relDict["toTemplate"] == endNodeTemplate))
                    or
                    ((relDict["fromTemplate"] == startNodeTemplate) and (endNodeTemplate in ["No Template Selected", ""]))
                    or
                    ((startNodeTemplate in ["No Template Selected", ""]) and (relDict["toTemplate"] == endNodeTemplate))
                    or
                    ((startNodeTemplate in ["No Template Selected", ""]) and (endNodeTemplate in ["No Template Selected", ""]))
                    ):
                    relTemplateList.append(relTemplate)
                    
        return relTemplateList
        
    def getInboundRelTemplates(self, nodeTemplateName = None):
        relTemplateList = []
        for relTemplate in self.instanceList("Relationship Template"):
            relIndex, relDict = self.getDictByName(topLevel="Relationship Template", objectName=relTemplate)
            if relDict["toTemplate"] == nodeTemplateName:
                relTemplateList.append(relDict)

        return relTemplateList 
        
    def getOutboundRelTemplates(self, nodeTemplateName = None):
        relTemplateList = []
        for relTemplate in self.instanceList("Relationship Template"):
            relIndex, relDict = self.getDictByName(topLevel="Relationship Template", objectName=relTemplate)
            if relDict["fromTemplate"] == nodeTemplateName:
                relTemplateList.append(relDict)

        return relTemplateList         

                
    def newLabel(self, name):
        # this function is used to automatically add a Label item when a new label is entered
        # on a node
        if len(name) == 0:
            return
        if self.objectExists(topLevel="Label",objectName=name ) == True:
            return
        # add a new Label to the list
        labelDict = {}
        labelDict["name"] = name
        labelDict["desc"] = ""
        self.modelData["Label"].append(labelDict)

    def newRelationship(self, name):
        '''this function is used to automatically add a Relationship item when a new relationship is entered in a rel template or an instance rel
        '''
        if len(name) == 0:
            return
        if self.objectExists(topLevel="Relationship",objectName=name ) == True:
            return
        # add a new Label to the list
        relDict = {}
        relDict["name"] = name
        relDict["desc"] = ""
        self.modelData["Relationship"].append(relDict)
        
    def newProperty(self, name=None, dataType=None):
        '''
        this function checks to see if a property name exists in the model
        this function should be called whenever a user has dynamically added a property name (from node and property templates and instances).
        if the property does not exist, then add it to the design model
        '''
        if len(name) == 0:
            return
        if self.objectExists(topLevel="Property",objectName=name ) == False:
            # add a new Property to the list
            propDict = {}
            propDict["name"] = name
            propDict["desc"] = ""
            propDict["dataType"] = dataType if not dataType is None else "Unknown"
            self.modelData["Property"].append(propDict)
        
    def propertyDataTypeValid(self, name=None, dataType=None):
        '''This function checks the given property name and datatype against the property definition.
            If the property definition has a datatype then return true if they match otherwise return false
            If the property definition doesn't have a datatype return True
            '''
        if len(name) == 0:
            return True
        if self.objectExists(topLevel="Property",objectName=name ) == True:
            # see if user changed datatype 
            if dataType != self.getPropertyDataType(name):
                return False
            else:
                return True
        else:
            return True
        
    def updatePropertyDataType(self, name=None, dataType=None):
        index, propDict = self.getDictByName(topLevel="Property", objectName=name)
        if not propDict is None:
            propDict["dataType"] = dataType
            
    def getTemplatePropDefVal(self, templateName=None, propName=None):
        if not propName is None:
            index, nodeTemplateDict = self.getDictByName(topLevel="Node Template", objectName=templateName)
            if not nodeTemplateDict is None:
                for prop in nodeTemplateDict["properties"]:
                    if prop[PROPERTY] == propName:
                        if prop[PROPDEF] != "":
                            return prop[PROPDEF]
        return None
                
                
    def getPropertyDataType(self, propName=None):
        if not propName is None:
            index, propDict = self.getDictByName(topLevel="Property", objectName=propName)
            if not propDict is None:
                return propDict.get("dataType", "Unknown")
        
        return "Unknown"
        
    def newNodeInstance(self, nodeID = None, templateName=None, labelList=None, propList=None,  NZID=None):
        '''
        templateName - the name of the node template this instance node is patterned after
        labelList is a list of lists.  each sublist contains two entries, name and required
        propList is a list of lists.  if the list has three values they are name, datatype, value
        NZID - the nodera id assigned to the node instance
        '''

        nodeInstanceDict = {}
        nodeInstanceDict["nodeTemplate"] = templateName
        nodeInstanceDict["labels"] = labelList
        if len(propList) > 0:
            newPropList = []
            for prop in propList:
                # Adding a node from the db you only get two values
                if len(prop) == 2:
                    newPropList.append( [prop[0], self.neoTypeFunc.getNeo4jDataType(prop[1]), self.neoTypeFunc.convertTypeToString(prop[1])])
                else:
                    newPropList.append( [prop[0], prop[1], prop[2]])
                    
            nodeInstanceDict["properties"] = newPropList
        else:
            nodeInstanceDict["properties"] = []
        
        if not NZID is None:
            nodeInstanceDict["NZID"] = NZID
        nodeInstanceDict["neoID"] = nodeID

        return nodeInstanceDict
        
    def getRelationshipDescription(self, relDict = None):
        descList = []
        descList.append("Generated Description for Relationship Template: {} \r\n".format(relDict["name"]))
        descList.append("\r\n")
        descList.append("( {} ) - [ {} ] -> ( {} ) \r\n".format(relDict["fromTemplate"], relDict["relname"], relDict["toTemplate"]))
        descList.append("\r\n")
        descList.append("Relationship Type: {} \r\n".format(relDict["relname"]))
        descList.append("\r\n")
        getDesc = self.getObjectDesc(topLevel = "Relationship", objectName = relDict["relname"] )
        descList.append("Relationship Type Description: {} \r\n".format(getDesc))
        descList.append("\r\n")
        descList.append("Relationship Description: {} \r\n".format(relDict["desc"]))
        descList.append("\r\n")

        index, fromTemplateDict = self.getDictByName("Node Template", relDict["fromTemplate"])
        index, toTemplateDict = self.getDictByName("Node Template", relDict["toTemplate"])        
        if not fromTemplateDict is None:
            descList.append("From Node Template: {} - {}\r\n".format(relDict["fromTemplate"], fromTemplateDict["desc"]))
        if not toTemplateDict is None:
            descList.append("To   Node Template: {} - {}\r\n".format(relDict["toTemplate"], toTemplateDict["desc"]))
        descList.append("\r\n")        
        descList.append("Properties:\r\n")
        descList += ([prop[PROPERTY] + " - " + self.getObjectDesc(topLevel="Property", objectName=prop[PROPERTY]) + "\r\n" for prop in relDict["properties"]])
        descList.append("\r\n")
           
        descText = ''.join(descList)
        return descText
        
    def newRelTemplateDict(self, name=None, relname=None,  propList=None, desc=None, fromTemplate=None, toTemplate=None, conList=None, fromCardinality=None, toCardinality=None):
        '''
        generate an object dictionary for a new relationship template
        '''
        relTemplateDict = {}        
        if name is None:
            relTemplateDict["name"] = ""
        else:
            relTemplateDict["name"] = name
            
        if relname is None:
            relTemplateDict["relname"] = ""
        else:
            relTemplateDict["relname"] = relname        
            
        if propList is None:
            relTemplateDict["properties"] = []
        else:
            relTemplateDict["properties"] = propList
        
        if desc is None:
            relTemplateDict["desc"] = ""
        else:
            relTemplateDict["desc"] = desc   

        if fromTemplate is None:
            relTemplateDict["fromTemplate"] = ""
        else:
            relTemplateDict["fromTemplate"] = fromTemplate
            
        if toTemplate is None:
            relTemplateDict["toTemplate"] = ""
        else:
            relTemplateDict["toTemplate"] = toTemplate
            
        if fromCardinality is None:
            relTemplateDict["fromCardinality"] = "0:M"
        else:
            relTemplateDict["fromCardinality"] = fromCardinality

        if toCardinality is None:
            relTemplateDict["toCardinality"] = "0:M"
        else:
            relTemplateDict["toCardinality"] = toCardinality
            
        if conList is None:
            relTemplateDict["constraints"] = None
        else:
            relTemplateDict["constraints"] = conList
        return relTemplateDict   


####################################################################################
# cypher generation helper functions
####################################################################################
    def getRelType(self, relTemplateName):       
        index, objectDict = self.getDictByName("Relationship Template",relTemplateName)
        if objectDict == None:
           return "Unknown"
        
        return objectDict["relname"]

    def genReqLbls(self, nodeTemplateName):
        index, nodeDict = self.getDictByName(topLevel="Node Template",objectName=nodeTemplateName)
        genStr = ""
        if nodeDict is None:        
            return genStr
        genStr = ":".join(x[LABEL]  for x in nodeDict["labels"] if x[REQUIRED] == Qt.Checked )
        if len(genStr) > 0:
            genStr = ":" + genStr
        return genStr
            
    def genMatchNode(self, nodeTemplateName):
        nodeDict = self.getDictByName(topLevel="Node Template",objectName=nodeTemplateName)
        if nodeDict is None:
            return "node template [{}] not found.".format(nodeTemplateName)
        cypher = "MATCH (n:{}) \nRETURN n".format(self.getNodeLabels(nodeTemplateName, requiredOnly=True))
        return cypher  
        
    def genMatchRel(self, relTemplateName):
        relDict = self.getDictByName(topLevel="Relationship Template",objectName=relTemplateName)
        if relDict is None:
            return "relationship template [{}] not found.".format(relTemplateName)
        cypher = "MATCH (n)-[r:{}]->(t) \nRETURN n,r,t".format(self.getRelType(relTemplateName))
        return cypher   

#################################################################################
# forward engineer schema methods
#################################################################################
    def genIndexes(self, indexType=None):
        # generate index statement for all node templates in the model
        # AUTOINDEX, IDXLBL, IDXPROPLIST
        nodeIdxList = []
        IdxList = []
        # gather all node prop unique definitions into a list and eliminate duplicates
        for index, listObject in enumerate(self.modelData["Node Template"]):
            if not listObject.get('indexes', []) is None:
                for nodeIdx in listObject.get('indexes', []):
                    if not nodeIdx in nodeIdxList:
                        if indexType == "all":
                            nodeIdxList.append(nodeIdx)
                        else:
                            if nodeIdx[AUTOINDEX] == "No":
                                nodeIdxList.append(nodeIdx)
                        
        # generate the index statements
        if len(nodeIdxList) > 0:
            for nodeIdx  in nodeIdxList:
                IdxList.append(self.genIndex(nodeIdx))
        
        return IdxList  

    def genNodePropUniqueConstraints(self, ):
        # generate node property unique constraint statement for all node templates in the model
        # CONTYPE, CONLBL, CONPROP, CONPROPLIST
        nodeConList = []
        createList = []
        # gather all node prop unique definitions into a list and eliminate duplicates
        for index, listObject in enumerate(self.modelData["Node Template"]):
            if not listObject.get('constraints', []) is None:
                for constraint in listObject.get('constraints', []):
                    if constraint[CONTYPE] == "Property Unique":
                        if not constraint in nodeConList:
                            nodeConList.append(constraint)
        # generate the constraint statements
        if len(nodeConList) > 0:
            for nodeCon  in nodeConList:
                createList.append(self.genNodePropUniqueConstraint(nodeCon))
        
        return createList  

    def genNodePropExistsConstraints(self, ):
        # generate node property Exists constraint statement for all node templates in the model
        # CONTYPE, CONLBL, CONPROP, CONPROPLIST
        nodeConList = []
        createList = []
        # gather all node prop Exists definitions into a list and eliminate duplicates
        for index, listObject in enumerate(self.modelData["Node Template"]):
            if not listObject.get('constraints', []) is None:
                for constraint in listObject.get('constraints', []):
                    if constraint[CONTYPE] == "Property Exists":
                        if not constraint in nodeConList:
                            nodeConList.append(constraint)
        # generate the constraint statements
        if len(nodeConList) > 0:
            for nodeCon  in nodeConList:
                createList.append(self.genNodePropExistsConstraint(nodeCon))
        
        return createList  
        
    def genNodeKeyConstraints(self,):
        # generate node key constraint statement for all node templates in the model
        # CONTYPE, CONLBL, CONPROP, CONPROPLIST
        # gather all node key definitions into a list and eliminate duplicates
        nodeKeyList = []
        createList = []
        for index, listObject in enumerate(self.modelData["Node Template"]):
            if not listObject.get('constraints', []) is None:
                for constraint in listObject.get('constraints', []):
                    if constraint[CONTYPE] == "Node Key":
                        if not constraint in nodeKeyList:
                            nodeKeyList.append(constraint)
        if len(nodeKeyList) > 0:
            for nodeKey  in nodeKeyList:
                createList.append(self.genNodeKeyConstraint(nodeKey))
        
        return createList
        
    def genRelPropExistsConstraints(self,   ):
        # generate rel property Exists constraint statement for all rel templates in the model
        # CONTYPE, CONPROP,
        relConList = []
        createList = []
        # gather all node prop Exists definitions into a list and eliminate duplicates
        for index, listObject in enumerate(self.modelData["Relationship Template"]):
            relName = listObject["relname"]
            if not listObject.get('constraints', []) is None:
                for constraint in listObject.get('constraints', []):
                    if constraint[CONTYPE] == "Property Exists":
                        if not constraint in relConList:
                            # add the relationship  name to the constraint list as it is needed to generate
                            constraint.append(relName)
                            relConList.append(constraint)
        # generate the constraint statements
        if len(relConList) > 0:
            for relCon  in relConList:
                createList.append(self.genRelPropExistsConstraint(relCon))
        
        return createList
        
    def genIndex(self, nodeIdx = None):
        '''
        generate an index command
        Create INDEX ON :APPLSYS(anotherProp) ;
        '''
        props = ", ".join(prop.strip() for prop in nodeIdx[IDXPROPLIST].split(","))
        cmd = "INDEX ON :{}({})".format(nodeIdx[IDXLBL], props)
        return cmd
                
    def genNodeKeyConstraint(self, nodeKey = None):
        '''
        generate a create node key command
        Create CONSTRAINT ON ( applsys:APPLSYS ) ASSERT (applsys.applSysName, applsys.NZID) IS NODE KEY ;
        '''
        props = ", ".join("n." + prop.strip() for prop in nodeKey[CONPROPLIST].split(","))
        cmd = "CONSTRAINT ON (n:{}) ASSERT ({}) IS NODE KEY".format(nodeKey[CONLBL], props)
        return cmd
    
    def genNodePropUniqueConstraint(self, nodeKey = None):
        '''
        generate a node property unique command
        CONSTRAINT ON ( company:COMPANY ) ASSERT company.companyName IS UNIQUE ;
        '''
        props = ", ".join("n." + prop.strip() for prop in nodeKey[CONPROPLIST].split(","))
        cmd = "CONSTRAINT ON (n:{}) ASSERT ({}) IS UNIQUE".format(nodeKey[CONLBL], props)
        return cmd

    def genNodePropExistsConstraint(self, nodeKey = None):
        '''
        generate a  node property exists command
        Create CONSTRAINT ON ( test:TEST ) ASSERT exists(test.x) ;
        '''
        props = ", ".join("n." + prop.strip() for prop in nodeKey[CONPROPLIST].split(","))
        cmd = "CONSTRAINT ON (n:{}) ASSERT exists({})".format(nodeKey[CONLBL], props)
        return cmd

    def genRelPropExistsConstraint(self, relCon = None):
        '''
        generate a  relationship property exists command
        Create CONSTRAINT ON ()-[ isa:IsA ]-() ASSERT exists(isa.NZID) ;
        '''
        relName = relCon[RELNAME]
        props = ", ".join("r." + prop.strip() for prop in relCon[CONPROP].split(","))
        cmd = "CONSTRAINT ON ()-[r:{}]-() ASSERT exists({})".format(relName, props)
        return cmd

    def newPathTemplateDict(self, name=None):     
        'initialize an empty Path Template'
        pathTemplateDict = {}
        pathTemplateDict["name"] = name
        pathTemplateDict["description"] = ""
        pathTemplateDict["queryPath"] = []
        return pathTemplateDict
        
    def newFormDict(self, name=None):     
        'initialize an empty Form'
        formDict = {}
        formDict["name"] = name
        formDict["description"] = ""
        formDict["formOutline"] = []
        return formDict

