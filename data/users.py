import datetime
import sqlalchemy
from flask_login import UserMixin

from . import db_session
from .blocked_users import BlockedUser
from .cities import City
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

from .selecteds import SelectedCity


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

    def get_selected_cities(self):
        db_sess = db_session.create_session()
        cities_id = [item[0] for item in
                     db_sess.query(SelectedCity.city_id).filter(SelectedCity.user_id == self.id).all()]
        cities = db_sess.query(City).filter(City.id.in_(cities_id))
        return cities

    def get_blocked_users(self):
        db_sess = db_session.create_session()
        b_users = db_sess.query(BlockedUser.id).filter(BlockedUser.user_id == self.id)
        users = db_sess.query(User).filter(User.id.in_(b_users)).all()
        return users
