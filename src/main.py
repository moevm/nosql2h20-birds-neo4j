import sys
from PyQt5 import QtWidgets

from src.backend.DatabaseConnector import DatabaseConnector
from src.frontend.windows import MainWindow


class ExampleApp(QtWidgets.QMainWindow, MainWindow.MainWindow):
    def __init__(self):
        super().__init__()
        self.databaseConnector = DatabaseConnector("bolt://localhost:7687", "neo4j", "password")
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

