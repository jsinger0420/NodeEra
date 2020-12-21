# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\John\SkyDrive\Documents\REPOS\NODEERA\forms\DropObjectDlg.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DropObjectDlg(object):
    def setupUi(self, DropObjectDlg):
        DropObjectDlg.setObjectName("DropObjectDlg")
        DropObjectDlg.resize(591, 137)
        DropObjectDlg.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(DropObjectDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.lblTitle = QtWidgets.QLabel(DropObjectDlg)
        self.lblTitle.setMinimumSize(QtCore.QSize(541, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")
        self.gridLayout.addWidget(self.lblTitle, 0, 0, 1, 2)
        self.label = QtWidgets.QLabel(DropObjectDlg)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.editObject = QtWidgets.QLineEdit(DropObjectDlg)
        self.editObject.setMinimumSize(QtCore.QSize(370, 0))
        self.editObject.setReadOnly(True)
        self.editObject.setObjectName("editObject")
        self.gridLayout.addWidget(self.editObject, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DropObjectDlg)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(DropObjectDlg)
        QtCore.QMetaObject.connectSlotsByName(DropObjectDlg)

    def retranslateUi(self, DropObjectDlg):
        _translate = QtCore.QCoreApplication.translate
        DropObjectDlg.setWindowTitle(_translate("DropObjectDlg", "Drop Schema Object"))
        self.lblTitle.setText(_translate("DropObjectDlg", "DropObjectDlg"))
        self.label.setText(_translate("DropObjectDlg", "Click OK to drop this schema object:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DropObjectDlg = QtWidgets.QDialog()
    ui = Ui_DropObjectDlg()
    ui.setupUi(DropObjectDlg)
    DropObjectDlg.show()
    sys.exit(app.exec_())

