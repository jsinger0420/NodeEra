# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\FrmDateTime.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrmDateTime(object):
    def setupUi(self, FrmDateTime):
        FrmDateTime.setObjectName("FrmDateTime")
        FrmDateTime.resize(483, 70)
        FrmDateTime.setWindowOpacity(0.0)
        FrmDateTime.setAutoFillBackground(True)
        self.frame = QtWidgets.QFrame(FrmDateTime)
        self.frame.setGeometry(QtCore.QRect(9, 9, 321, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(1, 1, 2, 1)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.editDate = QtWidgets.QDateEdit(self.frame)
        self.editDate.setObjectName("editDate")
        self.horizontalLayout.addWidget(self.editDate)
        self.editTime = QtWidgets.QTimeEdit(self.frame)
        self.editTime.setTimeSpec(QtCore.Qt.LocalTime)
        self.editTime.setObjectName("editTime")
        self.horizontalLayout.addWidget(self.editTime)
        self.editNano = QtWidgets.QLineEdit(self.frame)
        self.editNano.setMinimumSize(QtCore.QSize(80, 0))
        self.editNano.setMaximumSize(QtCore.QSize(80, 16777215))
        self.editNano.setObjectName("editNano")
        self.horizontalLayout.addWidget(self.editNano)
        self.lblTZ = QtWidgets.QLabel(self.frame)
        self.lblTZ.setObjectName("lblTZ")
        self.horizontalLayout.addWidget(self.lblTZ)
        self.editTZ = QtWidgets.QLineEdit(self.frame)
        self.editTZ.setMinimumSize(QtCore.QSize(60, 0))
        self.editTZ.setMaximumSize(QtCore.QSize(60, 16777215))
        self.editTZ.setObjectName("editTZ")
        self.horizontalLayout.addWidget(self.editTZ)
        spacerItem = QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.retranslateUi(FrmDateTime)
        QtCore.QMetaObject.connectSlotsByName(FrmDateTime)

    def retranslateUi(self, FrmDateTime):
        _translate = QtCore.QCoreApplication.translate
        FrmDateTime.setWindowTitle(_translate("FrmDateTime", "Form"))
        self.editDate.setToolTip(_translate("FrmDateTime", "Enter the date"))
        self.editTime.setToolTip(_translate("FrmDateTime", "Enter the time in hh:mm:ss"))
        self.editTime.setDisplayFormat(_translate("FrmDateTime", "hh:mm:ss"))
        self.editNano.setToolTip(_translate("FrmDateTime", "Enter Nano Seconds"))
        self.lblTZ.setText(_translate("FrmDateTime", "TZ:"))
        self.editTZ.setToolTip(_translate("FrmDateTime", "Enter timezone using format +/-hhmm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FrmDateTime = QtWidgets.QWidget()
    ui = Ui_FrmDateTime()
    ui.setupUi(FrmDateTime)
    FrmDateTime.show()
    sys.exit(app.exec_())

