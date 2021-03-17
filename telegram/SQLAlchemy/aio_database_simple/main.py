import os
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types.base import String
from aiogram.utils import executor
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import DB_FILENAME
from config import TOKEN
from db_map import Data, Base

logging.basicConfig(level=logging.INFO)

engine = create_engine(f'sqlite:///{DB_FILENAME}')

if not os.path.isfile(f'./{DB_FILENAME}'):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

bot = Bot(token= TOKEN)
dp = Dispatcher(bot)

date = datetime.datetime.today().strftime("%d.%m.%Y")
time = datetime.datetime.today().strftime("%H.%M.%S")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):

    chat_id = message.chat.id
    first_name: String = message.chat.first_name
    username: String = message.chat.username

    session = Session()
    newt = Data(date=date, time=time, chat_id=chat_id, first_name=first_name, username=username)
    session.add(newt)
    session.commit()
    session.close()

    await bot.send_message(message.chat.id, 'hello ' + message.chat.first_name)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
