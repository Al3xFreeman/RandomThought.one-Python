from email.policy import default
from typing import overload
from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
import random
from sqlalchemy.orm import remote

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
    #starred = db.relationship('Post', secondary=star, lazy='subquery', backref=db.backref('users_starred', lazy=True))
    starred = db.relationship('Post', secondary=star, lazy='dynamic')
    stars = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    #starred = db.relationship(User, secondary=star, lazy='subquery', backref=db.backref('starred_posts', lazy=True))
    starred = db.relationship(User, secondary=star, lazy='dynamic')

    def __repr__(self):
        return '<Post {} by: {}>'.format(self.body, self.author)
