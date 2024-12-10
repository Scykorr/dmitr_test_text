from PyQt5 import QtWidgets

from GUIpy.client_main import Ui_Form_client_main
from first_test import FirstTestWindow
from second_test import SecondTestWindow

from variant_1 import Task1Part1Var1
from variant_2 import Task1Part1Var2



class WindowChooseTest(QtWidgets.QWidget):
    def __init__(self, ip_address_server, user_name=None, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        if user_name is None:
            user_name = []
        self.user_name = user_name
        self.ip_address_server = ip_address_server
        self.ui_choose_test = Ui_Form_client_main()
        self.ui_choose_test.setupUi(self)
        self.ui_choose_test.pushButton_test1.clicked.connect(self.test_1)
        self.ui_choose_test.pushButton_test2.clicked.connect(self.test_2)
        self.ui_choose_test.pushButton_variant1.clicked.connect(self.get_variant_1)
        self.ui_choose_test.pushButton_variant2.clicked.connect(self.get_variant_2)

    def test_1(self):
        self.first_test_window = FirstTestWindow(ip_address_server=self.ip_address_server, user_name=self.user_name)
        self.hide()
        self.first_test_window.show()

    def test_2(self):
        self.second_test_window = SecondTestWindow(ip_address_server=self.ip_address_server, user_name=self.user_name)
        self.hide()
        self.second_test_window.show()

    def get_variant_1(self):
        self.first_variant_window = Task1Part1Var1(ip_address_server=self.ip_address_server, user_name=self.user_name)
        self.first_variant_window.show()

    def get_variant_2(self):
        self.second_variant_window = Task1Part1Var2(ip_address_server=self.ip_address_server, user_name=self.user_name)
        self.second_variant_window.show()
