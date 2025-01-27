# Version 2.5.1

import asyncio
import logging
from aiogram import Bot, Dispatcher

from DBOperator import get_token
from Handlers import MainHandlers, Add_activity
from Callbacks import MainCallbacks

async def main():
    bot = Bot(token=get_token())
    dp = Dispatcher()

    dp.include_routers(
        MainHandlers.router,
        Add_activity.router,
        MainCallbacks.router
    )

    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())