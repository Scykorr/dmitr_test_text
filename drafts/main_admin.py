from GUIpy.main_server import Ui_Form_server
from GUIpy.edit_questions import Ui_Form_questions
from GUIpy.edit_variants import Ui_Form_variants_answ
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap
import sys
import sqlite3 as sql


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.time_format = None

    def run(self):
        while True:
            self.sleep(1)
            select_result = WindowServerMain.select_from_users(self)
            self.mysignal.emit(select_result)


class WindowServerMain(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_main_server = Ui_Form_server()
        self.ui_main_server.setupUi(self)
        self.ui_main_server.tableWidget_server.setColumnCount(6)
        self.ui_main_server.pushButton_delete_all.clicked.connect(self.drop_db)
        self.questions_window = WindowEditQuestions()
        self.ui_main_server.pushButton_work_db.clicked.connect(self.open_window_db)
        self.mythread = MyThread()
        self.on_clicked()
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)

    def drop_db(self):
        con = sql.connect('data.db')
        cur = con.cursor()
        cur.execute('delete from user')
        con.commit()
        cur.close()
        con.close()
        self.ui_main_server.tableWidget_server.setRowCount(0)

    def open_window_db(self):
        self.questions_window.show()

    def on_clicked(self):
        self.mythread.start()

    def on_started(self):
        pass

    def on_finished(self):
        exit()

    def on_change(self, s):
        self.ui_main_server.tableWidget_server.clear()
        self.ui_main_server.tableWidget_server.setHorizontalHeaderLabels(
            ("ФИО;Правильных;Неправильных;Время;Отвечено;Баллы").split(";"))
        if self.ui_main_server.tableWidget_server.rowCount() == 0 or \
                self.ui_main_server.tableWidget_server.rowCount() < len(s):
            for _ in range(len(s) - self.ui_main_server.tableWidget_server.rowCount()):
                self.ui_main_server.tableWidget_server.insertRow(self.ui_main_server.tableWidget_server.rowCount())
        for i_res, res in enumerate(s):
            self.ui_main_server.tableWidget_server.setItem(i_res, 0, QTableWidgetItem(str(res[1])))
            self.ui_main_server.tableWidget_server.setItem(i_res, 1, QTableWidgetItem(str(res[2])))
            self.ui_main_server.tableWidget_server.setItem(i_res, 2, QTableWidgetItem(str(res[3])))
            self.ui_main_server.tableWidget_server.setItem(i_res, 3, QTableWidgetItem(str(res[4])))
            self.ui_main_server.tableWidget_server.setItem(i_res, 4, QTableWidgetItem(str(res[5])))
            self.ui_main_server.tableWidget_server.setItem(i_res, 5, QTableWidgetItem(str(res[6])))

    def select_from_users(self):
        vals = []
        con = sql.connect('data.db')
        cur = con.cursor()
        answer = cur.execute('select * from user')
        for el in answer:
            vals.append(el)
        con.commit()
        cur.close()
        con.close()
        return vals


