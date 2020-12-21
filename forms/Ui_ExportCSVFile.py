# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\forms\ExportCSVFile.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DlgExportCSV(object):
    def setupUi(self, DlgExportCSV):
        DlgExportCSV.setObjectName("DlgExportCSV")
        DlgExportCSV.resize(444, 416)
        DlgExportCSV.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(DlgExportCSV)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frmCSVWidget = QtWidgets.QFrame(DlgExportCSV)
        self.frmCSVWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frmCSVWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frmCSVWidget.setObjectName("frmCSVWidget")
        self.verticalLayout.addWidget(self.frmCSVWidget)
        self.frame = QtWidgets.QFrame(DlgExportCSV)
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
        spacerItem = QtWidgets.QSpacerItem(116, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnExport = QtWidgets.QPushButton(self.frame)
        self.btnExport.setObjectName("btnExport")
        self.horizontalLayout.addWidget(self.btnExport)
        self.btnCancel = QtWidgets.QPushButton(self.frame)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        spacerItem1 = QtWidgets.QSpacerItem(116, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(DlgExportCSV)
        QtCore.QMetaObject.connectSlotsByName(DlgExportCSV)

    def retranslateUi(self, DlgExportCSV):
        _translate = QtCore.QCoreApplication.translate
        DlgExportCSV.setWindowTitle(_translate("DlgExportCSV", "Export CSV File"))
        self.btnExport.setText(_translate("DlgExportCSV", "Export File"))
        self.btnCancel.setToolTip(_translate("DlgExportCSV", "Cancel the File Export"))
        self.btnCancel.setText(_translate("DlgExportCSV", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgExportCSV = QtWidgets.QDialog()
    ui = Ui_DlgExportCSV()
    ui.setupUi(DlgExportCSV)
    DlgExportCSV.show()
    sys.exit(app.exec_())

