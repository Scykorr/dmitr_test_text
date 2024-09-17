import pathlib
import os
from types import NoneType

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from GUI.client import Ui_MainWindow


class MainClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = None
        self.change_size(341, 300)
        self.setupUi(self)
        self.setWindowTitle('Клиент тестирования')
        self.lineEdit_2.setText('127.0.0.1')
        self.curr_ip = self.lineEdit_2.text()
        self.pushButton_2.clicked.connect(lambda: self.choose_operator(page_index=1))
        self.pushButton.clicked.connect(lambda: self.choose_operator(page_index=2))
        self.lineEdit.setText('Ivanov Ivan Ivanovich')
        self.lineEdit_4.setText('standard1.txt')

    def choose_operator(self, page_index):
        self.curr_ip = self.lineEdit_2.text()
        if page_index == 1 and self.lineEdit.text() != "":
            self.change_size(351, 531)
            self.stackedWidget.setCurrentIndex(page_index)
        elif self.lineEdit.text() == "":
            err_dialog = QtWidgets.QErrorMessage(self)
            err_dialog.showMessage("Заполните поле ФИО!")
        elif page_index == 2:
            self.change_size(721, 531)
            self.file_name = '_'.join(self.lineEdit.text().split())
            pathlib.Path(f'{self.file_name}.txt').touch()
            pathlib.Path(f'{self.file_name}.txt').write_text(self.textEdit.toPlainText())
            os.system(f'tftp {self.curr_ip} PUT {self.file_name}.txt')
            self.stackedWidget.setCurrentIndex(page_index)

            os.system(f'tftp {self.curr_ip} GET {self.file_name}.txt')
            with open(f'{self.file_name}.txt', 'r') as f:
                text = f.read()

            file_name_etalon = self.lineEdit_4.text()
            os.system(f'tftp {self.curr_ip} GET {file_name_etalon}')
            print(self.curr_ip)
            print(file_name_etalon)
            with open(f'{file_name_etalon}', 'r') as f_etalon:
                et_text = f_etalon.read()

            # init tableWidgets

            etalon_text_list = et_text.split('\n')
            etalon_table = self.tableWidget_2
            etalon_table.setRowCount(len(etalon_text_list))
            etalon_table.setColumnCount(1)
            etalon_table.setHorizontalHeaderLabels(["Строки скрипта"])

            for index_el, el in enumerate(etalon_text_list):
                etalon_table.setItem(index_el, 0, QtWidgets.QTableWidgetItem(str(el)))

            user_text_list = text.split('\n')
            user_table = self.tableWidget
            if len(user_text_list) < len(etalon_text_list):
                user_list_len = len(etalon_text_list)
            elif len(user_text_list) > len(etalon_text_list):
                etalon_text_list += ['']*(len(user_text_list) - len(etalon_text_list))
                user_list_len = len(user_text_list)
            else:
                user_list_len = len(user_text_list)
            user_table.setRowCount(user_list_len)
            user_table.setColumnCount(1)
            user_table.setHorizontalHeaderLabels(["Строки скрипта"])

            for index_el, el in enumerate(user_text_list):
                user_table.setItem(index_el, 0, QtWidgets.QTableWidgetItem(str(el)))

            pathlib.Path(f'{self.file_name}.txt').unlink()
            pathlib.Path(f'{file_name_etalon}').unlink()
            self.check_answer(etalon_text_list)

    def change_size(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)

    def check_answer(self, etalon_text_list):
        user_table = self.tableWidget
        etalon_table = self.tableWidget_2
        for el_index in range(len(etalon_text_list)):
            user_text = ''
            etalon_text = ''
            print()
            if type(user_table.item(el_index, 0)) == NoneType:
                user_table.setItem(el_index, 0, QtWidgets.QTableWidgetItem(str('')))
            else:
                user_text = user_table.item(el_index, 0).text()
            if type(etalon_table.item(el_index, 0)) == NoneType:
                etalon_table.setItem(el_index, 0, QtWidgets.QTableWidgetItem(str('')))
            else:
                etalon_text = etalon_table.item(el_index, 0).text()
            if user_text != etalon_text:
                user_table.item(el_index, 0).setBackground(QtGui.QColor(255, 0, 0))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
