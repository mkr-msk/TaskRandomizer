# Version 2.1.2 Telegram Bot

# Импорт внутренних модулей
from DBOperator import *
from RandomElementSelector import *
from Elements import *

# Библиотеки для AIOgram
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Логирование
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=get_token())

# Диспетчер
dp = Dispatcher()

# Обработка next
@dp.message(Command('next'))
async def cmd_next(message: types.Message):
    elements = []

    for row in get_all_items():
        elements.append(Element(row[0], row[1], row[2]))

    msg = choose_random_element(elements)

    await message.answer(msg)

# Обработка show
@dp.message(Command('show'))
async def cmd_show(message: types.Message):
    msg = ""
    for row in get_all_items('sorted'):
        msg += f'{row[0]:40}{row[1]} / {row[2]}' + '\n'

    await message.answer(msg)

# Обработка add
@dp.message(Command('add'))
async def cmd_add(message: types.Message):
    e = Element()

    e.name = f'"{message.args[0]}"'
    e.priority = message.args[1]
    e.active = message.args[2]

    add_item(e)

# Обработка update
@dp.message(Command('update'))
async def cmd_update(message: types.Message):
    target = message.args[0]

    if target == 'Default':
        update_item(target)

    else:
        name = message.args[1]
        new_value = message.args[2]
        update_item(target, name, new_value)

# Обработка delete
@dp.message(Command('delete'))
async def cmd_delete(message: types.Message):
    name = message.args[0]

    delete_item(name)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())