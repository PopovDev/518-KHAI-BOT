from aiogram import Bot, Dispatcher, types
import asyncio
from handlers import start
import logging
from config import BOT_KEY


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_KEY)
    dp = Dispatcher()

    dp.include_router(start.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())