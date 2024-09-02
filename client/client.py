import pathlib
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.client import Ui_MainWindow


class MainClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle('Клиент тестирования')
        self.pushButton_2.clicked.connect(lambda: self.choose_operator(page_index=1))
        self.pushButton.clicked.connect(lambda: self.choose_operator(page_index=2))
        # self.pushButton_2.clicked.connect(lambda: self.choose_operator(page_index=1, button=self.pushButton_2))
        # self.pushButton_3.clicked.connect(lambda: self.choose_operator(page_index=1, button=self.pushButton_3))
        # self.pushButton_4.clicked.connect(lambda: self.choose_operator(page_index=1, button=self.pushButton_4))
        # self.pushButton_5.clicked.connect(self.get_new_task)

    def choose_operator(self, page_index):
        self.stackedWidget.setCurrentIndex(page_index)
        if page_index == 1:
            self.setFixedWidth(351)
            self.setFixedHeight(531)
        elif page_index == 2:
            self.setFixedWidth(721)
            self.setFixedHeight(531)

    def put_file(self):
        pathlib.Path('test.txt').touch()
        pathlib.Path('test.txt').write_text('test')
        os.system(f'tftp 127.0.0.1 PUT {"test.txt"}')
        # pathlib.Path('test.txt').unlink()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
