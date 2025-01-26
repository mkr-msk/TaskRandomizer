from aiogram import Router, types, F

from DBOperator import *
from Keyboards import *

router = Router()

# Обработка show меню элемента
@router.callback_query(F.data.startswith("show_"))
async def callback_show(callback: types.CallbackQuery):
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
            pass # диалог с пользователем

        case 'update_priority':
            pass # диалог с пользователем

        case 'update_deactivate':
            update_item(target='Active', name=item, new_value='0')
            await callback.message.answer(
                text=f'{item} is deactivated',
            )