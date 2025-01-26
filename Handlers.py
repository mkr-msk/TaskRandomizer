from aiogram import Router, types
from aiogram.filters import Command

from DBOperator import *
from Elements import Element
from Keyboards import *
from RandomElementSelector import choose_random_element

router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(
        text='Select action:',
        reply_markup=get_start_kb(),
    )

@router.message(Command('next'))
async def cmd_next(message: types.Message):
    elements = []

    for row in get_all_items():
        elements.append(Element(row[0], row[1], row[2]))

    msg = choose_random_element(elements)

    await message.answer(msg)

@router.message(Command('show'))
async def cmd_show(message: types.Message):
    await message.answer(
        text="All activities",
        reply_markup=get_show_kb(),
    )

@router.message(Command('add_activity'))
async def cmd_add_activity(message: types.Message):
    pass # диалог с пользователем

@router.message(Command('reset_all'))
async def cmd_reset_all(message: types.Message):
    update_item(target='Default')
    await message.answer(
        text="All activities are reset to default",
    )