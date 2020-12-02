from PyQt5.QtWidgets import QWidget, QRadioButton, QLabel, QFileDialog, QMessageBox
from frontend.widgets.MplWidget import MplWidget
from PyQt5 import QtWidgets

from frontend.widgets.QHintCombo import QHintCombo


class DatabaseWindow(QWidget):
    canvas = None
    plotWidget = None
    importDbButton = None
    exportDbButton = None
    specInput = None
    axisLabel = None
    b1, b2 = None, None

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
        # demo thing:
        self.plotWidget.canvas.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.plotWidget.canvas.axes.set_xlabel('Latitude')
        self.plotWidget.canvas.axes.set_ylabel('Count')

        self.specInput = QHintCombo(items=["Воробей", "Петух", "Попугай", "Ворона"], parent=self)
        self.specInput.setGeometry(10, 550, 180, 25)

        self.axisLabel = QLabel("Axis 'X':", parent=self)
        self.axisLabel.setGeometry(200, 550, 50, 25)
        self.b1 = QRadioButton("Latitude", parent=self)
        self.b1.setGeometry(260, 550, 100, 25)
        self.b1.toggled.connect(lambda: self.btnstate(self.b1))
        self.b1.setChecked(True)
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
            print
            b.text() + " is selected"
        else:
            print
            b.text() + " is deselected"

    def importDatabase(self):
        # fname, err = QFileDialog.getOpenFileName(self, 'Open file', filter="Database files")
        try:
            self.databaseConnector.setCsv()
        except:
            exit(228)
        # TODO: open database for real
        # TODO: handle troubles

    def exportDatabase(self):
        fname, err = QFileDialog.getSaveFileName(self, 'Save file', filter="CSV (*.csv)")
        data = self.databaseConnector.getCsv();
        f = open(fname, 'w', encoding='utf-8')
        f.write(str(data))
        f.close()

        # TODO: save database
        # TODO: handle troubles
        msg = QMessageBox()
        msg.setText("Database saved!")
        msg.setWindowTitle("Success!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
