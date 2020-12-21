# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\EditNodeDlg.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditNodeDlg(object):
    def setupUi(self, EditNodeDlg):
        EditNodeDlg.setObjectName("EditNodeDlg")
        EditNodeDlg.resize(1015, 529)
        EditNodeDlg.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditNodeDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(EditNodeDlg)
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
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.txtTitle = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.txtTitle.setFont(font)
        self.txtTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.txtTitle.setObjectName("txtTitle")
        self.gridLayout.addWidget(self.txtTitle, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.frameBody = QtWidgets.QFrame(EditNodeDlg)
        self.frameBody.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBody.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBody.setObjectName("frameBody")
        self.verticalLayout.addWidget(self.frameBody)
        self.frame_2 = QtWidgets.QFrame(EditNodeDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(180, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnClose = QtWidgets.QPushButton(self.frame_2)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        spacerItem1 = QtWidgets.QSpacerItem(180, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(EditNodeDlg)
        QtCore.QMetaObject.connectSlotsByName(EditNodeDlg)

    def retranslateUi(self, EditNodeDlg):
        _translate = QtCore.QCoreApplication.translate
        EditNodeDlg.setWindowTitle(_translate("EditNodeDlg", "Edit Node"))
        self.txtTitle.setText(_translate("EditNodeDlg", "DialogTitle"))
        self.btnClose.setText(_translate("EditNodeDlg", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditNodeDlg = QtWidgets.QDialog()
    ui = Ui_EditNodeDlg()
    ui.setupUi(EditNodeDlg)
    EditNodeDlg.show()
    sys.exit(app.exec_())
