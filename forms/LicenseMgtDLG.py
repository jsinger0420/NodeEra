# -*- coding: utf-8 -*-

"""
Module implementing LicenseMgtDLG.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
import logging

from PyQt5.QtCore import pyqtSlot, QSettings, Qt
from PyQt5.QtWidgets import QDialog, QApplication

from core.helper import Helper
from core.License import License, EDDAPI
from .Ui_LicenseMgtDLG import Ui_LicenseMgtDLG

# license api commands
ACTIVATE='activate_license'
CHECK='check_license'
VERSION='get_version'
DEACTIVATE='deactivate_license'


class LicenseMgtDLG(QDialog, Ui_LicenseMgtDLG):
    """
    This is the license management dialog box. 
    It is accessed from the Settings/License Management... dropdown menu
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(LicenseMgtDLG, self).__init__(parent)
        self.setupUi(self)
        self.settings = QSettings()
        self.helper = Helper()
        
        # get existing license data from settings
        try:
            self.expirationDate = self.helper.getText(self.settings.value("License/expirationDate"))
#            self.expirationDate = self.settings.value("License/expirationDate")
        except:
            self.expirationDate = 'No expiration date set'
            self.settings.setValue("License/expirationDate",self.helper.putText(self.expirationDate))
        try:
            self.currentVersion = self.settings.value("License/currentVersion")
        except:
            self.currentVersion = "no version in settings"    
        try:
            self.licenseKey = self.settings.value("License/Key")
        except:
            self.licenseKey = "no key in settings"    
        try:
            self.itemID = self.settings.value("License/ItemID")
        except:
            self.itemID = "no id in settings"    
        try:
            self.licenseURL = self.settings.value("License/URL")
        except:
            self.licenseURL = "no URL in settings"
        
        # disable all buttons until check license is finished
        self.disableButtons()
        
        # more UI setups
        self.txtLicenseKey.setEnabled(False)
        self.txtLicenseKey.setText(self.licenseKey)
        self.lblCurrentVersion.setText(self.currentVersion)
        
        # remember what api action is currently being run
        self.currentAction = None
        
        # license status from api call
        self.licenseStatus = "No Status"
        
        # create the license object - only works if the qsettings has the license data, otherwise user must activate license
        self.createLicense()
        
        # start the thread that calls the check license api. only works if the license object was created.
        self.getLicenseDataStart(action=CHECK)
        

    def logMsg(self, msg):
        if logging:
            logging.info(msg)

    def disableButtons(self, ):
        # disable all buttons until check license is finished
        self.btnCheck.setEnabled(False)
        self.btnActivateLicKey.setEnabled(False)
        self.btnDeactivateLicKey.setEnabled(False)
        
    def adjustButtons(self, ):
        '''
        enable or disable the command buttons and license key text box depending on the status
        '''
        if self.licenseStatus == "valid":
            self.btnCheck.setEnabled(True)
            self.btnActivateLicKey.setEnabled(False)
            self.btnDeactivateLicKey.setEnabled(True)
            self.txtLicenseKey.setEnabled(False)
        elif self.licenseStatus in ["deactivated", "inactive", "No Status", "disabled"]:
            self.btnCheck.setEnabled(False)
            self.btnActivateLicKey.setEnabled(True)
            self.btnDeactivateLicKey.setEnabled(True)
            self.txtLicenseKey.setEnabled(True)

    def createLicense(self, ):
        # create the license object if we have a key
        if (self.licenseKey is not None):
            self.myLicense = License(url=self.licenseURL, licenseKey=self.licenseKey, itemID=self.itemID)
        else:
            self.myLicense = None
        
    def getLicenseDataStart(self, action=None):
        if not self.myLicense is None:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.currentAction = action
            self.logMsg("Begin License API call - {}".format(action))
            # create the thread
            self.checkLicenseThread = EDDAPI(self.myLicense, action)
            # connect slots
            self.checkLicenseThread.apiCallComplete.connect(self.getLicenseReturnData)
            self.checkLicenseThread.finished.connect(self.getLicenseDataFinished)
            self.checkLicenseThread.start()
            self.lblProgress.setText("Retrieving license data...")
        else:
            # enable/disable command buttons
            self.adjustButtons()            


    def getLicenseDataFinished(self, ):
        self.logMsg("End License API call - {}".format(self.currentAction))
        # if the last call was an activation, then we have to retrieve the results and display them
        if self.currentAction == ACTIVATE:
            self.getLicenseDataStart(action=CHECK)
        
        # clean up
        QApplication.restoreOverrideCursor()
        self.currentAction = None
        # enable/disable command buttons
        self.adjustButtons()

    @pyqtSlot(bool, str)
    def getLicenseReturnData(self, rc, msg ):
        if rc == True:
            self.lblProgress.setText("License Data Retrieved")
            if self.currentAction == CHECK:
                self.lblProductName.setText(self.myLicense.responseDict.get("item_name", "No Product Name"))
                self.lblLicensedTo.setText(self.myLicense.responseDict.get("customer_name", "No Customer Name"))
                self.lblLicensedToEmail.setText(self.myLicense.responseDict.get("customer_email", "No Customer Email"))
                self.lblExpiration.setText(self.myLicense.responseDict.get("expires", "No expiration date set"))
                # see if the expry date has changed and update the expry date in settings.
                if self.expirationDate != self.myLicense.responseDict.get("expires", "No expiration date set"):
                    self.settings.setValue("License/expirationDate",self.helper.putText(self.myLicense.responseDict.get("expires", "No expiration date set")))
                self.lblLicenseStatus.setText(self.myLicense.responseDict.get("license", "No Status"))
                self.licenseStatus = self.myLicense.responseDict.get("license", "No Status")
            elif self.currentAction == VERSION:
                # get new version.  this also gets url links to downloads etc.  but we aren't using them now
                self.lblAvailableVersion.setText(self.myLicense.responseDict.get("stable_version", "No Product Name"))
            elif self.currentAction == ACTIVATE:       
                if self.myLicense.responseDict.get("success", False) == True:
                    self.licenseStatus = self.myLicense.responseDict.get("license", "No Status")
                    self.lblLicenseStatus.setText(self.licenseStatus)
                    self.settings.setValue("License/Key",self.licenseKey)
                    # save new expiration date in settings
                    self.expirationDate = self.myLicense.responseDict.get("expires", "No expiration date set")
                    self.settings.setValue("License/expirationDate",self.helper.putText(self.expirationDate))
                    self.lblExpiration.setText(self.expirationDate)                
                else:
                    errorStatus = self.myLicense.responseDict.get("success", "no status")
                    errorMsg = self.myLicense.responseDict.get("error", "No error message")
                    self.helper.displayErrMsg("Activate License Error",  "Activate status: {} Activate Error: {}".format(errorStatus, errorMsg))
            elif self.currentAction == DEACTIVATE:       
                if self.myLicense.responseDict.get("success", False) == True:
                    self.licenseStatus = self.myLicense.responseDict.get("license", "No Status")
                    self.lblLicenseStatus.setText(self.licenseStatus)
                    self.lblExpiration.setText(self.expirationDate)                
                else:
                    errorStatus = self.myLicense.responseDict.get("success", "no status")
                    errorMsg = self.myLicense.responseDict.get("error", "No error message")
                    self.helper.displayErrMsg("Deactivate License Error",  "Deactivate status: {} Deactivate Error: {}".format(errorStatus, errorMsg))

        else:
            errorStatus = self.myLicense.responseDict.get("success", "no status")
            errorMsg = self.myLicense.responseDict.get("error", "No error message")
            self.lblProgress.setText("Error retrieving license data")
            self.helper.displayErrMsg("Get License Data Error",  "Status: {} Error: {}".format(errorStatus, errorMsg))

        
    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        User clicks the Close button
        """
        QDialog.accept(self)
    
    @pyqtSlot()
    def on_btnCheck_clicked(self):
        """
        User clicks the Check Version Button.
        """
        self.disableButtons()
        # make the api call
        self.getLicenseDataStart(action=VERSION)
        
        
    @pyqtSlot()
    def on_btnActivateLicKey_clicked(self):
        """
        User clicks the Activate License button
        """
        # make sure they've entered a license key
        if self.helper.NoTextValueError(self.txtLicenseKey.text(), "You must enter a license key."):
            return
            
        self.disableButtons()    
        # create a license object
        self.licenseKey = self.txtLicenseKey.text()
        self.createLicense()
        
        # activate the key
        self.getLicenseDataStart(action=ACTIVATE)
        
    
    @pyqtSlot()
    def on_btnDeactivateLicKey_clicked(self):
        """
        User clicks the Deactivate License button
        """
        self.disableButtons()
        # make the api call
        self.getLicenseDataStart(action=DEACTIVATE)
        
