import sys
import time

from PyQt5 import QtWidgets

from backend.DatabaseConnector import DatabaseConnector
from frontend.windows import MainWindow


class ExampleApp(QtWidgets.QMainWindow, MainWindow.MainWindow):
    HOST: str = 'neo4j'  # Gotta use database container name as host
    PORT: str = '7687'  # 7687 for bolt, 7474 for http, 7473 for https
    NAME: str = 'neo4j'  # Authorization
    PASSWORD: str = 'password'  # Authorization

    def __init__(self):
        super().__init__()
        while True:
            try:
                self.databaseConnector = DatabaseConnector("bolt://{}:{}".format(self.HOST, self.PORT),
                                                           self.NAME, self.PASSWORD)
                break
            except:  # Wait till neo4j gets available to connect to
                time.sleep(0.1)
        print('Connected to database')
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
