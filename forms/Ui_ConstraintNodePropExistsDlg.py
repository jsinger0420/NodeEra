# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\forms\ConstraintNodePropExistsDlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConstraintNodePropExistsDlg(object):
    def setupUi(self, ConstraintNodePropExistsDlg):
        ConstraintNodePropExistsDlg.setObjectName("ConstraintNodePropExistsDlg")
        ConstraintNodePropExistsDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        ConstraintNodePropExistsDlg.resize(591, 177)
        ConstraintNodePropExistsDlg.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConstraintNodePropExistsDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ConstraintNodePropExistsDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.frame = QtWidgets.QFrame(ConstraintNodePropExistsDlg)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.cbLabel = QtWidgets.QComboBox(self.frame)
        self.cbLabel.setMinimumSize(QtCore.QSize(150, 0))
        self.cbLabel.setEditable(True)
        self.cbLabel.setObjectName("cbLabel")
        self.gridLayout.addWidget(self.cbLabel, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(276, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.cbProperty = QtWidgets.QComboBox(self.frame)
        self.cbProperty.setMinimumSize(QtCore.QSize(250, 0))
        self.cbProperty.setEditable(True)
        self.cbProperty.setObjectName("cbProperty")
        self.gridLayout.addWidget(self.cbProperty, 1, 1, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(78, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConstraintNodePropExistsDlg)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ConstraintNodePropExistsDlg)
        QtCore.QMetaObject.connectSlotsByName(ConstraintNodePropExistsDlg)

    def retranslateUi(self, ConstraintNodePropExistsDlg):
        _translate = QtCore.QCoreApplication.translate
        ConstraintNodePropExistsDlg.setWindowTitle(_translate("ConstraintNodePropExistsDlg", "Node Property Exists Constraint"))
        self.label.setText(_translate("ConstraintNodePropExistsDlg", "Create Node Property Exists Constraint"))
        self.label_2.setText(_translate("ConstraintNodePropExistsDlg", "Enter or Select a Label:"))
        self.label_3.setText(_translate("ConstraintNodePropExistsDlg", "Enter or Select a Property:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConstraintNodePropExistsDlg = QtWidgets.QDialog()
    ui = Ui_ConstraintNodePropExistsDlg()
    ui.setupUi(ConstraintNodePropExistsDlg)
    ConstraintNodePropExistsDlg.show()
    sys.exit(app.exec_())

