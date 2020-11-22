from PyQt5.QtWidgets import QWidget
from src.frontend.widgets.MplWidget import MplWidget
from PyQt5 import QtWidgets

class DatabaseWindow(QWidget):
    canvas = None
    plotWidget = None

    def __init__(self):
        super().__init__()
        self.title = 'Database'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 800, 620)

        self.plotWidget = MplWidget(self, width=5, height=4, dpi=100)
        self.plotWidget.setGeometry(0, 0, 800, 620)
        # demo thing:
        self.plotWidget.canvas.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.plotWidget.canvas.axes.set_xlabel('Latitude')
        self.plotWidget.canvas.axes.set_ylabel('Count')

        self.importdbButton = QtWidgets.QPushButton(text="Import DB", parent=self)
        self.importdbButton.setGeometry(600, 10, 100, 25)

        self.exportdbButton = QtWidgets.QPushButton(text="Export DB", parent=self)
        self.exportdbButton.setGeometry(600, 40, 100, 25)

