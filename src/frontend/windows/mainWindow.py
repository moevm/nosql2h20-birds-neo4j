# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from src.frontend.widgets.QGMapsLocatorWidget import QGMapsLocatorWidget
from src.frontend.widgets.QHintCombo import QHintCombo


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        API_KEY = "AIzaSyD1VkY2p8-r3zH_wrpMk6xkPWc6dweaThM+"
        self.birdsMap = QGMapsLocatorWidget(api_key=API_KEY, parent=self.centralwidget)
        self.birdsMap.setGeometry(QtCore.QRect(10, 45, 780, 550))
        self.birdsMap.waitUntilReady()
        self.birdsMap.setZoom(14)
        lat, lng = self.birdsMap.centerAtAddress("Russia")
        if lat is None and lng is None:
            lat, lng = -12.0463731, -77.042754
            self.birdsMap.centerAt(lat, lng)

        self.specInput = QHintCombo(items=["Воробей", "Петух", "Попугай", "Ворона"], parent=self.centralwidget)
        self.specInput.setGeometry(10, 10, 180, 25)

        # self.addspecButton = QtWidgets.QPushButton(self.centralwidget)
        # self.addspecButton.setGeometry(200, 10, 25, 25)
        # self.addspecButton.setIcon(QIcon(QPixmap('./res/plus.png')))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

