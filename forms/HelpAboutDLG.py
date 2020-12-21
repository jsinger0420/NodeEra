# -*- coding: utf-8 -*-

"""
Module implementing HelpAboutDLG.
    Copyright: SingerLinks Consulting LLC dba NodeEra Software 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""
import sys
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5.sip import SIP_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QT_VERSION_STR

from .Ui_HelpAboutDLG import Ui_HelpAboutDLG

import icons.icons_rc

class HelpAboutDLG(QDialog, Ui_HelpAboutDLG):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(HelpAboutDLG, self).__init__(parent)
        self.setupUi(self)
        pixmap = QPixmap(":/FILE/FILE/NodeEraFullLogo.png")
        myScaledPixmap = pixmap.scaled(self.lblIcon.size(), Qt.KeepAspectRatio)
        self.lblIcon.setPixmap(myScaledPixmap)
        
        self.txtProduct.setText(QtWidgets.qApp.applicationName())
        self.txtVersion.setText(QtWidgets.qApp.applicationVersion())
        
        self.txtAbout.setText('''
NodeEra is the worlds leading property graph database design and management tool supporting the Neo4j Graph Database.
        
Copyright 2019 SingerLinks ConsultinQApplicationg LLC dba NodeEra Software all rights reserved.
        
Your use of this software is governed by the license agreement which can be viewed at www.noderapro.com/nodeera-software-license/

''' ) 
        self.txtAbout.append("running on platform: {}".format(sys.platform) )
#        self.txtAbout.append( "current style is: {}".format(QApplication().style().objectName())) 
        self.txtAbout.append( "Python version: {}".format(sys.version)) 
        self.txtAbout.append( "Qt version: {}".format(QT_VERSION_STR)) 
        self.txtAbout.append( "PyQt version: {}".format(PYQT_VERSION_STR)) 
        self.txtAbout.append( "sip version: {}".format(SIP_VERSION_STR)) 
    

    @pyqtSlot()
    def on_btnClose_clicked(self):
        """
        User clicks the Close button
        """
        QDialog.accept(self)

