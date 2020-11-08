# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap

from src.frontend.widgets.QGoogleMapsMarkerViewWidget import QGoogleMapsMarkerViewWidget
from src.frontend.widgets.QHintCombo import QHintCombo
from src.frontend.widgets.QtImageViewer import QImageviewer
from src.frontend.windows.newBirdwindow import AnotherWindow


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
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        API_KEY = "AIzaSyD1VkY2p8-r3zH_wrpMk6xkPWc6dweaThM+"
        self.birdsMap = QGoogleMapsMarkerViewWidget(api_key=API_KEY, parent=self.centralwidget)
        self.birdsMap.setGeometry(QtCore.QRect(0, 0, 800, 620))
        self.birdsMap.waitUntilReady()
        self.birdsMap.setZoom(14)
        lat, lng = self.birdsMap.centerAtAddress("Russia")
        if lat is None and lng is None:
            lat, lng = 60.010297, 30.418990
            self.birdsMap.centerAt(lat, lng)
        self.birdsMap.markerClicked.connect(self.showBird)

        # demo thing:
        mass = [['1', 60.010400, 30.416168, "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"],
                ['2', 60.010536, 30.412821, "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"],
                ['3', 60.010600, 30.410000, "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"]]
        self.birdsMap.showMarkers(mass)

        self.specInput = QHintCombo(items=["Воробей", "Петух", "Попугай", "Ворона"], parent=self.centralwidget)
        self.specInput.setGeometry(10, 10, 180, 25)

        self.addspecButton = QtWidgets.QPushButton(text="I saw a bird!", parent=self.centralwidget)
        self.addspecButton.clicked.connect(self.openNewBirdWindow)
        self.addspecButton.setGeometry(200, 10, 100, 25)

        self.image = QImageviewer(parent=self)
        self.image.setScaledContents(True)
        self.image.setGeometry(275, 420, 250, 180)
        self.image.hide()


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def openNewBirdWindow(self):
        if self.w is None:
            self.w = AnotherWindow()
        self.w.show()

    def showBird(self, key, lat, lng):
        # TODO: get bird data to show from DB
        image = QPixmap('../res/img/bird_photos/bird_photo1.jpg')
        self.image.setPixmap(image)
        g = self.image.geometry()
        g.setHeight(250.0 * image.height() / image.width())
        self.image.setGeometry(g)
        self.image.show(animation=False)
        print(key)
        return
