from xmlrpc.client import Boolean
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
    #print("Number of posts: ", Post.query.count())
    p = Post(body="Test Post")
    db.session.add(p)
    db.session.commit()
    #print("Number of posts: ", Post.query.count())
    return {'numPosts': Post.query.count()}

@bp.route("/", methods=['GET', 'POST'])
@bp.route("/index", methods=['GET', 'POST'])
def index():

    form = NewPostForm()
    if form.validate_on_submit():
        #print("ILLO SA METIO A PONER UN NUEVOPOST")
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Thought sent!')

        resp = make_response(redirect(url_for('main.index')))
        resp.set_cookie(key='form_red', value=str(True))

        current_user.last_post = datetime.datetime.now()
        db.session.add(current_user)
        db.session.commit()

        return resp

    
    if request.method == 'POST':
        b = request.form['body']
        #print(current_user.username + " --> ILLO SA METIO A PONER UN NUEVOPOST")
        post = Post(body=b, author=current_user)
        
        db.session.add(post)
        db.session.commit()
        flash('New Thought sent!')

        resp = make_response(redirect(url_for('main.index')))
        resp.set_cookie(key='form_red', value=str(True))

        return resp


    resp = make_response()

    # If page load came from redirect, will keep the last seen post, else, a new one is fetched
    form_red = request.cookies.get('form_red')
    form_red = form_red.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

    if not form_red:
        rC = Post.query.count()
        val = random.randrange(rC)
        post = getRandomRow(Post, val)
        if post is None:
            post = Post(body = "")

    else:
        postId = request.cookies.get('lastPost', type=int)
        post = Post.query.get(postId)
        if not post:
            rC = Post.query.count()
            val = random.randrange(rC)
            post = getRandomRow(Post, val)
            if post is None:
                post = Post(body = "")

    # Limit the ability to post a new Thought to the limit set in the Config
    if not current_user.is_anonymous:
        new_post_limit = current_app.config['NEW_POST_RATE']
        can_post = current_user.last_post + new_post_limit < datetime.datetime.now()
        print(current_user.last_post)
        print(datetime.datetime.now())
        next_post_time = current_app.config['NEW_POST_RATE'] - (datetime.datetime.now() - current_user.last_post)
    else:
        can_post = False
        next_post_time = 0
    
    
    

    resp.set_cookie(key='lastPost', value=str(post.id))
    resp.set_cookie(key='form_red', value=str(False))
    resp.set_data(render_template('index.html', title='RandomThought.one', post=post, form=form, can_post=can_post, next_post_time=next_post_time))
    
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
