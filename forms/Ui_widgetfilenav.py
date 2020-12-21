# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\John\Documents\NODEERA\V1\forms\widgetfilenav.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widgetFileNav(object):
    def setupUi(self, widgetFileNav):
        widgetFileNav.setObjectName("widgetFileNav")
        widgetFileNav.resize(407, 372)
        self.frame_2 = QtWidgets.QFrame(widgetFileNav)
        self.frame_2.setGeometry(QtCore.QRect(70, 20, 230, 322))
        self.frame_2.setMinimumSize(QtCore.QSize(200, 20))
        self.frame_2.setMaximumSize(QtCore.QSize(600, 600))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.editPath = QtWidgets.QLineEdit(self.frame_3)
        self.editPath.setReadOnly(True)
        self.editPath.setObjectName("editPath")
        self.horizontalLayout_3.addWidget(self.editPath)
        self.btnPickPath = QtWidgets.QPushButton(self.frame_3)
        self.btnPickPath.setObjectName("btnPickPath")
        self.horizontalLayout_3.addWidget(self.btnPickPath)
        self.verticalLayout_5.addWidget(self.frame_3)
        self.tvFileSystem = QtWidgets.QTreeView(self.frame_2)
        self.tvFileSystem.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tvFileSystem.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tvFileSystem.setObjectName("tvFileSystem")
        self.verticalLayout_5.addWidget(self.tvFileSystem)

        self.retranslateUi(widgetFileNav)
        QtCore.QMetaObject.connectSlotsByName(widgetFileNav)

    def retranslateUi(self, widgetFileNav):
        _translate = QtCore.QCoreApplication.translate
        widgetFileNav.setWindowTitle(_translate("widgetFileNav", "Form"))
        self.btnPickPath.setText(_translate("widgetFileNav", "Path..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widgetFileNav = QtWidgets.QWidget()
    ui = Ui_widgetFileNav()
    ui.setupUi(widgetFileNav)
    widgetFileNav.show()
    sys.exit(app.exec_())

