import sys

from PyQt5 import QtWidgets

from src.backend.DatabaseConnector import DatabaseConnector
from src.frontend.windows import MainWindow


class ExampleApp(QtWidgets.QMainWindow, MainWindow.MainWindow):
    HOST = 'localhost'  # Gotta use database container name as host
    PORT = '7687'   # 7687 for bolt, 7474 for http, 7473 for https
    NAME = 'neo4j'  # Authorization
    PASSWORD = 'password'  # Authorization

    def __init__(self):
        super().__init__()
        self.databaseConnector = DatabaseConnector("bolt://{}:{}".format(self.HOST, self.PORT), self.NAME, self.PASSWORD)
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

