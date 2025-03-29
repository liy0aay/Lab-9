from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///towns.db' # путь к бд

db = SQLAlchemy(app)

# таблица учета посещенных городов
class Visit(db.Model): 
    id = db.Column(db.Integer, primary_key=True)  
    town = db.Column(db.String(100), nullable=False)  # название города
    visit_date = db.Column(db.String(20), nullable=False)  #дата визита

# обаботка GET и POST запросов
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        town = request.form.get('town')  # данные о городе
        visit_date = request.form.get('visit_date')  # дата визита
        if town and visit_date:  
            new_visit = Visit(town=town, visit_date=visit_date)
            db.session.add(new_visit)  # добавляем запись в бд
            db.session.commit()  # сохраняем
            return redirect(url_for('index'))  # перенаправление на главную страницу

    visits = Visit.query.all()  # получаем все визиты из бд
    return render_template('index.html', visits=visits) #отправляем в HTML-шаблон

# очистка бд
@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(Visit).delete()  # удаляем все записи
    db.session.commit()  
    return redirect(url_for('index')) 

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('towns.db'):  # проверяем, существует ли бд
            db.create_all()  # если нет, создаем таблицы
    app.run(debug=True)  