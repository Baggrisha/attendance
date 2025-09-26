"""
Файл с клавиатурами админа
"""


# ипортирует всякие библиотеки и файлы

import yadisk
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from configs.settings import yandex_token


# долго и сложно объяснять че эта, но это словарь состояний
class SetAttendance(StatesGroup):
    user_id = State()
    date = State()
    name = State()

class SetAttendance1(StatesGroup):
    user_id = State()

class SendAnnounce(StatesGroup):
    post = State()
    confirmation = State()

class SetAttendanceAdmin(StatesGroup):
    pair = State()

class UploadHomework(StatesGroup):
    file = State()
    folder = State()
    confirm = State()


class FullUserInfo(CallbackData, prefix=''):
    status: str
    user: str

class GetHomeworkFolders(CallbackData, prefix=''):
    status: str
    folder: str


# клавиатура,где можно получить полную инфу про юзера, храняющуюся в бд
def get_full_info(user):
    pair_condition = InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(
                text='Подробнее',
                callback_data=FullUserInfo(
                    status='1', user=user
                ).pack()),
        ],
        ])
    return pair_condition

# кнопки да и нет
get_confirm = InlineKeyboardBuilder()
confirm_yes = InlineKeyboardButton(text='✅', callback_data='confirm_yes')
confirm_no = InlineKeyboardButton(text='❌', callback_data='confirm_no')
get_confirm.add(confirm_no, confirm_yes)
get_confirm = get_confirm.as_markup()


# делает клавиатуру со всеми папками на диске внутри папки /Дз
async def folder_button():
    folders = InlineKeyboardBuilder()
    y = yadisk.AsyncClient(token=yandex_token)
    index = 0
    async with y:
        async for item in y.listdir('/Дз'):
            if item['type'] == 'dir':
                index += 1
                button = InlineKeyboardButton(text=str(item['name']), callback_data=f'homework_{index}')
                folders.add(button)
    back = InlineKeyboardButton(text='Отменить', callback_data='homework_cancel')
    folders.add(back)
    folders.adjust(1, repeat=False)
    return folders.as_markup()