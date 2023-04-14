import sqlite3

from flask import Flask, render_template, redirect, request, make_response, session, abort
from sqlalchemy import create_engine

from data import db_session
from data.users import User
from data.cities import City
from data.blocked_users import BUsers
from data.selecteds import SelectedCity
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login import LoginForm
from forms.cities import CityForm
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sd23dq123sda4332wesdf212w121asdsdcxaium454'
login_manager = LoginManager()
login_manager.init_app(app)


def get_coord(city):
    try:
        url = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
              "&geocode={},1&format=json".format(city)
        response = requests.get(url)
        if response:
            d = response.json()
            point = d["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"][
                "pos"]
            return point
        else:
            return "засекречено"
    except Exception as er:
        return "засекречено"


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("main_sheet.html")


@app.route("/main")
@login_required
def main_sheet():
    db_sess = db_session.create_session()
    b_users = db_sess.query(BUsers.id).filter(BUsers.user_id == current_user.id)
    cities = db_sess.query(City).filter(City.user_id.notin_(b_users))
    return render_template("index.html", cities=cities)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        photo = form.photo.data.read()
        binary = sqlite3.Binary(photo)
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            photo=binary

        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/register")


@app.route('/cities/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_cities(id):
    form = CityForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        cities = db_sess.query(City).filter(City.id == id, City.user_id == current_user.id).first()
        if cities:
            form.city.data = cities.city
            form.count_of_people.data = cities.count_of_people
            form.sea.data = cities.sea
            form.subway.data = cities.subway
            form.information.data = cities.information
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cities = db_sess.query(City).filter(City.id == id, City.user_id == current_user.id).first()
        if cities:
            cities.city = form.city.data
            cities.count_of_people = form.count_of_people.data
            cities.sea = form.sea.data
            cities.subway = form.subway.data
            cities.information = form.information.data
            db_sess.commit()
            return redirect('/main')
        else:
            abort(404)
    return render_template('cities.html', title='Редактирование города', form=form)


@app.route('/cities', methods=['GET', 'POST'])
@login_required
def add_cities():
    form = CityForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        city = City()
        city.city = form.city.data
        city.count_of_people = form.count_of_people.data
        city.sea = form.sea.data
        city.subway = form.subway.data
        city.information = form.information.data
        city.user_id = current_user.id
        db_sess.add(city)
        db_sess.commit()
        return redirect('/main')
    return render_template('cities.html', title='Добавление новости',
                           form=form)


@app.route('/cities_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def cities_delete(id):
    db_sess = db_session.create_session()
    city = db_sess.query(City).filter(City.id == id,
                                      City.user == current_user
                                      ).first()
    if city:
        db_sess.delete(city)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/main')


@app.route('/info/<int:id>', methods=['GET', 'POST'])
@login_required
def get_info(id):
    db_sess = db_session.create_session()
    city = db_sess.query(City).filter(City.id == id).first()
    selected = db_sess.query(SelectedCity).filter(SelectedCity.city_id == id).filter(
        SelectedCity.user_id == current_user.id).first()
    selected = False if not selected else True
    return render_template('city.html', title=city.city, city=city, coord=get_coord(city.city),
                           selected=selected)


@app.route('/users/<int:id>', methods=['GET', 'POST'])
@login_required
def user_profile(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            b_users = db_sess.query(BUsers.id).filter(BUsers.user_id == current_user.id).all()
            if b_users:
                b_users = [blocked_user[0] for blocked_user in b_users]
            return render_template('user.html', title=user.name, user=user, b_users=b_users)
        else:
            abort(404)


@app.route('/userava/<int:id>')
@login_required
def userava(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    img = user.getAvatar()
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/unblock/<int:id>', methods=['GET', 'POST'])
@login_required
def unblock(id):
    db_sess = db_session.create_session()
    db_sess.query(BUsers).filter(BUsers.id == id).filter(BUsers.user_id == current_user.id).delete()
    db_sess.commit()
    return redirect('/main')


@app.route('/block/<int:id>', methods=['GET', 'POST'])
@login_required
def block(id):
    db_sess = db_session.create_session()
    b_user = BUsers(user_id=current_user.id, id=id)
    db_sess.add(b_user)
    db_sess.commit()
    return redirect('/main')


@app.route("/blocked_users")
@login_required
def blocked_users():
    db_sess = db_session.create_session()
    b_users = db_sess.query(BUsers.id).filter(BUsers.user_id == current_user.id)
    users = db_sess.query(User).filter(User.id.in_(b_users))
    return render_template("blocked.html", users=users)


@app.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like(id):
    db_sess = db_session.create_session()
    selected_city = SelectedCity(user_id=current_user.id, city_id=id)
    db_sess.add(selected_city)
    db_sess.commit()
    return redirect(f'/info/{id}')


@app.route('/unlike/<int:id>', methods=['GET', 'POST'])
@login_required
def unlike(id):
    db_sess = db_session.create_session()
    db_sess.query(SelectedCity).filter(SelectedCity.city_id == id).filter(
        SelectedCity.user_id == current_user.id).delete()
    db_sess.commit()
    return redirect(f'/info/{id}')


@app.route("/selected_cities")
@login_required
def selected_cities():
    db_sess = db_session.create_session()
    selected_cities = db_sess.query(SelectedCity.city_id).filter(
        SelectedCity.user_id == current_user.id)
    cities = db_sess.query(City).filter(City.id.in_(selected_cities))
    return render_template("selected_cities.html", cities=cities)


def main():
    db_session.global_init("db/cities.db")
    app.run(debug=True, port=5003)


if __name__ == '__main__':
    main()
