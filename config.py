import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'



# DATABASE CONFIG
    db_dir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(db_dir, 'lian.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(db_dir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# CSRF PROTECTION
    CSRF_PROTECTION_ENABLED = False

# OPEN ID CONFIG
    OPENID_PROVIDERS = [
        {'name': 'Google', 'url': 'https://accounts.google.com/o/oauth2/v2/auth'},
        {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
        {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
        {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
        {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

# MAIL SERVER SETTINGS
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

# ADMIN LIST
    ADMINS = ['you@example.com']
