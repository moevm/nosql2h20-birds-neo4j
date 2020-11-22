from PyQt5.QtWidgets import QWidget
from src.frontend.widgets.MplWidget import MplWidget


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
        # demo thing:
        self.plotWidget.canvas.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
