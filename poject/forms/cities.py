from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class CityForm(FlaskForm):
    city = StringField('Название')
    count_of_people = StringField("Население")
    is_capital = BooleanField("Столица")
    subway = BooleanField("Метро")
    submit = SubmitField('Добавить')
