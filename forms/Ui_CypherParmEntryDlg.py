# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\CypherParmEntryDlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CypherParmEntryDlg(object):
    def setupUi(self, CypherParmEntryDlg):
        CypherParmEntryDlg.setObjectName("CypherParmEntryDlg")
        CypherParmEntryDlg.resize(816, 317)
        CypherParmEntryDlg.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(CypherParmEntryDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(CypherParmEntryDlg)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.gridParms = QtWidgets.QTableView(self.groupBox)
        self.gridParms.setObjectName("gridParms")
        self.gridLayout.addWidget(self.gridParms, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.frame = QtWidgets.QFrame(CypherParmEntryDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 40))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(343, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnRunQuery = QtWidgets.QPushButton(self.frame)
        self.btnRunQuery.setObjectName("btnRunQuery")
        self.horizontalLayout.addWidget(self.btnRunQuery)
        self.btnCancel = QtWidgets.QPushButton(self.frame)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        spacerItem1 = QtWidgets.QSpacerItem(342, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(CypherParmEntryDlg)
        QtCore.QMetaObject.connectSlotsByName(CypherParmEntryDlg)

    def retranslateUi(self, CypherParmEntryDlg):
        _translate = QtCore.QCoreApplication.translate
        CypherParmEntryDlg.setWindowTitle(_translate("CypherParmEntryDlg", "Cypher Parameter Entry"))
        self.groupBox.setTitle(_translate("CypherParmEntryDlg", "Enter Parameter Values"))
        self.btnRunQuery.setText(_translate("CypherParmEntryDlg", "Run Query"))
        self.btnCancel.setText(_translate("CypherParmEntryDlg", "Cancel Query"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CypherParmEntryDlg = QtWidgets.QDialog()
    ui = Ui_CypherParmEntryDlg()
    ui.setupUi(CypherParmEntryDlg)
    CypherParmEntryDlg.show()
    sys.exit(app.exec_())

