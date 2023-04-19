import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class BUsers(SqlAlchemyBase):
    __tablename__ = 'blocked_users'
    operation_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    id = sqlalchemy.Column(sqlalchemy.Integer)
    user = orm.relationship('User')
