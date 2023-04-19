import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class SelectedCity(SqlAlchemyBase):
    __tablename__ = 'selected_cities'
    operation_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    city_id = sqlalchemy.Column(sqlalchemy.Integer)
    user = orm.relationship('User')
