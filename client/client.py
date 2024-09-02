import pathlib
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.client import Ui_MainWindow


class MainClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = None
        self.change_size(341, 300)
        self.setupUi(self)
        self.setWindowTitle('Клиент тестирования')
        self.pushButton_2.clicked.connect(lambda: self.choose_operator(page_index=1))
        self.pushButton.clicked.connect(lambda: self.choose_operator(page_index=2))

    def choose_operator(self, page_index):
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
            os.system(f'tftp 127.0.0.1 PUT {self.file_name}.txt')
            pathlib.Path(f'{self.file_name}.txt').unlink()
            self.stackedWidget.setCurrentIndex(page_index)
            os.system(f'tftp 127.0.0.1 GET {self.file_name}.txt')
            with open(f'{self.file_name}.txt', 'r') as f:
                text = f.read()
            self.textEdit_2.setText(text)
            file_name_etalon = self.lineEdit_4.text()
            os.system(f'tftp 127.0.0.1 GET {file_name_etalon}')
            with open(f'{file_name_etalon}', 'r') as f_etalon:
                et_text = f_etalon.read()
                print(et_text)
            self.textEdit_3.setText(et_text)

    def change_size(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
