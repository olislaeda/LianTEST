import os
import unittest

from config import db_dir
from sources import lian, db
from sources.models.users import User


class TestCase(unittest.TestCase):
    def setUp(self):
        lian.config['TESTING'] = True
        lian.config['CSRF_ENABLED'] = False
        lian.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_dir, 'test.db')
        self.app = lian.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(username = 'john', email = 'john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_username(self):
        u = User(username = 'john', email = 'john@example.com')
        db.session.add(u)
        db.session.commit()
        username = User.make_unique_username('john')
        assert username != 'john'
        u = User(username = username, email = 'susan@example.com')
        db.session.add(u)
        db.session.commit()
        username2 = User.make_unique_username('john')
        assert username2 != 'john'
        assert username2 != username


if __name__ == '__main__':
    unittest.main()
