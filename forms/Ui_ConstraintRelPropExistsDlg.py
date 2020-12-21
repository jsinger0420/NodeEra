# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\forms\ConstraintRelPropExistsDlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConstraintRelPropExistsDlg(object):
    def setupUi(self, ConstraintRelPropExistsDlg):
        ConstraintRelPropExistsDlg.setObjectName("ConstraintRelPropExistsDlg")
        ConstraintRelPropExistsDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        ConstraintRelPropExistsDlg.resize(591, 214)
        ConstraintRelPropExistsDlg.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConstraintRelPropExistsDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ConstraintRelPropExistsDlg)
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
        self.frame_2 = QtWidgets.QFrame(ConstraintRelPropExistsDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.cbRelationships = QtWidgets.QComboBox(self.frame_2)
        self.cbRelationships.setMinimumSize(QtCore.QSize(200, 0))
        self.cbRelationships.setEditable(True)
        self.cbRelationships.setObjectName("cbRelationships")
        self.gridLayout.addWidget(self.cbRelationships, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(139, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.cbProperty = QtWidgets.QComboBox(self.frame_2)
        self.cbProperty.setMinimumSize(QtCore.QSize(250, 0))
        self.cbProperty.setEditable(True)
        self.cbProperty.setObjectName("cbProperty")
        self.gridLayout.addWidget(self.cbProperty, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(78, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConstraintRelPropExistsDlg)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ConstraintRelPropExistsDlg)
        QtCore.QMetaObject.connectSlotsByName(ConstraintRelPropExistsDlg)

    def retranslateUi(self, ConstraintRelPropExistsDlg):
        _translate = QtCore.QCoreApplication.translate
        ConstraintRelPropExistsDlg.setWindowTitle(_translate("ConstraintRelPropExistsDlg", "Relationship Property Exists Constraint"))
        self.label.setText(_translate("ConstraintRelPropExistsDlg", "Create Relationship Property Exists Constraint"))
        self.label_4.setText(_translate("ConstraintRelPropExistsDlg", "Enter or Select a Relationship::"))
        self.label_3.setText(_translate("ConstraintRelPropExistsDlg", "Enter or Select a Property:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConstraintRelPropExistsDlg = QtWidgets.QDialog()
    ui = Ui_ConstraintRelPropExistsDlg()
    ui.setupUi(ConstraintRelPropExistsDlg)
    ConstraintRelPropExistsDlg.show()
    sys.exit(app.exec_())

