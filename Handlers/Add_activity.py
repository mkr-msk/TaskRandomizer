from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from Classes import AddElementState
from DBOperator import add_item

router = Router()

@router.message(Command('add_activity'))
async def cmd_add_activity(message: types.Message, state: FSMContext):
    await message.answer(
        text="Enter activity name:",
    )
    await state.set_state(AddElementState.name)

@router.message(AddElementState.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text="Enter activity priority:",
    )
    await state.set_state(AddElementState.priority)

@router.message(AddElementState.priority)
async def process_priority(message: types.Message, state: FSMContext):
    await state.update_data(priority=message.text)
    await message.answer(
        text="Enter activity active:",
    )
    await state.set_state(AddElementState.active)

@router.message(AddElementState.active)
async def process_active(message: types.Message, state: FSMContext):
    await state.update_data(active=message.text)
    data = await state.get_data()
    add_item(data['name'], data['priority'], data['active'])
    await message.answer(
        text="Activity added",
    )
    await state.clear()
