# Version 2.4.3

import asyncio
import logging
from aiogram import Bot, Dispatcher

from DBOperator import get_token
import Handlers, Callbacks

async def main():
    bot = Bot(token=get_token())
    dp = Dispatcher()

    dp.include_routers(Handlers.router, Callbacks.router)

    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())