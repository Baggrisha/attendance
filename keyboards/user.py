"""
Файл с клавиатурами для пользователей
"""



# ипортирует всякие библиотеки и файлы

import yadisk
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# долго и сложно объяснять че эта, но это словарь состояний
class UploadFile(StatesGroup):
    file = State()
    confirm = State()

class DeliteFile(StatesGroup):
    confirm = State()

class RegCallBackPairCondition(CallbackData, prefix=''):
    status: str
    pair: int
    condition: str


# клавиатура с кол-вом пар
pair = InlineKeyboardBuilder()
pair1 = InlineKeyboardButton(text='Первая пара', callback_data='pair_1')
pair2 = InlineKeyboardButton(text='Вторая пара', callback_data='pair_2')
pair3 = InlineKeyboardButton(text='Третья пара', callback_data='pair_3')
pair4 = InlineKeyboardButton(text='Четвертая пара', callback_data='pair_4')
pair5 = InlineKeyboardButton(text='Пятая пара', callback_data='pair_5')

pair.add(pair1, pair2, pair3, pair4, pair5)
pair.adjust(1, repeat=False)
pair = pair.as_markup()


# клавиатура, с вариантами нахождения на паре
def pair_condition(pair):
    pair_condition = InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(
                text='Присутсвую',
                callback_data=RegCallBackPairCondition(
                    status='0', pair=pair, condition='1'
                ).pack()),

        InlineKeyboardButton(
            text='Отсутсвую',
            callback_data=RegCallBackPairCondition(
                status='0', pair=pair, condition='0'
            ).pack()),

        ],
        ])
    return pair_condition

# клавиатура,где можно получить полную инфу про себя
get_info = InlineKeyboardBuilder()
more_details = InlineKeyboardButton(text='Подробнее', callback_data='get_info')
get_info.add(more_details)
get_info = get_info.as_markup()

# клавиатура, с основным фунционалом бота
information = InlineKeyboardBuilder()
schedule = InlineKeyboardButton(text='Расписание', url='https://disk.yandex.ru/d/qbTUIxveURk4nA/Цифровые%20коммуникации%20и%20искусственный%20интеллект')
exams = InlineKeyboardButton(text='Экзаменационная сессия', url='https://disk.yandex.ru/d/h4lx7G_pZum2zQ')
schedule_retake = InlineKeyboardButton(text='Расписание пересдач', url='https://ion.ranepa.ru/students/study/raspisanie-peresdach-bakalavriat/')
rating = InlineKeyboardButton(text='Рейтинг студентов', url='https://disk.yandex.ru/d/dyJR6mZA0Lv3Xw')
mark_system = InlineKeyboardButton(text='Система оценивания', url='https://ion.ranepa.ru/students/study/sistema-otsenivaniya/')
homework = InlineKeyboardButton(text='Домашка', callback_data='homework')
information.add(schedule, exams, schedule_retake, rating, mark_system, homework)
information.adjust(1, repeat=False)
information = information.as_markup()


# ещё одна клава да/нет , одной мне мало
confirm_upload = InlineKeyboardBuilder()
yes_upload = InlineKeyboardButton(text='✅', callback_data='confirm_yes')
no_upload = InlineKeyboardButton(text='❌', callback_data='confirm_no')
confirm_upload.add(yes_upload, no_upload)
# confirm_upload.adjust(1, repeat=False)
confirm_upload = confirm_upload.as_markup()

# клавиатура, где можно загрузить дз на диск
homework_1 = InlineKeyboardBuilder()
# all_homework = InlineKeyboardButton(text='Вся домашка', url='')
polit_homework = InlineKeyboardButton(text='Копирайтинг', url='')
disk = InlineKeyboardButton(text='Диск по копирайтиноу', url='')
back_homework = ''
homework_1.add(polit_homework, disk)
homework_1.adjust(1, repeat=False)
homework_1 = homework_1.as_markup()
