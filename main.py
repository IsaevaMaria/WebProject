from flask import Flask, render_template, redirect, request
from werkzeug.utils import secure_filename
from data import db_session, building
from data.building import Building
from data.categories import Categories
from data.users import User
from data.routes import Routes
from data.forms import RegisterForm, LoginForm, AddBuilding
import requests as req
import sys
import os
from flask_login import LoginManager, login_required, logout_user, login_user, current_user


NUMBER_PHOTO = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = '/static/img'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

def get_coords(adress):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode=" + adress
    response = req.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
    return toponym_coodrinates

def get_map(params):
    response = None
    map_request = "http://static-maps.yandex.ru/1.x/?"
    response = req.get(map_request, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return response.content

def cart_museum():
    session = db_session.create_session()
    b = session.query(Building).filter(Building.categories_id == 2)
    sp = [x.adress for x in b]
    coords = ',  '.join(get_coords("Кострома").split())
    sp = [','.join(get_coords("Кострома" + x).split()) for x in sp]
    s = ['pmwts'+str(i + 1)+'~'+x for i, x in enumerate(sp)]
    s = ''.join(s)
    d = {'ll': coords, 'l': 'map', 'spn': '0.01,0.01', 'pt': s}
    return d


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Мой город - Кострома')

@app.route('/attractions')
def attractions():
    session = db_session.create_session()
    b = session.query(Building).filter(Building.categories_id == 1)
    return render_template('attractions.html', title='Достопримечательности Костромы', items=b)

@app.route('/museums')
def museums():
    session = db_session.create_session()
    b = session.query(Building).filter(Building.categories_id == 2)
    return render_template('museums.html', title='Карта музеев Костромы', items=b)


@app.route('/kostroma_routes')
def routes():
    session = db_session.create_session()
    b = session.query(Routes).all()
    return render_template('route.html', title='Прогулки по Костроме', items=b)

@app.route('/slider/<int:rout_id>')
def slider(rout_id):
    session = db_session.create_session()
    b = session.query(Building).filter(Building.routes_id == rout_id)
    return render_template('carusel.html', title='Прогулки по Костроме', items=b)

@app.route('/attraction_id/<int:attrac_id>')
def attraction_id(attrac_id):
    session = db_session.create_session()
    b = session.query(Building).filter(Building.id == attrac_id).first()
    return render_template('attracabout.html', title='Прогулки по Костроме', item=b)

@app.route('/museum_id/<int:attrac_id>')
def museum_id(attrac_id):
    session = db_session.create_session()
    b = session.query(Building).filter(Building.id == attrac_id).first()
    a = get_coords("Кострома" + b.adress)
    coords = ',  '.join(get_coords("Кострома").split())
    sp = ','.join(a.split()) + ',pmwts1'
    s = ''.join(sp)
    d = {'ll': coords, 'l': 'map', 'spn': '0.01,0.01', 'pt': s}

    return render_template('museum_about.html', title=b.title, item=b, dic=d)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/account')
@login_required
def go_account():
    return render_template('account.html')

@app.route('/add_favourites/<int:my_id>')
@login_required
def add_favourites(my_id):
    session = db_session.create_session()
    b = session.query(Building).filter(Building.id == my_id).first()
    #current_user.buildings.append(b)
    #current_user.building = b
    #session.merge(current_user)
    #session.commit()
    return render_template('attracabout.html', title='Прогулки по Костроме', item=b)


@app.route('/add_building',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = AddBuilding()
    if form.validate_on_submit():
        session = db_session.create_session()
        r = session.query(Routes).all()
        c = session.query(Categories).all()
        b = Building()
        b.title = form.title.data
        b.content = form.content.data
        b.adress = form.adress.data
        if form.image.data:  # Если получена фотография.
            filename = form.image.data.filename  # Получение имени.
            form.image.data.save(
                "static/image/" + filename.split("/")[-1])

        b.image = "static/image/" + form.image.data.filename.split("/")[-1] if form.image.data else ""
        n = form.category.data
        tmp =  session.query(Categories).filter(Categories.name == n).first()
        b.categories_id = tmp.id
        n = form.route.data
        tmp = session.query(Routes).filter(Routes.title == n).first()
        b.routes_id = tmp.id
        session.add(b)
        session.commit()
        return redirect('/')
    return render_template('add.html', title='Добавление объекта',
                           form=form)

def main():
    db_session.global_init("db/my_city.sqlite")
    app.run(port=8080, host='127.0.0.1')

if __name__ == '__main__':
    #main()
    db_session.global_init("db/my_city.sqlite")
    iport = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=iport)

