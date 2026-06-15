import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import BOT_TOKEN
from bot.db.setup import init_db
from bot.handlers.start import router as start_router
from bot.handlers.menu import router as menu_router
from bot.handlers.navigation import router as nav_router
from bot.handlers.generate import router as gen_router
from bot.handlers.donate import router as donate_router
from data.seed import seed_db


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(nav_router)
    dp.include_router(gen_router)
    dp.include_router(donate_router)

    await init_db()
    await seed_db()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
