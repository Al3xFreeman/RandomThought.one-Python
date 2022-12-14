from app import db, login
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
import random
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
import sqlalchemy


star = db.Table('starred',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    starred_posts = db.relationship('Post', secondary=star, lazy='dynamic', backref=db.backref('users_starred', lazy=True))
    stars = db.Column(db.Integer, default=0)

    last_post = db.Column(db.DateTime, default = date.min)

    def __repr__(self):
        return '<User {}, last Post: {}>'.format(self.username, self.last_post)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def star_post(self, p):
        if p not in self.starred_posts:
            self.starred_posts.append(p)
            if p.author:
                p.author.stars += 1

            db.session.add_all([p, self])
            db.session.commit()
        
        return p
        
    def unstar_post(self, p):
        if p in self.starred_posts:
            self.starred_posts.remove(p)
            if p.author:
                p.author.stars -= 1

            db.session.add_all([p, self])
            db.session.commit()
        
        return p
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class AnonUser(AnonymousUserMixin):
    def get_id(self):
        return random.randrange(User.query.count())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    view_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<ID: {} | Post {} by: {} | Stars: {}>'.format(self.id, self.body, self.author, len(self.users_starred))

    def stars(self):
        return len(self.users_starred)

    def addView(self, amount = 1):
        print("huh?", self.view_count)
        self.view_count += amount
        print("huh?", self.view_count)
        return self.view_count

    @hybrid_property
    def popularity(self, decimals = 2):
        if self.view_count == 0:
            return 0
        else:
            return round(len(self.users_starred) / self.view_count, decimals)