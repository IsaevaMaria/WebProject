


from flask import Flask, render_template
from data import db_session

app = Flask(__name__)



@app.route('/')
@app.route('/index')
def index():
    user = 'Maria'

    return render_template('index.html', title='Домашняя страница',
                           username=user)




if __name__ == '__main__':
    #db_session.global_init("db/blogs.sqlite")
    app.run(port=8000, host='127.0.0.1')
