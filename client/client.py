from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.client import Ui_MainWindow


class MainClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle('Клиент тестирования')
        self.puss
        # self.pushButton.clicked.connect(lambda: self.choose_operator(page_index=1, button=self.pushButton))
        # self.pushButton_2.clicked.connect(lambda: self.choose_operator(page_index=1, button=self.pushButton_2))
        # self.pushButton_3.clicked.connect(lambda: self.choose_operator(page_index=1, button=self.pushButton_3))
        # self.pushButton_4.clicked.connect(lambda: self.choose_operator(page_index=1, button=self.pushButton_4))
        # self.pushButton_5.clicked.connect(self.get_new_task)

    def choose_operator(self, page_index, button):
        self.stackedWidget.setCurrentIndex(page_index)
        self.textBrowser.append(button.text())



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
