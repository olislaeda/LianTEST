from sources import db
from flask_login import UserMixin
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1


# DB structure of users table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    posts = db.relationship('Posts', backref='author', lazy='dynamic')
    about = db.Column(db.String(180))
    last_seen = db.Column(db.DateTime)
    def avatar(self, size):
            return 'http://www.gravatar.com/avatar/' + md5(self.email.encode('utf-8')).hexdigest() + '?d=mm&s=' + str(size)
    @staticmethod
    def make_unique_username(username):
        if User.query.filter_by(username=username).first() == None:
            return username
        version = 2
        while True:
            new_username = username + str(version)
            if User.query.filter_by(username=new_username).first() == None:
                break
            version += 1
        return new_username

def is_authenticated(self):
    return True


def is_active(self):
    return True


def is_anonymous(self):
    return False


def get_id(self):
    return str(self.id)

# Debug method
def __repr__(self):
    return '<Username %r>' % (self.username)
