from flask import Flask, render_template
from data import db_session
from data.building import Building
from data.categories import Categories

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def main():
    app.run(port=8000, host='127.0.0.1')
    #a1 = Categories()
    #a1.name = "Достопримечательности"
    #a1.about = "Посмотреть популярные достопримечательности Костромы"
    #a2 = Categories()
    #a2.name = "Музеи"
    #a2.about = "Список музеев Костромы"
    #a3 = Categories()
    #a3.name = "Мероприятия"
    #a3.about = "Праздники, фестивали, конкурсы"
    #a1 = Building()
    #a1.title = 'Пожарная каланча'
    #a1.content = '35-метровая пожарная каланча уже давно является архитектурным символом Костромы и самой высокой точкой в центре города. Приехав сюда в 1834 г., император Николай I восторженно воскликнул: «Такой каланчи у меня даже в Петербурге нет».'
    #a1.adress = 'ул. Симановского, д.1/2'
    #a1.image = '/static/image/calancha.jfif'
    #a2 = Building()
    #a2.title = 'Гауптвахта'
    #a2.content = 'По соседству с пожарной каланчей в Костроме находится здание бывшей гарнизонной гаупвахты. /' \
     #            'Автором этого шедевра является архитектор П.И. Фурсов. В течение XIX — начала ХХ веков здание Гауптвахты использовалось по-своему прямому назначению — как место пребывания арестованных военнослужащих.'
    #a2.adress = 'ул.Ленина, д. 1/2'
    #a2.image = '/static/image/gauptvahta.jfif'
    #session = db_session.create_session()
    #session.add(a1)
    #session.add(a2)
    #session.add(a3)
    #session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Мой город - Кострома')

@app.route('/attractions')
def attractions():
    session = db_session.create_session()
    a = session.query(Building).filter(Building.categories_id == 1)
    print(a)
    return render_template('attractions.html', title='Достопримечательности Костромы')




if __name__ == '__main__':
    db_session.global_init("db/my_city.sqlite")
    main()
