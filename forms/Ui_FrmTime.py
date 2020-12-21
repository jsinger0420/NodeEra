# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\FrmTime.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrmTime(object):
    def setupUi(self, FrmTime):
        FrmTime.setObjectName("FrmTime")
        FrmTime.resize(546, 57)
        FrmTime.setWindowOpacity(0.0)
        FrmTime.setAutoFillBackground(True)
        self.frame = QtWidgets.QFrame(FrmTime)
        self.frame.setGeometry(QtCore.QRect(9, 9, 404, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.lblHH = QtWidgets.QLabel(self.frame)
        self.lblHH.setObjectName("lblHH")
        self.gridLayout.addWidget(self.lblHH, 0, 0, 1, 1)
        self.editHH = QtWidgets.QLineEdit(self.frame)
        self.editHH.setMinimumSize(QtCore.QSize(41, 0))
        self.editHH.setMaximumSize(QtCore.QSize(41, 16777215))
        self.editHH.setObjectName("editHH")
        self.gridLayout.addWidget(self.editHH, 0, 1, 1, 1)
        self.lblMM = QtWidgets.QLabel(self.frame)
        self.lblMM.setObjectName("lblMM")
        self.gridLayout.addWidget(self.lblMM, 0, 2, 1, 1)
        self.editMM = QtWidgets.QLineEdit(self.frame)
        self.editMM.setMinimumSize(QtCore.QSize(41, 0))
        self.editMM.setMaximumSize(QtCore.QSize(41, 16777215))
        self.editMM.setObjectName("editMM")
        self.gridLayout.addWidget(self.editMM, 0, 3, 1, 1)
        self.lblSS = QtWidgets.QLabel(self.frame)
        self.lblSS.setObjectName("lblSS")
        self.gridLayout.addWidget(self.lblSS, 0, 4, 1, 1)
        self.editSS = QtWidgets.QLineEdit(self.frame)
        self.editSS.setMinimumSize(QtCore.QSize(95, 0))
        self.editSS.setMaximumSize(QtCore.QSize(95, 16777215))
        self.editSS.setObjectName("editSS")
        self.gridLayout.addWidget(self.editSS, 0, 5, 1, 1)
        self.lblTZ = QtWidgets.QLabel(self.frame)
        self.lblTZ.setObjectName("lblTZ")
        self.gridLayout.addWidget(self.lblTZ, 0, 6, 1, 1)
        self.editTZ = QtWidgets.QLineEdit(self.frame)
        self.editTZ.setMinimumSize(QtCore.QSize(95, 0))
        self.editTZ.setMaximumSize(QtCore.QSize(95, 16777215))
        self.editTZ.setObjectName("editTZ")
        self.gridLayout.addWidget(self.editTZ, 0, 7, 1, 1)
        self.lblHH.setBuddy(self.editHH)
        self.lblMM.setBuddy(self.editMM)
        self.lblSS.setBuddy(self.editSS)
        self.lblTZ.setBuddy(self.editSS)

        self.retranslateUi(FrmTime)
        QtCore.QMetaObject.connectSlotsByName(FrmTime)

    def retranslateUi(self, FrmTime):
        _translate = QtCore.QCoreApplication.translate
        FrmTime.setWindowTitle(_translate("FrmTime", "Form"))
        self.lblHH.setText(_translate("FrmTime", "HH:"))
        self.editHH.setToolTip(_translate("FrmTime", "Enter hours from 0 to 24"))
        self.lblMM.setText(_translate("FrmTime", "MM:"))
        self.editMM.setToolTip(_translate("FrmTime", "Enter minutes from 0 to 60"))
        self.lblSS.setText(_translate("FrmTime", "SS:"))
        self.editSS.setToolTip(_translate("FrmTime", "Enter seconds and nano seconds using format nn.nnnnnnnnn"))
        self.lblTZ.setText(_translate("FrmTime", "TZ:"))
        self.editTZ.setToolTip(_translate("FrmTime", "Enter timezone using format +/-hhmm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FrmTime = QtWidgets.QWidget()
    ui = Ui_FrmTime()
    ui.setupUi(FrmTime)
    FrmTime.show()
    sys.exit(app.exec_())

