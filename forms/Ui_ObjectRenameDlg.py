# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\ObjectRenameDlg.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(795, 495)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txtCurrentObject = QtWidgets.QLineEdit(self.frame)
        self.txtCurrentObject.setMinimumSize(QtCore.QSize(350, 0))
        self.txtCurrentObject.setText("")
        self.txtCurrentObject.setReadOnly(True)
        self.txtCurrentObject.setObjectName("txtCurrentObject")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtCurrentObject)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txtCurrentName = QtWidgets.QLineEdit(self.frame)
        self.txtCurrentName.setMinimumSize(QtCore.QSize(350, 0))
        self.txtCurrentName.setReadOnly(True)
        self.txtCurrentName.setObjectName("txtCurrentName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtCurrentName)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.editNewName = QtWidgets.QLineEdit(self.frame)
        self.editNewName.setMinimumSize(QtCore.QSize(350, 0))
        self.editNewName.setObjectName("editNewName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.editNewName)
        self.verticalLayout_2.addWidget(self.frame)
        self.grpWhereUsed = QtWidgets.QGroupBox(Dialog)
        self.grpWhereUsed.setObjectName("grpWhereUsed")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.grpWhereUsed)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridUsage = QtWidgets.QTableView(self.grpWhereUsed)
        self.gridUsage.setObjectName("gridUsage")
        self.verticalLayout.addWidget(self.gridUsage)
        self.verticalLayout_2.addWidget(self.grpWhereUsed)
        self.lblInstructions = QtWidgets.QLabel(Dialog)
        self.lblInstructions.setObjectName("lblInstructions")
        self.verticalLayout_2.addWidget(self.lblInstructions)
        self.lblInstructions2 = QtWidgets.QLabel(Dialog)
        self.lblInstructions2.setObjectName("lblInstructions2")
        self.verticalLayout_2.addWidget(self.lblInstructions2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.label_3.setBuddy(self.txtCurrentObject)
        self.label.setBuddy(self.txtCurrentName)
        self.label_2.setBuddy(self.editNewName)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Rename Project Object"))
        self.label_3.setText(_translate("Dialog", "Object Type:"))
        self.label.setText(_translate("Dialog", "Current Name:"))
        self.label_2.setText(_translate("Dialog", "New Name:"))
        self.grpWhereUsed.setTitle(_translate("Dialog", "Where Used"))
        self.lblInstructions.setText(_translate("Dialog", "Press OK to change the object name and change everywhere it is used."))
        self.lblInstructions2.setText(_translate("Dialog", "Press Cancel to exit this dialog without renaming."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
