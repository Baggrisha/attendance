"""
Бд с инфой про пользователей
"""


# ипортирует всякие библиотеки и файлы
import mysql.connector

from configs.settings import db_users_224_config


class Database_users_224:
    def __init__(self):
        # покдлючение к бд
        self.connection = mysql.connector.connect(
            host="",
            database="",
            user="",
            password=""
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    # удалиние таблицы
    def drop_table(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute("""DROP TABLE users_224;""")
            print("[INFO]Table users_224 was deleted")

    #  создание таблицы
    def create_table(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""{db_users_224_config}""")
            print("[INFO]Table users_224 created successfully")

    # добавление пользователя
    def add_user(self, user_id: int, name: str, group:str):
        with self.connection:
            self.connection.reconnect()
            return self.cursor.execute(
                f"""INSERT INTO users_224 (user_id, name, user_group) VALUES ({user_id}, '{name}', '{group}');""")

    def check_user(self, user_id: int):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM users_224 WHERE user_id = {user_id};""")
                return self.cursor.fetchall()[0]
            except:
                return False

    def get_user_id(self, name: str):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT user_id FROM users_224 WHERE name = '{name}';""")
                return self.cursor.fetchall()[0]
            except:
                try:
                    name1 = name.split()[-1] + ' ' + name.split()[0]
                    if name == 'Ю Ми Пак':
                        name1 = 'Пак Ю Ми'
                    self.cursor.execute(f"""SELECT user_id FROM users_224 WHERE name = '{name1}';""")
                    return self.cursor.fetchall()[0]
                except:
                    return False

    def get_user_name(self, user_id: int):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT name FROM users_224 WHERE user_id = {user_id};""")
                return self.cursor.fetchall()[0]
            except:
                return False

    def get_pass(self, name: str):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT pass FROM users_224 WHERE name = '{name}';""")
                data = self.cursor.fetchall()[0]
                if data[0] != '' and data[0] != None:
                    return data
                else:
                    return [0]
            except:
                return [0]

    def get_attendance(self, name: str):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT attendance FROM users_224 WHERE name = '{name}';""")
                data = self.cursor.fetchall()[0]
                if data[0] != '' and data[0] != None:
                    return data
                else:
                    return [0]
            except:
                return [0]

    def set_pass(self, user_id: int, pass1: int):
        with self.connection:
            self.connection.reconnect()
            return self.cursor.execute(f"""UPDATE users_224 SET pass = {pass1} WHERE user_id = {user_id};""")

    def set_attendance(self, user_id: int, attendance: int):
        with self.connection:
            self.connection.reconnect()
            return self.cursor.execute(f"""UPDATE users_224 SET attendance = {attendance} WHERE user_id = {user_id};""")

    def add_attendance(self, name: str):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT COUNT(attendance) FROM attendance WHERE attendance = 1 and name = '{name}';""")
                data = self.cursor.fetchall()[0]
                self.cursor.execute(f"""UPDATE users_224 SET attendance = {int(data[0])} WHERE name = '{name}';""")
            except:
                self.cursor.execute(f"""UPDATE users_224 SET attendance = 0 WHERE name = '{name}';""")

    def add_pass(self, name: str):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT COUNT(attendance) FROM attendance WHERE attendance = 0 and name = '{name}';""")
                data = self.cursor.fetchall()[0]
                self.cursor.execute(f"""UPDATE users_224 SET pass = {int(data[0])} WHERE name = '{name}';""")
            except:
                self.cursor.execute(f"""UPDATE users_224 SET pass = 0 WHERE name = '{name}';""")

    def get_all_user_id(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute("""SELECT user_id FROM users_224;""")
            return self.cursor.fetchall()

    def get_all_name(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute("""SELECT name FROM users_224;""")
            return self.cursor.fetchall()

    def get_all(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute('SELECT * FROM users_224;')
            return self.cursor.fetchall()

    def get_user_group(self, user_id: int):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f'SELECT user_group FROM users_224 WHERE user_id = {user_id};')
                return self.cursor.fetchall()[0]
            except:
                return False

    def set_file(self, user_id: int, file: str):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""UPDATE users_224 SET file = '{file}' WHERE user_id = {user_id};""")


    def get_file(self, user_id: int):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f'SELECT file FROM users_224 WHERE user_id = {user_id};')
                return self.cursor.fetchall()[0]
            except:
                return False