# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\forms\EditRoleDlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EditRoleDlg(object):
    def setupUi(self, EditRoleDlg):
        EditRoleDlg.setObjectName("EditRoleDlg")
        EditRoleDlg.resize(510, 469)
        EditRoleDlg.setSizeGripEnabled(True)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(EditRoleDlg)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame = QtWidgets.QFrame(EditRoleDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_5 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame_5)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txtRoleName = QtWidgets.QLineEdit(self.frame_5)
        self.txtRoleName.setMinimumSize(QtCore.QSize(130, 0))
        self.txtRoleName.setObjectName("txtRoleName")
        self.horizontalLayout.addWidget(self.txtRoleName)
        spacerItem = QtWidgets.QSpacerItem(230, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.frame_5)
        self.verticalLayout_5.addWidget(self.frame)
        self.frame1 = QtWidgets.QFrame(EditRoleDlg)
        self.frame1.setObjectName("frame1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame1)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.frame1)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setContentsMargins(2, 3, 2, 3)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_3 = QtWidgets.QFrame(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cbUserName = QtWidgets.QComboBox(self.frame_3)
        self.cbUserName.setMinimumSize(QtCore.QSize(180, 0))
        self.cbUserName.setObjectName("cbUserName")
        self.horizontalLayout_2.addWidget(self.cbUserName)
        self.btnAddUser = QtWidgets.QPushButton(self.frame_3)
        self.btnAddUser.setObjectName("btnAddUser")
        self.horizontalLayout_2.addWidget(self.btnAddUser)
        spacerItem1 = QtWidgets.QSpacerItem(151, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.frame_2 = QtWidgets.QFrame(self.groupBox)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lstRoleUsers = QtWidgets.QListWidget(self.frame_2)
        self.lstRoleUsers.setObjectName("lstRoleUsers")
        self.horizontalLayout_3.addWidget(self.lstRoleUsers)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnRemoveUsers = QtWidgets.QPushButton(self.frame_4)
        self.btnRemoveUsers.setObjectName("btnRemoveUsers")
        self.verticalLayout.addWidget(self.btnRemoveUsers)
        spacerItem2 = QtWidgets.QSpacerItem(20, 139, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_3.addWidget(self.frame_4)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.verticalLayout_5.addWidget(self.frame1)
        self.dlgBtnBox = QtWidgets.QDialogButtonBox(EditRoleDlg)
        self.dlgBtnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.dlgBtnBox.setObjectName("dlgBtnBox")
        self.verticalLayout_5.addWidget(self.dlgBtnBox)
        self.label.setBuddy(self.txtRoleName)

        self.retranslateUi(EditRoleDlg)
        QtCore.QMetaObject.connectSlotsByName(EditRoleDlg)

    def retranslateUi(self, EditRoleDlg):
        _translate = QtCore.QCoreApplication.translate
        EditRoleDlg.setWindowTitle(_translate("EditRoleDlg", "Edit Role"))
        self.label.setText(_translate("EditRoleDlg", "Role Name:"))
        self.groupBox.setTitle(_translate("EditRoleDlg", "Role Users"))
        self.cbUserName.setToolTip(_translate("EditRoleDlg", "Select a role to add to the User"))
        self.btnAddUser.setText(_translate("EditRoleDlg", "Add User"))
        self.btnRemoveUsers.setText(_translate("EditRoleDlg", "Remove User"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditRoleDlg = QtWidgets.QDialog()
    ui = Ui_EditRoleDlg()
    ui.setupUi(EditRoleDlg)
    EditRoleDlg.show()
    sys.exit(app.exec_())

