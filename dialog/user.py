# ипортирует всякие библиотеки и файлы
import datetime

from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import (
    DialogManager, StartMode,
)


from db.attendance_db import Database_attendance
from db.users_224_db import Database_users_224

db_users_224 = Database_users_224()
db_attendance = Database_attendance()
router_user_dialog = Router()

class SelectDataUser(StatesGroup):
    date = State()

async def on_date_selected(call: CallbackQuery, widget,
                           manager: DialogManager, selected_date: datetime.date) -> None:
    msg_text = f'{db_users_224.get_user_name(user_id=call.from_user.id)[0]}\n\n'
    date = str(selected_date.strftime('%d.%m.%Y'))
    name = db_users_224.get_user_name(user_id=call.from_user.id)
    list = (db_attendance.get_full_attendance(name=name, date=date))
    if type(list) == list:
        for i in list:
            if i[3] == 1:
                attendance = 'Был'
            else:
                attendance = 'Не был'
            msg_text += f'{i[1]} пара №{i[2]} {attendance}\n'
        if len(msg_text.splitlines()) > 2:
            await manager.done()
            await call.message.answer(msg_text)
        else:
            await call.answer('Данных за данный отрезок времени не найдено')
    else:
        await call.answer('Данных за данный отрезок времени не найдено')



@router_user_dialog.callback_query(F.data == 'get_info')
async def get_full_user_info(call: CallbackQuery, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=SelectDataUser.date, mode=StartMode.RESET_STACK)