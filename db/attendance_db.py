"""
Файл с подключением к бд с посещением
"""


# ипортирует всякие библиотеки и файлы
import mysql.connector

from configs.settings import db_attendance_config


class Database_attendance:
    def __init__(self):
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
            self.cursor.execute("""DROP TABLE name_rank;""")
            print("[INFO]Table attendance was deleted")

    #  создание таблицы
    def create_table(self):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""{db_attendance_config};""")
            print("[INFO]Table attendance created successfully")


    # добавление пользователя
    def add_attendance(self, name: str, date: str, pair: int, attendance: int):
        with self.connection:
            self.connection.reconnect()
            return self.cursor.execute(
                f"""INSERT INTO attendance (name, date, pair, attendance) VALUES ('{name}', '{date}', {pair}, {attendance});""")


    def get_attendance(self, name: str, pair: int, date: str):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT attendance FROM attendance WHERE name = '{name}' and pair = {pair} and date = '{date}';""")
                if self.cursor.fetchall()[0] == 0:
                    return 'Был'
                else:
                    return 'Не был'
            except:
                return False

    def edit_attendance(self, name: str, attendance: int, date: str, pair: int):
        with self.connection:
            self.connection.reconnect()
            self.cursor.execute(f"""UPDATE attendance SET attendance = {attendance} WHERE name = '{name}' and date = '{date}' and pair = '{pair}';""")

    def get_redacted(self, name: str, pair: int, date: str):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT redacted FROM attendance WHERE name = '{name}' and pair = {pair} and date = {date};""")
                return self.cursor.fetchall()[0]
            except:
                return False
    def set_redacted(self, name: str, pair: int, date: str):
        with self.connection:
            self.connection.reconnect()
            return self.cursor.execute(f"""UPDATE attendance SET redacted = 1 WHERE name = '{name}' and pair = {pair} and date = {date};""")

    def get_full_attendance(self, name: str, date: str):
        with self.connection:
            self.connection.reconnect()
            try:
                self.cursor.execute(f"""SELECT * FROM attendance WHERE name = '{name}' and date = '{date}';""")
                return self.cursor.fetchall()
            except:
                return False