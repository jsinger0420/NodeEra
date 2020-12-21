#!/usr/bin/env python3
'''    
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
'''
from PyQt5.QtCore import QSettings
from core.helper import Helper
#############################################################################
# this class defines basic info about a page widget
#############################################################################
class PageItem():
    def __init__(self, neoConName=None, actionButton=None, pageWidget=None, pageWidgetIndex=None ):
        self.settings = QSettings()     
        self.helper = Helper()
        # the name of the neocon for this page
        self.neoConName = neoConName
        # see if we need to prompt for the password
        self.promptPW = None
        self.checkPW()
        # the qaction on the menubar
        self.actionButton = actionButton
        self.pageWidget = pageWidget
        self.pageWidgetIndex = pageWidgetIndex
        return

    def checkPW(self, ):
        '''If the connection is prompt for password, then prompt until the user enters something.
        '''
        # get the neocon dictionary
        neoDict=self.settings.value("NeoCon/connection/{}".format(self.neoConName))
        if not neoDict is None:
            if neoDict["prompt"] == "True":
                # prompt for a password if needed and save what the user enters
                pw = ''
                while len(pw) < 1:
                    pw = self.helper.passwordPrompt(conName=self.neoConName, conURL=neoDict["URL"])
                    if not pw is None:
                        if len(pw) > 0:
                            # save the encrypted password in the page item so it's ready to be used by any function
                            self.promptPW = self.helper.putText(pw)
                        else:
                            self.helper.displayErrMsg("Prompt Password", "You must enter a password.")

                
            
