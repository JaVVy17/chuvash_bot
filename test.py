import sqlite3
import random
# import datetime
import time


cursor = None
connection = None

def init_bd():
    global connection, cursor
    try:
        print('DataBase was launched')
        with sqlite3.connect('DataBase.db') as connection:
            cursor = connection.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chuvash_words(
                id INTEGER PRIMARY KEY,
                chuvash TEXT NOT NULL
            )              
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS russian_words (
                id INTEGER PRIMARY KEY,
                russian TEXT NOT NULL
            )
                        
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS translations (
                russian_id INTEGER NOT NULL,
                chuvash_id INTEGER NOT NULL,
                PRIMARY KEY (russian_id, chuvash_id),
                FOREIGN KEY (russian_id) REFERENCES russian_words (id) ON DELETE CASCADE,
                FOREIGN KEY (chuvash_id) REFERENCES chuvash_words (id) ON DELETE CASCADE
            )           
            ''')
            connection.commit()
    except sqlite3.Error as e:
        print(f'Database error: {e}')
    
    except Exception as e:
        print(f'Error: {e}')

def get_random_word():
    try:
        table = random.choice(['chuvash','russian'])
        cursor.execute(f'SELECT {table} FROM {table}_words ORDER BY RANDOM() LIMIT 1') #f-строки в sql опасно!
        # if table == 'chuvash':
        #     cursor.execute('SELECT chuvash FROM chuvash_words ORDER BY RANDOM() LIMIT 1')
        # else:
        #     cursor.execute('SELECT russian FROM russian_words ORDER BY RANDOM() LIMIT 1')
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        
    except Exception as e:
        print(f'Error {e}')
        return False

def correct_word(random_word):
    try:
        cursor.execute('SELECT id FROM chuvash_words WHERE chuvash=?', (random_word,))
        chuvash_word_id = cursor.fetchone() 

        cursor.execute('SELECT id FROM russian_words WHERE russian=?', (random_word,))
        russian_word_id = cursor.fetchone() 
        
        if chuvash_word_id is not None:
            cursor.execute('''
                SELECT r.russian
                FROM russian_words r JOIN translations t
                on t.russian_id = r.id
                WHERE t.chuvash_id = ?''', (chuvash_word_id))

        elif russian_word_id is not None:
            cursor.execute('''
                SELECT c.chuvash
                FROM chuvash_words c JOIN translations t
                on t.chuvash_id = c.id
                WHERE t.russian_id = ?''', (russian_word_id))
        traslation_result = cursor.fetchone()
        return traslation_result[0] if traslation_result is not None else None

    except Exception as e:
        print(f'Error {e}')
        return False



def is_translation_correct(random_word, user_word):
    #почитать и узнать про [0] с fetch
    user_word = user_word.lower()
    try:
        # print(f"DEBUG: random_word='{random_word}', user_word='{user_word}'")
        cursor.execute('SELECT id FROM chuvash_words WHERE chuvash=?', (random_word,)) 
        chuvash_word_id = cursor.fetchone()

        cursor.execute('SELECT id FROM russian_words WHERE russian=?', (random_word,)) 
        russian_word_id = cursor.fetchone()

        if (chuvash_word_id is None and russian_word_id is None):
            return False
        

        if chuvash_word_id is not None:
            cursor.execute(f'SELECT id FROM russian_words WHERE russian="{user_word}" ') #есть какие то EXISTS #также это еще и небезопасный варик :/ почитать почему
            user_word_id = cursor.fetchone()

            if user_word_id is None:
                return False  # user_word не найден в русской таблице

            cursor.execute('SELECT * FROM translations WHERE chuvash_id=? AND russian_id=?', (chuvash_word_id[0],user_word_id[0],))


        elif russian_word_id is not None:
            cursor.execute(f'SELECT id FROM chuvash_words WHERE chuvash="{user_word}" ') #есть какие то EXISTS #также это еще и небезопасный варик :/ почитать почему
            user_word_id = cursor.fetchone()

            if user_word_id is None:
                return False 

            cursor.execute('SELECT * FROM translations WHERE chuvash_id=? AND russian_id=?', (user_word_id[0], russian_word_id[0],))

        result = cursor.fetchone()
        return bool(result)
    
    except Exception as e:
        print(f'Error {e}')
        return False


def print_rules():
    """Правила игры с красивым оформлением"""
    
    rules = [
        "📝 ПРАВИЛА ИГРЫ:",
        "🎲 Случайно выпадают слова на чувашском или русском",
        "💭 Твоя задача - написать перевод",
        "✅ За правильный ответ: +1 балл",
        "❌ За неправильный ответ: -1 балл",
        "🏆 Игра продолжается до выбранного тобой ",
        "🏆 количества правильных ответов:",
        "⏸️  Введи 'q', 'quit' или 'exit' чтобы выйти"
    ]
    

    for rule in rules:
        print(f"📌 {rule}")
    print()

def print_game_intro():
    """Красивое представление игры с эмодзи"""
    
    intro_messages = [
        "🎮 ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'ПЕРЕВОДЧИК'! 🎮",
        " Проверь свои знания чувашского и русского языков! ",
        "🚀 Готов к вызову? Начинаем! 🚀"
    ]
    
    print("✨" * 30)
    for message in intro_messages:
        print(f"✨ {message:^50} ✨")
    print("✨" * 30)
    print()
def print_game_over(final_score, target_score):
    """Сообщение об окончании игры"""
    
    print("\n" + "🎊" * 30)
    
    if final_score >= target_score:
        achievements = [
            f"🏆 ТЫ ПОБЕДИЛ! Набрано {final_score} из {target_score}!",
            f"🎯 ВЕЛИКОЛЕПНО! Цель достигнута: {final_score}/{target_score}",
            f"⭐ МАСТЕР ПЕРЕВОДА! {final_score} очков!"
        ]
        print(random.choice(achievements))
        print("🥇 Ты настоящий полиглот! 🥇")
        
    else:
        motivations = [
            f"💪 Не сдавайся! Набрано {final_score} из {target_score}",
            f"📚 Хорошая попытка! Попробуй еще раз!",
            f"🌱 Каждая ошибка - шаг к успеху!"
        ]
        print(random.choice(motivations))
    
    print("🎊" * 30)
    print("\nСпасибо за игру! Возвращайся скорее! 👋")

    
def print_score(current_score, target_score):
    """Красивое отображение счета"""
    progress = min(current_score / target_score * 100, 100) if target_score > 0 else 0
    
    print(f"\n⭐ ТВОЙ СЧЕТ: {current_score}/{target_score}")
    print(f"📊 Прогресс: [{ '█' * int(progress/5) }{ '░' * (20 - int(progress/5)) }] {progress:.1f}%")
    
    if current_score > 0:
        print(f"🎯 Осталось набрать: {max(0, target_score - current_score)} очков")
    print()    


def main():
    init_bd()
    print_game_intro()
    print_rules()


    target_score = int(input('До скольки правильных слов играем? :  '))
    current_score = 0 

    while current_score != target_score:
        time.sleep(2)
        print_score(current_score, target_score)
        random_word = get_random_word()
        user_word = input(f'Введите перевод для слова "{random_word}": ')


        if user_word in ('q', 'quit', 'exit'):
            break

        if is_translation_correct(random_word, user_word):
            print("✅ Правильно! Молодец! +1 балл")
            current_score += 1
            print(f"✅ Общий счет: {current_score}")
        else:
            print(f"❌ Неправильно. Правильный ответ: {correct_word(random_word)}")
            if current_score !=0: current_score -= 1
            print(f"❌ Общий счет: {current_score}")
            
    print_game_over(current_score, target_score)      




if __name__ == "__main__":
    main()







#Таймер мб
# режимы с чвш на рус, с рус на чвш
# Виды игры в обсидиане есть пример  
