import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class City(SqlAlchemyBase):
    __tablename__ = 'cities'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    city = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    count_of_people = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_capital = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    subway = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
