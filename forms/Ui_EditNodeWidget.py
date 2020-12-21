# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\EditNodeWidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditNodeWidget(object):
    def setupUi(self, EditNodeWidget):
        EditNodeWidget.setObjectName("EditNodeWidget")
        EditNodeWidget.resize(801, 474)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(EditNodeWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtWidgets.QSplitter(EditNodeWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.frameLabels = QtWidgets.QFrame(self.splitter)
        self.frameLabels.setMinimumSize(QtCore.QSize(375, 0))
        self.frameLabels.setFrameShape(QtWidgets.QFrame.Box)
        self.frameLabels.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameLabels.setObjectName("frameLabels")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frameLabels)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLabels = QtWidgets.QTableView(self.frameLabels)
        self.gridLabels.setObjectName("gridLabels")
        self.horizontalLayout_3.addWidget(self.gridLabels)
        self.frame_4 = QtWidgets.QFrame(self.frameLabels)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMinimumSize(QtCore.QSize(95, 0))
        self.frame_4.setMaximumSize(QtCore.QSize(95, 16777215))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setLineWidth(0)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 140, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_3.addWidget(self.frame_4)
        self.framePropertys = QtWidgets.QFrame(self.splitter)
        self.framePropertys.setFrameShape(QtWidgets.QFrame.Box)
        self.framePropertys.setFrameShadow(QtWidgets.QFrame.Plain)
        self.framePropertys.setObjectName("framePropertys")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.framePropertys)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridProps = QtWidgets.QTableView(self.framePropertys)
        self.gridProps.setObjectName("gridProps")
        self.horizontalLayout.addWidget(self.gridProps)
        self.frame_3 = QtWidgets.QFrame(self.framePropertys)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnSetNull = QtWidgets.QPushButton(self.frame_3)
        self.btnSetNull.setObjectName("btnSetNull")
        self.verticalLayout.addWidget(self.btnSetNull)
        self.btnAddNew = QtWidgets.QPushButton(self.frame_3)
        self.btnAddNew.setObjectName("btnAddNew")
        self.verticalLayout.addWidget(self.btnAddNew)
        spacerItem1 = QtWidgets.QSpacerItem(20, 152, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.frame_3)
        self.verticalLayout_3.addWidget(self.splitter)

        self.retranslateUi(EditNodeWidget)
        QtCore.QMetaObject.connectSlotsByName(EditNodeWidget)

    def retranslateUi(self, EditNodeWidget):
        _translate = QtCore.QCoreApplication.translate
        EditNodeWidget.setWindowTitle(_translate("EditNodeWidget", "Form"))
        self.btnSetNull.setText(_translate("EditNodeWidget", "Set Value Null"))
        self.btnAddNew.setText(_translate("EditNodeWidget", "Add New Node"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditNodeWidget = QtWidgets.QWidget()
    ui = Ui_EditNodeWidget()
    ui.setupUi(EditNodeWidget)
    EditNodeWidget.show()
    sys.exit(app.exec_())
