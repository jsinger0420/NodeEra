# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jsing\OneDrive\Documents\DEV_LAPTOP_LOCAL_REPO\NODEERA\forms\cypherPageWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CypherPageWidget(object):
    def setupUi(self, CypherPageWidget):
        CypherPageWidget.setObjectName("CypherPageWidget")
        CypherPageWidget.resize(890, 623)
        self.horizontalLayout = QtWidgets.QHBoxLayout(CypherPageWidget)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(CypherPageWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frmExplorer = QtWidgets.QFrame(self.splitter)
        self.frmExplorer.setFrameShape(QtWidgets.QFrame.Box)
        self.frmExplorer.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmExplorer.setObjectName("frmExplorer")
        self.gridLayout = QtWidgets.QGridLayout(self.frmExplorer)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.frameExplorer = QtWidgets.QFrame(self.frmExplorer)
        self.frameExplorer.setMinimumSize(QtCore.QSize(0, 0))
        self.frameExplorer.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frameExplorer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameExplorer.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameExplorer.setObjectName("frameExplorer")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frameExplorer)
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter_2 = QtWidgets.QSplitter(self.frameExplorer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.frame = QtWidgets.QFrame(self.splitter_2)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_3.setSpacing(1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.editNeo4j = QtWidgets.QLineEdit(self.frame)
        self.editNeo4j.setReadOnly(True)
        self.editNeo4j.setObjectName("editNeo4j")
        self.gridLayout_3.addWidget(self.editNeo4j, 0, 0, 1, 1)
        self.btnRefresh = QtWidgets.QPushButton(self.frame)
        self.btnRefresh.setObjectName("btnRefresh")
        self.gridLayout_3.addWidget(self.btnRefresh, 0, 1, 1, 1)
        self.tvSchema = QtWidgets.QTreeWidget(self.frame)
        self.tvSchema.setObjectName("tvSchema")
        self.tvSchema.headerItem().setText(0, "1")
        self.gridLayout_3.addWidget(self.tvSchema, 1, 0, 1, 2)
        self.frmNav = QtWidgets.QFrame(self.splitter_2)
        self.frmNav.setMinimumSize(QtCore.QSize(0, 0))
        self.frmNav.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frmNav.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frmNav.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmNav.setObjectName("frmNav")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frmNav)
        self.verticalLayout_5.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_3 = QtWidgets.QFrame(self.frmNav)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.editPath = QtWidgets.QLineEdit(self.frame_3)
        self.editPath.setReadOnly(True)
        self.editPath.setObjectName("editPath")
        self.horizontalLayout_3.addWidget(self.editPath)
        self.btnPickPath = QtWidgets.QPushButton(self.frame_3)
        self.btnPickPath.setObjectName("btnPickPath")
        self.horizontalLayout_3.addWidget(self.btnPickPath)
        self.verticalLayout_5.addWidget(self.frame_3)
        self.frame_2 = QtWidgets.QFrame(self.frmNav)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tvFileSystem = QtWidgets.QTreeView(self.frame_2)
        self.tvFileSystem.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tvFileSystem.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tvFileSystem.setObjectName("tvFileSystem")
        self.gridLayout_2.addWidget(self.tvFileSystem, 0, 0, 1, 1)
        self.verticalLayout_5.addWidget(self.frame_2)
        self.verticalLayout_3.addWidget(self.splitter_2)
        self.gridLayout.addWidget(self.frameExplorer, 0, 0, 1, 1)
        self.frameTabs = QtWidgets.QFrame(self.splitter)
        self.frameTabs.setFrameShape(QtWidgets.QFrame.Box)
        self.frameTabs.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameTabs.setObjectName("frameTabs")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frameTabs)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frmMainButtons = QtWidgets.QFrame(self.frameTabs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmMainButtons.sizePolicy().hasHeightForWidth())
        self.frmMainButtons.setSizePolicy(sizePolicy)
        self.frmMainButtons.setMinimumSize(QtCore.QSize(0, 40))
        self.frmMainButtons.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frmMainButtons.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frmMainButtons.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmMainButtons.setObjectName("frmMainButtons")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frmMainButtons)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnNew = QtWidgets.QToolButton(self.frmMainButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/FILE/FILE/CreateNew.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNew.setIcon(icon)
        self.btnNew.setIconSize(QtCore.QSize(32, 32))
        self.btnNew.setAutoRaise(True)
        self.btnNew.setObjectName("btnNew")
        self.horizontalLayout_2.addWidget(self.btnNew)
        self.btnOpen = QtWidgets.QToolButton(self.frmMainButtons)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/FILE/FILE/Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOpen.setIcon(icon1)
        self.btnOpen.setIconSize(QtCore.QSize(32, 32))
        self.btnOpen.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.btnOpen.setAutoRaise(True)
        self.btnOpen.setObjectName("btnOpen")
        self.horizontalLayout_2.addWidget(self.btnOpen)
        self.btnSave = QtWidgets.QToolButton(self.frmMainButtons)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/FILE/FILE/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon2)
        self.btnSave.setIconSize(QtCore.QSize(32, 32))
        self.btnSave.setAutoRaise(True)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_2.addWidget(self.btnSave)
        self.btnSaveAs = QtWidgets.QToolButton(self.frmMainButtons)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/FILE/FILE/Saveas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSaveAs.setIcon(icon3)
        self.btnSaveAs.setIconSize(QtCore.QSize(32, 32))
        self.btnSaveAs.setAutoRaise(True)
        self.btnSaveAs.setObjectName("btnSaveAs")
        self.horizontalLayout_2.addWidget(self.btnSaveAs)
        self.btnClose = QtWidgets.QToolButton(self.frmMainButtons)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/FILE/FILE/Close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClose.setIcon(icon4)
        self.btnClose.setIconSize(QtCore.QSize(32, 32))
        self.btnClose.setAutoRaise(True)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout_2.addWidget(self.btnClose)
        self.btnZoomIn = QtWidgets.QToolButton(self.frmMainButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnZoomIn.sizePolicy().hasHeightForWidth())
        self.btnZoomIn.setSizePolicy(sizePolicy)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/DIAGRAM/DIAGRAM/icons8-zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnZoomIn.setIcon(icon5)
        self.btnZoomIn.setIconSize(QtCore.QSize(32, 32))
        self.btnZoomIn.setAutoRaise(True)
        self.btnZoomIn.setObjectName("btnZoomIn")
        self.horizontalLayout_2.addWidget(self.btnZoomIn)
        self.btnZoomOut = QtWidgets.QToolButton(self.frmMainButtons)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/DIAGRAM/DIAGRAM/icons8-zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnZoomOut.setIcon(icon6)
        self.btnZoomOut.setIconSize(QtCore.QSize(32, 32))
        self.btnZoomOut.setAutoRaise(True)
        self.btnZoomOut.setObjectName("btnZoomOut")
        self.horizontalLayout_2.addWidget(self.btnZoomOut)
        self.btnComment = QtWidgets.QToolButton(self.frmMainButtons)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/FILE/FILE/comment.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnComment.setIcon(icon7)
        self.btnComment.setIconSize(QtCore.QSize(32, 32))
        self.btnComment.setAutoRaise(True)
        self.btnComment.setObjectName("btnComment")
        self.horizontalLayout_2.addWidget(self.btnComment)
        self.btnUnComment = QtWidgets.QToolButton(self.frmMainButtons)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/FILE/FILE/nocomment.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUnComment.setIcon(icon8)
        self.btnUnComment.setIconSize(QtCore.QSize(32, 32))
        self.btnUnComment.setAutoRaise(True)
        self.btnUnComment.setObjectName("btnUnComment")
        self.horizontalLayout_2.addWidget(self.btnUnComment)
        self.btnUndo = QtWidgets.QToolButton(self.frmMainButtons)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/FILE/icons8-undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUndo.setIcon(icon9)
        self.btnUndo.setIconSize(QtCore.QSize(32, 32))
        self.btnUndo.setAutoRaise(True)
        self.btnUndo.setObjectName("btnUndo")
        self.horizontalLayout_2.addWidget(self.btnUndo)
        self.btnRedo = QtWidgets.QToolButton(self.frmMainButtons)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/FILE/icons8-redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRedo.setIcon(icon10)
        self.btnRedo.setIconSize(QtCore.QSize(32, 32))
        self.btnRedo.setAutoRaise(True)
        self.btnRedo.setObjectName("btnRedo")
        self.horizontalLayout_2.addWidget(self.btnRedo)
        spacerItem = QtWidgets.QSpacerItem(413, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frmMainButtons)
        self.frmCypherTabs = QtWidgets.QFrame(self.frameTabs)
        self.frmCypherTabs.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frmCypherTabs.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmCypherTabs.setObjectName("frmCypherTabs")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frmCypherTabs)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.frmCypherTabs)
        self.tabCypher = QtWidgets.QTabWidget(self.frameTabs)
        self.tabCypher.setToolTip("")
        self.tabCypher.setTabsClosable(True)
        self.tabCypher.setMovable(True)
        self.tabCypher.setObjectName("tabCypher")
        self.verticalLayout.addWidget(self.tabCypher)
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(CypherPageWidget)
        QtCore.QMetaObject.connectSlotsByName(CypherPageWidget)
        CypherPageWidget.setTabOrder(self.editNeo4j, self.btnRefresh)
        CypherPageWidget.setTabOrder(self.btnRefresh, self.tvSchema)
        CypherPageWidget.setTabOrder(self.tvSchema, self.editPath)
        CypherPageWidget.setTabOrder(self.editPath, self.btnPickPath)
        CypherPageWidget.setTabOrder(self.btnPickPath, self.tvFileSystem)
        CypherPageWidget.setTabOrder(self.tvFileSystem, self.btnNew)
        CypherPageWidget.setTabOrder(self.btnNew, self.btnOpen)
        CypherPageWidget.setTabOrder(self.btnOpen, self.btnSave)
        CypherPageWidget.setTabOrder(self.btnSave, self.btnSaveAs)
        CypherPageWidget.setTabOrder(self.btnSaveAs, self.btnClose)
        CypherPageWidget.setTabOrder(self.btnClose, self.btnZoomIn)
        CypherPageWidget.setTabOrder(self.btnZoomIn, self.btnZoomOut)
        CypherPageWidget.setTabOrder(self.btnZoomOut, self.btnComment)
        CypherPageWidget.setTabOrder(self.btnComment, self.btnUnComment)
        CypherPageWidget.setTabOrder(self.btnUnComment, self.btnUndo)
        CypherPageWidget.setTabOrder(self.btnUndo, self.btnRedo)
        CypherPageWidget.setTabOrder(self.btnRedo, self.tabCypher)

    def retranslateUi(self, CypherPageWidget):
        _translate = QtCore.QCoreApplication.translate
        CypherPageWidget.setWindowTitle(_translate("CypherPageWidget", "Form"))
        self.btnRefresh.setText(_translate("CypherPageWidget", "Refresh"))
        self.btnPickPath.setText(_translate("CypherPageWidget", "Path..."))
        self.btnNew.setToolTip(_translate("CypherPageWidget", "New Cypher Query"))
        self.btnNew.setText(_translate("CypherPageWidget", "New"))
        self.btnOpen.setToolTip(_translate("CypherPageWidget", "Open Cypher File"))
        self.btnOpen.setText(_translate("CypherPageWidget", "Open"))
        self.btnSave.setToolTip(_translate("CypherPageWidget", "Save Cypher File"))
        self.btnSave.setText(_translate("CypherPageWidget", "Save"))
        self.btnSaveAs.setToolTip(_translate("CypherPageWidget", "Save Cypher file As..."))
        self.btnSaveAs.setText(_translate("CypherPageWidget", "SaveAs"))
        self.btnClose.setToolTip(_translate("CypherPageWidget", "Close Cypher File"))
        self.btnClose.setText(_translate("CypherPageWidget", "Close"))
        self.btnZoomIn.setToolTip(_translate("CypherPageWidget", "Increase Font Size"))
        self.btnZoomIn.setText(_translate("CypherPageWidget", "..."))
        self.btnZoomOut.setToolTip(_translate("CypherPageWidget", "Decrease Font Size"))
        self.btnZoomOut.setText(_translate("CypherPageWidget", "..."))
        self.btnComment.setToolTip(_translate("CypherPageWidget", "Comment Line"))
        self.btnComment.setText(_translate("CypherPageWidget", "..."))
        self.btnUnComment.setToolTip(_translate("CypherPageWidget", "Uncomment Line"))
        self.btnUnComment.setText(_translate("CypherPageWidget", "..."))
        self.btnUndo.setToolTip(_translate("CypherPageWidget", "UnDo"))
        self.btnUndo.setText(_translate("CypherPageWidget", "..."))
        self.btnRedo.setToolTip(_translate("CypherPageWidget", "ReDo"))
        self.btnRedo.setText(_translate("CypherPageWidget", "..."))

import icons.icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CypherPageWidget = QtWidgets.QWidget()
    ui = Ui_CypherPageWidget()
    ui.setupUi(CypherPageWidget)
    CypherPageWidget.show()
    sys.exit(app.exec_())

