import pathlib
import os
from types import NoneType

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from GUI.teacher import Ui_MainWindow


class MainClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = None
        self.change_size(341, 300)
        self.setupUi(self)
        self.setWindowTitle('Клиент тестирования')
        self.pushButton_2.clicked.connect(lambda: self.choose_operator(page_index=1))
        self.lineEdit_3.setText('C:\Program Files\Tftpd64')
        self.pushButton.clicked.connect(lambda: self.choose_operator(page_index=1))
        self.users_files_table = self.tableWidget
        self.users_files_table.doubleClicked.connect(lambda: self.choose_operator(page_index=2))
        self.comboBox.currentTextChanged.connect(self.show_standard_file)

    def choose_operator(self, page_index):
        if page_index == 1:
            self.stackedWidget.setCurrentIndex(page_index)
            self.change_size(721, 551)
            self.get_standard_files()
            self.show_standard_file()
            self.get_user_files()
        if page_index == 2:
            self.stackedWidget.setCurrentIndex(page_index)

    def get_standard_files(self):
        directory = self.lineEdit_3.text()

        files = list()

        files += os.listdir(directory)
        standard_files = list()
        for file in files:
            if 'standard' in file:
                standard_files.append(file)
        self.comboBox.addItems(standard_files)

    def get_user_files(self):
        directory = self.lineEdit_3.text()
        files = list()

        files += os.listdir(directory)
        users_files = list()
        for file in files:
            if 'standard' not in file:
                users_files.append(file)
        self.users_files_table.setColumnCount(1)
        self.users_files_table.setRowCount(len(users_files))
        self.users_files_table.setHorizontalHeaderLabels(["Строки скрипта"])

        for index_el, el in enumerate(users_files):
            self.users_files_table.setItem(index_el, 0, QtWidgets.QTableWidgetItem(str(el)))

    def show_standard_file(self):
        file_name_standard = self.comboBox.currentText()
        os.system(f'tftp 127.0.0.1 GET {file_name_standard}')
        with open(f'{file_name_standard}', 'r') as f_standard:
            st_text = f_standard.read()

        # init tableWidgets

        standard_text_list = st_text.split('\n')
        standard_table = self.tableWidget_2
        standard_table.setRowCount(len(standard_text_list))
        standard_table.setColumnCount(1)
        standard_table.setHorizontalHeaderLabels(["Строки скрипта"])

        for index_el, el in enumerate(standard_text_list):
            standard_table.setItem(index_el, 0, QtWidgets.QTableWidgetItem(str(el)))

        pathlib.Path(f'{file_name_standard}').unlink()

    def change_size(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
