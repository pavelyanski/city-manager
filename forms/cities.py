from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, InputRequired


def check_type(form, field):
    if not field.data.isdigit():
        raise ValidationError('Количество населения должно быть числом')

class CityForm(FlaskForm):
    city = StringField('Название', validators=[DataRequired()])
    count_of_people = StringField("Население", validators=[InputRequired(), check_type])
    sea = BooleanField("Море")
    subway = BooleanField("Метро")
    information = TextAreaField("Подробная информация")
    submit = SubmitField('Добавить')


