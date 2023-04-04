from flask import Flask, render_template, redirect, request, make_response, session, abort
from data import db_session
from data.users import User
from data.cities import City
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login import LoginForm
from forms.cities import CityForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sd23dq123sda4332wesdf212w121asdsdcxaium454'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    cities = db_sess.query(City)
    return render_template("index.html", news=cities)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
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
            return redirect("/")
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
            form.is_capital.data = cities.is_capital
            form.subway.data = cities.subway
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cities = db_sess.query(City).filter(City.id == id, City.user_id == current_user.id).first()
        if cities:
            cities.city = form.city.data
            cities.count_of_people = form.count_of_people.data
            cities.is_capital = form.is_capital.data
            cities.subway = form.subway.data
            db_sess.commit()
            return redirect('/')
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
        city.is_capital = form.is_capital.data
        city.subway = form.subway.data
        city.user_id = current_user.id
        db_sess.add(city)
        db_sess.commit()
        return redirect('/')
    return render_template('cities.html', title='Добавление новости',
                           form=form)


@app.route('/cities_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    city = db_sess.query(City).filter(City.id == id,
                                      City.user == current_user
                                      ).first()
    if city:
        db_sess.delete(city)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    db_session.global_init("db/cities.db")
    app.run(debug=True, port=5002)


if __name__ == '__main__':
    main()
