# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\FrmGPoint.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrmGPoint(object):
    def setupUi(self, FrmGPoint):
        FrmGPoint.setObjectName("FrmGPoint")
        FrmGPoint.resize(362, 40)
        FrmGPoint.setWindowOpacity(0.0)
        self.frame = QtWidgets.QFrame(FrmGPoint)
        self.frame.setGeometry(QtCore.QRect(0, 0, 361, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblLon = QtWidgets.QLabel(self.frame)
        self.lblLon.setObjectName("lblLon")
        self.horizontalLayout.addWidget(self.lblLon)
        self.editLon = QtWidgets.QLineEdit(self.frame)
        self.editLon.setObjectName("editLon")
        self.horizontalLayout.addWidget(self.editLon)
        self.lblLat = QtWidgets.QLabel(self.frame)
        self.lblLat.setObjectName("lblLat")
        self.horizontalLayout.addWidget(self.lblLat)
        self.editLat = QtWidgets.QLineEdit(self.frame)
        self.editLat.setObjectName("editLat")
        self.horizontalLayout.addWidget(self.editLat)
        self.lblHeight = QtWidgets.QLabel(self.frame)
        self.lblHeight.setObjectName("lblHeight")
        self.horizontalLayout.addWidget(self.lblHeight)
        self.editHeight = QtWidgets.QLineEdit(self.frame)
        self.editHeight.setObjectName("editHeight")
        self.horizontalLayout.addWidget(self.editHeight)
        self.lblLon.setBuddy(self.editLon)
        self.lblLat.setBuddy(self.editLat)
        self.lblHeight.setBuddy(self.editHeight)

        self.retranslateUi(FrmGPoint)
        QtCore.QMetaObject.connectSlotsByName(FrmGPoint)

    def retranslateUi(self, FrmGPoint):
        _translate = QtCore.QCoreApplication.translate
        FrmGPoint.setWindowTitle(_translate("FrmGPoint", "Form"))
        self.lblLon.setText(_translate("FrmGPoint", "Lon:"))
        self.editLon.setToolTip(_translate("FrmGPoint", "Enter Y coordinate"))
        self.lblLat.setText(_translate("FrmGPoint", "Lat:"))
        self.editLat.setToolTip(_translate("FrmGPoint", "Enter the X coordinate"))
        self.lblHeight.setText(_translate("FrmGPoint", "Height:"))
        self.editHeight.setToolTip(_translate("FrmGPoint", "Enter Z coordinate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FrmGPoint = QtWidgets.QWidget()
    ui = Ui_FrmGPoint()
    ui.setupUi(FrmGPoint)
    FrmGPoint.show()
    sys.exit(app.exec_())

