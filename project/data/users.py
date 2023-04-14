import datetime
import sqlalchemy
from flask import url_for
from flask_login import UserMixin

from . import db_session
from .cities import City
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash



class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def getAvatar(self):
        img = self.photo
        return img

    def city_count(self):
        db_sess = db_session.create_session()
        cities = db_sess.query(City).filter(City.user_id == self.id).all()
        return len(cities)
