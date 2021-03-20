import asyncio
from datetime import date
print("Copyright (c) 2016 - %d | Dmitrii Voronchikhin " % date.today().year)
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.config_reader import load_config
from app.handlers.anketa import register_handlers_anketa

logger = logging.getLogger(__name__)

async def set_commands(bot: Bot):
    commands = [BotCommand(command="/start", description="Запустить бота"),
                BotCommand(command="/anketa", description="Заполнить анкету"),
                BotCommand(command="/cancel", description="Отменить действие")]
    await bot.set_my_commands(commands)


async def main():
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    config = load_config("config/bot.ini")

    
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    
    register_handlers_anketa(dp)

   
    await set_commands(bot)

    
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())

