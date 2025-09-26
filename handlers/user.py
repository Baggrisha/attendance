"""
Файл с комманлами для анонсов
"""


# ипортирует всякие библиотеки и файлы
import asyncio
import datetime
import os

import yadisk
from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import *

from configs.settings import TOKEN, yandex_token
from db.attendance_db import Database_attendance
from db.users_224_db import Database_users_224
from keyboards.user import pair_condition, RegCallBackPairCondition, information, UploadFile, \
    confirm_upload, DeliteFile, homework_1


# позволяет обращаться к функциям с помощью коротких фраз
db_users_224 = Database_users_224()
db_attendance = Database_attendance()
router_user = Router()
bot = Bot(token=TOKEN)


# выбор был ли ты на паре
@router_user.callback_query(F.data.startswith('pair_'))
async def pair_select(call: CallbackQuery) -> None:
    if call.data == 'pair_1':
        await call.message.edit_text(text='Выберите свое присутсвие на паре', reply_markup=pair_condition(pair=1))
    if call.data == 'pair_2':
        await call.message.edit_text(text='Выберите свое присутсвие на паре', reply_markup=pair_condition(pair=2))
    if call.data == 'pair_3':
        await call.message.edit_text(text='Выберите свое присутсвие на паре', reply_markup=pair_condition(pair=3))
    if call.data == 'pair_4':
        await call.message.edit_text(text='Выберите свое присутсвие на паре', reply_markup=pair_condition(pair=4))
    if call.data == 'pair_5':
        await call.message.edit_text(text='Выберите свое присутсвие на паре', reply_markup=pair_condition(pair=5))


# внесение этого всего в бд
@router_user.callback_query(RegCallBackPairCondition.filter(F.status == '0'))
async def condition(call: CallbackQuery, callback_data: RegCallBackPairCondition) -> None:
    if datetime.datetime.now().strftime('%W') != 7:
        
        date_now = datetime.datetime.now().strftime('%d.%m.%Y')
        name = db_users_224.get_user_name(call.from_user.id)
        if not db_attendance.get_redacted(name=name, pair=callback_data.pair, date=date_now):
            if db_attendance.get_attendance(name=name, pair=callback_data.pair, date=date_now):
                db_attendance.edit_attendance(name=name, pair=callback_data.pair,
                                              attendance=int(callback_data.condition), date=date_now)
            else:
                db_attendance.add_attendance(name=name, pair=callback_data.pair,
                                             date=date_now, attendance=int(callback_data.condition))
            if callback_data.condition == '1':
                db_users_224.add_attendance(name=name)
                await call.message.edit_text(f'Вы отметили свое присутвие на {callback_data.pair} паре')
            else:
                db_users_224.add_pass(name=name)
                await call.message.edit_text(f'Вы отметили свое отсутсвие на {callback_data.pair} паре')
        else:
            await call.message.edit_text('Посешение было отмеченно старостой')
    else:
        await call.message.edit_text('Сегодня выходной')

# отменяет все действия
@router_user.message(F.text.startswith('/cancel'))
async def cancel(msg: Message, state: FSMContext):
    if msg.from_user.id == 222320537:
        await asyncio.sleep(60)
    await msg.answer('Действие отмененно')
    await state.clear()

# стартовое сообщение
@router_user.message(F.text.startswith('/information'))
async def information_h(msg: Message):
    if db_users_224.check_user(msg.from_user.id) and db_users_224.get_user_group(msg.from_user.id)[0] == '224':
        
        await msg.answer('Информация', reply_markup=information)


# позволяет загружать файл на яндекс диск
@router_user.message(F.text == ('/upload'))
async def file_upload(msg: Message, state: FSMContext):
    if db_users_224.check_user(msg.from_user.id) and msg.chat.type == 'private' and db_users_224.get_user_group(msg.from_user.id)[0] == '224':
        
        await msg.answer('Отправьте файл, для отмены воспользуйтесь коммандой /cancel')
        await state.set_state(UploadFile.file)

# подтверждение отправки
@router_user.message(StateFilter('UploadFile:file'))
async def send_file(msg: Message, state: FSMContext):
    if msg.document:
        
        await msg.answer('Подтвердите отправку, для отмены воспользуйтесь коммандой /cancel', reply_markup=confirm_upload)
        await state.update_data(file=msg.document.file_id, confirm=msg.document.file_name)
        await state.set_state(UploadFile.confirm)
        # await msg.answer()
    else:
        await msg.answer('Отправтьте файл')

