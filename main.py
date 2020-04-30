from flask import Flask, render_template
from data import db_session
from data.building import Building
from data.categories import Categories
from data.routes import Routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def main():
    db_session.global_init("db/my_city.sqlite")
    a1 = Routes()
    a1.title = 'Ансамбль Сусанинской площади'
    a2 = Routes()
    a2.title = 'Прогулка по центру'
    a3 = Routes()
    a3.title = 'Прогулка по ул.Советской'
    a4 = Routes()
    a4.title = 'Прогулка по ул. Симановского'
    a5 = Routes()
    a5.title = 'Прогулка по проспекту Мира'
    a6 = Routes()
    a6.title = 'Торговые ряды'
    a7 = Routes()
    a7.title = 'Места Н.А. Островского'
    a8 = Routes()
    a8.title = 'Приезд Екатерины II'
    a9 = Routes()
    a9.title = 'Династия Романовых'


    app.run(port=8000, host='127.0.0.1')
    #session = db_session.create_session()
    #user = session.query(Categories).first()
    #for user in session.query(Building).filter(Building.categories_id == 1):
     #   print(user.title)




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Мой город - Кострома')

@app.route('/attractions')
def attractions():
    session = db_session.create_session()
    b = session.query(Building).filter(Building.categories_id == 1)
    print(b)

    return render_template('attractions.html', title='Достопримечательности Костромы', items=b)




if __name__ == '__main__':
    main()
