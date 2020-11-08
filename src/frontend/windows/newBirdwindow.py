# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton

from src.frontend.widgets.QGMapsLocatorWidget import QGMapsLocatorWidget
from src.frontend.widgets.QHintCombo import QHintCombo


class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'New marker'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 620
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

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

        self.show()

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file'
                                            , filter="Image files (*.jpg *.gif *.png *.bmp)")
        self.le.setPixmap(QPixmap(fname))
