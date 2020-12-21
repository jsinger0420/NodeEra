# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\FormMain.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormMain(object):
    def setupUi(self, FormMain):
        FormMain.setObjectName("FormMain")
        FormMain.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(FormMain)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.frmMain = QtWidgets.QFrame(FormMain)
        self.frmMain.setFrameShape(QtWidgets.QFrame.Box)
        self.frmMain.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmMain.setObjectName("frmMain")
        self.gridLayout.addWidget(self.frmMain, 0, 0, 1, 1)

        self.retranslateUi(FormMain)
        QtCore.QMetaObject.connectSlotsByName(FormMain)

    def retranslateUi(self, FormMain):
        _translate = QtCore.QCoreApplication.translate
        FormMain.setWindowTitle(_translate("FormMain", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormMain = QtWidgets.QWidget()
    ui = Ui_FormMain()
    ui.setupUi(FormMain)
    FormMain.show()
    sys.exit(app.exec_())
