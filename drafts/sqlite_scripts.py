import sqlite3

# Создаем (или подключаемся к существующей) базе данных
conn = sqlite3.connect('main.db')

# Создаем курсор
cursor = conn.cursor()

# SQL-запрос для создания таблицы
create_table_query = '''
CREATE TABLE IF NOT EXISTS answer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NULL,
    answer TEXT NULL
);
'''

# Выполняем запрос
cursor.execute(create_table_query)

# # SQL-запрос для добавления данных
# insert_query = '''
# INSERT INTO pass (pass)
# VALUES (?)
# '''
#
# # Данные для добавления
# data = ('1')
#
# # Выполняем запрос
# cursor.execute(insert_query, data)


# select_query = 'SELECT * FROM pass'
# cursor.execute(select_query)
# rows = cursor.fetchall()
# print(rows[0][1])
# print("Данные из таблицы:")
# for row in rows:
#     print(row)
# update_query = 'UPDATE pass SET pass = ? WHERE id = ?'
# data = ('2', 1)  # Укажите новые данныеВыполняем запрос на обновление
# cursor.execute(update_query, data)
#
# select_query = 'SELECT * FROM pass'
# cursor.execute(select_query)
# rows = cursor.fetchall()
# print("Данные из таблицы:")
# for row in rows:
#     print(row)

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()