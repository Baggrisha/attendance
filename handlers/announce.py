"""
Файл с комманлами для анонсов
"""


# ипортирует всякие библиотеки и файлы
import datetime

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import *

from configs.scripts import check_admin
from configs.settings import TOKEN
from db.attendance_db import Database_attendance
from db.users_224_db import Database_users_224
from keyboards.admin import SendAnnounce, get_confirm


# позволяет обращаться к функциям с помощью коротких фраз
db_users_224 = Database_users_224()
db_attendance = Database_attendance()
router_announce = Router()
state = State
bot = Bot(token=TOKEN)

# включает состояние, когда вы можете скинуть любой текст/фото и тд и он перешлёт его
@router_announce.message(F.text == '/announce')
async def announce(msg: Message, state: FSMContext):
    if check_admin(user_id=msg.from_user.id):
        await msg.answer('Отправьте сообщение для рассылки')
        await state.set_state(SendAnnounce.post)


# дает проверить, все ли правильно отправляется
@router_announce.message(StateFilter('SendAnnounce:post'))
async def announce_topic(msg: Message, state:FSMContext, album: list[Message] = None):
    media_group = []
    if album != None:
        for msg in album:
            if msg.photo:
                file_id = msg.message_id
                media_group.append(file_id)
            else:
                obj_dict = msg.dict()
                file_id = obj_dict[msg.message_id]
                media_group.append(file_id)

        await bot.forward_messages(chat_id=msg.chat.id, message_ids=media_group, from_chat_id=msg.chat.id)
    else:
        media_group.append(msg.message_id)
        await bot.forward_message(chat_id=msg.chat.id, message_id=msg.message_id, from_chat_id=msg.chat.id)
    await state.update_data(post=media_group)
    await msg.answer('Подтвердите отправку сообщения', reply_markup=get_confirm)
    await state.set_state(SendAnnounce.confirmation)


# отправляет сообщение всем пользователям из базы данных
@router_announce.callback_query(StateFilter('SendAnnounce:confirmation'))
async def announce_topic(call: CallbackQuery, state: FSMContext):
    if call.data == 'confirm_yes':
        msg_id = await state.get_data()
        list = db_users_224.get_all_user_id()
        error_msg = 'Не получилось отправить сообщеение для:\n\n'
        await call.message.edit_text('Начата отправка сообщений')
        for i in list:
            if db_users_224.get_user_group(user_id=i[0])[0] == '224':
                try:
                    await bot.forward_messages(chat_id=i[0], message_ids=msg_id['post'],
                                               from_chat_id=call.from_user.id)
                except:
                    error_msg += f'{db_users_224.get_user_name(user_id=i[0])[0]}, '
        try:
            await bot.forward_messages(chat_id=-1002455662855, message_ids=msg_id['post'],
                                               from_chat_id=call.from_user.id)
        except:
            pass
        await call.message.edit_text('Сообщения отправленны')
        await call.message.answer(error_msg)
    else:
        await call.message.edit_text('Отправка сообщения отменена')
    await state.clear()

# логгирует ошибки
@router_announce.error()
async def errors_h(error: ErrorEvent):
    with open('logs_announce.log', 'a') as f:
        f.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")} - [ERROR] {error.exception}\n')

