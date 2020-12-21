# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\PropPropertyBox.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_propPropertyBox(object):
    def setupUi(self, propPropertyBox):
        propPropertyBox.setObjectName("propPropertyBox")
        propPropertyBox.setWindowModality(QtCore.Qt.ApplicationModal)
        propPropertyBox.resize(505, 383)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(propPropertyBox.sizePolicy().hasHeightForWidth())
        propPropertyBox.setSizePolicy(sizePolicy)
        propPropertyBox.setSizeGripEnabled(False)
        propPropertyBox.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(propPropertyBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label1 = QtWidgets.QLabel(propPropertyBox)
        self.label1.setObjectName("label1")
        self.gridLayout.addWidget(self.label1, 0, 0, 1, 1)
        self.editName = QtWidgets.QLineEdit(propPropertyBox)
        self.editName.setToolTip("")
        self.editName.setMaxLength(32)
        self.editName.setObjectName("editName")
        self.gridLayout.addWidget(self.editName, 0, 1, 1, 1)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtWidgets.QSpacerItem(71, 31, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(propPropertyBox)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(propPropertyBox)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.hboxlayout, 2, 0, 1, 2)
        self.tabProperty = QtWidgets.QTabWidget(propPropertyBox)
        self.tabProperty.setObjectName("tabProperty")
        self.tabDescription = QtWidgets.QWidget()
        self.tabDescription.setObjectName("tabDescription")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabDescription)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.tabDescription)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.cmbDataType = QtWidgets.QComboBox(self.tabDescription)
        self.cmbDataType.setMinimumSize(QtCore.QSize(200, 0))
        self.cmbDataType.setObjectName("cmbDataType")
        self.gridLayout_2.addWidget(self.cmbDataType, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(191, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 2, 1, 1)
        self.label2 = QtWidgets.QLabel(self.tabDescription)
        self.label2.setObjectName("label2")
        self.gridLayout_2.addWidget(self.label2, 1, 0, 1, 1)
        self.editDescription = QtWidgets.QPlainTextEdit(self.tabDescription)
        self.editDescription.setToolTip("")
        self.editDescription.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.editDescription.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.editDescription.setObjectName("editDescription")
        self.gridLayout_2.addWidget(self.editDescription, 2, 0, 1, 3)
        self.tabProperty.addTab(self.tabDescription, "")
        self.gridLayout.addWidget(self.tabProperty, 1, 0, 1, 2)
        self.label1.setBuddy(self.editName)
        self.label.setBuddy(self.cmbDataType)
        self.label2.setBuddy(self.editDescription)

        self.retranslateUi(propPropertyBox)
        self.tabProperty.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(propPropertyBox)
        propPropertyBox.setTabOrder(self.editName, self.tabProperty)
        propPropertyBox.setTabOrder(self.tabProperty, self.cmbDataType)
        propPropertyBox.setTabOrder(self.cmbDataType, self.editDescription)
        propPropertyBox.setTabOrder(self.editDescription, self.okButton)
        propPropertyBox.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, propPropertyBox):
        _translate = QtCore.QCoreApplication.translate
        propPropertyBox.setWindowTitle(_translate("propPropertyBox", "Property Editor"))
        self.label1.setText(_translate("propPropertyBox", "Name:"))
        self.okButton.setText(_translate("propPropertyBox", "&OK"))
        self.cancelButton.setText(_translate("propPropertyBox", "&Cancel"))
        self.label.setText(_translate("propPropertyBox", "Data Type:"))
        self.label2.setText(_translate("propPropertyBox", "Description:"))
        self.tabProperty.setTabText(self.tabProperty.indexOf(self.tabDescription), _translate("propPropertyBox", "Description"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    propPropertyBox = QtWidgets.QDialog()
    ui = Ui_propPropertyBox()
    ui.setupUi(propPropertyBox)
    propPropertyBox.show()
    sys.exit(app.exec_())

