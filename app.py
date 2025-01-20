from flask import Flask, render_template, request
from chat_bot import get_answer_from_db, add_new_question_answer, get_categories, get_questions_by_category
'''Импорт фласк.'''

app = Flask(__name__)

'''Отслеживание главной страницы'''
@app.route('/')
@app.route('/home')
@app.route('/', methods=['GET', 'POST'])
def index():
    """Главная страница с выбором действий."""
    step = 1
    action = None
    answer = None
    message = None
    categories = []

    if request.method == 'POST':
        user_input = request.form.get('user_input')

        if step == 1:
            # Обрабатываем выбор действия
            if user_input == "1":
                step = 2
                action = "1"
            elif user_input == "2":
                step = 2
                action = "2"
            elif user_input == "3":
                step = 2
                action = "3"
                categories = get_categories()
            elif user_input == "4":
                return render_template('index.html', message="До свидания!")
            else:
                message = "Некорректный выбор. Попробуйте еще раз."

        elif step == 2:
            if action == "1":
                # Задать вопрос
                question = user_input
                answer = get_answer_from_db(question)
                step = 3
            elif action == "2":
                # Добавить новый вопрос
                new_question = request.form.get('new_question')
                new_answer = request.form.get('new_answer')
                new_category = request.form.get('new_category', 'Без категории')
                message = add_new_question_answer(new_question, new_answer, new_category)
                step = 1

    return render_template('index.html', step=step, action=action, answer=answer, message=message, categories=categories)



@app.route('/about')
def about():
    return render_template("about.html")


''' Для запуска приложения. Для отслеживания ошибок добавлен атрибут. False если отключить показ'''
if __name__ =="__main__":
    app.run(debug=True)
