import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers.user import user # type: ignore
from app.handlers.admin import admin

from config import TOKEN

from app.database.models import async_main


async def main():
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp = Dispatcher()
    dp.include_routers(user, admin)
    async def on_shutdown(dispatcher: Dispatcher):
        await dispatcher.storage.close()
        await dispatcher.storage.wait_closed()
        await dispatcher.shutdown()
        await dp.start_polling(bot)


async def on_startup(dispatcher: Dispatcher):
    await async_main()
    print('Starting up...')


async def on_shutdown(dispatcher: Dispatcher):
    print('Shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
