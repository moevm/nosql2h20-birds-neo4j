# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QMessageBox

from frontend.widgets.QGMapsLocatorWidget import QGMapsLocatorWidget
from frontend.widgets.QHintCombo import QHintCombo
from frontend.widgets.QtImageViewer import QImageviewer


class NewBirdwindow(QWidget):
    # These are new bird nodes fields specified currently
    fname = None
    lat = 0
    lang = 0

    def __init__(self, databaseConnector, parent=None):
        super().__init__()
        self.parent = parent
        self.databaseConnector = databaseConnector
        self.title = 'New marker'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 800, 620)

        API_KEY = "AIzaSyD1VkY2p8-r3zH_wrpMk6xkPWc6dweaThM+"
        self.birdsMap = QGMapsLocatorWidget(api_key=API_KEY, parent=self)
        self.birdsMap.setGeometry(QtCore.QRect(0, 0, 800, 620))
        self.birdsMap.waitUntilReady()
        self.birdsMap.setZoom(14)
        lat, lng = 59.9713021, 30.3239561
        self.birdsMap.centerAt(lat, lng)
        self.birdsMap.move(0, 0)
        self.birdsMap.mapClicked.connect(self.rememberCords)

        self.specInput = QHintCombo(items=self.databaseConnector.getSpecies(), parent=self)
        self.specInput.setGeometry(190, 10, 180, 25)

        self.picBtn = QPushButton(icon=QIcon(QPixmap('./res/img/add_photo_icon.png')), parent=self)
        self.picBtn.clicked.connect(self.getfile)
        self.picBtn.setGeometry(380, 10, 25, 25)

        self.okBtn = QPushButton('✓', parent=self)
        self.okBtn.clicked.connect(self.addBird)
        self.okBtn.setGeometry(415, 10, 25, 25)

        self.image = QImageviewer(parent=self)
        self.image.setScaledContents(True)
        self.image.setGeometry(10, 45, 250, 180)
        self.image.hide()

        self.show()

    def rememberCords(self, lat, lang):
        self.lat, self.lang = lat, lang

    def getfile(self):
        fname, err = QFileDialog.getOpenFileName(self, 'Open file', filter="Image files (*.jpg *.jpeg *.gif *.png *.bmp)")
        self.fname = fname
        image = QPixmap(fname)
        self.image.setPixmap(image)
        g = self.image.geometry()
        g.setHeight(250.0 * image.height() / image.width())
        self.image.setGeometry(g)
        self.image.show(animation=True)

    def addBird(self):
        msg = QMessageBox()
        birdName = self.specInput.currentText()
        self.databaseConnector.create_bird(url=self.fname, name=birdName, latitude=self.lat, longitude=self.lang)
        # msg.setWindowIcon(QIcon(QPixmap('../res/img/success_icon.png')))
        # refresh those fields in a stupid way
        self.parent.refresh()
        if self.parent.dbWindow:  # Might be None
            self.parent.dbWindow.refresh()
        self.specInput.setItems(self.databaseConnector.getSpecies())
        msg.setText("bird marker added!")
        msg.setWindowTitle("Success!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.image.hide()
        return
