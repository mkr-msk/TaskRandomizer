# Version 2.2.1 Telegram Bot

# Импорт внутренних модулей
from DBOperator import *
from RandomElementSelector import *
from Elements import *

# Библиотеки для AIOgram
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Логирование
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(
    token=get_token(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Диспетчер
dp = Dispatcher()

# Обработка start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="/next")],
        [
            types.KeyboardButton(text="/show"),
            types.KeyboardButton(text="/update"),
        ],
        [
            types.KeyboardButton(text="/add"),
            types.KeyboardButton(text="/delete"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Select a menu item"
    )
    await message.answer('Select action:', reply_markup=keyboard)

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
    msg = ''

    for row in get_all_items('sorted'):
        msg += f'<b>{row[0]:35}</b>{row[1]} / {row[2]}\n'

    await message.answer(msg)

# Обработка add
@dp.message(Command('add'))
async def cmd_add(message: types.Message, command: CommandObject):
    e = Element()
    args = command.args.split()

    e.name = f'"{args[0]}"'
    e.priority = args[1]
    e.active = args[2]

    add_item(e)

# Обработка update
@dp.message(Command('update'))
async def cmd_update(message: types.Message, command: CommandObject):
    args = command.args.split()
    target = args[0]

    if target == 'Default':
        update_item(target)

    else:
        name = args[1]
        new_value = args[2]
        update_item(target, name, new_value)

# Обработка delete
@dp.message(Command('delete'))
async def cmd_delete(message: types.Message, command: CommandObject):
    args = command.args.split()
    name = args[0]

    delete_item(name)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())