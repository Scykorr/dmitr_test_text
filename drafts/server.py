from socket import *
import sqlite3 as sql
import json
from random import shuffle
import get_ip

with open('ip_address', 'r', encoding='utf-8') as ip_file:
    for el in ip_file:
        ip_address_server = el

# ip_address_server = get_ip.get_local_ip()


class Server:
    def __init__(self, ip, port, base_name):
        self.new_gen_list_questions = None
        print('SERVER IP: {ip}\nSERVER PORT: {port}\n'.format(
            ip=ip,
            port=port,
        ))
        self.data_name = base_name
        self.ser = socket(AF_INET, SOCK_STREAM)
        self.ser.bind(
            (ip, port)
        )
        self.generated_list_question = []
        self.generated_list_variant = []
        self.result_list = []
        self.gen_list()
        self.ser.listen(30)

    def gen_list(self):
        con = sql.connect(self.data_name)
        cur = con.cursor()

        self.generated_list_question = [x for x in cur.execute('select iq_question, text_question from question')]
        shuffle(self.generated_list_question)
        self.new_gen_list_questions = self.generated_list_question[:10]
        self.generated_list_variant = [y for y in cur.execute(
            'select id_var_answ, text_var_answ, var_answ_right, id_question from variant_answer')]
        shuffle(self.generated_list_variant)
        self.new_sorted_variants = self.sort_variants()
        self.result_list = self.new_gen_list_questions + self.new_sorted_variants
        con.commit()
        cur.close()
        con.close()

    def sort_variants(self):
        new_list = [[] for _ in range(10)]
        counter = 0
        for question in self.new_gen_list_questions:
            for var in self.generated_list_variant:
                if question[0] == var[3]:
                    new_list[counter].append(var)
            counter += 1
        return new_list

    def sender(self, user, text):
        user.send(text.encode('utf-8'))

    def start_server(self):
        while True:
            user, addr = self.ser.accept()
            print('CLIENT CONNECTED:\n\tIP: {addr_0}\nPORT: {addr_1}'.format(
                addr_0=addr[0],
                addr_1=addr[1],
            ))
            self.listen(user)

    def listen(self, user):
        self.sender(user, 'YOU ARE CONNECTED!')

        is_work = True

        while is_work:
            try:
                data = user.recv(1024)
                self.sender(user, 'getted')
            except Exception as e:
                data = ''
                is_work = False

            if len(data) > 0:

                msg = data.decode('utf-8')

                if msg == 'disconnect':
                    self.sender(user, 'YOU ARE DISCONNECTED!')
                    user.close()
                    is_work = False
                elif msg == 'test2_question':
                    try:
                        answer = self.result_list
                        error = ''
                    except Exception as e:
                        error = str(e)
                        answer = ''

                    ans = json.dumps(
                        {'answer': answer, 'error': error}
                    )
                    self.sender(user, ans)
                elif 1 < len(msg.split()) <= 3:
                    try:
                        answer = "adding name success!"
                        error = ''
                    except Exception as e:
                        error = str(e)
                        answer = ''

                    ans = json.dumps(
                        {'answer': answer, 'error': error}
                    )
                    self.sender(user, ans)
                else:

                    con = sql.connect(self.data_name)
                    cur = con.cursor()

                    try:
                        answer = [x for x in cur.execute(msg)]
                        error = ''
                    except Exception as e:
                        error = str(e)
                        answer = ''

                    con.commit()
                    cur.close()
                    con.close()

                    ans = json.dumps(
                        {'answer': answer, 'error': error}
                    )
                    self.sender(user, ans)

                data = b''
                msg = ''

            else:
                print('CLIENT DISCONNECTED')
                is_work = False


if __name__ == '__main__':
    Server(ip_address_server, 7000, "data.db").start_server()
