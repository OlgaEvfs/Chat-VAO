from flask import Flask, render_template, url_for
'''Импорт фласк. '''

app = Flask(__name__)

'''Отслеживание главной страницы'''
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")



''' Для запуска приложения. Для отслеживания ошибок добавлен атрибут. False если отключить показ'''
if __name__ =="__main__":
    app.run(debug=True)