import pathlib
import os
from datetime import datetime
from types import NoneType

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView

from GUI.teacher import Ui_MainWindow


class MainClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = None
        self.change_size(341, 300)
        self.setupUi(self)
        self.setWindowTitle('Проверка тестирования')
        self.pushButton_2.clicked.connect(lambda: self.choose_operator(page_index=1))
        self.lineEdit_3.setText('C:\Program Files\Tftpd64')
        self.pushButton.clicked.connect(lambda: self.choose_operator(page_index=1))
        self.users_files_table = self.tableWidget
        self.users_files_table.doubleClicked.connect(lambda: self.choose_operator(page_index=2))
        self.users_files_table.clicked.connect(
            lambda: self.show_checked_user_script(user_script_file=self.users_files_table.currentItem().text()))
        self.comboBox.currentTextChanged.connect(self.show_standard_file)
        self.lineEdit_2.setText('127.0.0.1')
        self.ip_address = self.lineEdit_2.text()
        self.pushButton_3.clicked.connect(lambda: self.choose_operator(page_index=1))

    def choose_operator(self, page_index):
        if page_index == 1:
            self.stackedWidget.setCurrentIndex(page_index)
            self.change_size(921, 551)
            if self.comboBox.currentText() == '':
                self.get_standard_files()
            self.show_standard_file()
            self.get_user_files()
        if page_index == 2:
            if '.txt' in self.users_files_table.currentItem().text():
                self.change_size(721, 551)
                self.stackedWidget.setCurrentIndex(page_index)
                self.show_user_script(self.users_files_table.currentItem().text())


    def get_standard_files(self):
        directory = self.lineEdit_3.text()

        files = list()

        files += os.listdir(directory)
        standard_files = list()

        for file in files:
            if 'standard' in file:
                standard_files.append(file)
        self.comboBox.clear()
        self.comboBox.addItems(standard_files)

    def get_user_files(self):
        directory = self.lineEdit_3.text()
        files = list()

        files += os.listdir(directory)
        users_files = list()
        for file in files:
            if '.txt' in file and 'standard' not in file:
                users_files.append(file)
        self.users_files_table.setColumnCount(5)
        self.users_files_table.setRowCount(len(users_files))
        self.users_files_table.setHorizontalHeaderLabels(
            ["Строки скрипта", "Ош. строк", "Лишние строки", "Ош. символов", "Время сохранения файла"])
        header = self.users_files_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        file_name_standard = self.comboBox.currentText()
        os.system(f'tftp {self.lineEdit_2.text()} GET {file_name_standard}')
        with open(f'{file_name_standard}', 'r') as f_standard:
            st_text = f_standard.read()

        standard_text_list = st_text.split('\n')

        for index_el, el in enumerate(users_files):
            filename = f"{self.lineEdit_3.text()}\\{el}"
            mtime = os.path.getmtime(filename)
            mtime_readable = datetime.fromtimestamp(mtime)
            self.users_files_table.setItem(index_el, 0, QtWidgets.QTableWidgetItem(str(el)))
            self.users_files_table.setItem(index_el, 4, QtWidgets.QTableWidgetItem(str(mtime_readable)))
            os.system(f'tftp {self.lineEdit_2.text()} GET {file_name_standard}')
            with open(f'{filename}', 'r') as f_user:
                usr_text = f_user.read()
            user_text_list = usr_text.split('\n')
            if len(user_text_list) > len(standard_text_list):
                self.users_files_table.setItem(index_el, 2, QtWidgets.QTableWidgetItem(
                    str(len(user_text_list) - len(standard_text_list))))
            else:
                self.users_files_table.setItem(index_el, 2, QtWidgets.QTableWidgetItem(str(0)))
            counter_error_strings = 0
            counter_error_symbols = 0
            if len(user_text_list) < len(standard_text_list):
                user_text_list += ['']*(len(standard_text_list) - len(user_text_list))
            user_text_edge = user_text_list[:len(standard_text_list)]
            for i_el, elem in enumerate(standard_text_list):
                if elem != user_text_edge[i_el]:
                    counter_error_strings += 1
                    for i_symb, letter in enumerate(elem):
                        if len(elem) > len(user_text_edge[i_el]):
                            user_text_edge[i_el] += 'a' * (len(elem) - len(user_text_edge[i_el]))
                        if letter != user_text_edge[i_el][i_symb]:
                            counter_error_symbols += 1
            self.users_files_table.setItem(index_el, 1, QtWidgets.QTableWidgetItem(str(counter_error_strings)))
            self.users_files_table.setItem(index_el, 3, QtWidgets.QTableWidgetItem(str(counter_error_symbols)))
        pathlib.Path(f'{file_name_standard}').unlink()



    def show_standard_file(self):
        file_name_standard = self.comboBox.currentText()
        os.system(f'tftp {self.lineEdit_2.text()} GET {file_name_standard}')
        with open(f'{file_name_standard}', 'r') as f_standard:
            st_text = f_standard.read()

        self.tableWidget_2.clear()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(0)

        # init tableWidgets

        standard_text_list = st_text.split('\n')

        # second standard widget

        standard_table_second = self.tableWidget_3
        standard_table_second.setRowCount(len(standard_text_list))
        standard_table_second.setColumnCount(1)
        standard_table_second.setHorizontalHeaderLabels(["Строки скрипта"])

        for index_el, el in enumerate(standard_text_list):
            standard_table_second.setItem(index_el, 0, QtWidgets.QTableWidgetItem(str(el)))

        pathlib.Path(f'{file_name_standard}').unlink()

        self.get_user_files()

    def show_user_script(self, user_script_file):
        if '.txt' in user_script_file:
            file_name_standard = self.comboBox.currentText()
            os.system(f'tftp {self.lineEdit_2.text()} GET {file_name_standard}')
            with open(f'{file_name_standard}', 'r') as f_standard:
                st_text = f_standard.read()

            # init tableWidgets

            standard_text_list = st_text.split('\n')

            os.system(f'tftp {self.lineEdit_2.text()} GET {user_script_file}')
            with open(f'{user_script_file}', 'r') as f:
                text = f.read()

            user_text_list = text.split('\n')
            user_table = self.tableWidget_4
            if len(user_text_list) < len(standard_text_list):
                user_list_len = len(standard_text_list)
            else:
                user_list_len = len(user_text_list)
            user_table.setRowCount(user_list_len)
            user_table.setColumnCount(1)
            user_table.setHorizontalHeaderLabels(["Строки скрипта"])

            for index_el, el in enumerate(user_text_list):
                user_table.setItem(index_el, 0, QtWidgets.QTableWidgetItem(str(el)))

            pathlib.Path(f'{user_script_file}').unlink()
            pathlib.Path(f'{file_name_standard}').unlink()
            self.check_answer(standard_text_list, user_text_list)

    def check_answer(self, etalon_text_list, user_list):
        user_table = self.tableWidget_4
        etalon_table = self.tableWidget_3
        if len(user_list) > len(etalon_text_list):
            etalon_text_list += [''] * (len(user_list) - len(etalon_text_list))
            etalon_table.setRowCount(len(user_list))
        for el_index in range(len(etalon_text_list)):
            user_text = ''
            print()
            if type(user_table.item(el_index, 0)) == NoneType:
                user_table.setItem(el_index, 0, QtWidgets.QTableWidgetItem(str('')))
            else:
                user_text = user_table.item(el_index, 0).text()

            etalon_text = ''
            if type(etalon_table.item(el_index, 0)) == NoneType:
                etalon_table.setItem(el_index, 0, QtWidgets.QTableWidgetItem(str('')))
            else:
                etalon_text = etalon_table.item(el_index, 0).text()

            if user_text != etalon_text:
                user_table.item(el_index, 0).setBackground(QtGui.QColor(255, 0, 0))

    def change_size(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)

    def show_checked_user_script(self, user_script_file):
        if self.users_files_table.currentColumn() == 0:
            file_name_standard = self.comboBox.currentText()
            os.system(f'tftp {self.lineEdit_2.text()} GET {file_name_standard}')
            with open(f'{file_name_standard}', 'r') as f_standard:
                st_text = f_standard.read()

            # init tableWidgets

            standard_text_list = st_text.split('\n')

            os.system(f'tftp {self.lineEdit_2.text()} GET {user_script_file}')
            with open(f'{user_script_file}', 'r') as f:
                text = f.read()

            user_text_list = text.split('\n')
            user_table = self.tableWidget_2
            if len(user_text_list) < len(standard_text_list):
                user_list_len = len(standard_text_list)
            else:
                user_list_len = len(user_text_list)
            user_table.setRowCount(user_list_len)
            user_table.setColumnCount(1)
            user_table.setHorizontalHeaderLabels(["Строки скрипта"])

            for index_el, el in enumerate(user_text_list):
                if type(user_table.item(index_el, 0)) == NoneType:
                    user_table.setItem(index_el, 0, QtWidgets.QTableWidgetItem(str('')))
                user_table.setItem(index_el, 0, QtWidgets.QTableWidgetItem(str(el)))

            pathlib.Path(f'{user_script_file}').unlink()
            pathlib.Path(f'{file_name_standard}').unlink()
            self.checked_user_script(standard_text_list, user_text_list)

    def checked_user_script(self, etalon_text_list, user_list):
        user_table = self.tableWidget_2

        if len(user_list) > len(etalon_text_list):
            etalon_text_list += [''] * (len(user_list) - len(etalon_text_list))
        for el_index in range(len(etalon_text_list)):
            user_text = ''
            print()
            if type(user_table.item(el_index, 0)) == NoneType:
                user_table.setItem(el_index, 0, QtWidgets.QTableWidgetItem(str('')))
            else:
                user_text = user_table.item(el_index, 0).text()

            etalon_text = etalon_text_list[el_index]

            if user_text != etalon_text:
                user_table.item(el_index, 0).setBackground(QtGui.QColor(255, 0, 0))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
