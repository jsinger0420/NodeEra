# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\forms\TemplateNodeNew.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TemplateNodeNew(object):
    def setupUi(self, TemplateNodeNew):
        TemplateNodeNew.setObjectName("TemplateNodeNew")
        TemplateNodeNew.resize(873, 177)
        TemplateNodeNew.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(TemplateNodeNew)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(TemplateNodeNew)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTitle = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")
        self.horizontalLayout.addWidget(self.lblTitle)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(TemplateNodeNew)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 61))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridNewNode = QtWidgets.QTableView(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridNewNode.sizePolicy().hasHeightForWidth())
        self.gridNewNode.setSizePolicy(sizePolicy)
        self.gridNewNode.setMaximumSize(QtCore.QSize(16777215, 41))
        self.gridNewNode.setObjectName("gridNewNode")
        self.horizontalLayout_2.addWidget(self.gridNewNode)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(TemplateNodeNew)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TemplateNodeNew)
        self.buttonBox.accepted.connect(TemplateNodeNew.accept)
        self.buttonBox.rejected.connect(TemplateNodeNew.reject)
        QtCore.QMetaObject.connectSlotsByName(TemplateNodeNew)

    def retranslateUi(self, TemplateNodeNew):
        _translate = QtCore.QCoreApplication.translate
        TemplateNodeNew.setWindowTitle(_translate("TemplateNodeNew", "New Node"))
        self.lblTitle.setText(_translate("TemplateNodeNew", "New Node From Template"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TemplateNodeNew = QtWidgets.QDialog()
    ui = Ui_TemplateNodeNew()
    ui.setupUi(TemplateNodeNew)
    TemplateNodeNew.show()
    sys.exit(app.exec_())

