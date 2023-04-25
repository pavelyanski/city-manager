from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired, Length, ValidationError

from data import db_session
from data.users import User


def check_availability(form, field):
    db_sess = db_session.create_session()
    users = db_sess.query(User.name).all()
    users = [i[0] for i in users]
    if field.data in users:
        raise ValidationError("Такое имя занято")


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                                   Length(min=6, max=15, message="от 6 до 15")])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired(), check_availability])
    photo = FileField("Аватарка")
    about = TextAreaField("Немного о себе", validators=[Length(max=50, message="не больше 50")])
    submit = SubmitField('Зарегистрироваться')
