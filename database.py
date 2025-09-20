import sqlite3
import random


def init_bd():
    try:
        print('DataBase was launched')
        with sqlite3.connect('database/DataBase.db') as connection:
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
        with sqlite3.connect('database/DataBase.db') as connection:
            cursor = connection.cursor()
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
        with sqlite3.connect('database/DataBase.db') as connection:
            cursor = connection.cursor()
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
        with sqlite3.connect('database/DataBase.db') as connection:
            cursor = connection.cursor()
            # print(f"DEBUG: random_word='{random_word}', user_word='{user_word}'")
            cursor.execute('SELECT id FROM chuvash_words WHERE chuvash=?', (random_word,)) 
            chuvash_word_id = cursor.fetchone()

            cursor.execute('SELECT id FROM russian_words WHERE russian=?', (random_word,)) 
            russian_word_id = cursor.fetchone()

            if (chuvash_word_id is None and russian_word_id is None):
                return False
            

            if chuvash_word_id is not None:
                # cursor.execute(f'SELECT id FROM russian_words WHERE russian="{user_word}" ') #есть какие то EXISTS #также это еще и небезопасный варик :/ почитать почему
                cursor.execute('SELECT id FROM russian_words WHERE russian=?', (user_word,))
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