import time
from random import shuffle

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from GUIpy.client_test1 import Ui_Form_client_test1
from threads import MyThread
from users import Client
import sqlite3 as sql


class FirstTestWindow(QtWidgets.QWidget):
    def __init__(self, ip_address_server, parent=None, user_name=None):
        if user_name is None:
            user_name = []
        self.ip_address_server = ip_address_server
        self.user_name = user_name
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_first_test = Ui_Form_client_test1()
        self.ui_first_test.setupUi(self)
        self.ui_first_test.pushButton.clicked.connect(self.answer)
        self.questions = Client(self.ip_address_server, 7000).connect(
            'select iq_question, text_question from question')
        shuffle(self.questions)
        self.new_lst_question = self.questions[:10]
        self.variants = Client(self.ip_address_server, 7000).connect(
            'select id_var_answ, text_var_answ, var_answ_right, id_question from variant_answer')
        shuffle(self.variants)
        self.sorted_variants = self.sort_variants()
        self.counter_questions = 0
        self.counter_questions_result = 0
        self.right_answer = 0
        self.wrong_answer = 0
        self.student_fio = user_name[0]
        self.ui_first_test.radioButton_answer1.setChecked(True)
        self.get_questionts()
        self.mythread = MyThread()
        self.on_clicked()
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)

    def on_clicked(self):
        self.mythread.start()

    def on_started(self):
        self.ui_first_test.label_timer.setText("")

    def on_finished(self):
        res_sec = 600 - int(self.mythread.result_time[0])
        time_format_result = time.strftime("%H:%M:%S", time.gmtime(res_sec))
        result_points = self.right_answer * 10
        Client(self.ip_address_server, 7000).connect(
            "update user set time='{0}', true_answer={1}, false_answer={2}, current_answer={3},"
            " result_score={5} where fio_user='{4}'".format(
                time_format_result,
                self.right_answer,
                self.wrong_answer,
                self.counter_questions_result,
                self.student_fio,
                result_points,
            ))
        QMessageBox.about(self, 'Ваш результат:', 'Тест завершен.\n{0} верных ответов из 10.'.format(
            self.right_answer
        ))
        exit()

    def on_change(self, s):
        self.ui_first_test.label_timer.setText(s)

    def answer(self):
        self.counter_questions_result += 1
        if self.ui_first_test.radioButton_answer1.isChecked() \
                and self.sorted_variants[self.counter_questions][0][2] == 1:
            self.right_answer += 1
            self.right_answer_append()
        elif self.ui_first_test.radioButton_answer2.isChecked() \
                and self.sorted_variants[self.counter_questions][1][2] == 1:
            self.right_answer += 1
            self.right_answer_append()
        elif self.ui_first_test.radioButton_answer3.isChecked() \
                and self.sorted_variants[self.counter_questions][2][2] == 1:
            self.right_answer += 1
            self.right_answer_append()
        elif self.ui_first_test.radioButton_4.isChecked() \
                and self.sorted_variants[self.counter_questions][3][2] == 1:
            self.right_answer += 1
            self.right_answer_append()
        else:
            self.wrong_answer += 1
            Client(self.ip_address_server, 7000).connect(
                "update user set false_answer={0}, current_answer={1} where fio_user='{2}'".format(
                    self.wrong_answer,
                    self.counter_questions_result,
                    self.student_fio,
                ))

        self.ui_first_test.radioButton_answer1.setChecked(True)
        self.ui_first_test.radioButton_answer2.setChecked(False)
        self.ui_first_test.radioButton_answer3.setChecked(False)
        self.ui_first_test.radioButton_4.setChecked(False)
        self.counter_questions += 1
        if self.counter_questions < 10:
            self.get_questionts()
        else:
            self.on_finished()
            exit()

    def right_answer_append(self):
        Client(self.ip_address_server, 7000).connect(
            "update user set true_answer={0}, current_answer={1} where fio_user='{2}'".format(
                self.right_answer,
                self.counter_questions_result,
                self.student_fio,
            ))

    def get_questionts(self):

        self.setWindowTitle('Вопрос №{0}'.format(
            self.counter_questions + 1,
        ))
        self.ui_first_test.plainTextEdit.setPlainText(self.new_lst_question[self.counter_questions][1])
        self.ui_first_test.textBrowser.setText(self.sorted_variants[self.counter_questions][0][1])
        self.ui_first_test.textBrowser_2.setText(self.sorted_variants[self.counter_questions][1][1])
        self.ui_first_test.textBrowser_3.setText(self.sorted_variants[self.counter_questions][2][1])
        self.ui_first_test.textBrowser_4.setText(self.sorted_variants[self.counter_questions][3][1])

    def sort_variants(self):
        new_list = [[] for _ in range(10)]
        counter = 0
        for question in self.new_lst_question:
            for var in self.variants:
                if question[0] == var[3]:
                    new_list[counter].append(var)
            counter += 1
        return new_list
