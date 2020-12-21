# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\forms\tabPageWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_pageWidget(object):
    def setupUi(self, pageWidget):
        pageWidget.setObjectName("pageWidget")
        pageWidget.resize(691, 491)
        self.verticalLayout = QtWidgets.QVBoxLayout(pageWidget)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabPage = QtWidgets.QTabWidget(pageWidget)
        self.tabPage.setTabsClosable(True)
        self.tabPage.setMovable(True)
        self.tabPage.setObjectName("tabPage")
        self.verticalLayout.addWidget(self.tabPage)

        self.retranslateUi(pageWidget)
        QtCore.QMetaObject.connectSlotsByName(pageWidget)

    def retranslateUi(self, pageWidget):
        _translate = QtCore.QCoreApplication.translate
        pageWidget.setWindowTitle(_translate("pageWidget", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pageWidget = QtWidgets.QWidget()
    ui = Ui_pageWidget()
    ui.setupUi(pageWidget)
    pageWidget.show()
    sys.exit(app.exec_())

