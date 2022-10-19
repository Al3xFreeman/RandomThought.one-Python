from flask import render_template, flash, redirect, url_for, request, session, make_response
from app import app, db
from app.forms import LoginForm, NewPostForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required, user_unauthorized
from app.models import User, Post
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

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
#@login_required
def index():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Thought sent!')
        return redirect(url_for('index'))

    resp = make_response()
    cookie_key = 'RT_rndPost'
    
    if request.cookies.get(key=cookie_key, type=int, default=None) is None:
        rC = Post.query.count()
        cookie_value = random.randrange(rC) #if it is an anonymous user, the id will be a random value
        #TODO save that random value so if the user logs in, the post shown is the same
        t_now = datetime.datetime.today().utcnow()
        t_cookie_duration = datetime.timedelta(days=1)
        t_end = datetime.datetime(year=t_now.year, month=t_now.month, day=t_now.day) + t_cookie_duration
        cookie_max_age = (t_end - t_now).seconds

        resp.set_cookie(key = cookie_key, value = str(cookie_value), max_age=cookie_max_age, expires=cookie_max_age)
    else:
        cookie_value = request.cookies.get(key=cookie_key, type=int, default=None)

    test = getRandomRow(Post, cookie_value)
    print(test.body)
    #resp.set_data("Result: {}".format(test.username))
    resp.set_data(render_template('index.html', title='RandomThought.one', post=test, form=form))
    
    return resp

def getRandomRow(table, offset):
    table.query.count()
    return table.query.offset(offset).first_or_404()


@app.route("/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('profile.html', title="{}'s Profile".format(username), user=user)



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
