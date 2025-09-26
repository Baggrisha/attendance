"""
Файл с админскими клавиатурами
"""


# ипортирует всякие библиотеки и файлы
import datetime
import operator

from aiogram import F, Router
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (
    Dialog, DialogManager, Window, StartMode, ChatEvent,
)
from aiogram_dialog.widgets.kbd import Button, ManagedMultiselect, ScrollingGroup
from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog.widgets.kbd import Cancel, Column, Next, Back, Row, \
    SwitchTo
from aiogram_dialog.widgets.kbd import Multiselect
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Format

from configs.scripts import check_admin
from db.attendance_db import Database_attendance
from db.users_224_db import Database_users_224
from keyboards.admin import FullUserInfo

# позволяет обращаться к функциям с помощью коротких фраз
router_admin_dialog = Router()
db_users_224 = Database_users_224()
db_attendance = Database_attendance()


# переменное состояние
class SelectDataAdmin(StatesGroup):
    users = State()
    more_details = State()
    date = State()


class DialogAdmin(StatesGroup):
    date = State()
    pair = State()
    user1 = State()
    user2 = State()
    user3 = State()
    user4 = State()


# выбор был ли пользователь на паре
async def on_date_selected(call: CallbackQuery, widget,
                           manager: DialogManager, selected_date: datetime.date) -> None:
    data = (await manager.load_data())['start_data']
    msg_text = f'{data[1]}\n\n'
    date = str(selected_date.strftime('%d.%m.%Y'))
    name = db_users_224.get_user_name(user_id=data[0])
    list = (db_attendance.get_full_attendance(name=name, date=date))
    for i in list:
        if i[3] == 1:
            attendance = 'Был'
        else:
            attendance = 'Не был'
        msg_text += f'{i[1]} пара №{i[2]} {attendance}\n'
    if len(msg_text.splitlines()) > 2:
        await manager.done()
        await call.message.answer(msg_text)
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
    else:
        await call.answer('Данных за данный отрезок времени не найдено')


# вообще должен был быть чек бокс, но когда я понял, как его сделать, я осознал, что легче делать все на диске
async def note(event: ChatEvent, multi: ManagedMultiselect,
               manager: DialogManager, call: CallbackQuery, *args):
    data = (await manager.load_data())['start_data']
    if multi.is_checked(call):
        attendance = 1
    else:
        attendance = 0
    if not db_attendance.get_attendance(name=str(call), date=data[0], pair=data[1]):
        db_attendance.set_redacted(name=str(call), date=str(data[0]), pair=int(data[1]))
        db_attendance.add_attendance(name=str(call), date=str(data[0]), pair=int(data[1]), attendance=attendance)
    else:
        db_attendance.edit_attendance(name=str(call), date=str(data[0]), pair=int(data[1]), attendance=attendance)
    db_attendance.set_redacted(name=str(call), date=str(data[0]), pair=int(data[1]))


# показывает календарик, где можно выбрать определенный день
async def on_date_selected_admin(call: CallbackQuery, widget,
                                 manager: DialogManager, selected_date: datetime.date):
    await manager.start(DialogAdmin.pair, mode=StartMode.NEW_STACK, data=[selected_date.strftime('%d.%m.%Y'), ''])
    await manager.done()
    await call.message.delete()


async def on_pair_selected(call: CallbackQuery, widget,
                           manager: DialogManager):
    data = (await manager.load_data())['start_data']
    data[1] = call.data
    await manager.start(DialogAdmin.user1, mode=StartMode.NEW_STACK, data=data)
    await manager.done()
    await call.message.delete()

async def on_user_selected(call: CallbackQuery, widget,
                           manager: DialogManager) -> None:
    data = call.data.split('_')[1]
    await manager.start(SelectDataAdmin.date, mode=StartMode.NEW_STACK, data=data)
    await manager.done()
    await call.message.delete()


async def on_date_selected_user(call: CallbackQuery, widget,
                           manager: DialogManager, selected_date: datetime.date) -> None:
    data = (await manager.load_data())['start_data']
    name = db_users_224.get_all()[int(data[0])-1]
    msg_text = f'{name[1]}\n\n'
    date = str(selected_date.strftime('%d.%m.%Y'))
    list = (db_attendance.get_full_attendance(name=name[1], date=date))
    for i in list:
        if i[3] == 1:
            attendance = 'Был'
        else:
            attendance = 'Не был'
        msg_text += f'{i[1]} пара №{i[2]} {attendance}\n'
    if len(msg_text.splitlines()) > 2:
        await call.message.delete()
        await manager.done()
        await call.message.answer(msg_text)
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
    else:
        await call.answer('Данных за данный отрезок времени не найдено')


# клавиши где написанно фио людей(разбил на 7, ибо так красивее), а так же время и номер странички
async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        'stack': dialog_manager.current_stack(),
        'context': dialog_manager.current_context(),
        'now': datetime.datetime.now(),
        'counter': dialog_manager.dialog_data.get('counter', 0),
        'last_text': dialog_manager.dialog_data.get('last_text', ''),
        'users1': [
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
    ('6', 6),
    ('7', 7),
],
    'users2': [
        ('8', 8),
        ('9', 9),
        ('10', 10),
        ('11', 11),
        ('12', 12),
        ('13', 13),
        ('14', 14),
    ],
    'users3': [
        ('15', 15),
        ('16', 16),
        ('17', 17),
        ('18', 18),
        ('19', 19),
        ('20', 20),
        ('21', 21),
    ],
    }


