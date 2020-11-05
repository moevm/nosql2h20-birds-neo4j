import sys
from PyQt5 import QtWidgets

from src.frontend.windows import mainWindow


class ExampleApp(QtWidgets.QMainWindow, mainWindow.MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

