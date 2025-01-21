from flask import Flask, render_template, request,  session
from chat_bot import get_categories, get_questions_by_category, add_new_question_answer, update_question, update_answer, update_category, get_answer_from_db
import spacy

app = Flask(__name__)
app.secret_key = "12346789"
nlp = spacy.load('ru_core_news_lg')  # модель для русского языка

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'step' not in session:
        session['step'] = 1
    if 'action' not in session:
        session['action'] = None
    step = session['step']
    action = session['action']
    answer = None
    message = None
    categories = []
    questions = []
   
    if request.method == 'POST':
        user_input = request.form.get('user_input')
       
        if step == 1:
            # Приветствие и выбор действия
            if user_input == "1":
                session['step'] = 2
                session['action']  = "1"
                categories = get_categories()  # Получаем список категорий
                message = "Выберите категорию для вашего вопроса."
            elif user_input == "2":
                step = 2
                action = "2"
                message = "Введите новый вопрос, ответ и категорию."
            elif user_input == "3":
                step = 2
                action = "3"
                categories = get_categories()
                message = "Выберите категорию для изменения вопроса."
            elif user_input == "4":
                step = 2
                action = "4"
                categories = get_categories()
                message = "Выберите категорию для изменения ответа."
            elif user_input == "5":
                step = 2
                action = "5"
                categories = get_categories()
                message = "Выберите категорию для изменения вопроса."
            else:
                message = "Некорректный выбор. Попробуйте еще раз."

        elif step == 2:
            if action == "1":
                print("Test")
                # Задать вопрос
                category_choice = request.form.get('category_choice')
                print("Category: ",category_choice)
                if category_choice:
                    session['step'] = 3
                    session['category_choice'] = category_choice
                    questions = get_questions_by_category(category_choice)
                    message = "Выберите вопрос из списка."
                else:
                    message = "Пожалуйста, выберите вопрос."

            elif action == "2":
                # Добавить новый вопрос
                new_question = request.form.get('new_question')
                new_answer = request.form.get('new_answer')
                new_category = request.form.get('new_category', 'Без категории')
                message = add_new_question_answer(new_question, new_answer, new_category)
                step = 1

            elif action == "3":
                # Изменить вопрос
                category_choice = request.form.get('category_choice')
                if category_choice:
                    questions = get_questions_by_category(category_choice)
                    step = 4
                    message = "Выберите вопрос для изменения."
                else:
                    message = "Пожалуйста, выберите категорию."

            elif action == "4":
                # Изменить ответ
                category_choice = request.form.get('category_choice')
                if category_choice:
                    questions = get_questions_by_category(category_choice)
                    step = 5
                    message = "Выберите вопрос для изменения ответа."
                else:
                    message = "Пожалуйста, выберите категорию."

            elif action == "5":
                # Изменить категорию
                category_choice = request.form.get('category_choice')
                if category_choice:
                    questions = get_questions_by_category(category_choice)
                    step = 6
                    message = "Выберите вопрос для изменения категории."
                else:
                    message = "Пожалуйста, выберите категорию."

        elif step == 3:
             if action == "1":
                print("Test1")
                # Ответ на вопрос
                question_choice = request.form.get('question_choice')
                answer = get_answer_from_db(question_choice)
                message = f"Ответ на ваш вопрос: {answer}. Хотите задать еще вопрос или вернуться к действиям?"
                session['step'] = 1

        elif step == 4:
            # Изменить вопрос
            question_choice = request.form.get('question_choice')
            new_question = request.form.get('new_question')
            message = update_question(question_choice, new_question)
            step = 1

        elif step == 5:
            # Изменить ответ
            question_choice = request.form.get('question_choice')
            new_answer = request.form.get('new_answer')
            message = update_answer(question_choice, new_answer)
            step = 1

        elif step == 6:
            # Изменить категорию
            question_choice = request.form.get('question_choice')
            new_category = request.form.get('new_category')
            message = update_category(question_choice, new_category)
            step = 1
    print(step)
    return render_template('index.html', step=session.get('step'), action=session.get('action'), message=message, categories=categories, questions=questions, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)

