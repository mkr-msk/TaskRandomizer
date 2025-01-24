# Version 2.4.1

# Импорт внутренних модулей
from DBOperator import *
from RandomElementSelector import *
from Elements import *

# Библиотеки для AIOgram
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
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
    builder = InlineKeyboardBuilder()

    for row in get_all_items('sorted'):
        builder.row(types.InlineKeyboardButton(
            text=f'{row[0]:25}{row[1]} / {row[2]}',
            callback_data=f'show_{row[0]}')
        )

    await message.answer(
        text="All activities",
        reply_markup=builder.as_markup()
    )

# Обработка команды update_menu
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

# Обработка update_menu callbacks
@dp.callback_query(F.data.startswith("update_"))
async def callback_update(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    all_items = get_all_items(mode='sorted')

    match action:
        case 'default':
            update_item(target='Default')

            await callback.message.answer(text='Ok')

        case 'active':
            builder = InlineKeyboardBuilder()
            for row in all_items:
                builder.row(types.InlineKeyboardButton(
                    text=row[0],
                    callback_data=f'update_{row[0]}')
                )

            await callback.message.answer(
                text='Select item to deactivate:',
                reply_markup=builder.as_markup(resize_keyboard=True),
            )

    for row in all_items:
        if row[0] == action:
            update_item('Active', row[0], '0')

            await callback.message.answer(text='Ok')

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())