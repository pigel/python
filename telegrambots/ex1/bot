import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

# sti in config file
    sti = open('sticker.webp', 'rb')		
    bot.send_sticker(message.chat.id, config.sti)
    bot.send_message(message.chat.id, "Hello")
	
# cycling
bot.polling(none_stop=True)
