from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def check_dog(form, field):
    if "@" not in field.data:
        raise ValidationError("Где собачка??")
    if field.data[0] == "@":
        raise ValidationError("Нельзя с собачки начинать")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), check_dog])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
