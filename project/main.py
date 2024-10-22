import telebot
from telebot import types
from telebot.types import WebAppInfo
import os
from dotenv import load_dotenv

# # Загрузка переменных окружения из файла .env
load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

ALLOWED_USER_ID = 898641850
my_chat_id = ALLOWED_USER_ID

# Список всех пользователей
users = set()

# Обработка ввода пользователя
@bot.message_handler()
def info(message):
    if message.text.lower() == '/start' or message.text.lower() == '/find_love' :
        hello(message)
        users.add(message.chat.id)
    elif message.text.lower() == '/help':
        help(message)
    elif message.text.lower() == '/clear_users' and message.from_user.id == ALLOWED_USER_ID:
        clear_users(message)
    elif message.text.lower() == '/id':
        # ID и username Леры
        bot.send_message(message.chat.id, f'ID: {message.from_user.id}\nUsername: {message.from_user.username}')
    elif message.from_user.id == ALLOWED_USER_ID:
        forward_message_to_all(message)
    else:
        bot.send_message(message.chat.id, 'Неверный ввод')
        # bot.delete_message(message.chat.id, message.message_id)
        

# Приветствие
@bot.message_handler(commands=['start', 'find_love'])
def hello(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Найти свою судьбу', web_app= WebAppInfo(url= 'https://tvoyamatritsa.ru/')))
    
    photo = open('./photo/Astrology.jpg', 'rb')
    bot.send_photo ( message.chat.id, photo, 
                      f'<b>{message.from_user.first_name}, добро пожаловать в Astro Love</b>✨\n\n Это место, где матрицы и нумерология соединяют людей, создавая глубокие и осознанные связи. Здесь звёзды и числа раскрывают совместимость и помогают найти свою истинную любовь.\nКаждый профиль проходит тщательную проверку, чтобы каждая встреча приносила настоящий, неповторимый опыт.',
                      parse_mode='HTML', reply_markup= markup 
                    )
    photo.close()


# Обращение в поддержку
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'По вем вопросом пишите @heroineVM\nА если что-то поломалось пишите @EllabetDce')


# Обработчик сообщений с файлами (фото, видео и т.д.)
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio', 'sticker', 'voice', 'video_note', 'location', 'contact'])
def handle_non_text_messages(message):
    if message.from_user.id == ALLOWED_USER_ID:
        forward_message_to_all(message)

    else:
        bot.send_message(message.chat.id, 'Пожалуйста, не отправляйте файлы')
        bot.delete_message(message.chat.id, message.message_id)

# Функция для пересылки сообщения админа всем пользователям
def forward_message_to_all(message):
    for user_id in users:
        try:
            bot.copy_message(user_id, message.chat.id, message.message_id)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


# Функция для очистки списка пользователей (только для админа)
def clear_users(message):
    users.clear()
    bot.send_message(message.chat.id, 'Список пользователей был успешно очищен 🧹')




bot.infinity_polling()
