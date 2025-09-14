import telebot
from telebot import types #для клавиатуры и кнопок
from config import BOT_TOKEN
from database import init_bd, get_random_word, correct_word, is_translation_correct
from game import print_rules


bot = telebot.TeleBot(BOT_TOKEN)
init_bd()

users_word = {}

@bot.message_handler(commands=['start', 'home'])
def start_bot(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=4)
    button_rule = types.KeyboardButton('/home')
    button_play = types.KeyboardButton('/play')
    keyboard.add(button_rule, button_play)

    bot.send_message(message.chat.id, print_rules(), reply_markup=keyboard, parse_mode='Markdown')


@bot.message_handler(commands=['play'])
def start_game(message):
    random_word = get_random_word()
    users_word[message.from_user.id] = random_word
    print(users_word)
    bot.send_message(message.chat.id, f"Переведи слово:\t{random_word}" )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in users_word:
        bot.reply_to(message, "Нажмите 'play' чтобы начать играть!")
        return
    

    user_answer = message.text
    random_word = users_word[user_id]

    if is_translation_correct(random_word, user_answer):
        bot.send_message(message.chat.id, "✅ Правильно! Молодец!")
    else:
        bot.send_message(message.chat.id, f"❌ Неправильно. Правильный ответ: {correct_word(random_word)}")

    new_random_word = get_random_word()
    users_word[message.from_user.id] = new_random_word
    bot.send_message(message.chat.id, f"🎲 Следующее слово: *{new_random_word}*", parse_mode='Markdown')





@bot.message_handler(content_types=['sticker'])
def echo(message):
    users_stick = message.sticker.file_id
    bot.send_sticker(message.chat.id,'CAACAgEAAxkBAAEBl4xoxtFa5kq0soHOe8tzPCYCeF6nVgACcAADToKJEJ6tLxE2XYGrNgQ') 
    # bot.send_sticker(message.chat.id, users_stick) 

bot.polling(none_stop=True)

