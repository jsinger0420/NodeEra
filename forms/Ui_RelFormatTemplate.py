# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\John\Documents\ERIC\UI\RelFormatTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RelFormatTemplate(object):
    def setupUi(self, RelFormatTemplate):
        RelFormatTemplate.setObjectName("RelFormatTemplate")
        RelFormatTemplate.setWindowModality(QtCore.Qt.ApplicationModal)
        RelFormatTemplate.resize(367, 411)
        RelFormatTemplate.setSizeGripEnabled(False)
        RelFormatTemplate.setModal(True)
        self.layoutWidget = QtWidgets.QWidget(RelFormatTemplate)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 370, 331, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.hboxlayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtWidgets.QSpacerItem(71, 31, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(self.layoutWidget)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(self.layoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.boxFillStyle = QtWidgets.QGroupBox(RelFormatTemplate)
        self.boxFillStyle.setGeometry(QtCore.QRect(10, 70, 116, 99))
        self.boxFillStyle.setObjectName("boxFillStyle")
        self.formLayout_2 = QtWidgets.QFormLayout(self.boxFillStyle)
        self.formLayout_2.setObjectName("formLayout_2")
        self.rbNone = QtWidgets.QRadioButton(self.boxFillStyle)
        self.rbNone.setChecked(True)
        self.rbNone.setObjectName("rbNone")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.rbNone)
        self.rbFill = QtWidgets.QRadioButton(self.boxFillStyle)
        self.rbFill.setObjectName("rbFill")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rbFill)
        self.rbPattern = QtWidgets.QRadioButton(self.boxFillStyle)
        self.rbPattern.setObjectName("rbPattern")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rbPattern)
        self.spinPattern = QtWidgets.QSpinBox(self.boxFillStyle)
        self.spinPattern.setMinimum(1)
        self.spinPattern.setMaximum(7)
        self.spinPattern.setObjectName("spinPattern")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinPattern)
        self.groupBox = QtWidgets.QGroupBox(RelFormatTemplate)
        self.groupBox.setGeometry(QtCore.QRect(10, 200, 341, 152))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frmView = QtWidgets.QFrame(self.groupBox)
        self.frmView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frmView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frmView.setObjectName("frmView")
        self.gridLayout_3.addWidget(self.frmView, 0, 0, 3, 1)
        self.btnFillColor = QtWidgets.QPushButton(self.groupBox)
        self.btnFillColor.setObjectName("btnFillColor")
        self.gridLayout_3.addWidget(self.btnFillColor, 0, 1, 1, 1)
        self.btnLineColor = QtWidgets.QPushButton(self.groupBox)
        self.btnLineColor.setObjectName("btnLineColor")
        self.gridLayout_3.addWidget(self.btnLineColor, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 58, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 2, 1, 1, 1)
        self.boxLineStyle = QtWidgets.QGroupBox(RelFormatTemplate)
        self.boxLineStyle.setGeometry(QtCore.QRect(205, 10, 120, 191))
        self.boxLineStyle.setObjectName("boxLineStyle")
        self.formLayout = QtWidgets.QFormLayout(self.boxLineStyle)
        self.formLayout.setObjectName("formLayout")
        self.rbNoLine = QtWidgets.QRadioButton(self.boxLineStyle)
        self.rbNoLine.setObjectName("rbNoLine")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.rbNoLine)
        self.rbSolidLine = QtWidgets.QRadioButton(self.boxLineStyle)
        self.rbSolidLine.setObjectName("rbSolidLine")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rbSolidLine)
        self.rbDashLine = QtWidgets.QRadioButton(self.boxLineStyle)
        self.rbDashLine.setObjectName("rbDashLine")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.rbDashLine)
        self.rbDotLine = QtWidgets.QRadioButton(self.boxLineStyle)
        self.rbDotLine.setObjectName("rbDotLine")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.rbDotLine)
        self.rbDashDotLine = QtWidgets.QRadioButton(self.boxLineStyle)
        self.rbDashDotLine.setObjectName("rbDashDotLine")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.rbDashDotLine)
        self.rbDashDotDotLine = QtWidgets.QRadioButton(self.boxLineStyle)
        self.rbDashDotDotLine.setObjectName("rbDashDotDotLine")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.rbDashDotDotLine)
        self.lblLineWidth = QtWidgets.QLabel(self.boxLineStyle)
        self.lblLineWidth.setObjectName("lblLineWidth")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.lblLineWidth)
        self.spinLineWidth = QtWidgets.QSpinBox(self.boxLineStyle)
        self.spinLineWidth.setMinimum(1)
        self.spinLineWidth.setMaximum(10)
        self.spinLineWidth.setObjectName("spinLineWidth")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.spinLineWidth)
        self.lblLineWidth.setBuddy(self.spinLineWidth)

        self.retranslateUi(RelFormatTemplate)
        self.okButton.clicked.connect(RelFormatTemplate.accept)
        self.cancelButton.clicked.connect(RelFormatTemplate.reject)
        QtCore.QMetaObject.connectSlotsByName(RelFormatTemplate)

    def retranslateUi(self, RelFormatTemplate):
        _translate = QtCore.QCoreApplication.translate
        RelFormatTemplate.setWindowTitle(_translate("RelFormatTemplate", "Relationship Instance Format"))
        self.okButton.setText(_translate("RelFormatTemplate", "&OK"))
        self.cancelButton.setText(_translate("RelFormatTemplate", "&Cancel"))
        self.boxFillStyle.setTitle(_translate("RelFormatTemplate", "Fill Style"))
        self.rbNone.setText(_translate("RelFormatTemplate", "None"))
        self.rbFill.setText(_translate("RelFormatTemplate", "Solid"))
        self.rbPattern.setText(_translate("RelFormatTemplate", "Pattern"))
        self.groupBox.setTitle(_translate("RelFormatTemplate", "Sample Node Formatting"))
        self.btnFillColor.setText(_translate("RelFormatTemplate", "Fill Color"))
        self.btnLineColor.setText(_translate("RelFormatTemplate", "Line Color"))
        self.boxLineStyle.setTitle(_translate("RelFormatTemplate", "Line Style"))
        self.rbNoLine.setText(_translate("RelFormatTemplate", "No Line"))
        self.rbSolidLine.setText(_translate("RelFormatTemplate", "Solid"))
        self.rbDashLine.setText(_translate("RelFormatTemplate", "Dash"))
        self.rbDotLine.setText(_translate("RelFormatTemplate", "Dot"))
        self.rbDashDotLine.setText(_translate("RelFormatTemplate", "Dash Dot"))
        self.rbDashDotDotLine.setText(_translate("RelFormatTemplate", "Dash Dot Dot"))
        self.lblLineWidth.setText(_translate("RelFormatTemplate", "Line Width: "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RelFormatTemplate = QtWidgets.QDialog()
    ui = Ui_RelFormatTemplate()
    ui.setupUi(RelFormatTemplate)
    RelFormatTemplate.show()
    sys.exit(app.exec_())

