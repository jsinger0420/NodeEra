# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\forms\OnlineHelpDLG.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OnlineHelpDLG(object):
    def setupUi(self, OnlineHelpDLG):
        OnlineHelpDLG.setObjectName("OnlineHelpDLG")
        OnlineHelpDLG.resize(400, 300)
        OnlineHelpDLG.setSizeGripEnabled(True)
        self.btnClose = QtWidgets.QPushButton(OnlineHelpDLG)
        self.btnClose.setGeometry(QtCore.QRect(160, 270, 75, 23))
        self.btnClose.setObjectName("btnClose")
        self.label = QtWidgets.QLabel(OnlineHelpDLG)
        self.label.setGeometry(QtCore.QRect(10, 20, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.lblHelp1 = QtWidgets.QLabel(OnlineHelpDLG)
        self.lblHelp1.setGeometry(QtCore.QRect(80, 100, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lblHelp1.setFont(font)
        self.lblHelp1.setObjectName("lblHelp1")

        self.retranslateUi(OnlineHelpDLG)
        QtCore.QMetaObject.connectSlotsByName(OnlineHelpDLG)

    def retranslateUi(self, OnlineHelpDLG):
        _translate = QtCore.QCoreApplication.translate
        OnlineHelpDLG.setWindowTitle(_translate("OnlineHelpDLG", "Online Help"))
        self.btnClose.setText(_translate("OnlineHelpDLG", "Close"))
        self.label.setText(_translate("OnlineHelpDLG", "NodeEra Help"))
        self.lblHelp1.setText(_translate("OnlineHelpDLG", "www.singerlinks.comNodeEraHelp"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OnlineHelpDLG = QtWidgets.QDialog()
    ui = Ui_OnlineHelpDLG()
    ui.setupUi(OnlineHelpDLG)
    OnlineHelpDLG.show()
    sys.exit(app.exec_())

