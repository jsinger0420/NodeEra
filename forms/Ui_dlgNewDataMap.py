# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\John\Documents\NODEERA\V1\forms\dlgNewDataMap.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DlgNewDataMap(object):
    def setupUi(self, DlgNewDataMap):
        DlgNewDataMap.setObjectName("DlgNewDataMap")
        DlgNewDataMap.resize(400, 168)
        DlgNewDataMap.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(DlgNewDataMap)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(DlgNewDataMap)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtName = QtWidgets.QLineEdit(DlgNewDataMap)
        self.txtName.setObjectName("txtName")
        self.gridLayout.addWidget(self.txtName, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(DlgNewDataMap)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cboStrategy = QtWidgets.QComboBox(DlgNewDataMap)
        self.cboStrategy.setObjectName("cboStrategy")
        self.gridLayout.addWidget(self.cboStrategy, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DlgNewDataMap)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.label.setBuddy(self.txtName)

        self.retranslateUi(DlgNewDataMap)
        QtCore.QMetaObject.connectSlotsByName(DlgNewDataMap)

    def retranslateUi(self, DlgNewDataMap):
        _translate = QtCore.QCoreApplication.translate
        DlgNewDataMap.setWindowTitle(_translate("DlgNewDataMap", "Dialog"))
        self.label.setText(_translate("DlgNewDataMap", "Data Mapping Name:"))
        self.label_2.setText(_translate("DlgNewDataMap", "Data Mapping Strategy:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgNewDataMap = QtWidgets.QDialog()
    ui = Ui_DlgNewDataMap()
    ui.setupUi(DlgNewDataMap)
    DlgNewDataMap.show()
    sys.exit(app.exec_())