def button_select():
    buttons = []
    btn_quantity = ['']
    for i in btn_quantity:
        buttons.append(Button(Const(f'{i}'), id=f'select_{btn_quantity.index(i)+1}', on_click=on_user_selected))
    return buttons

page1 = Column(Multiselect(
    Format('× {item[0]}'),
    Format('✓ {item[0]}'),
    id='check1',
    item_id_getter=operator.itemgetter(1),
    items='users1', on_click=note)
)

page2 = Column(Multiselect(
    Format('× {item[0]}'),  # E.g `✓ Apple`
    Format('✓ {item[0]}'),
    id='check2',
    item_id_getter=operator.itemgetter(1),
    items='users2', on_click=note)
)

page3 = Column(Multiselect(
    Format('× {item[0]}'),  # E.g `✓ Apple`
    Format('✓ {item[0]}'),
    id='check3',
    item_id_getter=operator.itemgetter(1),
    items='users3', on_click=note)
)

button_select = button_select()

select = (ScrollingGroup(
    *button_select,
    id="select", height=7, width=1
))


go_calendar_select = SwitchTo(
    Const('Выбор даты'),
    id='date',
    state=SelectDataAdmin.date
)

go_calendar = SwitchTo(
    Const('Выбор даты'),
    id='date',
    state=DialogAdmin.date
)

go_pair = SwitchTo(
    Const('Выбор пары'),
    id='pair',
    state=DialogAdmin.pair
)



async def add_all(call: CallbackQuery, widget,
                  manager: DialogManager):
    data = (await manager.load_data())['start_data']
    users_id = db_users_224.get_all_name()
    await call.answer('Начало отметки')
    for i in users_id:
        try:
            db_users_224.add_attendance(name=i[0])
            if not db_attendance.get_attendance(name=(i[0]), date=str(data[0]), pair=int(data[1])):
                db_attendance.set_redacted(name=(i[0]), date=str(data[0]), pair=int(data[1]))
                db_attendance.add_attendance(name=(i[0]), date=str(data[0]), pair=int(data[1]), attendance=1)
            else:
                db_attendance.set_redacted(name=(i[0]), date=str(data[0]), pair=int(data[1]))
                db_attendance.edit_attendance(name=(i[0]), date=str(data[0]), pair=int(data[1]), attendance=1)


        except:
            pass
    await call.answer('Отметка завершена')


dialog_admin_select = Dialog(
     Window(
    Const("Hello, nigga"),
        Calendar(id='calendar', on_click=on_date_selected_user),
        Cancel(),
        state=SelectDataAdmin.date,
),
    Window(
        Format('Выберите студента\n'),
        select,
        go_calendar_select,
        Cancel(),
        state=SelectDataAdmin.users,
        getter=get_data,
    ),
)

dialog_admin = Dialog(

    Window(
        Format('Выберите дату\n'),
        Calendar(id='calendar', on_click=on_date_selected_admin),
        Cancel(),
        state=DialogAdmin.date,
        getter=get_data,
    ),

    Window(
        Format('Выберете пару\n'),
        Button(Const('1 пара'), on_click=on_pair_selected, id='1'),
        Button(Const('2 пара'), on_click=on_pair_selected, id='2'),
        Button(Const('3 пара'), on_click=on_pair_selected, id='3'),
        Button(Const('4 пара'), on_click=on_pair_selected, id='4'),
        Button(Const('5 пара'), on_click=on_pair_selected, id='5'),
        go_calendar,
        Cancel(),
        state=DialogAdmin.pair,
        getter=get_data,
    ),

    Window(
        Format('Выберите студента\n'),
        page1,
        Row(Button(Const('Отметить всех'), id='add_add', on_click=add_all), Next(Const('Вперед'))),
        go_pair,
        state=DialogAdmin.user1,
        getter=get_data,
    ),
    Window(
        Format('Выберите студента\n'),
        page2,
        Row(Back(Const('Назад')),
            Button(Const('Отметить всех'), id='add_add', on_click=add_all),
            Next(Const('Вперед'))),
        go_pair,
        state=DialogAdmin.user2,
        getter=get_data,
    ),
    Window(
        Format('Выберите студента\n'),
        page3,
        Row(Back(Const('Назад')),
            Button(Const('Отметить всех'), id='add_add', on_click=add_all), ),

        go_pair,
        state=DialogAdmin.user3,
        getter=get_data,
    ),

)

@router_admin_dialog.message(F.text == '/info')
async def info(msg: Message, state: FSMContext, dialog_manager: DialogManager) -> None:
    if check_admin(user_id=msg.from_user.id):
        await dialog_manager.start(state=SelectDataAdmin.users)
        # await state.set_state(SetAttendance1.user_id)


@router_admin_dialog.callback_query(FullUserInfo.filter(F.status == '1'))
async def get_full_user_info(call: CallbackQuery, callback_data: FullUserInfo, dialog_manager: DialogManager) -> None:
    user_id = int(db_users_224.get_user_id(callback_data.user)[0])
    await dialog_manager.start(state=SelectDataAdmin.date, data=[user_id, callback_data.user], mode=StartMode.RESET_STACK)



@router_admin_dialog.message(F.text == '/list')
async def edit_list(msg: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(DialogAdmin.date, mode=StartMode.NEW_STACK)
