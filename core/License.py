#!/usr/bin/env python3
"""
The License class manages the EDD license key api calls

    Author: John Singer
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
import http.client
import urllib
import json
#from json import JSONDecodeError
from PyQt5.QtCore import QSettings, QThread, pyqtSignal

# license api commands
ACTIVATE='activate_license'
CHECK='check_license'
VERSION='get_version'
DEACTIVATE='deactivate_license'

class EDDAPI(QThread):
    '''
    This class provides a thread that is used to call EDD API's in the License object.
    '''
    apiCallComplete = pyqtSignal(bool, str)
    
    def __init__(self, myLicense, action):
        QThread.__init__(self)
        self.myLicense = myLicense
        self.action = action
        
    def __del__(self):
        self.wait()

    def run(self):
        if self.action == CHECK:
            rc, msg = self.myLicense.checkLicense()
            self.apiCallComplete.emit(rc, msg)
        elif self.action == VERSION:
            rc, msg = self.myLicense.getVersion()
            self.apiCallComplete.emit(rc, msg)
        elif self.action == ACTIVATE:
            rc, msg = self.myLicense.activateLicense()
            self.apiCallComplete.emit(rc, msg)   
        elif self.action == DEACTIVATE:
            rc, msg = self.myLicense.deactivateLicense()
            self.apiCallComplete.emit(rc, msg)      
            
class License():
    def __init__(self, url=None, licenseKey=None, itemID=None):
        self.settings = QSettings()
        self.licenseKey = licenseKey
        self.url = url
        self.itemID = itemID
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.conn = http.client.HTTPConnection(url)           # You can use 80 (http) or 443 (https) "l2q.aa7.myftpupload.com:80"
        self.response = None
        self.responseDict = None
        self.responseStatus = None
        
    def activateLicense(self, ):
        try:
            rc = True
            self.responseDict = {}
            msg = "Check License status code 200"
            params = urllib.parse.urlencode({
            'edd_action': ACTIVATE ,  
            'item_id':self.itemID   ,                                    
            'license':self.licenseKey
            })
            # make the api call
            self.conn.request("POST", "/edd-sl", params, self.headers)
            # get the response
            self.response = self.conn.getresponse()
            # get the response status code
            self.responseStatus = self.response.status
            # return True if you get a 200, everything else is false
            if self.responseStatus != 200:
                rc = False
                msg = "Check License status code: {}".format(str(self.responseStatus))
            else:
                # get the JSON data
                strData = self.response.read().decode()
                self.responseDict = json.loads(strData)
            
        except Exception as e: 
            rc = False
            msg = "Check License failed: {}".format(str(e))
#            print(msg)
        
        finally:
            return rc,  msg
        
        
    def checkLicense(self, ):
        try:
            rc = True
            self.responseDict = {}
            msg = "Check License status code 200"
            params = urllib.parse.urlencode({
            'edd_action':CHECK ,  
            'item_id':self.itemID   ,                                    
            'license':self.licenseKey
            })
            # make the api call
            self.conn.request("POST", "/edd-sl", params, self.headers)
            # get the response
            self.response = self.conn.getresponse()
            # get the response status code
            self.responseStatus = self.response.status
            # return True if you get a 200, everything else is false
            if self.responseStatus != 200:
                rc = False
                msg = "Check License status code: {}".format(str(self.responseStatus))
            else:
                # get the JSON data
                strData = self.response.read().decode()
                # this is a hack to get only the json data
                strData = strData[strData.find("{"):strData.find("}")+1]
                self.responseDict = json.loads(strData)
            
        except Exception as e: 
            rc = False
            msg = "Check License failed: {}".format(str(e))
#            print(msg)
        
        finally:
            return rc,  msg
        
    def getVersion(self, ):
        try:
            rc = True
            self.responseDict = {}
            msg = "Get Version status code 200"
            params = urllib.parse.urlencode({
            'edd_action':VERSION ,  
            'item_id':self.itemID   ,                                    
            'license':self.licenseKey
            })
            # make the api call
            self.conn.request("POST", "/edd-sl", params, self.headers)
            # get the response
            self.response = self.conn.getresponse()
            # get the response status code
            self.responseStatus = self.response.status
            # return True if you get a 200, everything else is false
            if self.responseStatus != 200:
                rc = False
                msg = "Check License status code: {}".format(str(self.responseStatus))
            else:
                # get the JSON data
                strData = self.response.read().decode()
                self.responseDict = json.loads(strData)   
                
        except Exception as e: 
            rc = False
            msg = "Check License failed: {}".format(str(e))
#            print(msg)
        finally:
            return rc,  msg   
            
    def deactivateLicense(self, ):
        try:
            rc = True
            self.responseDict = {}
            msg = "Check License status code 200"
            params = urllib.parse.urlencode({
            'edd_action': DEACTIVATE ,  
            'item_id':self.itemID   ,                                    
            'license':self.licenseKey
            })
            # make the api call
            self.conn.request("POST", "/edd-sl", params, self.headers)
            # get the response
            self.response = self.conn.getresponse()
            # get the response status code
            self.responseStatus = self.response.status
            # return True if you get a 200, everything else is false
            if self.responseStatus != 200:
                rc = False
                msg = "Check License status code: {}".format(str(self.responseStatus))
            else:
                # get the JSON data
                strData = self.response.read().decode()
                self.responseDict = json.loads(strData)
            
        except Exception as e: 
            rc = False
            msg = "Check License failed: {}".format(str(e))
#            print(msg)
        
        finally:
            return rc,  msg
        
        
