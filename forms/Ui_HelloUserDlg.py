# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\HelloUserDlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HelloUserDlg(object):
    def setupUi(self, HelloUserDlg):
        HelloUserDlg.setObjectName("HelloUserDlg")
        HelloUserDlg.resize(455, 304)
        HelloUserDlg.setSizeGripEnabled(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(HelloUserDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblHello = QtWidgets.QLabel(HelloUserDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblHello.sizePolicy().hasHeightForWidth())
        self.lblHello.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblHello.setFont(font)
        self.lblHello.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHello.setObjectName("lblHello")
        self.verticalLayout.addWidget(self.lblHello)
        self.txtMessageArea = QtWidgets.QTextBrowser(HelloUserDlg)
        self.txtMessageArea.setObjectName("txtMessageArea")
        self.verticalLayout.addWidget(self.txtMessageArea)
        self.frame = QtWidgets.QFrame(HelloUserDlg)
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
        spacerItem = QtWidgets.QSpacerItem(162, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnClose = QtWidgets.QPushButton(self.frame)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        spacerItem1 = QtWidgets.QSpacerItem(162, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(HelloUserDlg)
        QtCore.QMetaObject.connectSlotsByName(HelloUserDlg)

    def retranslateUi(self, HelloUserDlg):
        _translate = QtCore.QCoreApplication.translate
        HelloUserDlg.setWindowTitle(_translate("HelloUserDlg", "NodeEra Startup"))
        self.lblHello.setText(_translate("HelloUserDlg", "Welcome To NodeEra"))
        self.btnClose.setText(_translate("HelloUserDlg", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HelloUserDlg = QtWidgets.QDialog()
    ui = Ui_HelloUserDlg()
    ui.setupUi(HelloUserDlg)
    HelloUserDlg.show()
    sys.exit(app.exec_())

