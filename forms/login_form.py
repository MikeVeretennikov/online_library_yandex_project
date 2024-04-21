from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField('Подтвердить')
