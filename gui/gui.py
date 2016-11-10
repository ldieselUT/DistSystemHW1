# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(869, 591)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.connectionVLayout = QtGui.QVBoxLayout()
        self.connectionVLayout.setMargin(11)
        self.connectionVLayout.setSpacing(6)
        self.connectionVLayout.setObjectName(_fromUtf8("connectionVLayout"))
        self.connectionHLayout = QtGui.QHBoxLayout()
        self.connectionHLayout.setMargin(11)
        self.connectionHLayout.setSpacing(6)
        self.connectionHLayout.setObjectName(_fromUtf8("connectionHLayout"))
        self.addresLabel = QtGui.QLabel(self.centralWidget)
        self.addresLabel.setObjectName(_fromUtf8("addresLabel"))
        self.connectionHLayout.addWidget(self.addresLabel)
        self.addressLineEdit = QtGui.QLineEdit(self.centralWidget)
        self.addressLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.addressLineEdit.setObjectName(_fromUtf8("addressLineEdit"))
        self.connectionHLayout.addWidget(self.addressLineEdit)
        self.portLabel = QtGui.QLabel(self.centralWidget)
        self.portLabel.setObjectName(_fromUtf8("portLabel"))
        self.connectionHLayout.addWidget(self.portLabel)
        self.portSpinBox = QtGui.QSpinBox(self.centralWidget)
        self.portSpinBox.setWrapping(False)
        self.portSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.portSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.portSpinBox.setMaximum(65535)
        self.portSpinBox.setProperty("value", 7777)
        self.portSpinBox.setObjectName(_fromUtf8("portSpinBox"))
        self.connectionHLayout.addWidget(self.portSpinBox)
        self.newPushButton = QtGui.QPushButton(self.centralWidget)
        self.newPushButton.setObjectName(_fromUtf8("newPushButton"))
        self.connectionHLayout.addWidget(self.newPushButton)
        self.remotePushButton = QtGui.QPushButton(self.centralWidget)
        self.remotePushButton.setObjectName(_fromUtf8("remotePushButton"))
        self.connectionHLayout.addWidget(self.remotePushButton)
        self.connectionVLayout.addLayout(self.connectionHLayout)
        self.statusLabel = QtGui.QLabel(self.centralWidget)
        self.statusLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statusLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.connectionVLayout.addWidget(self.statusLabel)
        self.verticalLayout.addLayout(self.connectionVLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textEdit = QtGui.QTextEdit(self.centralWidget)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout.addWidget(self.textEdit)
        self.textEdit_2 = QtGui.QTextEdit(self.centralWidget)
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.horizontalLayout.addWidget(self.textEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 869, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.addresLabel.setText(_translate("MainWindow", "Address", None))
        self.addressLineEdit.setInputMask(_translate("MainWindow", "000.000.000.000", None))
        self.addressLineEdit.setText(_translate("MainWindow", "127.000.000.001", None))
        self.addressLineEdit.setPlaceholderText(_translate("MainWindow", "e.g. localhost", None))
        self.portLabel.setText(_translate("MainWindow", "Port", None))
        self.newPushButton.setText(_translate("MainWindow", "New Document", None))
        self.remotePushButton.setText(_translate("MainWindow", "Remote Document", None))
        self.statusLabel.setText(_translate("MainWindow", "Not connected", None))

