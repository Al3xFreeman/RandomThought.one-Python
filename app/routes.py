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

@app.route("/testPost")
def testPost():
    print("Number of posts: ", Post.query.count())
    p = Post(body="Test Post")
    db.session.add(p)
    db.session.commit()
    print("Number of posts: ", Post.query.count())
    return {'numPosts': Post.query.count()}

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
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
        cookie_value = random.randrange(rC)

        t_now = datetime.datetime.today().utcnow()
        t_cookie_duration = datetime.timedelta(days=1)
        t_end = datetime.datetime(year=t_now.year, month=t_now.month, day=t_now.day) + t_cookie_duration
        cookie_max_age = (t_end - t_now).seconds

        resp.set_cookie(key = cookie_key, value = str(cookie_value), max_age=cookie_max_age, expires=cookie_max_age)
    else:
        cookie_value = request.cookies.get(key=cookie_key, type=int, default=None)

    rC = Post.query.count()
    val = random.randrange(rC)
    randomPost = getRandomRow(Post, val)
    test = getRandomRow(Post, cookie_value)
    print(test.body)

    resp.set_data(render_template('index.html', title='RandomThought.one', post=randomPost, form=form))
    
    return resp

def getRandomRow(table, offset):
    table.query.count()
    return table.query.offset(offset).first_or_404()


@app.route("/<username>")
def profile(username):

    posts_page = request.args.get('posts_page', 1, type=int)
    starred_page = request.args.get('starred_page', 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()

    user_posts = user.posts.paginate(page=posts_page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    starred_posts = user.starred_posts.paginate(page=starred_page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)

    user_posts_next_url = url_for('profile', username=username, posts_page=user_posts.next_num, starred_page=starred_page) if user_posts.has_next else None
    user_posts_prev_url = url_for('profile', username=username, posts_page=user_posts.prev_num, starred_page=starred_page) if user_posts.has_prev else None

    starred_posts_next_url = url_for('profile', username=username, posts_page=posts_page, starred_page=starred_posts.next_num) if starred_posts.has_next else None
    starred_posts_prev_url = url_for('profile', username=username, posts_page=posts_page, starred_page=starred_posts.prev_num) if starred_posts.has_prev else None

    return render_template('profile.html', title="{}'s Profile".format(username),\
                                                                    user=user, \
                                                                    user_posts=user_posts.items, \
                                                                    starred_posts=starred_posts.items, \
                                                                    user_posts_next_url = user_posts_next_url, \
                                                                    user_posts_prev_url = user_posts_prev_url, \
                                                                    starred_posts_next_url = starred_posts_next_url, \
                                                                    starred_posts_prev_url = starred_posts_prev_url, \
                                                                    )

@app.route("/<post_id>/star")
@login_required
def star_post(post_id):
    p = Post.query.get_or_404(post_id)
    if p not in current_user.starred_posts:
        current_user.starred_posts.append(p)
        print("POST: {}".format(p))
        if p.author:
            print("POST AUTHOR STARS: {}".format(p.author.stars))
        if p.author is not None:
            p.author.stars += 1
        if p.author:        
            print("POST AUTHOR STARS: {}".format(p.author.stars))
        db.session.add(p)
        db.session.add(current_user)
        db.session.commit()

    return redirect(url_for('index'))


@app.route("/<post_id>/unstar")
@login_required
def untar_post(post_id):

    p = Post.query.get_or_404(post_id)
    if p in current_user.starred_posts:
        current_user.starred_posts.remove(p)
        print("POST: {}".format(p))
        if p.author:
            print("POST AUTHOR STARS: {}".format(p.author.stars))
        if p.author is not None:
            p.author.stars -= 1
        if p.author:
            print("POST AUTHOR STARS: {}".format(p.author.stars))
        db.session.add(p)
        db.session.add(current_user)
        db.session.commit()

    return redirect(url_for('index'))



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
