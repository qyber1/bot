import asyncio
import logging

from create_bot import bot, dp
from handlers import client
from config import db_login,db_pass, db_host, db_name

from db.engine import create_asyncengine, proseed_schemas, session_maker





logging.basicConfig(level=logging.INFO)




url =f'postgresql+asyncpg://{db_login}:{db_pass}@localhost:{db_host}/{db_name}'

async def main():

    dp.include_router(client.router)

    async_engine = create_asyncengine(url)
    session = session_maker(async_engine)
    await proseed_schemas(async_engine)


    await dp.start_polling(bot, db_pool = session)


if __name__ == "__main__":
    asyncio.run(main())