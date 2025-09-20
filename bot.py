import telebot
from telebot import types #для клавиатуры и кнопок
from config import BOT_TOKEN
from database import init_bd, get_random_word, correct_word, is_translation_correct
from game import print_rules, print_score


bot = telebot.TeleBot(BOT_TOKEN)
init_bd()

users_states = {}

keyboard = types.ReplyKeyboardMarkup(row_width=4)
button_rule = types.KeyboardButton('/home')
button_play = types.KeyboardButton('/play')
keyboard.add(button_rule, button_play)

@bot.message_handler(commands=['start', 'home'])
def start_bot(message):
    user_id = message.from_user.id
    if user_id in users_states:
        del users_states[user_id]
    bot.send_message(message.chat.id, print_rules(), reply_markup=keyboard, parse_mode='Markdown')



@bot.message_handler(commands=['play'])
def start_game(message):
    user_id = message.from_user.id
    users_states[user_id] = {
        'random_word': get_random_word(),
        'target_score': 10,
        'current_score': 0
   }
    bot.send_message(message.chat.id, f"Введите перевод для слова: {users_states[message.from_user.id]['random_word']}")



@bot.message_handler(func=lambda message: True)
def handle_message(message):

    user_id = message.from_user.id


    if user_id in users_states:
        random_word = users_states[user_id]['random_word']
        target_score = users_states[user_id]['target_score']
        current_score = users_states[user_id]['current_score']

        user_answer = message.text
        if is_translation_correct(random_word, user_answer):
            if current_score != target_score:
                users_states[user_id]['current_score'] += 1
                current_score = users_states[user_id]['current_score']

            bot.send_message(message.chat.id, 
                           f"✅ <b>Правильно!</b> +1 балл!\n{print_score(current_score, target_score)}", 
                           parse_mode='HTML')

        else:
            if current_score != 0:
                users_states[user_id]['current_score'] -= 1
                current_score = users_states[user_id]['current_score']
            bot.send_message(message.chat.id,
                           f"❌ <b>Неправильно!</b> Правильное слово: {correct_word(random_word)}\n{print_score(current_score, target_score)}",
                           parse_mode='HTML')

        
        if current_score != target_score:
            users_states[user_id]['random_word'] = get_random_word()
            new_random_word = users_states[user_id]['random_word']
            bot.send_message(message.chat.id, 
                           f"📝 <b>Введите перевод для слова:</b>\n<code>{new_random_word}</code>", 
                           parse_mode='HTML')
        else:
            bot.send_message(message.chat.id,
                           f"🎉 <b>Поздравляю! Ты победил!</b>\n",reply_markup=keyboard,
                           parse_mode='HTML')
            del users_states[user_id]
            return


    else:
        bot.send_message(message.chat.id, "Запустите игру командой /play ")


@bot.message_handler(content_types=['sticker'])
def echo(message):
    users_stick = message.sticker.file_id
    bot.send_sticker(message.chat.id,'CAACAgEAAxkBAAEBl4xoxtFa5kq0soHOe8tzPCYCeF6nVgACcAADToKJEJ6tLxE2XYGrNgQ') 
    # bot.send_sticker(message.chat.id, users_stick) 

bot.polling(none_stop=True)

