# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqt4_gui.ui'
#
# Created: Sun Jul 11 16:38:37 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.mnuFile = QtGui.QMenu(self.menubar)
        self.mnuFile.setObjectName("mnuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dwProperties = QtGui.QDockWidget(MainWindow)
        self.dwProperties.setObjectName("dwProperties")
        self.dwcProperties = QtGui.QWidget()
        self.dwcProperties.setObjectName("dwcProperties")
        self.verticalLayout = QtGui.QVBoxLayout(self.dwcProperties)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gbOptions = QtGui.QGroupBox(self.dwcProperties)
        self.gbOptions.setObjectName("gbOptions")
        self.verticalLayout.addWidget(self.gbOptions)
        self.twProperties = QtGui.QTableWidget(self.dwcProperties)
        self.twProperties.setObjectName("twProperties")
        self.twProperties.setColumnCount(0)
        self.twProperties.setRowCount(0)
        self.verticalLayout.addWidget(self.twProperties)
        self.dwProperties.setWidget(self.dwcProperties)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dwProperties)
        self.mnuExit = QtGui.QAction(MainWindow)
        self.mnuExit.setObjectName("mnuExit")
        self.mnuFile.addAction(self.mnuExit)
        self.menubar.addAction(self.mnuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "pybox2d testbed", None, QtGui.QApplication.UnicodeUTF8))
        self.mnuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.dwProperties.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.gbOptions.setTitle(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.twProperties.setSortingEnabled(True)
        self.mnuExit.setText(QtGui.QApplication.translate("MainWindow", "E&xit", None, QtGui.QApplication.UnicodeUTF8))