# загружает файл на яндекс диск
@router_user.callback_query(StateFilter('UploadFile:confirm'))
async def confirm_send_file(call: CallbackQuery, state: FSMContext):
    if call.data == 'confirm_yes':
            if call.from_user.id == 222320537:
                await asyncio.sleep(60)
            list = []
            await call.answer('Загрузка файла')
        # try:
            if db_users_224.get_user_group(user_id=call.from_user.id)[0] == '224':
                y_224 = yadisk.AsyncClient(token=yandex_token)
                async with y_224 as y:
                    async for item in (y.listdir('/Копирайтинг')):
                        if item['type'] == 'dir':
                            list.append(item['name'])
                    file_name = (await state.get_data())['confirm']
                    file_id = (await state.get_data())['file']
                    file = await bot.get_file(file_id)
                    file_path = file.file_path
                    await bot.download_file(file_path, file_name)
                    await y.upload(file_name, f'/Копирайтинг/{list[-1]}/{file_name}')
            else:
                y_124 = yadisk.AsyncClient(token=yandex_token)
                async with y_124 as y:
                    async for item in (y.listdir('/Копирайтинг')):
                        if item['type'] == 'dir':
                            list.append(item['name'])
                    file_name = (await state.get_data())['confirm']
                    file_id = (await state.get_data())['file']
                    file = await bot.get_file(file_id)
                    file_path = file.file_path
                    await bot.download_file(file_path, file_name)
                    await y.upload(file_name, f'/Копирайтинг/{list[-1]}/{file_name}')
            os.remove(file_name)
            db_users_224.set_file(user_id=call.from_user.id, file=f'/Копирайтинг/{list[-1]}/{file_name}')
            await state.clear()
            await call.message.edit_text('Файл отправлен, если хотите его удалить, воспользуйте коммандой /del')
        # except:
        #     await state.clear()
        #     await call.message.edit_text('Произошла ошибка')
    else:
        await state.set_state(UploadFile.file)
        await call.message.edit_text('Отправьте файл, для отмены воспользуйтесь коммандой /cancel')


# удаляет последний загруженный вами файл с диска
@router_user.message(F.text == ('/del'))
async def file_delite(msg: Message, state: FSMContext):
    if msg.chat.type == 'private':
        if db_users_224.check_user(msg.from_user.id):
            if msg.from_user.id == 222320537:
                await asyncio.sleep(60)
            if db_users_224.get_file(user_id=msg.from_user.id) != '':
                file = db_users_224.get_file(user_id=msg.from_user.id)[0].split('/')[-1]
                await msg.answer(f'Подтвердите удаление файла "{file}", для отмены воспользуйтесь коммандой /cancel', reply_markup=confirm_upload)
                await state.set_state(DeliteFile.confirm)
            else:
                await msg.answer('Файл не найден')

# удаляет последний загруженный вами файл с диска
@router_user.callback_query(StateFilter('DeliteFile:confirm'))
async def confirm_delite_file(call: CallbackQuery, state: FSMContext):
    if call.from_user.id == 222320537:
        await asyncio.sleep(60)
    if call.data == 'confirm_yes':
            await call.answer('Удаление файла')
        # try:
            file = db_users_224.get_file(user_id=call.from_user.id)[0]
            if db_users_224.get_user_group(user_id=call.from_user.id):
                y_224 = yadisk.AsyncClient(token=yandex_token)
                async with y_224 as y:
                    await y.remove(file)
            else:
                y_124 = yadisk.AsyncClient(token=yandex_token)
                async with y_124 as y:
                    await y.remove(file)
            await state.clear()
            db_users_224.set_file(user_id=call.from_user.id, file='')
            await call.message.edit_text('Файл удалён')
        # except:
        #     await call.message.edit_text('Произошла ошибка')

    else:
        await state.clear()
        await call.message.edit_text('Удаление файла отменено')


# отправляет на яндекс диск с дз
@router_user.callback_query(F.data=='homework')
async def homework(call: CallbackQuery):
    await call.message.edit_text('Выберите дз', reply_markup=homework_1)


# логирует ошибки
@router_user.error()
async def errors_h(error: ErrorEvent) -> None:
    with open('logs_user.log', 'a') as f:
        f.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")} - [ERROR] {error.exception}\n')

