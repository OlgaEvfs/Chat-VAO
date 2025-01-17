import sqlite3

def get_answer_from_db(question):
    try:
        # Подключаемся к базе данных
        connection = sqlite3.connect('faq.db')
        cursor = connection.cursor()

        # Ищем ответ в базе
        cursor.execute("""
                       SELECT id, question, answer FROM questions_answers WHERE question = ?
                       """, (question,))
        result = cursor.fetchone() # Получаем первую строку результа

        connection.close() # Закрываем соединение с базой

        if result:
            return result # Если ответ найден, возвращаем его иначе сообщение о том, где можно искать ответ
        else:
            return None
    except Exception as e:
        return f"Произошла ошибка при подключении к базе данных:{str(e)} "
 
def add_question_and_answer(question, answer):
    try:
        # Подключаемся к базе данных
        connection = sqlite3.connect('faq.db')
        cursor = connection.cursor()

        # Добавляем новый вопрос и ответ в базу данных
        cursor.execute("""INSERT INTO questions_answers (question, answer) VALUES (?, ?)""", (question, answer))

        # Сохраняем изменения
        connection.commit()

        connection.close()  # Закрываем соединение с базой
        return "Ваш вопрос и ответ успешно добавлены в базу данных!"
    except Exception as e:
        return f"Произошла ошибка при добавлении данных: {str(e)}"

# Функция для обновления вопроса
def update_question(question_id, new_question):
    try:
        # Подключаемся к базе данных
        connection = sqlite3.connect('faq.db')
        cursor = connection.cursor()

        # Обновляем вопрос
        cursor.execute("""UPDATE questions_answers SET question = ? WHERE id = ?""", (new_question, question_id))

        # Сохраняем изменения
        connection.commit()

        connection.close()  # Закрываем соединение с базой
        return "Вопрос успешно обновлен!"
    except Exception as e:
        return f"Произошла ошибка при обновлении вопроса: {str(e)}"

# Функция для обновления ответа
def update_answer(question_id, new_answer):
    try:
        # Подключаемся к базе данных
        connection = sqlite3.connect('faq.db')
        cursor = connection.cursor()

        # Обновляем ответ
        cursor.execute("""UPDATE questions_answers SET answer = ? WHERE id = ?""", (new_answer, question_id))

        # Сохраняем изменения
        connection.commit()

        connection.close()  # Закрываем соединение с базой
        return "Ответ успешно обновлен!"
    except Exception as e:
        return f"Произошла ошибка при обновлении ответа: {str(e)}"
    
def chat_bot():

    # Ввод пользователя
    print("Бот: Привет! Задайте вопрос. Напишите 'выход', чтобы завершить.")

    while True:
        question = input('Вы: ').strip()
        
        # Проверяем на завершение чата
        if question.lower() in ('выход', 'exit', 'quit'): # Завершаем работу, если пользователь пишет 'выход'
            print("Бот: До свидания!")
            break

        # Получаем ответ из базы данных
        result = get_answer_from_db(question)

        if result:
            question_id, existing_question, answer = result
            print(f'Бот: Вопрос: "{existing_question}"\nОтвет: {answer}')

            # Предлагаем редактировать ответ, вопрос или оба
            edit_choice = input("Бот: Хотите изменить вопрос, ответ или оба? (вопрос/ответ/оба/нет): ").strip().lower()
            
            if edit_choice == 'вопрос':
                new_question = input("Бот: Введите новый вопрос: ").strip()
                update_confirmation = update_question(question_id, new_question)
                print(f'Бот: {update_confirmation}')
            elif edit_choice == 'ответ':
                new_answer = input("Бот: Введите новый ответ: ").strip()
                update_confirmation = update_answer(question_id, new_answer)
                print(f'Бот: {update_confirmation}')
            elif edit_choice == 'оба':
                new_question = input("Бот: Введите новый вопрос: ").strip()
                new_answer = input("Бот: Введите новый ответ: ").strip()
                update_question_confirmation = update_question(question_id, new_question)
                update_answer_confirmation = update_answer(question_id, new_answer)
                print(f'Бот: {update_question_confirmation}')
                print(f'Бот: {update_answer_confirmation}')
        else:
            print("Бот: Извините, я не нашел ответа на ваш вопрос.")
            add_new = input("Бот: Хотите добавить новый вопрос и ответ? (да/нет): ").strip().lower()
            if add_new == 'да':
                new_question = input("Бот: Введите новый вопрос: ").strip()
                new_answer = input("Бот: Введите ответ на этот вопрос: ").strip()
                add_confirmation = add_question_and_answer(new_question, new_answer)
                print(f'Бот: {add_confirmation}')

# Запуск бота
if __name__ == "__main__":
    chat_bot()