class WindowEditQuestions(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.variants_window = WindowEditVariants()
        self.variants_window.setWindowTitle('Редактор ответов')
        self.variants_window.ui_form_variants.pushButton_add_variants.clicked.connect(self.update_variants)
        self.ui_form_question = Ui_Form_questions()
        self.ui_form_question.setupUi(self)
        self.ui_form_question.tableWidget_question_list.setColumnCount(3)
        self.ui_form_question.tableWidget_question_list.setRowCount(1)
        self.ui_form_question.tableWidget_question_list.hideColumn(0)
        self.ui_form_question.tableWidget_question_list.clicked.connect(self.get_val)
        self.ui_form_question.pushButton_view_var.clicked.connect(self.get_variants_form)
        self.ui_form_question.pushButton_new_val.clicked.connect(self.get_new_question)
        self.ui_form_question.pushButton_dell.clicked.connect(self.sql_delete)
        self.ui_form_question.pushButton_add.clicked.connect(self.add_question)
        self.ui_form_question.pushButton_delete_img.clicked.connect(self.del_img_question)
        self.update_question_list()
        self.setWindowTitle('Редактор вопросов')
        self.ui_form_question.tableWidget_question_list.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.ui_form_question.pushButton_download_img.clicked.connect(self.openFileNameDialog)
        self.variants_window.ui_form_variants.pushButton_zagr1.clicked.connect(self.open_file_name_dialog_variant1)
        self.variants_window.ui_form_variants.pushButton_zagr2.clicked.connect(self.open_file_name_dialog_variant2)
        self.variants_window.ui_form_variants.pushButton_zagr3.clicked.connect(self.open_file_name_dialog_variant3)
        self.variants_window.ui_form_variants.pushButton_zagr4.clicked.connect(self.open_file_name_dialog_variant4)
        self.variants_window.ui_form_variants.pushButtondel1.clicked.connect(self.del_img_var1)
        self.variants_window.ui_form_variants.pushButton_del2.clicked.connect(self.del_img_var2)
        self.variants_window.ui_form_variants.pushButton_del3.clicked.connect(self.del_img_var3)
        self.variants_window.ui_form_variants.pushButton_del4.clicked.connect(self.del_img_var4)
        self.ui_form_question.lineEdit_update_time.setText(str(self.get_seconds_for_count()))
        self.ui_form_question.pushButton_update_time.clicked.connect(self.update_seconds_test2)

    def update_seconds_test2(self):
        update_value = self.ui_form_question.lineEdit_update_time.text()
        if update_value.isdigit():
            con = sql.connect('data.db')
            cur = con.cursor()
            cur.execute(
                f'update score_for_count set seconds_for_test2 = {int(update_value)} where id_score = 1')
            con.commit()
            cur.close()
            con.close()
        self.ui_form_question.lineEdit_update_time.setText(str(self.get_seconds_for_count()))

    def get_seconds_for_count(self):
        con = sql.connect('data.db')
        cur = con.cursor()
        seconds = cur.execute('select seconds_for_test2 from score_for_count')
        seconds = seconds.fetchone()[0]
        con.commit()
        cur.close()
        con.close()
        if not seconds:
            return 0
        else:
            return seconds

    def del_img_var1(self):
        self.variants_window.ui_form_variants.label_var1_path.setText('Путь до изображения')
        self.variants_window.ui_form_variants.label_var1_img.clear()

    def del_img_var2(self):
        self.variants_window.ui_form_variants.label_var2_path.setText('Путь до изображения')
        self.variants_window.ui_form_variants.label_var2_img.clear()

    def del_img_var3(self):
        self.variants_window.ui_form_variants.label_var3_path.setText('Путь до изображения')
        self.variants_window.ui_form_variants.label_var3_img.clear()

    def del_img_var4(self):
        self.variants_window.ui_form_variants.label_var4_path.setText('Путь до изображения')
        self.variants_window.ui_form_variants.label_var4_img.clear()

    def del_img_question(self):
        self.ui_form_question.label_show_img.clear()
        self.ui_form_question.label_img_address.clear()

    def clear_variants(self):
        self.variants_window.ui_form_variants.label_var1_path.setText('Путь до изображения')
        self.variants_window.ui_form_variants.label_var2_path.setText('Путь до изображения')
        self.variants_window.ui_form_variants.label_var3_path.setText('Путь до изображения')
        self.variants_window.ui_form_variants.label_var4_path.setText('Путь до изображения')
        self.variants_window.ui_form_variants.label_var1_img.clear()
        self.variants_window.ui_form_variants.label_var2_img.clear()
        self.variants_window.ui_form_variants.label_var3_img.clear()
        self.variants_window.ui_form_variants.label_var4_img.clear()
        self.variants_window.ui_form_variants.label_question_img.clear()

    def update_variants(self):
        id_quest = self.get_id_question()
        id_variants = self.get_id_variants(id_quest)
        data_tuple_var1 = (self.variants_window.ui_form_variants.textEdit_var1.toPlainText(),
                           int(self.variants_window.ui_form_variants.textEdit_var1_t_f.toPlainText()),
                           id_quest, id_variants[0][0])
        self.update_variant1_sql(data_tuple_var1)
        data_tuple_var2 = (self.variants_window.ui_form_variants.textEdit_var2.toPlainText(),
                           int(self.variants_window.ui_form_variants.textEdit_var2_t_f.toPlainText()),
                           id_quest, id_variants[1][0])
        self.update_variant2_sql(data_tuple_var2)
        data_tuple_var3 = (self.variants_window.ui_form_variants.textEdit_var3.toPlainText(),
                           int(self.variants_window.ui_form_variants.textEdit_var3_t_f.toPlainText()),
                           id_quest, id_variants[2][0])
        self.update_variant3_sql(data_tuple_var3)
        data_tuple_var4 = (self.variants_window.ui_form_variants.textEdit_var4.toPlainText(),
                           int(self.variants_window.ui_form_variants.textEdit_var4_t_f.toPlainText()),
                           id_quest, id_variants[3][0])
        self.update_variant4_sql(data_tuple_var4)

    def get_id_variants(self, id_question):
        con = sql.connect('data.db')
        cur = con.cursor()
        id_question = cur.execute('select id_var_answ from variant_answer where id_question={0}'.format(
            id_question,
        ))
        id_question = id_question.fetchall()
        con.commit()
        cur.close()
        con.close()
        if not id_question:
            return 0
        else:
            return id_question

    def update_variant1_sql(self, data_tuple):
        file_address = self.variants_window.ui_form_variants.label_var1_path.text()
        if file_address == 'Путь до изображения':
            emp_photo = None
        else:
            emp_photo = self.convert_to_binary_data(file_address)
        sqlite_insert_blob_query = """ update variant_answer set text_var_answ = ?, var_answ_right= ?,  variant_img = ? where id_question = ? and id_var_answ= ? """
        data_tuple = (data_tuple[0], data_tuple[1], emp_photo, data_tuple[2], data_tuple[3])
        con = sql.connect('data.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple)
        con.commit()
        cur.close()
        con.close()
        sqlite_insert_blob_query = """ update img set image = ? where id_variant= ? """
        data_tuple1 = (emp_photo, data_tuple[4])
        con = sql.connect('img.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple1)
        con.commit()
        cur.close()
        con.close()
        self.update_question_list()

    def update_variant2_sql(self, data_tuple):
        file_address = self.variants_window.ui_form_variants.label_var2_path.text()
        if file_address == 'Путь до изображения':
            emp_photo = None
        else:
            emp_photo = self.convert_to_binary_data(file_address)
        sqlite_insert_blob_query = """ update variant_answer set text_var_answ = ?, var_answ_right= ?,  variant_img = ? where id_question = ? and id_var_answ= ? """
        data_tuple = (data_tuple[0], data_tuple[1], emp_photo, data_tuple[2], data_tuple[3])
        con = sql.connect('data.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple)
        con.commit()
        cur.close()
        con.close()
        sqlite_insert_blob_query = """ update img set image = ? where id_variant= ? """
        data_tuple2 = (emp_photo, data_tuple[4])
        con = sql.connect('img.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple2)
        con.commit()
        cur.close()
        con.close()
        self.update_question_list()

    def update_variant3_sql(self, data_tuple):
        file_address = self.variants_window.ui_form_variants.label_var3_path.text()
        if file_address == 'Путь до изображения':
            emp_photo = None
        else:
            emp_photo = self.convert_to_binary_data(file_address)
        sqlite_insert_blob_query = """ update variant_answer set text_var_answ = ?, var_answ_right= ?,  variant_img = ? where id_question = ? and id_var_answ= ? """
        data_tuple = (data_tuple[0], data_tuple[1], emp_photo, data_tuple[2], data_tuple[3])
        con = sql.connect('data.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple)
        con.commit()
        cur.close()
        con.close()
        sqlite_insert_blob_query = """ update img set image = ? where id_variant= ? """
        data_tuple3 = (emp_photo, data_tuple[4])
        con = sql.connect('img.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple3)
        con.commit()
        cur.close()
        con.close()
        self.update_question_list()

    def update_variant4_sql(self, data_tuple):
        file_address = self.variants_window.ui_form_variants.label_var4_path.text()
        if file_address == 'Путь до изображения':
            emp_photo = None
        else:
            emp_photo = self.convert_to_binary_data(file_address)
        sqlite_insert_blob_query = """ update variant_answer set text_var_answ = ?, var_answ_right= ?,  variant_img = ? where id_question = ? and id_var_answ= ? """
        data_tuple = (data_tuple[0], data_tuple[1], emp_photo, data_tuple[2], data_tuple[3])
        con = sql.connect('data.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple)
        con.commit()
        cur.close()
        con.close()
        sqlite_insert_blob_query = """ update img set image = ? where id_variant= ? """
        data_tuple4 = (emp_photo, data_tuple[4])
        con = sql.connect('img.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple4)
        con.commit()
        cur.close()
        con.close()
        self.update_question_list()

    def add_question(self):
        id_curr_question = self.get_id_question()
        if id_curr_question == 0 and self.ui_form_question.tableWidget_question_list.currentRow() == 0:
            file_address = self.ui_form_question.label_img_address.text()
            if file_address == '':
                emp_photo = None
            else:
                emp_photo = self.convert_to_binary_data(file_address)
            sqlite_insert_blob_query = """ INSERT INTO question (text_question, img_question) VALUES (?,?)"""
            data_tuple = (self.ui_form_question.textEdit_add_new_question.toPlainText(), emp_photo)
            con = sql.connect('data.db')
            cur = con.cursor()
            cur.execute(sqlite_insert_blob_query, data_tuple)
            con.commit()
            cur.close()
            con.close()
            id_curr_question = self.get_id_question()
            sqlite_insert_blob_query = """ INSERT INTO img (image, id_question) VALUES (?,?)"""
            data_tuple1 = (emp_photo, id_curr_question)
            con = sql.connect('img.db')
            cur = con.cursor()
            cur.execute(sqlite_insert_blob_query, data_tuple1)
            con.commit()
            cur.close()
            con.close()
            for i_num in range(1, 5):
                val = 'Вариант' + str(i_num)
                self.insert_variant_answer(val, id_curr_question)
        else:
            id_curr_question = int(self.ui_form_question.tableWidget_question_list.item(
                self.ui_form_question.tableWidget_question_list.currentRow(), 0).text())
            data_tuple_upd = (self.ui_form_question.textEdit_add_new_question.toPlainText(), id_curr_question)
            self.update_question_value(data_tuple_upd)
        self.update_question_list()
        self.get_new_question()

    def convert_to_binary_data(self, filename):
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    def update_question_value(self, data_tuple):
        file_address = self.ui_form_question.label_img_address.text()
        if file_address == '':
            emp_photo = None
        else:
            emp_photo = self.convert_to_binary_data(file_address)
        sqlite_insert_blob_query = """ update question set text_question = ?, img_question = ? where iq_question=?"""
        data_tuple = (data_tuple[0], emp_photo, data_tuple[1])
        con = sql.connect('data.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple)
        con.commit()
        cur.close()
        con.close()
        sqlite_insert_blob_query = """ update img set image = ? where id_question=?"""
        data_tuple1 = (emp_photo, data_tuple[1])
        con = sql.connect('img.db')
        cur = con.cursor()
        cur.execute(sqlite_insert_blob_query, data_tuple1)
        con.commit()
        cur.close()
        con.close()
        self.update_question_list()

    def insert_variant_answer(self, val, id_question):
        con = sql.connect('data.db')
        cur = con.cursor()
        cur.execute(
            'insert into variant_answer (text_var_answ, var_answ_right, id_question) '
            'values("{ins_val}", 0, {id_quest})'.format(
                ins_val=val,
                id_quest=id_question,
            ))
        con.commit()
        cur.close()
        con.close()
        con = sql.connect('data.db')
        cur = con.cursor()
        id_var_question = cur.execute(
            'select id_var_answ from variant_answer '
            'where text_var_answ = "{ins_val}" and id_question = {id_quest}'.format(
                ins_val=val,
                id_quest=id_question,
            ))
        id_var_question = id_var_question.fetchone()[0]
        con.commit()
        cur.close()
        con.close()
        con = sql.connect('img.db')
        cur = con.cursor()
        cur.execute(
            'insert into img (id_question, id_variant) '
            'values({id_quest}, {id_val})'.format(
                id_quest=id_question,
                id_val=id_var_question,
            ))
        con.commit()
        cur.close()
        con.close()

    def get_id_question(self):
        con = sql.connect('data.db')
        cur = con.cursor()
        id_question = cur.execute('select iq_question from question where text_question="{0}"'.format(
            self.ui_form_question.textEdit_add_new_question.toPlainText(),
        ))
        id_question = id_question.fetchall()
        con.commit()
        cur.close()
        con.close()
        if not id_question:
            return 0
        else:
            return id_question[0][0]

    def sql_delete(self):
        if self.ui_form_question.textEdit_add_new_question.toPlainText() != '':
            id_question = self.get_id_question()
            con = sql.connect('data.db')
            cur = con.cursor()
            cur.execute('delete from variant_answer where id_question={0}'.format(
                id_question,
            ))
            con.commit()
            cur.close()
            con.close()
            con = sql.connect('data.db')
            cur = con.cursor()
            cur.execute('delete from question where iq_question={0}'.format(
                id_question,
            ))
            con.commit()
            cur.close()
            con.close()
            con = sql.connect('img.db')
            cur = con.cursor()
            cur.execute('delete from img where id_question={0}'.format(
                id_question,
            ))
            con.commit()
            cur.close()
            con.close()
        self.update_question_list()

    def get_val(self):
        self.ui_form_question.label_show_img.clear()
        if self.ui_form_question.tableWidget_question_list.currentRow() != 0 and \
                self.ui_form_question.tableWidget_question_list.currentColumn() == 2:
            cur_text = self.ui_form_question.tableWidget_question_list.currentItem().text()
            self.ui_form_question.textEdit_add_new_question.setText(cur_text)
            con = sql.connect('data.db')
            cur = con.cursor()
            img_bin = cur.execute(
                'select img_question from question where text_question="{0}"'.format(
                    cur_text,
                ))
            img_bin = img_bin.fetchone()
            con.commit()
            cur.close()
            con.close()
            pix = QPixmap()
            if pix.loadFromData(img_bin[0], 'png'):
                self.ui_form_question.label_show_img.setPixmap(pix)

    def get_variants_form(self):
        current_item_value = self.ui_form_question.tableWidget_question_list.currentItem().text()
        if current_item_value == '-' or current_item_value == '' or current_item_value == '1':
            pass
        else:
            self.clear_variants()
            vals_answ = []
            curr_row = self.ui_form_question.tableWidget_question_list.currentRow()
            self.ui_form_question.tableWidget_question_list.setCurrentCell(curr_row, 0)
            con = sql.connect('data.db')
            cur = con.cursor()
            answer = cur.execute(
                'select text_var_answ, var_answ_right, variant_img from variant_answer where id_question={0}'.format(
                    self.ui_form_question.tableWidget_question_list.currentItem().text()
                ))
            for el in answer:
                vals_answ.append(el)
            curr_text_question = self.ui_form_question.textEdit_add_new_question.toPlainText()
            self.variants_window.ui_form_variants.textEdit_question_name.setText(
                curr_text_question)
            self.variants_window.ui_form_variants.textEdit_question_name.setEnabled(False)
            self.variants_window.ui_form_variants.textEdit_var1.setText(vals_answ[0][0])
            self.variants_window.ui_form_variants.textEdit_var2.setText(vals_answ[1][0])
            self.variants_window.ui_form_variants.textEdit_var3.setText(vals_answ[2][0])
            self.variants_window.ui_form_variants.textEdit_var4.setText(vals_answ[3][0])
            self.variants_window.ui_form_variants.textEdit_var1_t_f.setText(str(vals_answ[0][1]))
            self.variants_window.ui_form_variants.textEdit_var2_t_f.setText(str(vals_answ[1][1]))
            self.variants_window.ui_form_variants.textEdit_var3_t_f.setText(str(vals_answ[2][1]))
            self.variants_window.ui_form_variants.textEdit_var4_t_f.setText(str(vals_answ[3][1]))
            pix1 = QPixmap()
            if pix1.loadFromData(vals_answ[0][2], 'png'):
                self.variants_window.ui_form_variants.label_var1_img.setPixmap(pix1)
            pix2 = QPixmap()
            if pix2.loadFromData(vals_answ[1][2], 'png'):
                self.variants_window.ui_form_variants.label_var2_img.setPixmap(pix2)
            pix3 = QPixmap()
            if pix3.loadFromData(vals_answ[2][2], 'png'):
                self.variants_window.ui_form_variants.label_var3_img.setPixmap(pix3)
            pix4 = QPixmap()
            if pix4.loadFromData(vals_answ[3][2], 'png'):
                self.variants_window.ui_form_variants.label_var4_img.setPixmap(pix4)
            con.commit()
            cur.close()
            con.close()
            con = sql.connect('data.db')
            cur = con.cursor()
            img_bin = cur.execute(
                'select img_question from question where text_question="{0}"'.format(
                    curr_text_question,
                ))
            img_bin = img_bin.fetchone()
            con.commit()
            cur.close()
            con.close()
            pix = QPixmap()
            if pix.loadFromData(img_bin[0], 'png'):
                self.variants_window.ui_form_variants.label_question_img.setPixmap(pix)
            self.variants_window.show()

    def get_new_question(self):
        self.ui_form_question.textEdit_add_new_question.setText('')
        self.ui_form_question.tableWidget_question_list.setCurrentCell(0, 0)
        self.ui_form_question.tableWidget_question_list.clearSelection()
        self.ui_form_question.label_show_img.clear()
        self.ui_form_question.label_img_address.clear()

    def update_question_list(self):
        self.ui_form_question.tableWidget_question_list.clear()
        self.ui_form_question.tableWidget_question_list.setRowCount(0)
        self.ui_form_question.tableWidget_question_list.verticalHeader().setVisible(False)
        self.ui_form_question.tableWidget_question_list.setHorizontalHeaderLabels(
            ("id;№;Текст вопроса").split(";"))
        con = sql.connect('data.db')
        cur = con.cursor()
        questions = cur.execute('select * from question')
        self.ui_form_question.tableWidget_question_list.insertRow(
            self.ui_form_question.tableWidget_question_list.rowCount())

        self.ui_form_question.tableWidget_question_list.setItem(0, 0, QTableWidgetItem('-'))
        self.ui_form_question.tableWidget_question_list.setItem(0, 1, QTableWidgetItem('-'))
        self.ui_form_question.tableWidget_question_list.setItem(0, 2, QTableWidgetItem('-'))
        self.ui_form_question.tableWidget_question_list.hideRow(0)
        for i_el, el in enumerate(questions):
            self.ui_form_question.tableWidget_question_list.insertRow(
                self.ui_form_question.tableWidget_question_list.rowCount())
            self.ui_form_question.tableWidget_question_list.setItem(i_el + 1, 0, QTableWidgetItem(str(el[0])))
            self.ui_form_question.tableWidget_question_list.setItem(i_el + 1, 1, QTableWidgetItem(str(i_el + 1)))
            self.ui_form_question.tableWidget_question_list.setItem(i_el + 1, 2, QTableWidgetItem(str(el[1])))
        con.commit()
        cur.close()
        con.close()
        self.ui_form_question.tableWidget_question_list.resizeColumnsToContents()

    def open_file_name_dialog_variant1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        if fileName:
            self.variants_window.ui_form_variants.label_var1_path.setText(str(fileName))
            pixmap = QPixmap(fileName)
            self.variants_window.ui_form_variants.label_var1_img.setPixmap(pixmap)

    def open_file_name_dialog_variant2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        if fileName:
            self.variants_window.ui_form_variants.label_var2_path.setText(str(fileName))
            pixmap = QPixmap(fileName)
            self.variants_window.ui_form_variants.label_var2_img.setPixmap(pixmap)

    def open_file_name_dialog_variant3(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        if fileName:
            self.variants_window.ui_form_variants.label_var3_path.setText(str(fileName))
            pixmap = QPixmap(fileName)
            self.variants_window.ui_form_variants.label_var3_img.setPixmap(pixmap)

    def open_file_name_dialog_variant4(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        if fileName:
            self.variants_window.ui_form_variants.label_var4_path.setText(str(fileName))
            pixmap = QPixmap(fileName)
            self.variants_window.ui_form_variants.label_var4_img.setPixmap(pixmap)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        if fileName:
            self.ui_form_question.label_img_address.setText(str(fileName))
            pixmap = QPixmap(fileName)
            self.ui_form_question.label_show_img.setPixmap(pixmap)


class WindowEditVariants(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_form_variants = Ui_Form_variants_answ()
        self.ui_form_variants.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_server_window = WindowServerMain()
    main_server_window.show()
    sys.exit(app.exec_())
