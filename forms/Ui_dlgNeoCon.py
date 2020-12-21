# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\forms\dlgNeoCon.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgNeoCons(object):
    def setupUi(self, dlgNeoCons):
        dlgNeoCons.setObjectName("dlgNeoCons")
        dlgNeoCons.resize(714, 493)
        dlgNeoCons.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(dlgNeoCons)
        self.gridLayout.setObjectName("gridLayout")
        self.boxConnections = QtWidgets.QGroupBox(dlgNeoCons)
        self.boxConnections.setObjectName("boxConnections")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.boxConnections)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridNeoCons = QtWidgets.QTableView(self.boxConnections)
        self.gridNeoCons.setCornerButtonEnabled(False)
        self.gridNeoCons.setObjectName("gridNeoCons")
        self.gridNeoCons.verticalHeader().setDefaultSectionSize(50)
        self.gridNeoCons.verticalHeader().setMinimumSectionSize(50)
        self.horizontalLayout.addWidget(self.gridNeoCons)
        self.frame = QtWidgets.QFrame(self.boxConnections)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnAdd = QtWidgets.QPushButton(self.frame)
        self.btnAdd.setObjectName("btnAdd")
        self.verticalLayout.addWidget(self.btnAdd)
        self.btnEdit = QtWidgets.QPushButton(self.frame)
        self.btnEdit.setObjectName("btnEdit")
        self.verticalLayout.addWidget(self.btnEdit)
        self.btnTest = QtWidgets.QPushButton(self.frame)
        self.btnTest.setObjectName("btnTest")
        self.verticalLayout.addWidget(self.btnTest)
        self.btnRemove = QtWidgets.QPushButton(self.frame)
        self.btnRemove.setObjectName("btnRemove")
        self.verticalLayout.addWidget(self.btnRemove)
        spacerItem = QtWidgets.QSpacerItem(20, 247, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.frame)
        self.gridLayout.addWidget(self.boxConnections, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgNeoCons)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(dlgNeoCons)
        self.buttonBox.accepted.connect(dlgNeoCons.accept)
        self.buttonBox.rejected.connect(dlgNeoCons.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgNeoCons)

    def retranslateUi(self, dlgNeoCons):
        _translate = QtCore.QCoreApplication.translate
        dlgNeoCons.setWindowTitle(_translate("dlgNeoCons", "Neo4j Connection Manager"))
        self.boxConnections.setTitle(_translate("dlgNeoCons", "Neo4j Connections"))
        self.btnAdd.setText(_translate("dlgNeoCons", "Add..."))
        self.btnEdit.setText(_translate("dlgNeoCons", "Edit..."))
        self.btnTest.setText(_translate("dlgNeoCons", "Test..."))
        self.btnRemove.setText(_translate("dlgNeoCons", "Remove"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlgNeoCons = QtWidgets.QDialog()
    ui = Ui_dlgNeoCons()
    ui.setupUi(dlgNeoCons)
    dlgNeoCons.show()
    sys.exit(app.exec_())

