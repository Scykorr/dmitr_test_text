from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from GUIpy.client_login import Ui_Form_client_login
from users import Client
from choose_test import WindowChooseTest
from socket import socket, AF_INET, SOCK_STREAM
import json
import sqlite3
from PyQt5 import QtCore, QtWidgets
from PyQt5 import *

import os
import sys

with open('ip_address.txt', 'r', encoding='utf-8') as ip_file:
    for el in ip_file:
        ip_address_server = el


# ip_address_server = get_ip.get_local_ip()

class WindowLogin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.choose_test_window = None
        self.ui_client_login = Ui_Form_client_login()
        self.ui_client_login.setupUi(self)
        self.ui_client_login.pushButton_fio.clicked.connect(self.send_fio)
        self.student_fio = ''

    def send_fio(self):
        self.student_fio = self.ui_client_login.lineEdit_fio.text()
        user_name.append(self.student_fio)
        self.choose_test_window = WindowChooseTest(ip_address_server, user_name)
        Client(ip_address_server, 7000).connect("insert into user(fio_user) values ('{0}')".format(
            self.student_fio,
        ))
        self.hide()
        self.choose_test_window.show()


if __name__ == '__main__':
    user_name = []
    app = QApplication(sys.argv)
    login_window = WindowLogin()
    login_window.show()
    sys.exit(app.exec_())
