# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\RelationshipPropertyBox.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RelationshipPropertyBox(object):
    def setupUi(self, RelationshipPropertyBox):
        RelationshipPropertyBox.setObjectName("RelationshipPropertyBox")
        RelationshipPropertyBox.setWindowModality(QtCore.Qt.ApplicationModal)
        RelationshipPropertyBox.resize(461, 415)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RelationshipPropertyBox.sizePolicy().hasHeightForWidth())
        RelationshipPropertyBox.setSizePolicy(sizePolicy)
        RelationshipPropertyBox.setSizeGripEnabled(False)
        RelationshipPropertyBox.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(RelationshipPropertyBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(RelationshipPropertyBox)
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
        self.tabLabel = QtWidgets.QTabWidget(RelationshipPropertyBox)
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
        self.okButton = QtWidgets.QPushButton(RelationshipPropertyBox)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(RelationshipPropertyBox)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.label1.setBuddy(self.editName)
        self.label2.setBuddy(self.editDescription)

        self.retranslateUi(RelationshipPropertyBox)
        self.tabLabel.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RelationshipPropertyBox)
        RelationshipPropertyBox.setTabOrder(self.editName, self.tabLabel)
        RelationshipPropertyBox.setTabOrder(self.tabLabel, self.editDescription)
        RelationshipPropertyBox.setTabOrder(self.editDescription, self.okButton)
        RelationshipPropertyBox.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, RelationshipPropertyBox):
        _translate = QtCore.QCoreApplication.translate
        RelationshipPropertyBox.setWindowTitle(_translate("RelationshipPropertyBox", "Relationship Type Editor"))
        self.label1.setText(_translate("RelationshipPropertyBox", "Name:"))
        self.label2.setText(_translate("RelationshipPropertyBox", "Description:"))
        self.tabLabel.setTabText(self.tabLabel.indexOf(self.tabDescription), _translate("RelationshipPropertyBox", "Description"))
        self.okButton.setText(_translate("RelationshipPropertyBox", "&OK"))
        self.cancelButton.setText(_translate("RelationshipPropertyBox", "&Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RelationshipPropertyBox = QtWidgets.QDialog()
    ui = Ui_RelationshipPropertyBox()
    ui.setupUi(RelationshipPropertyBox)
    RelationshipPropertyBox.show()
    sys.exit(app.exec_())

