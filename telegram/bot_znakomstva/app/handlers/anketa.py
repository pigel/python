from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.config_reader import load_config
from aiogram.dispatcher.filters import Text
from aiogram import Bot

config = load_config("config/bot.ini")
bot = Bot(token=config.tg_bot.token)

first_action = ["создать анкету", "отменить"]
gender = ["девушку", "парня", "кого нибудь"]
action = ["отправить", "отменить"]


class userVal(StatesGroup):
    pic_state = State()
    name_state = State()
    age_state = State()
    adr_state = State()
    desc_state = State()
    whom_state = State()


async def start_enter(message: types.Message):
    await message.answer("Выберите фото профиля", reply_markup=types.ReplyKeyboardRemove())
    await userVal.pic_state.set()


async def pic_entered(message: types.Message, state: FSMContext):

    await state.update_data(pic=message.photo[2].file_id)
    await userVal.next()
    await message.answer("Ваше имя ?" )


async def name_entered(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await userVal.next()
    await message.answer("Возраст ?")


async def age_entered(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)

    if not message.text.isdigit():

        await message.answer("Пожалуйста, введите возраст")
        return

    await userVal.next()
    await message.answer("Город ?")


async def adr_entered(message: types.Message, state: FSMContext):
    await state.update_data(adr=message.text)
    await userVal.next()
    await message.answer("Опишите себя ")


async def desc_entered(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for sex in gender:
        keyboard.add(sex)
    await userVal.next()
    await message.answer("Кого бы хотели найти ?", reply_markup=keyboard)


async def whom_entered(message: types.Message, state: FSMContext):
    await state.update_data(whom=message.text)
    if message.text not in gender:
        await message.answer("Пожалуйста, выберите, кого Вы ищете")
        return
    username = message.from_user.username
    await message.answer(message.from_user.first_name + ", пожалуйста проверьте анкету перед отправкой", reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()
    ###
    userpic = user_data['pic']
    await bot.send_photo(message.chat.id, caption=
        f"Имя:  {user_data['name']}\n"
        f"Возраст: {user_data['age']}\n"
        f"Город: {user_data['adr']}\n"
        f"О себе: {user_data['desc']}\n"
        f"Хочу найти: {user_data['whom']}\n"
        f"Контакты:  @{username}", photo=userpic)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for act in action:
        keyboard.add(act)

    channel = '@XXXXXXX'
    await message.answer(f"Готово к публикации в канал {channel}", reply_markup=keyboard)
    await userVal.next()


async def cmd_go(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    chat = '-XXXXXXXXXX'
    userpic = user_data['pic']
    await bot.send_photo(chat_id=chat, caption=
    f"Имя:  {user_data['name']}\n"
    f"Возраст: {user_data['age']}\n"
    f"Город: {user_data['adr']}\n"
    f"О себе: {user_data['desc']}\n"
    f"Хочу найти: {user_data['whom']}\n"
    f"Контакты:  @{message.from_user.username}", photo=userpic)
    await message.answer("Ваша анкета отправлена", reply_markup=types.ReplyKeyboardRemove())


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for btns in first_action:
        keyboard.add(btns)

    user = message.from_user.first_name
    await message.answer(user + ", для заполнения воспользуйтесь меню", reply_markup=keyboard)


def register_handlers_anketa(dp: Dispatcher):

    dp.register_message_handler(start_enter, Text(equals="создать анкету", ignore_case=True), state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отменить", ignore_case=True), state="*")
    dp.register_message_handler(cmd_go, Text(equals="отправить", ignore_case=True), state="*")

    dp.register_message_handler(pic_entered, state=userVal.pic_state, content_types=['photo'])
    dp.register_message_handler(name_entered, state=userVal.name_state)
    dp.register_message_handler(age_entered, state=userVal.age_state)
    dp.register_message_handler(adr_entered, state=userVal.adr_state)
    dp.register_message_handler(desc_entered, state=userVal.desc_state)
    dp.register_message_handler(whom_entered, state=userVal.whom_state)

    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(start_enter, commands="anketa", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
