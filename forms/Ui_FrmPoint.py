# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\FrmPoint.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrmPoint(object):
    def setupUi(self, FrmPoint):
        FrmPoint.setObjectName("FrmPoint")
        FrmPoint.resize(352, 41)
        FrmPoint.setWindowOpacity(0.0)
        self.frame = QtWidgets.QFrame(FrmPoint)
        self.frame.setGeometry(QtCore.QRect(0, 0, 351, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setObjectName("gridLayout")
        self.lblX = QtWidgets.QLabel(self.frame)
        self.lblX.setObjectName("lblX")
        self.gridLayout.addWidget(self.lblX, 0, 0, 1, 1)
        self.editX = QtWidgets.QLineEdit(self.frame)
        self.editX.setObjectName("editX")
        self.gridLayout.addWidget(self.editX, 0, 1, 1, 1)
        self.lblY = QtWidgets.QLabel(self.frame)
        self.lblY.setObjectName("lblY")
        self.gridLayout.addWidget(self.lblY, 0, 2, 1, 1)
        self.editY = QtWidgets.QLineEdit(self.frame)
        self.editY.setObjectName("editY")
        self.gridLayout.addWidget(self.editY, 0, 3, 1, 1)
        self.lblZ = QtWidgets.QLabel(self.frame)
        self.lblZ.setObjectName("lblZ")
        self.gridLayout.addWidget(self.lblZ, 0, 4, 1, 1)
        self.editZ = QtWidgets.QLineEdit(self.frame)
        self.editZ.setObjectName("editZ")
        self.gridLayout.addWidget(self.editZ, 0, 5, 1, 1)
        self.lblX.setBuddy(self.editX)
        self.lblY.setBuddy(self.editY)
        self.lblZ.setBuddy(self.editZ)

        self.retranslateUi(FrmPoint)
        QtCore.QMetaObject.connectSlotsByName(FrmPoint)

    def retranslateUi(self, FrmPoint):
        _translate = QtCore.QCoreApplication.translate
        FrmPoint.setWindowTitle(_translate("FrmPoint", "Form"))
        self.lblX.setText(_translate("FrmPoint", "X:"))
        self.editX.setToolTip(_translate("FrmPoint", "Enter the X coordinate"))
        self.lblY.setText(_translate("FrmPoint", "Y:"))
        self.editY.setToolTip(_translate("FrmPoint", "Enter Y coordinate"))
        self.lblZ.setText(_translate("FrmPoint", "Z:"))
        self.editZ.setToolTip(_translate("FrmPoint", "Enter Z coordinate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FrmPoint = QtWidgets.QWidget()
    ui = Ui_FrmPoint()
    ui.setupUi(FrmPoint)
    FrmPoint.show()
    sys.exit(app.exec_())

