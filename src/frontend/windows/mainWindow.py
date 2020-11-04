# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets

from src.frontend.widgets.QGMapsLocatorWidget import QGMapsLocatorWidget


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        API_KEY = "AIzaSyD1VkY2p8-r3zH_wrpMk6xkPWc6dweaThM+"

        self.w = QGMapsLocatorWidget(api_key=API_KEY, parent=self.centralwidget)
        self.w.setGeometry(QtCore.QRect(10, 10, 640, 480))
        # self.w.resize(640, 480)
        # self.w.show()
        self.w.waitUntilReady()
        self.w.setZoom(14)
        lat, lng = self.w.centerAtAddress("Russia")
        if lat is None and lng is None:
            lat, lng = -12.0463731, -77.042754
            self.w.centerAt(lat, lng)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
