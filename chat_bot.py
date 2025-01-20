import sqlite3
import spacy


nlp = spacy.load('ru_core_news_sm') # модель для русского языка

def find_similar_question(question): # функция для поиска схожих ответов
    question_doc = nlp(question) # преобразует в Doc для читабельности
    connection = sqlite3.connect('faq.db') # подключение к базе данных
    cursor = connection.cursor() # создает cursor для выполнения запросами из базы данных
    cursor.execute("SELECT id, question FROM questions_answers") # нахождение всех вопросов в базе данных
    rows = cursor.fetchall() # сохраняет все строки в список rows, каждая строка кортеж с ключом и значением
    most_similar_question = None # предотвращает ошибки, если переменная не установлена на конкретный вопрос, но если найдется похожий, то в дальнейшем будет обновлена
    highest_similarity = 0 # используется для нахождения наибольшей схожести

    for row in rows: # цикл к.т перебирает вопросы и ответы
        db_question = row[1] # извлекает элемент из кортежа, к.т является вопросом из базы данных
        db_question_doc = nlp(db_question) # преобразует в Doc для читабельности
        similarity = question_doc.similarity(db_question_doc) # преобразуем вопрос из базы данных в Doc, чтобы работать с ним, как с текстом в spacy

        if similarity > highest_similarity: # если текущая схожесть больше, чем наибольшая найденная до этого, то обновляем переменные
            highest_similarity = similarity # обновляем наибольшую схожесть
            most_similar_question = row # обновляем наибольшую схожесть

    connection.close()

    if most_similar_question and highest_similarity > 0.7:  # Порог схожести
        return most_similar_question # возврвщает наиболее подходящий вопрос
    else:
        return None # если схожий вопрос не найден

def get_answer_from_db(question): # получение ответа
    try:
        connection = sqlite3.connect('faq.db') # Подключаемся к базе данных
        cursor = connection.cursor() # для SQL запросов

        
        cursor.execute("""
                       SELECT id, question, answer FROM questions_answers WHERE question = ?
                       """, (question,)) #  Ищем ответ в базе
        result = cursor.fetchone() # Получаем первый результат

        connection.close() # Закрываем соединение с базой

        if result: # result это кортеж с ключом и значением
            return result # Если ответ найден, возвращаем его
        else:
            similar_question = find_similar_question(question) # Если точного ответа нет, ищем похожий вопрос в функции выше
            if similar_question:
                question_id, existing_question = similar_question 
                cursor.execute("SELECT answer FROM questions_answers WHERE id = ?", (question_id,))
                similar_answer = cursor.fetchone()
                return question_id, existing_question, similar_answer[0] 
            else:
                return None # если не найден вопрос возвращаем none
    except Exception as e:
        return f"Произошла ошибка при подключении к базе данных:{str(e)} "
 
def add_question_and_answer(question, answer):
    try:
        connection = sqlite3.connect('faq.db') # Подключаемся к базе данных
        cursor = connection.cursor()

        
        cursor.execute("SELECT 1 FROM questions_answers WHERE question = ?", (question,)) # Проверяет, есть ли такой вопрос
        existing_question = cursor.fetchone()

        if existing_question:
            connection.close()
            return "Такой вопрос уже есть."

        cursor.execute("""INSERT INTO questions_answers (question, answer) VALUES (?, ?)""", (question, answer)) # Добавляем новый вопрос и ответ в базу данных

        connection.commit() # Сохраняем изменения

        connection.close()  # Закрываем соединение с базой
        return "Ваш вопрос и ответ успешно добавлены в базу данных!"
    except Exception as e:
        return f"Произошла ошибка при добавлении данных: {str(e)}"
    
def chat_bot():

    # Ввод пользователя
    print("Бот: Привет! Задайте вопрос. Напишите 'выход', чтобы завершить.")

    while True:
        question = input('Вы: ').strip() # считывает ввод пользователя, strip удаляет лишние пробелы в строке 
        
        # Проверяем на завершение чата
        if question.lower() in ('выход', 'exit', 'quit'): # Завершаем работу, если пользователь пишет 'выход'
            print("Бот: До свидания!")
            break

        result = get_answer_from_db(question)  # Получаем ответ из базы данных

        if result:
            if result[2]:  # Если найден ответ
                print(f"Бот: Ответ: {result[2]}")
            else:  # Если найден похожий вопрос
                print(f"Бот: Похожий вопрос: '{result[1]}'\nОтвет: {result[2]}")  
        else:
            print("Бот: Извините, я не нашел ответа на ваш вопрос.")
            add_new = input("Бот: Хотите добавить новый вопрос и ответ? (да/нет): ").strip().lower()
            if add_new == 'да':
                new_question = input("Бот: Введите новый вопрос: ").strip()
                new_answer = input("Бот: Введите ответ на этот вопрос: ").strip()
                add_confirmation = add_question_and_answer(new_question, new_answer)
                print(f'Бот: {add_confirmation}')

# Запуск бота
if __name__ == "__main__": # гарантирует, что функция chat_bot будет выполнена тогда, когда скрипт запускается напрямую, а не импортируется как модуль
    chat_bot()