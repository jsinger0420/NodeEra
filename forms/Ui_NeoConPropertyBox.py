# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\NeoConPropertyBox.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NeoConPropertyBox(object):
    def setupUi(self, NeoConPropertyBox):
        NeoConPropertyBox.setObjectName("NeoConPropertyBox")
        NeoConPropertyBox.setWindowModality(QtCore.Qt.ApplicationModal)
        NeoConPropertyBox.resize(474, 309)
        NeoConPropertyBox.setSizeGripEnabled(False)
        NeoConPropertyBox.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(NeoConPropertyBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.boxConnection = QtWidgets.QGroupBox(NeoConPropertyBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boxConnection.sizePolicy().hasHeightForWidth())
        self.boxConnection.setSizePolicy(sizePolicy)
        self.boxConnection.setObjectName("boxConnection")
        self.gridLayout = QtWidgets.QGridLayout(self.boxConnection)
        self.gridLayout.setObjectName("gridLayout")
        self.cboScheme = QtWidgets.QComboBox(self.boxConnection)
        self.cboScheme.setMinimumSize(QtCore.QSize(101, 0))
        self.cboScheme.setObjectName("cboScheme")
        self.cboScheme.addItem("")
        self.cboScheme.addItem("")
        self.gridLayout.addWidget(self.cboScheme, 0, 2, 1, 1)
        self.editPort = QtWidgets.QLineEdit(self.boxConnection)
        self.editPort.setObjectName("editPort")
        self.gridLayout.addWidget(self.editPort, 3, 1, 1, 2)
        self.chkSecureCon = QtWidgets.QCheckBox(self.boxConnection)
        self.chkSecureCon.setChecked(False)
        self.chkSecureCon.setObjectName("chkSecureCon")
        self.gridLayout.addWidget(self.chkSecureCon, 1, 0, 1, 3)
        self.labelPort = QtWidgets.QLabel(self.boxConnection)
        self.labelPort.setObjectName("labelPort")
        self.gridLayout.addWidget(self.labelPort, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.boxConnection)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.labelScheme = QtWidgets.QLabel(self.boxConnection)
        self.labelScheme.setObjectName("labelScheme")
        self.gridLayout.addWidget(self.labelScheme, 0, 0, 1, 2)
        self.editHostName = QtWidgets.QLineEdit(self.boxConnection)
        self.editHostName.setObjectName("editHostName")
        self.gridLayout.addWidget(self.editHostName, 2, 1, 1, 3)
        self.verticalLayout.addWidget(self.boxConnection)
        self.boxUser = QtWidgets.QGroupBox(NeoConPropertyBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boxUser.sizePolicy().hasHeightForWidth())
        self.boxUser.setSizePolicy(sizePolicy)
        self.boxUser.setObjectName("boxUser")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.boxUser)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lblUserid = QtWidgets.QLabel(self.boxUser)
        self.lblUserid.setObjectName("lblUserid")
        self.gridLayout_2.addWidget(self.lblUserid, 0, 0, 1, 1)
        self.editUserid = QtWidgets.QLineEdit(self.boxUser)
        self.editUserid.setObjectName("editUserid")
        self.gridLayout_2.addWidget(self.editUserid, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(212, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 2)
        self.lblPassWord = QtWidgets.QLabel(self.boxUser)
        self.lblPassWord.setObjectName("lblPassWord")
        self.gridLayout_2.addWidget(self.lblPassWord, 1, 0, 1, 1)
        self.editPassWord = QtWidgets.QLineEdit(self.boxUser)
        self.editPassWord.setEchoMode(QtWidgets.QLineEdit.Password)
        self.editPassWord.setObjectName("editPassWord")
        self.gridLayout_2.addWidget(self.editPassWord, 1, 1, 1, 1)
        self.btnShow = QtWidgets.QPushButton(self.boxUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnShow.sizePolicy().hasHeightForWidth())
        self.btnShow.setSizePolicy(sizePolicy)
        self.btnShow.setMinimumSize(QtCore.QSize(50, 0))
        self.btnShow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btnShow.setObjectName("btnShow")
        self.gridLayout_2.addWidget(self.btnShow, 1, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(156, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 3, 1, 1)
        self.chkPromptForPW = QtWidgets.QCheckBox(self.boxUser)
        self.chkPromptForPW.setObjectName("chkPromptForPW")
        self.gridLayout_2.addWidget(self.chkPromptForPW, 2, 0, 1, 2)
        self.verticalLayout.addWidget(self.boxUser)
        self.frame = QtWidgets.QFrame(NeoConPropertyBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(109, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.okButton = QtWidgets.QPushButton(self.frame)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(self.frame)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addWidget(self.frame)
        self.labelPort.setBuddy(self.editPort)
        self.label.setBuddy(self.editHostName)
        self.labelScheme.setBuddy(self.editHostName)
        self.lblUserid.setBuddy(self.editUserid)
        self.lblPassWord.setBuddy(self.editPassWord)

        self.retranslateUi(NeoConPropertyBox)
        QtCore.QMetaObject.connectSlotsByName(NeoConPropertyBox)
        NeoConPropertyBox.setTabOrder(self.cboScheme, self.chkSecureCon)
        NeoConPropertyBox.setTabOrder(self.chkSecureCon, self.editHostName)
        NeoConPropertyBox.setTabOrder(self.editHostName, self.editPort)
        NeoConPropertyBox.setTabOrder(self.editPort, self.editUserid)
        NeoConPropertyBox.setTabOrder(self.editUserid, self.editPassWord)
        NeoConPropertyBox.setTabOrder(self.editPassWord, self.btnShow)
        NeoConPropertyBox.setTabOrder(self.btnShow, self.chkPromptForPW)
        NeoConPropertyBox.setTabOrder(self.chkPromptForPW, self.okButton)
        NeoConPropertyBox.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, NeoConPropertyBox):
        _translate = QtCore.QCoreApplication.translate
        NeoConPropertyBox.setWindowTitle(_translate("NeoConPropertyBox", "Neo4j Connection"))
        self.boxConnection.setTitle(_translate("NeoConPropertyBox", "Connection"))
        self.cboScheme.setItemText(0, _translate("NeoConPropertyBox", "bolt"))
        self.cboScheme.setItemText(1, _translate("NeoConPropertyBox", "bolt+routing"))
        self.chkSecureCon.setText(_translate("NeoConPropertyBox", "Use Secure Connection"))
        self.labelPort.setText(_translate("NeoConPropertyBox", "Port:"))
        self.label.setText(_translate("NeoConPropertyBox", "Host Name:"))
        self.labelScheme.setText(_translate("NeoConPropertyBox", "Connection Type:"))
        self.boxUser.setTitle(_translate("NeoConPropertyBox", "User"))
        self.lblUserid.setText(_translate("NeoConPropertyBox", "User ID:"))
        self.lblPassWord.setText(_translate("NeoConPropertyBox", "Password:"))
        self.btnShow.setText(_translate("NeoConPropertyBox", "Show"))
        self.chkPromptForPW.setText(_translate("NeoConPropertyBox", "Prompt For Password"))
        self.okButton.setText(_translate("NeoConPropertyBox", "&OK"))
        self.cancelButton.setText(_translate("NeoConPropertyBox", "&Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NeoConPropertyBox = QtWidgets.QDialog()
    ui = Ui_NeoConPropertyBox()
    ui.setupUi(NeoConPropertyBox)
    NeoConPropertyBox.show()
    sys.exit(app.exec_())
