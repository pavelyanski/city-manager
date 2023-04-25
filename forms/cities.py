from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from data import db_session
from data.cities import City


def check_type(form, field):
    if not field.data.isdigit():
        raise ValidationError("Количество населения должно быть числом")


def check_availability(form, field):
    db_sess = db_session.create_session()
    cities = db_sess.query(City.city).all()
    cities = [i[0] for i in cities]
    if field.data in cities:
        raise ValidationError("Такой город уже существует")


class CityForm(FlaskForm):
    city = StringField('Название', validators=[DataRequired(), check_availability])
    count_of_people = StringField("Население", validators=[DataRequired(), check_type])
    sea = BooleanField("Море")
    subway = BooleanField("Метро")
    information = TextAreaField("Подробная информация")
    submit = SubmitField('Добавить')
