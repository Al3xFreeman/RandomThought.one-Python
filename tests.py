from datetime import datetime
import unittest
from app import create_app, db
from app.models import User, Post
from config import TestConfig

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='test1')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_new_post(self):
        u = User(username='test1')
        p = Post(body="Body test", author = u, timestamp = datetime.now())

        db.session.add_all([u, p])
        db.session.commit()

        self.assertEqual(p.author, u)

    def test_star_post(self):
        u1 = User(username='test1')
        u2 = User(username='test2')
        p = Post(body="Body test", author = u1, timestamp = datetime.now())

        db.session.add_all([u1, u2, p])
        db.session.commit()

        u1.star_post(p)

        self.assertEqual(p.users_starred[0], u1)
        self.assertEqual(u1.starred_posts[0], p)
        self.assertEqual(p.stars(), 1)
        self.assertEqual(u1.stars, 1)

    def test_unstar_post(self):
        u1 = User(username='test1')
        u2 = User(username='test2')
        p = Post(body="Body test", author = u1, timestamp = datetime.now())

        db.session.add_all([u1, u2, p])
        db.session.commit()

        u1.star_post(p)

        u1.unstar_post(p)

        self.assertEqual(len(p.users_starred), 0)
        self.assertEqual(len(u1.starred_posts.all()), 0)
        self.assertEqual(p.stars(), 0)
        self.assertEqual(u1.stars, 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)