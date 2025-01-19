#Version 2.0.0 Telegram Bot

from DBOperator import *
from RandomElementSelector import *
from Elements import *

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def next(upd: Update, context: ContextTypes.DEFAULT_TYPE):
    elements = []

    for row in get_all_items():
        elements.append(Element(row[0], row[1], row[2]))

    msg = choose_random_element(elements)

    await context.bot.send_message(
        chat_id=upd.effective_chat.id,
        text=msg
    )


async def show(upd: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ""
    for row in get_all_items('sorted'):
        msg += f'{row[0]:15} {row[1]} / {row[2]}' + '\n'

    await context.bot.send_message(
        chat_id=upd.effective_chat.id,
        text=msg
    )


async def add(upd: Update, context: ContextTypes.DEFAULT_TYPE):
    e = Element()

    e.name = input('name = ')
    e.priority = input('priority = ')
    e.active = input('active = ')

    add_item(e)


async def update(upd: Update, context: ContextTypes.DEFAULT_TYPE):
    target = input('target = ')

    if target == 'Default':
        update_item(target)

    else:
        name = input('name contains > ')
        new_value = input('new value = ')
        update_item(target, name, new_value)


async def delete(upd: Update, context: ContextTypes.DEFAULT_TYPE):
    name = input('name contains > ')

    delete_item(name)


if __name__ == '__main__':
    application = ApplicationBuilder().token('7773844836:AAHNvyJc1updfK-ND1xpGmEOHBPe73ShirM').build()

    start_handler = CommandHandler('next', next)
    application.add_handler(start_handler)

    start_handler = CommandHandler('show', show)
    application.add_handler(start_handler)

    start_handler = CommandHandler('add', add)
    application.add_handler(start_handler)

    start_handler = CommandHandler('update', update)
    application.add_handler(start_handler)

    start_handler = CommandHandler('delete', delete)
    application.add_handler(start_handler)

    application.run_polling()