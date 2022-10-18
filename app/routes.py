from flask import render_template, flash, redirect, url_for, request, session, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required, user_unauthorized
from app.models import User
from werkzeug.urls import url_parse
from sqlalchemy.sql.expression import func
import random
import datetime

"""
@app.before_request
def make_session_permanent():
    print("Session Permanent")
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(seconds=30)
    print("COOKIE: {}".format(app.session_cookie_name))
"""

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = {'username': 'Paco'}
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }]

    rC = User.query.count()
    #test = User.query.offset(rC*random.random()).first().username #Random each time
    num = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days
    num += current_user.id #If it is anon, the id will be a random number
    print("NUM: {}".format(num))
    test = User.query.offset(num%rC).first() #Based on an input
    print("ID to show: {}".format(test.id))
    return render_template('index.html', title='Home', posts=posts, test=test.username)

@app.route("/test")
def test2():

    resp = make_response()
    cookie_key = 'RT_rndPost'
    
    if request.cookies.get(key=cookie_key, type=int, default=None) is None:
        cookie_value = current_user.get_id() #if it is an anonymous user, the id will be a random value
        #TODO save that random value so if the user logs in, the post shown is the same
        t_now = datetime.datetime.today().utcnow()
        t_end = datetime.datetime(year=t_now.year, month=t_now.month, day=t_now.day, hour=t_now.hour, minute=(t_now.minute + 1) % 59)
        cookie_max_age = (t_end - t_now).seconds

        resp.set_cookie(key = cookie_key, value = str(cookie_value), max_age=cookie_max_age, expires=cookie_max_age)
    else:
        cookie_value = request.cookies.get(key=cookie_key, type=int, default=None)

    test = getRandomRow(User, cookie_value)
    resp.set_data("Result: {}".format(test.username))

    return resp

def getRandomRow(table, offset):
    table.query.count()
    return table.query.offset(offset).first()


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title="Sign In", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
