# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\GetCursorDlg.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GetCursorDlg(object):
    def setupUi(self, GetCursorDlg):
        GetCursorDlg.setObjectName("GetCursorDlg")
        GetCursorDlg.resize(221, 119)
        GetCursorDlg.setSizeGripEnabled(False)
        GetCursorDlg.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GetCursorDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(GetCursorDlg)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lblElapsedTime = QtWidgets.QLabel(GetCursorDlg)
        self.lblElapsedTime.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblElapsedTime.setFont(font)
        self.lblElapsedTime.setText("")
        self.lblElapsedTime.setAlignment(QtCore.Qt.AlignCenter)
        self.lblElapsedTime.setObjectName("lblElapsedTime")
        self.verticalLayout.addWidget(self.lblElapsedTime)
        self.frame = QtWidgets.QFrame(GetCursorDlg)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnCancel = QtWidgets.QPushButton(self.frame)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(GetCursorDlg)
        QtCore.QMetaObject.connectSlotsByName(GetCursorDlg)

    def retranslateUi(self, GetCursorDlg):
        _translate = QtCore.QCoreApplication.translate
        GetCursorDlg.setWindowTitle(_translate("GetCursorDlg", "Run Cypher Query"))
        self.label.setText(_translate("GetCursorDlg", "Running Query..."))
        self.btnCancel.setText(_translate("GetCursorDlg", "Cancel Query"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GetCursorDlg = QtWidgets.QDialog()
    ui = Ui_GetCursorDlg()
    ui.setupUi(GetCursorDlg)
    GetCursorDlg.show()
    sys.exit(app.exec_())
