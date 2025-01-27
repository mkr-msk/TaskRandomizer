from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from Classes import UpdateNameState, UpdatePriorityState
from DBOperator import delete_item, update_item
from Keyboards import get_show_submenu, get_update_submenu

router = Router()

# Обработка show меню элемента
@router.callback_query(F.data.startswith("show_"))
async def callback_show(callback: types.CallbackQuery, state: FSMContext):
    commands = callback.data.split("_", 2)
    item = commands[1]
    action = commands[2]

    match action:
        # Подменю show: update / delete
        case 'submenu':
            await callback.message.answer(
                text=f'What to do with {item}',
                reply_markup=get_show_submenu(item),
            )

        # Подменю update: name / priority / deactivate
        case 'update':
            await callback.message.answer(
                text=f'What to update in {item}',
                reply_markup=get_update_submenu(item),
            )

        case 'delete':
            delete_item(item)

        case 'update_name':
            await callback.message.answer(
                text="Enter new name:",
            )
            await state.set_state(UpdateNameState.name)
            await state.update_data(name=item)

        case 'update_priority':
            await callback.message.answer(
                text="Enter new priority:",
            )
            await state.set_state(UpdatePriorityState.priority)
            await state.update_data(name=item)

        case 'update_deactivate':
            update_item(target='Active', name=item, new_value='0')
            await callback.message.answer(
                text=f'{item} is deactivated',
            )

@router.message(UpdateNameState.name)
async def update_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    update_item(target='Name', name=data['name'], new_value=message.text)
    await message.answer(
        text='Name is updated',
    )
    await state.clear()

@router.message(UpdatePriorityState.priority)
async def update_priority(message: types.Message, state: FSMContext):
    data = await state.get_data()
    update_item(target='Priority', name=data['name'], new_value=message.text)
    await message.answer(
        text='Priority is updated',
    )
    await state.clear()