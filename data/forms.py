from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
#from wtforms import FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class AddBuilding(FlaskForm):
    title = StringField('Название объекта', validators=[DataRequired()])
    content = TextAreaField("Описание", validators=[DataRequired()])
    adress = StringField("Адрес объекта")
    image = FileField("Прикрепите картинку") #, validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jfif'], 'Images only!')])
    category = SelectField('Название категории', choices=[
    	("Музеи", "Музеи"),
    	("Достопримечательности", "Достопримечательности")])
    route = SelectField('Название категории', choices=[
        ("Ансамбль Сусанинской площади", "Ансамбль Сусанинской площади"),
        ("Прогулка по центру", "Прогулка по центру")])

    submit = SubmitField('Добавить')