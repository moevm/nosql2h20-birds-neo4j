from PyQt5.QtWidgets import QWidget, QRadioButton, QLabel, QFileDialog, QMessageBox
from frontend.widgets.MplWidget import MplWidget
from PyQt5 import QtWidgets
import numpy as np

from frontend.widgets.QHintCombo import QHintCombo


class DatabaseWindow(QWidget):
    ALL_LABEL = "Все"
    canvas = None
    plotWidget = None
    importDbButton = None
    exportDbButton = None
    specInput = None
    axisLabel = None
    b1, b2, selected_btn = None, None, None

    def __init__(self, databaseConnector):
        super().__init__()
        self.databaseConnector = databaseConnector
        self.title = 'Statistics/management'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 800, 600)
        self.plotWidget = MplWidget(self, width=5, height=4, dpi=100)
        self.plotWidget.setGeometry(0, 0, 800, 550)

        species = self.databaseConnector.getSpecies()
        species.append(self.ALL_LABEL)
        species.reverse()  # ALL_LABEL comes first
        self.specInput = QHintCombo(items=species, parent=self)
        self.specInput.setGeometry(10, 550, 180, 25)
        self.specInput.currentIndexChanged.connect(lambda: self.draw_statistics(self.selected_btn))

        self.axisLabel = QLabel("Axis 'X':", parent=self)
        self.axisLabel.setGeometry(200, 550, 50, 25)

        self.b1 = QRadioButton("Latitude", parent=self)
        self.b1.setGeometry(260, 550, 100, 25)
        self.b1.toggled.connect(lambda: self.btnstate(self.b1))
        self.b1.setChecked(True)
        self.selected_btn = self.b1

        self.b2 = QRadioButton("Longitude", parent=self)
        self.b2.setGeometry(260, 575, 100, 25)
        self.b2.toggled.connect(lambda: self.btnstate(self.b2))

        self.importDbButton = QtWidgets.QPushButton(text="Import DB", parent=self)
        self.importDbButton.setGeometry(580, 550, 100, 25)
        self.importDbButton.clicked.connect(self.importDatabase)

        self.exportDbButton = QtWidgets.QPushButton(text="Export DB", parent=self)
        self.exportDbButton.setGeometry(690, 550, 100, 25)
        self.exportDbButton.clicked.connect(self.exportDatabase)

    def btnstate(self, b):
        if b.isChecked():
            self.selected_btn = b
            self.draw_statistics(b)

    def draw_statistics(self, b):
        bird_kind = self.specInput.currentText()
        geo_coord = b.text()

        if bird_kind == self.ALL_LABEL:
            a = self.databaseConnector.get_all_birds_area()
        else:
            a = self.databaseConnector.get_birds_area(bird_kind)

        x_axis = ([a[i][geo_coord.lower()] for i in range(len(a))])
        y_axis = [self.count_range_in_list(x_axis, i - 5, i + 5) for i in np.arange(0, 90, 10)]

        self.plotWidget.canvas.axes.clear()
        self.plotWidget.canvas.axes.bar(np.arange(0, 90, 10), y_axis, width=10)
        self.plotWidget.canvas.axes.set_xlabel(geo_coord)
        self.plotWidget.canvas.axes.set_ylabel(bird_kind)
        self.plotWidget.canvas.axes.set_xlim(0)
        self.plotWidget.canvas.axes.set_xticks(np.arange(0, 90, 5))
        self.plotWidget.canvas.axes.set_yticks(np.arange(0, max(y_axis) + 1, max(y_axis) // 10 + 1))
        self.plotWidget.canvas.draw()
        self.plotWidget.canvas.flush_events()
        return

    def count_range_in_list(self, lst, min, max):
        ctr = 0
        for x in lst:
            if min <= x <= max:
                ctr += 1
        return ctr

    def importDatabase(self):
        fname, err = QFileDialog.getOpenFileName(self, 'Save file', filter="CSV (*.csv)")
        try:
            self.databaseConnector.importData(fname)
            msg = QMessageBox()
            msg.setText("Database loaded!")
            msg.setWindowTitle("Success!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setText("Database not loaded! Very bad!")
            msg.setWindowTitle("Failure!")
            msg.setStandardButtons(QMessageBox.Discard)
            msg.exec_()

    def exportDatabase(self):
        fname, err = QFileDialog.getSaveFileName(self, 'Save file', filter="CSV (*.csv)")
        try:
            self.databaseConnector.exportData(fname)
            msg = QMessageBox()
            msg.setText("Database saved!")
            msg.setWindowTitle("Success!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setText("Database not saved! Very bad!")
            msg.setWindowTitle("Failure!")
            msg.setStandardButtons(QMessageBox.Discard)
            msg.exec_()
