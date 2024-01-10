import asyncio
import logging

from aiogram import Bot, Dispatcher
from utils.config import BotConfig, DBConfig
from handlers import registration, time_logging
from utils.db import get_engine, proseed_schemas, session_maker

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(BotConfig.bot_token)
    dp = Dispatcher()

    dp.include_router(registration.router)
    dp.include_router(time_logging.router)

    async_ = get_engine(DBConfig.url)
    session = session_maker(async_.engine)
    await proseed_schemas(async_.engine)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db_pool=session)


if __name__ == "__main__":
    asyncio.run(main())


