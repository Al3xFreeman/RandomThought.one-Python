from flask import render_template, flash, redirect, url_for, request, make_response, jsonify, current_app
from app import db
from app.main import bp
from app.main.forms import NewPostForm
from flask_login import current_user, login_required
from app.models import User, Post
import random
import datetime

@bp.route("/testPost")
def testPost():
    print("Number of posts: ", Post.query.count())
    p = Post(body="Test Post")
    db.session.add(p)
    db.session.commit()
    print("Number of posts: ", Post.query.count())
    return {'numPosts': Post.query.count()}

@bp.route("/", methods=['GET', 'POST'])
@bp.route("/index", methods=['GET', 'POST'])
def index():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Thought sent!')
        return redirect(url_for('main.index'))

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
    #test = getRandomRow(Post, cookie_value)
    print(randomPost)

    resp.set_data(render_template('index.html', title='RandomThought.one', post=randomPost, form=form))
    
    return resp

def getRandomRow(table, offset):
    table.query.count()
    return table.query.offset(offset).first_or_404()


@bp.route("/user/<username>")
def profile(username):

    posts_page = request.args.get('posts_page', 1, type=int)
    starred_page = request.args.get('starred_page', 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()

    user_posts = user.posts.paginate(page=posts_page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    starred_posts = user.starred_posts.paginate(page=starred_page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    user_posts_next_url = url_for('main.profile', username=username, posts_page=user_posts.next_num, starred_page=starred_page) if user_posts.has_next else None
    user_posts_prev_url = url_for('main.profile', username=username, posts_page=user_posts.prev_num, starred_page=starred_page) if user_posts.has_prev else None

    starred_posts_next_url = url_for('main.profile', username=username, posts_page=posts_page, starred_page=starred_posts.next_num) if starred_posts.has_next else None
    starred_posts_prev_url = url_for('main.profile', username=username, posts_page=posts_page, starred_page=starred_posts.prev_num) if starred_posts.has_prev else None

    return render_template('profile.html', title="{}'s Profile".format(username),\
                                                                    user=user, \
                                                                    user_posts=user_posts.items, \
                                                                    starred_posts=starred_posts.items, \
                                                                    user_posts_next_url = user_posts_next_url, \
                                                                    user_posts_prev_url = user_posts_prev_url, \
                                                                    starred_posts_next_url = starred_posts_next_url, \
                                                                    starred_posts_prev_url = starred_posts_prev_url, \
                                                                    )

@bp.route("/post/<post_id>/star")
@login_required
def star_post(post_id):
    """
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
    """
    p = Post.query.get_or_404(post_id)
    p = current_user.star_post(p)

    return jsonify({'stars': p.stars()})
    #return redirect(url_for('index'))


@bp.route("/post/<post_id>/unstar")
@login_required
def unstar_post(post_id):
    """
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
    """
    p = Post.query.get_or_404(post_id)
    p = current_user.unstar_post(p)

    return jsonify({'stars': p.stars()})
    #return redirect(url_for('index'))
