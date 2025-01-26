from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from DBOperator import get_all_items


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(
        types.KeyboardButton(text="/next"),
        types.KeyboardButton(text="/show"),
    )
    kb.row(
        types.KeyboardButton(text="/add_activity"),
        types.KeyboardButton(text="/reset_all"),
    )
    return kb.as_markup(resize_keyboard=True)

def get_show_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for row in get_all_items('sorted'):
        kb.row(types.InlineKeyboardButton(
            text=f'{row[0]:25}{row[1]} / {row[2]}',
            callback_data=f'show_{row[0]}_submenu')
        )
    return kb.as_markup(resize_keyboard=True)

def get_show_submenu(item: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # Кнопки Update и Delete
    kb.add(types.InlineKeyboardButton(
        text="Update",
        callback_data=f"show_{item}_update")
    )
    kb.add(types.InlineKeyboardButton(
        text="Delete",
        callback_data=f"show_{item}_delete")
    )
    return kb.as_markup(resize_keyboard=True)

def get_update_submenu(item: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # Кнопки Name / Priority / Deactivate
    kb.add(types.InlineKeyboardButton(
        text="Name",
        callback_data=f"show_{item}_update_name")
    )
    kb.add(types.InlineKeyboardButton(
        text="Priority",
        callback_data=f"show_{item}_update_priority")
    )
    kb.add(types.InlineKeyboardButton(
        text="Deactivate",
        callback_data=f"show_{item}_update_deactivate")
    )
    return kb.as_markup(resize_keyboard=True)