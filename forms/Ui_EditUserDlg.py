# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\forms\EditUserDlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EditUserDlg(object):
    def setupUi(self, EditUserDlg):
        EditUserDlg.setObjectName("EditUserDlg")
        EditUserDlg.resize(510, 469)
        EditUserDlg.setSizeGripEnabled(True)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(EditUserDlg)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame = QtWidgets.QFrame(EditUserDlg)
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
        self.txtUserName = QtWidgets.QLineEdit(self.frame_5)
        self.txtUserName.setMinimumSize(QtCore.QSize(130, 0))
        self.txtUserName.setObjectName("txtUserName")
        self.horizontalLayout.addWidget(self.txtUserName)
        spacerItem = QtWidgets.QSpacerItem(230, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.frame_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_4.setContentsMargins(2, 3, 2, 3)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pbActivate = QtWidgets.QRadioButton(self.groupBox_6)
        self.pbActivate.setObjectName("pbActivate")
        self.horizontalLayout_4.addWidget(self.pbActivate)
        self.pbSuspend = QtWidgets.QRadioButton(self.groupBox_6)
        self.pbSuspend.setObjectName("pbSuspend")
        self.horizontalLayout_4.addWidget(self.pbSuspend)
        self.verticalLayout_3.addWidget(self.groupBox_6)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setContentsMargins(2, 3, 2, 3)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.pbChangeOnLogin = QtWidgets.QRadioButton(self.groupBox_2)
        self.pbChangeOnLogin.setObjectName("pbChangeOnLogin")
        self.gridLayout.addWidget(self.pbChangeOnLogin, 0, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(330, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 3)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.txtNewPassword = QtWidgets.QLineEdit(self.groupBox_2)
        self.txtNewPassword.setMinimumSize(QtCore.QSize(151, 0))
        self.txtNewPassword.setObjectName("txtNewPassword")
        self.gridLayout.addWidget(self.txtNewPassword, 1, 1, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(159, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 3, 1, 1)
        self.btnChangePassword = QtWidgets.QPushButton(self.groupBox_2)
        self.btnChangePassword.setObjectName("btnChangePassword")
        self.gridLayout.addWidget(self.btnChangePassword, 1, 4, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_5.addWidget(self.frame)
        self.frame1 = QtWidgets.QFrame(EditUserDlg)
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
        self.cbRoleName = QtWidgets.QComboBox(self.frame_3)
        self.cbRoleName.setMinimumSize(QtCore.QSize(180, 0))
        self.cbRoleName.setObjectName("cbRoleName")
        self.horizontalLayout_2.addWidget(self.cbRoleName)
        self.btnAddRole = QtWidgets.QPushButton(self.frame_3)
        self.btnAddRole.setObjectName("btnAddRole")
        self.horizontalLayout_2.addWidget(self.btnAddRole)
        spacerItem3 = QtWidgets.QSpacerItem(151, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.frame_2 = QtWidgets.QFrame(self.groupBox)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lstUserRoles = QtWidgets.QListWidget(self.frame_2)
        self.lstUserRoles.setObjectName("lstUserRoles")
        self.horizontalLayout_3.addWidget(self.lstUserRoles)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnRemoveRoles = QtWidgets.QPushButton(self.frame_4)
        self.btnRemoveRoles.setObjectName("btnRemoveRoles")
        self.verticalLayout.addWidget(self.btnRemoveRoles)
        spacerItem4 = QtWidgets.QSpacerItem(20, 139, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_3.addWidget(self.frame_4)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.verticalLayout_5.addWidget(self.frame1)
        self.dlgBtnBox = QtWidgets.QDialogButtonBox(EditUserDlg)
        self.dlgBtnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.dlgBtnBox.setObjectName("dlgBtnBox")
        self.verticalLayout_5.addWidget(self.dlgBtnBox)
        self.label.setBuddy(self.txtUserName)
        self.label_2.setBuddy(self.txtNewPassword)

        self.retranslateUi(EditUserDlg)
        QtCore.QMetaObject.connectSlotsByName(EditUserDlg)

    def retranslateUi(self, EditUserDlg):
        _translate = QtCore.QCoreApplication.translate
        EditUserDlg.setWindowTitle(_translate("EditUserDlg", "Edit User"))
        self.label.setText(_translate("EditUserDlg", "User Name:"))
        self.groupBox_6.setTitle(_translate("EditUserDlg", "User Status"))
        self.pbActivate.setText(_translate("EditUserDlg", "Active"))
        self.pbSuspend.setText(_translate("EditUserDlg", "Suspended"))
        self.groupBox_2.setTitle(_translate("EditUserDlg", "User Password"))
        self.pbChangeOnLogin.setText(_translate("EditUserDlg", "Change on next login"))
        self.label_2.setText(_translate("EditUserDlg", "New Password:"))
        self.btnChangePassword.setText(_translate("EditUserDlg", "Change Password"))
        self.groupBox.setTitle(_translate("EditUserDlg", "User Roles"))
        self.cbRoleName.setToolTip(_translate("EditUserDlg", "Select a role to add to the User"))
        self.btnAddRole.setText(_translate("EditUserDlg", "Add Role"))
        self.btnRemoveRoles.setText(_translate("EditUserDlg", "Remove Role"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditUserDlg = QtWidgets.QDialog()
    ui = Ui_EditUserDlg()
    ui.setupUi(EditUserDlg)
    EditUserDlg.show()
    sys.exit(app.exec_())

