from flask import Flask, render_template
from data import db_session
from data.building import Building
from data.categories import Categories
from data.routes import Routes
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
bootstrap = Bootstrap(app)

def main():
    db_session.global_init("db/my_city.sqlite")


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
    return render_template('attractions.html', title='Достопримечательности Костромы', items=b)

@app.route('/routes')
def routes():
    session = db_session.create_session()
    b = session.query(Routes).all()
    return render_template('route.html', title='Прогулки по Костроме', items=b)

@app.route('/slider/<int:rout_id>')
def slider(rout_id):
    session = db_session.create_session()
    b = session.query(Building).filter(Building.routes_id == rout_id)
    return render_template('carusel.html', title='Прогулки по Костроме', items=b)


if __name__ == '__main__':
    main()
