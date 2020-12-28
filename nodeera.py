#!/usr/bin/python
''' 
    UC-00 Startup Python file
    Author: John Singer
    Copyright: SingerLinks Consulting LLC 2018 - all rights reserved
'''
import os
import logging
import argparse
import sys
import time
from pathlib import Path

from datetime import datetime
from core.userExceptions import loggingsetupError
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from forms.main import NodeeraMain
from PyQt5.sip import SIP_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QT_VERSION_STR


def parseCommandLine():
    '''
    parse the command line parameters
    '''
    parser = argparse.ArgumentParser(description="NodeEra - The best Neo4j property graph design tool in the universe")
    parser.add_argument("-l","--logdir",  help="The directory location to place the log file.")
    parser.add_argument("-d", "--debug", help="Generate more detail in the log file.", action="store_true")
    parser.add_argument("-b", help="Enable beta functionality.", action="store_true")    
    parser.parse_args()
    args = parser.parse_args()
    return args

def setupLogging(logdir):
    '''
    start logging and prune old log files
    '''
    logfile = logdir + r"/NodeEra_" + '{:%Y-%m-%d-%H%M%S}'.format(datetime.now()) + ".log"
    FORMAT='%(asctime)s %(levelname)s:%(message)s'  
    try:
        logging.basicConfig(filename=logfile, level=logging.INFO, format=FORMAT)
        # delete log files older than 30 days
        deleteLogFiles(path=logdir, numDays=30)
    except Exception as e:
        raise loggingsetupError(logfile,"Error Creating The Log File - {}".format(str(e)))    

def deleteLogFiles(path=None, numDays=None):
    '''
    Delete log files older than numDays ago.
    '''
    try:
        criticalTime = time.time() - (numDays * 86400)
        for f in Path(path).glob('*.log'):
            f = os.path.join(path, f)
            if os.stat(f).st_mtime < criticalTime:
                if os.path.isfile(f):
                    os.remove(f)
    except Exception as e:
        raise loggingsetupError(path,"Error Deleting Old Log Files - {}".format(str(e)))    
    
def logMsg(msg):
    if logging:
        logging.info(msg)

    
def main():
    # parse the command line
    args = parseCommandLine()

    # create app object and initialize it
    app = QApplication(sys.argv)
    app.setOrganizationName("NodeEra Software")
    app.setOrganizationDomain("singerlinks.com")

    app.setApplicationName("NodeEra")
    app.setApplicationVersion("2020.12.01")
    app.setStyleSheet(
    """
    QToolButton#conbtn { background:white }
    QToolBar {spacing:4px;}
    QTableView {selection-background-color:LightSkyBlue;
                      alternate-background-color: Gainsboro; 
                      background-color: White; 
                    }
    QHeaderView::section
        {
        spacing: 10px;
        background-color:LightSteelBlue;
        color: black;
        margin: 10px;
        text-align: right;
        font-family: arial;
        font-size:12px;
        font-weight: 600;
        }
        
    """
    )
    #keep this print statement
    print("Starting NodeEra...")
    
    # get the settings
    settings = QSettings()
    # get logging directory, set it to nodeera execution path if no setting exists
    logDir = None
    try:    
        logDir = settings.value("Default/LoggingPath")
        if logDir is None:
            logDir = os.getcwd()
            logDir = os.path.realpath(os.path.abspath(logDir))
            settings.setValue("Default/LoggingPath",logDir)
    except:
        logDir = os.getcwd()
        logDir = os.path.realpath(os.path.abspath(logDir))
        settings.setValue("Default/LoggingPath",logDir)
    # start logging
    try:
        if not logDir is None:         
            print("logdir: {}".format(logDir))
            setupLogging(logDir)    
            logMsg("Logging to: {}".format(logDir))
        else:
            print("unable to start logging")
    except loggingsetupError as inst:
        # logging setup failed so print to stdout
        print("{}: {} - logging setup failed".format(inst.args[1], inst.args[0]))
    except Exception as e: 
        # unknown error so print to stdout
        print("Error during logging setup - {}".format(repr(e)))        
    finally:
        logMsg("Command Line Parameters: {}".format(str(args)))    
    
    logMsg("running on platform: {}".format(sys.platform) )
    logMsg( "current style is: {}".format(app.style().objectName())) 
    logMsg( "Python version: {}".format(sys.version)) 
    logMsg( "Qt version: {}".format(QT_VERSION_STR)) 
    logMsg( "PyQt version: {}".format(PYQT_VERSION_STR)) 
    logMsg( "sip version: {}".format(SIP_VERSION_STR)) 
    
    logMsg("Launch Main Window")
    # start the main window running
    wnd = NodeeraMain()
    wnd.show()    
    sys.exit(app.exec_())
        


if __name__ == '__main__':
    main()
