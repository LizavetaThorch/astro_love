import telebot
from telebot import types
import os
from dotenv import load_dotenv

# # Загрузка переменных окружения из файла .env
load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

# Обработка ввода пользователя
@bot.message_handler()
def info(message):
    if message.text.lower() == '/start':
        hello(message)
    elif message.text.lower() == '/help':
        help(message)
    elif message.text.lower() == 'привет':
        hello(message)
    elif message.text.lower() == '/id':
        # ID и username Леры
        bot.send_message(message.chat.id, f'ID: {message.from_user.id}\nUsername: {message.from_user.username}')
    else:
        bot.send_message(message.chat.id, 'Неверный ввод')
        # bot.delete_message(message.chat.id, message.message_id)
        

# Приветствие
@bot.message_handler(commands=['start'])
def hello(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Найти свою судьбу', url= 'https://lordfilmhd.homes/tvshows/судья-из-ада-2024/#player1'))
    
    photo = open('./photo/Astrology.jpg', 'rb')
    bot.send_photo ( message.chat.id, photo, 
                      f'<b>{message.from_user.first_name}, добро пожаловать в Astro Love</b>✨\n\n Это место, где матрицы и нумерология соединяют людей, создавая глубокие и осознанные связи. Здесь звёзды и числа раскрывают совместимость и помогают найти свою истинную любовь.\nКаждый профиль проходит тщательную проверку, чтобы каждая встреча приносила настоящий, неповторимый опыт.',
                      parse_mode='HTML', reply_markup= markup 
                    )


# Обращение в поддержку
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'По вем вопросом пишите @heroineVM\nА если что-то поломалось пишите @EllabetDce')


# Обработчик сообщений с файлами (фото, видео и т.д.)
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio', 'sticker', 'voice', 'video_note', 'location', 'contact'])
def handle_non_text_messages(message):
    bot.send_message(message.chat.id, 'Пожалуйста, не отправляйте файлы')
    bot.delete_message(message.chat.id, message.message_id)
    hello(message)



# bot.polling(non_stop=True)
bot.infinity_polling()
 