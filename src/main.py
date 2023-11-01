import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.config.config import load_config, Config
from src.handlers import handlers


logger = logging.getLogger(__name__)

config: Config = load_config()

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Start bot')

    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
