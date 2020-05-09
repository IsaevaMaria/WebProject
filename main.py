from flask import Flask, render_template
from data import db_session
from data.building import Building
from data.categories import Categories
from data.routes import Routes
import requests
import sys
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def get_coords(adress):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode=" + adress
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
    return toponym_coodrinates

def get_map(params):
    response = None
    map_request = "http://static-maps.yandex.ru/1.x/?"
    #print(map_request)
    response = requests.get(map_request, params=params)
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
    sp = [','.join(get_coords("Кострома"+x).split()) for x in sp]
    s = ['pmwts'+str(i + 1)+'~'+x for i, x in enumerate(sp)]
    s = ''.join(s)
    d = {'ll': coords, 'l': 'map', 'spn': '0.01,0.01', 'pt': s}
    return d


def main():
    db_session.global_init("db/my_city.sqlite")
    app.run(port=8080, host='127.0.0.1')

@app.route('/')
@app.route('/index')
def index():
    #dic = cart_museum()
    dic={}
    return render_template('index.html', title='Мой город - Кострома', items=dic)

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
    print(b.id)
    return render_template('attracabout.html', title='Прогулки по Костроме', item=b)

if __name__ == '__main__':
    main()
    #iport = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=iport)

