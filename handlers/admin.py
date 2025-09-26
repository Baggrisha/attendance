"""
Файл с админскими комманлами
"""


# ипортирует всякие библиотеки и файлы
import os
from datetime import datetime

import yadisk
from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import *

from configs.scripts import check_admin
from configs.settings import TOKEN, yandex_token
from db.attendance_db import Database_attendance
from db.users_224_db import Database_users_224
from keyboards.admin import get_full_info, folder_button, UploadHomework, get_confirm

# позволяет обращаться к функциям с помощью коротких фраз
db_users_224 = Database_users_224()
db_attendance = Database_attendance()
router_admin = Router()
bot = Bot(token=TOKEN)
state = State

# позволяет посмотреть статистику по пользователю кол-во посещений и прогулов
@router_admin.message(StateFilter('SetAttendance1:user_id'))
async def set_name(msg: Message, state: FSMContext) -> None:
    if db_users_224.get_user_id(name=msg.text):
        pass1 = int(db_users_224.get_pass(name=msg.text)[0])
        attendance = int(db_users_224.get_attendance(name=msg.text)[0])
        if pass1+attendance != 0:
            summ = (attendance/(pass1+attendance))*100
        else:
            summ = 0
        if type(summ) == float:
            summ = round(summ, 2)
        msg_text = (f'{msg.text}\n\n'
                    f'Прогулов {pass1}\n'
                    f'Посещений {attendance}\n'
                    f'Посещаемость {summ}%')
        await msg.answer(msg_text, reply_markup=get_full_info(user=msg.text))
        await state.clear()
    else:
        await msg.reply('Пользователь не найден')


# загрузка дз в папки
@router_admin.message(F.text == '/h')
async def homework_add(msg: Message, state: FSMContext):
    if check_admin(user_id=msg.from_user.id):
        await msg.answer('Выберите папку', reply_markup=(await folder_button()))
        await state.set_state(UploadHomework.file)


# получение и обработка файла
@router_admin.callback_query(F.data.startswith('homework_') and StateFilter('UploadHomework:file'))
async def select_folder(call: CallbackQuery, state: FSMContext):
    if call.data != 'homework_cancel':
        await state.set_state(UploadHomework.folder)
        await call.message.edit_text('Отправте файл')
        await state.update_data(folder=call.data.split('_')[1])
    else:
        await call.message.edit_text('Отмена')
        await state.clear()


# подтверждение отправки
@router_admin.message(StateFilter('UploadHomework:folder'))
async def confirm_homework(msg: Message, state: FSMContext):
    if msg.document:
        await msg.answer('Подтвердите отправку, для отмены воспользуйтесь коммандой /cancel', reply_markup=get_confirm)
        await state.update_data(file=msg.document.file_id, confirm=msg.document.file_name)
        await state.set_state(UploadHomework.confirm)
    else:
        await msg.answer('Отправьте файл')


# отправка файла на яндекс диск(есть ограничения по размерам)
@router_admin.callback_query(StateFilter('UploadHomework:confirm'))
async def send_homework(call: CallbackQuery, state: FSMContext):
    # если вы подтвердили, то бот скачивает файл на сервер, отправляет на диск и чистит его с сервера
    if call.data == 'confirm_yes':
        await call.answer('Загрузка файла')
        list = []
        y = yadisk.AsyncClient(token=yandex_token)
        async with y:
            async for item in (y.listdir('/Дз')):
                if item['type'] == 'dir':
                    list.append(item['name'])

            file_name = (await state.get_data())['confirm']
            file_id = (await state.get_data())['file']
            folder = (await state.get_data())['folder']
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, file_name)
            await y.upload(file_name, f'/Дз/{list[int(folder)-1]}/{file_name}')
            os.remove(file_name)
            await call.message.edit_text('Файл загружен')
    else:
        # иначе он отменяет отправку
        await call.message.edit_text('Загрузка файла отменена')
    await state.clear()



# логирует ошибким
@router_admin.error()
async def errors_h(error: ErrorEvent) -> None:
    with open('logs_admin.log', 'a') as f:
        f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")} - [ERROR] {error.exception}\n')


