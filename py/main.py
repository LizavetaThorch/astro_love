import telebot
from telebot import types

bot = telebot.TeleBot('7566850087:AAFv7vWuzj60esH234Lx16Ox9-okcYH9fnY')

# Обработка ввода пользователя
@bot.message_handler()
def info(message):
    if message.text.lower() == '/start':
        hello(message)
    elif message.text.lower() == '/help':
        help(message)
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 
                        f'<b>{message.from_user.first_name}, добро пожаловать в Astro Love</b>✨\n\n Это место, где матрицы и нумерология соединяют людей, создавая глубокие и осознанные связи. Здесь звёзды и числа раскрывают совместимость и помогают найти свою истинную любовь.\nКаждый профиль проходит тщательную проверку, чтобы каждая встреча приносила настоящий, неповторимый опыт.',
                        parse_mode='HTML'
                        )
    else:
        bot.send_message(message.chat.id, 'Неверный ввод')
        # bot.delete_message(message.chat.id, message.message_id)
        

# Приветствие
@bot.message_handler(commands=['start'])
def hello(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Открой приложение', url= 'https://lordfilmhd.homes/tvshows/судья-из-ада-2024/#player1'))
    
    bot.send_message(message.chat.id, 
                        f'<b>{message.from_user.first_name}, добро пожаловать в Astro Love</b>✨\n\n Это место, где матрицы и нумерология соединяют людей, создавая глубокие и осознанные связи. Здесь звёзды и числа раскрывают совместимость и помогают найти свою истинную любовь.\nКаждый профиль проходит тщательную проверку, чтобы каждая встреча приносила настоящий, неповторимый опыт.',
                        parse_mode='HTML', reply_markup= markup
                    )

# Обращение в поддержку
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Если что-то поломалось пишите @EllabetDce')



# bot.polling(non_stop=True)
bot.infinity_polling()
 