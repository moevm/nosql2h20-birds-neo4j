# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QLabel, QMessageBox

from src.frontend.widgets.QGMapsLocatorWidget import QGMapsLocatorWidget
from src.frontend.widgets.QHintCombo import QHintCombo
from src.frontend.widgets.QtImageViewer import QImageviewer


class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'New marker'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 800, 620)

        API_KEY = "AIzaSyD1VkY2p8-r3zH_wrpMk6xkPWc6dweaThM+"
        birdsMap = QGMapsLocatorWidget(api_key=API_KEY, parent=self)
        birdsMap.setGeometry(QtCore.QRect(0, 0, 800, 620))
        birdsMap.waitUntilReady()
        birdsMap.setZoom(14)
        lat, lng = birdsMap.centerAtAddress("Russia")
        if lat is None and lng is None:
            lat, lng = 60.010297, 30.418990
            birdsMap.centerAt(lat, lng)
        birdsMap.move(0, 0)

        self.specInput = QHintCombo(items=["Воробей", "Петух", "Попугай", "Ворона"], parent=self)
        self.specInput.setGeometry(10, 10, 180, 25)

        self.picBtn = QPushButton(icon=QIcon(QPixmap('../res/img/add_photo_icon.png')), parent=self)
        self.picBtn.clicked.connect(self.getfile)
        self.picBtn.setGeometry(200, 10, 25, 25)

        self.okBtn = QPushButton(icon=QIcon(QPixmap('../res/img/ok_icon.jpg')), parent=self)
        self.okBtn.clicked.connect(self.addBird)
        self.okBtn.setGeometry(235, 10, 25, 25)

        self.image = QImageviewer(parent=self)
        self.image.setScaledContents(True)
        self.image.setGeometry(10, 45, 250, 180)
        self.image.hide()

        self.show()

    def getfile(self):
        fname, err = QFileDialog.getOpenFileName(self, 'Open file', filter="Image files (*.jpg *.gif *.png *.bmp)")
        image = QPixmap(fname)
        self.image.setPixmap(image)
        g = self.image.geometry()
        g.setHeight(250.0 * image.height() / image.width())
        self.image.setGeometry(g)
        self.image.show(animation=True)

    def addBird(self):
        msg = QMessageBox()
        # msg.setWindowIcon(QIcon(QPixmap('../res/img/success_icon.png')))
        msg.setText("bird marker added!")
        msg.setWindowTitle("Success!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.image.hide()
        return

