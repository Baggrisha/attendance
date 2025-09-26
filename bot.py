"""
Основной файл для запуска
"""


# ипортирует всякие библиотеки и файлы
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from configs.scripts import dell_logs
from configs.settings import TOKEN
from handlers.admin import router_admin
from handlers.announce import router_announce
from handlers.user import router_user

# базовая фигня,тупо копируется везде
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)


# позволяет объеденить все предыдущие файлы в один и запустить
async def main():
        # удаляет старые логи
        dell_logs()
        # запускает логирование
        logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')
        dp.include_router(router_user)
        dp.include_router(router_admin)
        dp.include_router(router_announce)
        setup_dialogs(dp)
        await dp.start_polling(bot)

# чтоб понять работает ли скрипт
print(1)

# запускает цикл, чтобы бот работал без остановок
if __name__ == "__main__":
    asyncio.run(main())