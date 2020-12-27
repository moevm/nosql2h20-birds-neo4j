# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap

from frontend.widgets.QGoogleMapsMarkerViewWidget import QGoogleMapsMarkerViewWidget
from frontend.widgets.QHintCombo import QHintCombo
from frontend.widgets.QtImageViewer import QImageviewer
from frontend.windows.DatabaseWindow import DatabaseWindow
from frontend.windows.NewBirdwindow import NewBirdwindow


class MainWindow(object):
    ALL_LABEL = "Все"
    dbWindow = None
    secondWindow = None
    data = None

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

        self.data = self.databaseConnector.get_all_birds_area()  # All the birds
        marker = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"
        self.birdsMap.showMarkers([[i, r['latitude'], r['longitude'], marker] for i, r in enumerate(self.data)])

        species = self.databaseConnector.getSpecies()
        species.append(self.ALL_LABEL)
        species.reverse()  # ALL_LABEl comes first
        self.specInput = QHintCombo(items=species, parent=self.centralwidget)
        self.specInput.setGeometry(10, 10, 180, 25)
        self.specInput.currentIndexChanged.connect(self.chooseSpec)

        self.addspecButton = QtWidgets.QPushButton(text="I saw a bird!", parent=self.centralwidget)
        self.addspecButton.clicked.connect(self.openNewBirdWindow)
        self.addspecButton.setGeometry(200, 10, 100, 25)

        self.showStatsButton = QtWidgets.QPushButton(text="Database...", parent=self.centralwidget)
        self.showStatsButton.clicked.connect(self.openDatabaseWindow)
        self.showStatsButton.setGeometry(690, 10, 100, 25)

        self.image = QImageviewer(parent=self)
        self.image.setScaledContents(True)
        self.image.setGeometry(275, 420, 250, 180)
        self.image.hide()

        self.secondWindow = None

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def openNewBirdWindow(self):
        if self.secondWindow is None:
            self.secondWindow = NewBirdwindow(self.databaseConnector, self)
        self.secondWindow.show()

    def openDatabaseWindow(self):
        if self.dbWindow is None:
            self.dbWindow = DatabaseWindow(self.databaseConnector)
        self.dbWindow.show()

    def showBird(self, key, lat, lng):
        try:
            fname = self.databaseConnector.getBirdById(int(key))
            image = QPixmap(fname)
            self.image.setPixmap(image)
            g = self.image.geometry()
            g.setHeight(250.0 * image.height() / image.width())
            self.image.setGeometry(g)
            self.image.show(animation=False)
        except:
            print('Failed to open photo; make sure it is located in a directory mounted if using docker!')
        return

    def chooseSpec(self, index):
        specLabel = self.specInput.currentText()
        # specLabel = None if specLabel == self.ALL_LABEL else specLabel
        if specLabel == self.ALL_LABEL:
            self.data = self.databaseConnector.get_all_birds_area()  # All the birds
        else:
            self.data = self.databaseConnector.get_birds_area(specLabel)
        print(self.data)
        marker = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"
        self.birdsMap.showMarkers([[r["id"], r["latitude"], r["longitude"], marker] for i, r in enumerate(self.data)])

    def refreshSpec(self):
        species = self.databaseConnector.getSpecies()
        species.append(self.ALL_LABEL)
        species.reverse()  # ALL_LABEl comes first
        self.specInput = QHintCombo(items=species, parent=self.centralwidget)
        self.specInput.setGeometry(10, 10, 180, 25)
        self.specInput.currentIndexChanged.connect(self.chooseSpec)
