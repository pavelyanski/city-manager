import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class City(SqlAlchemyBase):
    __tablename__ = 'cities'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    city = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
    count_of_people = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sea = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    subway = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    information = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="Отсутствует")
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
