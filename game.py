from database import init_bd, get_random_word, is_translation_correct, correct_word
import random
import time


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


def start_game():
    """Запуск консольной версии игры"""
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