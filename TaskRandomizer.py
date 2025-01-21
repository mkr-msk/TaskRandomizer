# Version 2.2.3

# Импорт внутренних модулей
from DBOperator import *
from RandomElementSelector import *
from Elements import *

# Библиотеки для AIOgram
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

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
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="/next"),
        types.KeyboardButton(text="/show"),
    )
    builder.row(types.KeyboardButton(text='/update_menu'))

    await message.answer(
        text='Select action:',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

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
async def cmd_add(command: CommandObject):
    e = Element()
    args = command.args.split()

    e.name = f'"{args[0]}"'
    e.priority = args[1]
    e.active = args[2]

    add_item(e)

# Обработка update
@dp.message(Command('update'))
async def cmd_update(command: CommandObject):
    args = command.args.split()
    target = args[0]
    name = args[1]
    new_value = args[2]
    update_item(target, name, new_value)

# Обработка update_menu
@dp.message(Command('update_menu'))
async def cmd_update_menu(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Reset all",
        callback_data="update_default")
    )
    builder.add(types.InlineKeyboardButton(
        text="Deactivate",
        callback_data="update_active")
    )

    await message.answer(
        text="Select update mode:",
        reply_markup=builder.as_markup()
    )

# Обработка delete
@dp.message(Command('delete'))
async def cmd_delete(command: CommandObject):
    args = command.args.split()
    name = args[0]

    delete_item(name)

# Обработка update_menu / update_default
@dp.callback_query(F.data == "update_default")
async def update_default():
    update_item('Default')

# Обработка update_menu / update_active
@dp.callback_query(F.data == "update_active")
async def update_active(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Chores",
        callback_data="update_active_chores")
    )
    builder.add(types.InlineKeyboardButton(
        text="Hygiene",
        callback_data="update_active_hygiene")
    )
    builder.add(types.InlineKeyboardButton(
        text="Workout",
        callback_data="update_active_workout")
    )

    await callback.message.answer(
        text='Select item to deactivate:',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

# Обработка update_menu / update_active / update_active_chores
@dp.callback_query(F.data == "update_active_chores")
async def update_active_chores():
    update_item('Active', 'Chores', '0')

# Обработка update_menu / update_active / update_active_hygiene
@dp.callback_query(F.data == "update_active_hygiene")
async def update_active_hygiene():
    update_item('Active', 'Hygiene', '0')

# Обработка update_menu / update_active / update_active_workout
@dp.callback_query(F.data == "update_active_workout")
async def update_active_workout():
    update_item('Active', 'Workout', '0')


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())