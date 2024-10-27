import telebot
from telebot import types
from telebot.types import WebAppInfo
import os
from dotenv import load_dotenv



load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

ALLOWED_USER_ID = 898641850
# ALLOWED_USER_ID = 490973300 # Лера
my_chat_id = ALLOWED_USER_ID

users = {}         # Словарь пользователей: {user_id: username}
blacklist = set()  # Список заблокированных пользователей


# Обработка ввода пользователя
@bot.message_handler()
def info(message):
    if message.text.lower() == '/start' or message.text.lower() == '/find_love':
        username = message.from_user.username or "Без имени пользователя"
        add_user(message.chat.id, username, message)
        print('Список пользователей:', users)

    elif message.text.lower() == '/help':
        help(message)
    
    elif message.text.lower() == '/user_list' and message.from_user.id == ALLOWED_USER_ID:
        list_users(message)

    elif message.text.lower() == '/blacklist' and message.from_user.id == ALLOWED_USER_ID:
        blacklist_users(message)
    
    elif  message.text.startswith('/remove_user') and message.from_user.id == ALLOWED_USER_ID:
        remove_user(message)
    
    elif message.text.startswith('/unblacklist') and message.from_user.id == ALLOWED_USER_ID:
        unblacklist_user(message)

    elif message.text.lower() == '/clear_users' and message.from_user.id == ALLOWED_USER_ID:
        clear_users(message)

    elif message.text.lower() == '/clear_blacklist' and message.from_user.id == ALLOWED_USER_ID:
        clear_blacklist(message)
   
    # elif message.text.lower() == '/id':
    #     #bot.send_message(message.chat.id, f'ID: {message.from_user.id}\nUsername: {message.from_user.username}')
    #     #bot.send_message(message.chat.id, message)
    
    elif message.from_user.id == ALLOWED_USER_ID:
        forward_message_to_all(message)

    else:
        bot.delete_message(message.chat.id, message.message_id)




# Добавление пользователя с проверкой черного списка
def add_user(user_id, username, message):
    if user_id in blacklist:
        bot.send_message(user_id, 'Доступ запрещен⛔️')
    else:
        users[user_id] = username.lower()
        hello(message)



# Приветствие
@bot.message_handler(commands=['start', 'find_love'])
def hello(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Найти свою судьбу', web_app= WebAppInfo(url= 'https://lizavetathorch.github.io/astro_love/')))
    
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



# Пересылка сообщения админа всем пользователям
def forward_message_to_all(message):
    for user_id in users:
        try:
            bot.copy_message(user_id, message.chat.id, message.message_id)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


# Просмотр списка всех пользвателей
@bot.message_handler(commands=['user_list'])
def list_users(message):
    if users:
        users_list = []

        for user_id in users:
            user_info = bot.get_chat(user_id)
            username = user_info.username if user_info.username else "Без имени пользователя"
            users_list.append(f"ID: {user_id}, Username: @{username}")
        
        
        users_list_text = "\n".join(users_list)
        bot.send_message(message.chat.id, f"Список всех пользователей:\n\n{users_list_text}")
    
    else:
        bot.send_message(message.chat.id, "Список пользователей пуст")




# Очистка списка пользователей (только для админа)
@bot.message_handler(commands=['clear_users'])
def clear_users(message):
    users.clear()
    bot.send_message(message.chat.id, 'Список пользователей пуст 🧹')



# Удаление пользователя по username или user_id (только для админа)
@bot.message_handler(commands=['remove_user'])
def remove_user(message):
    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.send_message(message.chat.id, "Пожалуйста, используйте команду в формате /remove_user <username или user_id>")
        return

    identifier = command_parts[1].lower()

    user_id_to_remove = None

    if identifier.isdigit():
        user_id_to_remove = int(identifier) if int(identifier) in users else None
    else:
        user_id_to_remove = next((user_id for user_id, user_username in users.items() if user_username == identifier), None)

    if user_id_to_remove is not None:
        blacklist.add(user_id_to_remove)
        del users[user_id_to_remove]
        bot.send_message(message.chat.id, f"Пользователь @{identifier} удален и добавлен в черный список")
    else:
        bot.send_message(message.chat.id, f"Пользователь @{identifier} не найден")


########################################################################################################################################################
#
# BLACKLIST
########################################################################################################################################################


# Просмотр черного списка
@bot.message_handler(commands=['blacklist'])
def blacklist_users(message):
    if blacklist:
        users_blacklist = []

        for user_id in blacklist:
            user_info = bot.get_chat(user_id)
            username = user_info.username if user_info.username else "Без имени пользователя"
            users_blacklist.append(f"ID: {user_id}, Username: @{username}")
        
        
        users_blacklist_text = "\n".join(users_blacklist)
        bot.send_message(message.chat.id, f"Список пользователей черного списка:\n\n{users_blacklist_text}")
    
    else:
        bot.send_message(message.chat.id, "Список пользователей пуст")



# Удаление пользователя из черного списка (только для админа)
@bot.message_handler(commands=['unblacklist'])
def unblacklist_user(message):
    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.send_message(message.chat.id, "Пожалуйста, используйте команду в формате /unblacklist <user_id>")
        return

    user_id_to_unblock = int(command_parts[1])  # Предполагаем, что ID передается в формате числа

    if user_id_to_unblock in blacklist:
        blacklist.remove(user_id_to_unblock)  # Удаляем пользователя из черного списка

        # Получаем username, если он есть
        username = users.get(user_id_to_unblock, "Без имени пользователя")
        users[user_id_to_unblock] = username  # Добавляем пользователя обратно в users

        bot.send_message(message.chat.id, f"Пользователь с ID {user_id_to_unblock} был удален из черного списка и возвращен в список пользователей")
    else:
        bot.send_message(message.chat.id, f"Пользователь с ID {user_id_to_unblock} не найден в черном списке")



# Очистка черного списка (только для админа)
@bot.message_handler(commands=['clear_blacklist'])
def clear_blacklist(message):
    blacklist.clear()
    bot.send_message(message.chat.id, 'Черный список пуст 🧹')




bot.infinity_polling()
