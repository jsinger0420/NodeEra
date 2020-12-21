# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\John\SkyDrive\Documents\REPOS\NODEERA\forms\DataGrid.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DataGrid(object):
    def setupUi(self, DataGrid):
        DataGrid.setObjectName("DataGrid")
        DataGrid.resize(814, 455)
        self.verticalLayout = QtWidgets.QVBoxLayout(DataGrid)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(DataGrid)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnExport = QtWidgets.QPushButton(self.frame)
        self.btnExport.setObjectName("btnExport")
        self.horizontalLayout.addWidget(self.btnExport)
        self.btnBegin = QtWidgets.QPushButton(self.frame)
        self.btnBegin.setObjectName("btnBegin")
        self.horizontalLayout.addWidget(self.btnBegin)
        self.btnBack = QtWidgets.QPushButton(self.frame)
        self.btnBack.setObjectName("btnBack")
        self.horizontalLayout.addWidget(self.btnBack)
        self.btnForward = QtWidgets.QPushButton(self.frame)
        self.btnForward.setObjectName("btnForward")
        self.horizontalLayout.addWidget(self.btnForward)
        self.btnEnd = QtWidgets.QPushButton(self.frame)
        self.btnEnd.setObjectName("btnEnd")
        self.horizontalLayout.addWidget(self.btnEnd)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(303, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(DataGrid)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridNodeWidget = QtWidgets.QTableView(self.frame_2)
        self.gridNodeWidget.setObjectName("gridNodeWidget")
        self.horizontalLayout_2.addWidget(self.gridNodeWidget)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(DataGrid)
        QtCore.QMetaObject.connectSlotsByName(DataGrid)

    def retranslateUi(self, DataGrid):
        _translate = QtCore.QCoreApplication.translate
        DataGrid.setWindowTitle(_translate("DataGrid", "Form"))
        self.btnExport.setText(_translate("DataGrid", "Export..."))
        self.btnBegin.setText(_translate("DataGrid", "<<"))
        self.btnBack.setText(_translate("DataGrid", "<"))
        self.btnForward.setText(_translate("DataGrid", ">"))
        self.btnEnd.setText(_translate("DataGrid", ">>"))
        self.pushButton.setText(_translate("DataGrid", "Refresh Data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DataGrid = QtWidgets.QWidget()
    ui = Ui_DataGrid()
    ui.setupUi(DataGrid)
    DataGrid.show()
    sys.exit(app.exec_())

