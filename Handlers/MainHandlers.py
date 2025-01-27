from aiogram import Router, types
from aiogram.filters import Command

from DBOperator import choose_random_element, update_item
from Keyboards import get_start_kb, get_show_kb

router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(
        text='Select action:',
        reply_markup=get_start_kb(),
    )

@router.message(Command('next'))
async def cmd_next(message: types.Message):
    msg = choose_random_element()
    await message.answer(msg)

@router.message(Command('show'))
async def cmd_show(message: types.Message):
    await message.answer(
        text="All activities",
        reply_markup=get_show_kb(),
    )

@router.message(Command('reset_all'))
async def cmd_reset_all(message: types.Message):
    update_item(target='Default')
    await message.answer(
        text="All activities are reset to default",
    )
