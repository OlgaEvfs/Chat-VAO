from flask import Flask, render_template, request
from chat_bot import find_similar_question, get_answer_from_db, add_new_question_answer, update_question, update_answer, update_category, get_categories, get_questions_by_category, add_new_data, chat_bot 
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
            elif action == "3":
                # Выбор категории и получение вопросов
                category_choice = request.form.get('category_choice')
                if category_choice:
                    questions = get_questions_by_category(category_choice)  # Получаем вопросы по выбранной категории
                    message = f"Вопросы из категории {category_choice}: {', '.join(questions)}"
                else:
                    message = "Выберите категорию из списка."
                step = 1

    return render_template('index.html', step=step, action=action, answer=answer, message=message, categories=categories)

# Страница "О нас"
@app.route('/about')
def about():
    return render_template("about.html")

# Обработчики для добавления, изменения вопросов и ответов
@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        new_question = request.form.get('new_question')
        new_answer = request.form.get('new_answer')
        new_category = request.form.get('new_category', 'Без категории')
        message = add_new_question_answer(new_question, new_answer, new_category)
        return render_template('index.html', message=message)
    return render_template('add_new.html')

# Обработчик для изменения вопроса
@app.route('/update_question', methods=['GET', 'POST'])
def update_question_view():
    if request.method == 'POST':
        old_question = request.form.get('old_question')
        new_question = request.form.get('new_question')
        message = update_question(old_question, new_question)
        return render_template('index.html', message=message)
    return render_template('update_question.html')

# Обработчик для изменения ответа
@app.route('/update_answer', methods=['GET', 'POST'])
def update_answer_view():
    if request.method == 'POST':
        question = request.form.get('question')
        new_answer = request.form.get('new_answer')
        message = update_answer(question, new_answer)
        return render_template('index.html', message=message)
    return render_template('update_answer.html')

# Обработчик для изменения категории
@app.route('/update_category', methods=['GET', 'POST'])
def update_category_view():
    if request.method == 'POST':
        question = request.form.get('question')
        new_category = request.form.get('new_category')
        message = update_category(question, new_category)
        return render_template('index.html', message=message)
    return render_template('update_category.html')

# Обработчик для поиска схожего вопроса
@app.route('/find_similar_question', methods=['GET', 'POST'])
def find_similar_question_view():
    if request.method == 'POST':
        question = request.form.get('question')
        similar_question = find_similar_question(question)
        if similar_question:
            message = f"Похожий вопрос: {similar_question[1]}"
        else:
            message = "Похожий вопрос не найден."
        return render_template('index.html', message=message)
    return render_template('find_similar_question.html')


''' Для запуска приложения. Для отслеживания ошибок добавлен атрибут. False если отключить показ'''
if __name__ =="__main__":
    app.run(debug=True)