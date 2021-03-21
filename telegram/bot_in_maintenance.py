import telebot
from telebot import types
import os
import gspread
import time
gc = gspread.service_account(filename='creds.json')
sheet = gc.open("sheetstest").sheet1
token = 'TOKEN'
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Выберите режим', reply_markup=keyboard())
@bot.message_handler(content_types=['text'])
def btnMenu(message):                                                                        # main menu
    if message.text == 'Поиск':
        msg = bot.send_message(message.chat.id, 'что ищем?', reply_markup=keyboard_searh())
        bot.register_next_step_handler(msg, btnMenu_search)
    if message.text == 'Поиск 2':
        msg = bot.send_message(message.chat.id, 'меню поиск2 включено ', reply_markup=keyboard())
        bot.register_next_step_handler(msg, poisk2)
    if message.text == 'Записать в базу':
        msg = bot.send_message(message.chat.id, 'меню записи включено ', reply_markup=keyboard())
        bot.register_next_step_handler(msg, write)
    if message.text == 'Создать':
        msg = bot.send_message(message.chat.id, 'создать файл', reply_markup=keyboard())
        bot.register_next_step_handler(msg, btnMenu)
@bot.message_handler(content_types=['text'])
def btnMenu_search(message):                                                                     # submenu
    if message.text == 'НКМ':
        msg = bot.send_message(message.chat.id, 'введите номер НКМ')
        bot.register_next_step_handler(msg, btnNKM)
    if message.text == 'Меню поиска':
        msg = bot.send_message(message.chat.id, 'что ищем?', reply_markup=keyboard_searh())
        bot.register_next_step_handler(msg, btnMenu_search)
    if message.text == 'Главное меню':
        msg = bot.send_message(message.chat.id, 'Выберите режим ', reply_markup=keyboard())
        bot.register_next_step_handler(msg, btnMenu)
@bot.message_handler(content_types=['text'])
def btnNKM(message):                                                                             # action
        sheet.update_acell('A2:', message.text)
        time.sleep(5)
        nodata = '#N/A'
        res = sheet.acell('B2').value
        if res == nodata:
            bot.send_message(message.chat.id, "нет данных", reply_markup=keyboard_searh())
        else:
            bot.send_message(message.chat.id, "найдено \n" + res, reply_markup=keyboard_searh())
        msg = bot.send_message(message.chat.id, 'что ищем?')
        bot.register_next_step_handler(msg, btnMenu_search)



@bot.message_handler(content_types=['text'])
def poisk2(message):
    c = sheet.find(message.text)
    (row, col) = (c.row, c.col)
    values_list = sheet.row_values(row)
    print(values_list)
    bot.send_message(message.chat.id, "найдено \n" + str(values_list)[1:-1], reply_markup=keyboard_searh())





def write(message):
    sheet.append_row([message.text])
def keyboard_searh():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('НКМ')
    btn2 = types.KeyboardButton('VIN')
    btn3 = types.KeyboardButton('Госномер')
    btn5 = types.KeyboardButton('Главное меню')
    markup.add(btn1, btn2, btn3, btn5)
    return markup
def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Поиск')
    btn2 = types.KeyboardButton('Поиск 2')
    btn3 = types.KeyboardButton('Записать в базу')
    btn4 = types.KeyboardButton('Создать')
    markup.add(btn1, btn2, btn3, btn4 )
    return markup
bot.polling()
