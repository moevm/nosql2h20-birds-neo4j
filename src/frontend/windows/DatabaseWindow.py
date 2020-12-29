from PyQt5.QtWidgets import QWidget, QRadioButton, QLabel, QFileDialog, QMessageBox, QPushButton
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
    b1, b2, b3, selected_btn = None, None, None, None
    distIndex = 0
    kindsShown = 5

    def __init__(self, databaseConnector, parent=None):
        super().__init__()
        self.parent = parent
        self.databaseConnector = databaseConnector
        self.nKinds = len(self.databaseConnector.getSpecies())
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

        self.lftBtn = QPushButton(text='<', parent=self)
        self.lftBtn.setGeometry(20, 510, 25, 25)
        self.rghtBtn = QPushButton(text='>', parent=self)
        self.rghtBtn.setGeometry(760, 510, 25, 25)
        self.lftBtn.setVisible(False)
        self.rghtBtn.setVisible(False)
        self.lftBtn.clicked.connect(self.goLeft)
        self.rghtBtn.clicked.connect(self.goRight)

        self.b1 = QRadioButton("Latitude", parent=self)
        self.b1.setGeometry(260, 550, 100, 25)
        self.b2 = QRadioButton("Longitude", parent=self)
        self.b2.setGeometry(260, 575, 100, 25)
        self.b3 = QRadioButton("Kinds", parent=self)
        self.b3.setGeometry(370, 550, 100, 25)
        self.b1.toggled.connect(lambda: self.btnstate(self.b1))
        self.b1.setChecked(True)
        self.selected_btn = self.b1



        self.b2.toggled.connect(lambda: self.btnstate(self.b2))
        self.b3.toggled.connect(lambda: self.btnstate(self.b3))

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
            print("nkinds={};showing {}".format(self.nKinds, self.kindsShown))
            cond = b == self.b3 and self.kindsShown < self.nKinds
            self.lftBtn.setVisible(cond)
            self.rghtBtn.setVisible(cond)

    def draw_statistics(self, b):
        self.nKinds = len(self.databaseConnector.getSpecies())
        bird_kind = self.specInput.currentText()
        geo_coord = b.text()
        bounds_shift = 0
        range_shift = 0
        x_axis = []
        y_axis = []

        specCountStats = self.b3 == self.selected_btn
        if specCountStats:
            kinds = self.databaseConnector.getSpecies()
            self.distIndex = max(self.distIndex, 0)
            while self.distIndex >= len(kinds):
                self.distIndex -= self.kindsShown
            lBound = self.distIndex
            # self.distIndex = min(self.distIndex, len(kinds))
            rBound = min(self.distIndex + self.kindsShown, len(kinds))
            x_axis = kinds[lBound:rBound]
            freq = [self.databaseConnector.countBirdsByKind(k) for k in x_axis]
            y_axis = freq

        if bird_kind == self.ALL_LABEL:
            a = self.databaseConnector.get_all_birds_area()
        else:
            a = self.databaseConnector.get_birds_area(bird_kind)

        if geo_coord == 'Longitude':
            bounds_shift = 90
            range_shift = 5

        self.plotWidget.canvas.axes.clear()
        if not specCountStats:
            x_axis = ([a[i][geo_coord.lower()] for i in range(len(a))])
            y_axis = [self.count_range_in_list(x_axis, i - 5, i + 5) for i in np.arange(0, 90 + bounds_shift, 10)]
            self.plotWidget.canvas.axes.bar(np.arange(0, 90 + bounds_shift, 10), y_axis, width=10)
            self.plotWidget.canvas.axes.set_xlabel(geo_coord)
            self.plotWidget.canvas.axes.set_ylabel(bird_kind)
            self.plotWidget.canvas.axes.set_xlim(0)
            self.plotWidget.canvas.axes.set_xticks(np.arange(0, 90 + bounds_shift, 5 + range_shift))
            self.plotWidget.canvas.axes.set_yticks(np.arange(0, max(y_axis) + 1, max(y_axis) // 10 + 1))

        else:
            self.plotWidget.canvas.axes.bar(x_axis, y_axis)
            self.plotWidget.canvas.axes.set_yticks(np.arange(0, max(y_axis) + 1, max(y_axis) // 10 + 1))


        # self.plotWidget.canvas.axes.bar(['a', 'b'], ['c', 'd'], width=10)

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
        self.parent.refresh()
        if self.parent.secondWindow:
            self.parent.secondWindow.specInput.setItems(self.databaseConnector.getSpecies())
        self.refresh()
        self.draw_statistics(self.selected_btn)

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

    def goLeft(self):
        print('going west')
        self.distIndex -= self.kindsShown
        self.draw_statistics(self.selected_btn)

    def goRight(self):
        print('going east')
        self.distIndex += self.kindsShown
        self.draw_statistics(self.selected_btn)

    def refresh(self):
        species = self.databaseConnector.getSpecies()
        species.append(self.ALL_LABEL)
        species.reverse()  # ALL_LABEL comes first
        self.specInput.setItems(species)