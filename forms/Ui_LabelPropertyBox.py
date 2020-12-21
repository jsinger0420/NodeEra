# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\LabelPropertyBox.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(461, 415)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label1 = QtWidgets.QLabel(self.frame)
        self.label1.setObjectName("label1")
        self.horizontalLayout.addWidget(self.label1)
        self.editName = QtWidgets.QLineEdit(self.frame)
        self.editName.setToolTip("")
        self.editName.setMaxLength(32)
        self.editName.setObjectName("editName")
        self.horizontalLayout.addWidget(self.editName)
        spacerItem = QtWidgets.QSpacerItem(187, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame)
        self.tabLabel = QtWidgets.QTabWidget(Dialog)
        self.tabLabel.setObjectName("tabLabel")
        self.tabDescription = QtWidgets.QWidget()
        self.tabDescription.setObjectName("tabDescription")
        self.gridLayout = QtWidgets.QGridLayout(self.tabDescription)
        self.gridLayout.setObjectName("gridLayout")
        self.label2 = QtWidgets.QLabel(self.tabDescription)
        self.label2.setObjectName("label2")
        self.gridLayout.addWidget(self.label2, 0, 0, 1, 1)
        self.editDescription = QtWidgets.QPlainTextEdit(self.tabDescription)
        self.editDescription.setToolTip("")
        self.editDescription.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.editDescription.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.editDescription.setObjectName("editDescription")
        self.gridLayout.addWidget(self.editDescription, 1, 0, 1, 1)
        self.tabLabel.addTab(self.tabDescription, "")
        self.verticalLayout.addWidget(self.tabLabel)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem1 = QtWidgets.QSpacerItem(71, 31, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.label1.setBuddy(self.editName)
        self.label2.setBuddy(self.editDescription)

        self.retranslateUi(Dialog)
        self.tabLabel.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.editName, self.tabLabel)
        Dialog.setTabOrder(self.tabLabel, self.editDescription)
        Dialog.setTabOrder(self.editDescription, self.okButton)
        Dialog.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Label Editor"))
        self.label1.setText(_translate("Dialog", "Name:"))
        self.label2.setText(_translate("Dialog", "Description:"))
        self.tabLabel.setTabText(self.tabLabel.indexOf(self.tabDescription), _translate("Dialog", "Description"))
        self.okButton.setText(_translate("Dialog", "&OK"))
        self.cancelButton.setText(_translate("Dialog", "&Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

