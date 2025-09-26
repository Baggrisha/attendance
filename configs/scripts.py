"""
Файл с различными основными функциями
"""



# ипортирует всякие библиотеки и файлы
import os
from configs.settings import admins


# проверка на то является ли пользователь админом
def check_admin(user_id):
    if user_id in admins:
        return True
    else:
        return False


# считает процент посещения
def attendance_percent(name, pass1, attendance):
    # смотрит если данные в таблице
    if attendance == None:
        attendance = 0
    else:
        attendance = int(attendance)

    if pass1 == None:
        pass1 = 0
    else:
        pass1 = int(pass1)
    # считает процент
    if pass1 + attendance != 0:
        summ = (attendance / (pass1 + attendance)) * 100
    else:
        summ = 0
    if type(summ) == float:
        summ = round(summ, 2)
    #  возвращает результат
    return summ


# очищает логи
def dell_logs():
    try:
        os.remove('logs.log')

    except:
        pass

    try:
        os.remove('logs_user.log')
    except:
        pass

    try:
        os.remove('logs_admin.log')
    except:
        pass

    try:
        os.remove('logs_announce.log')
    except:
        pass


