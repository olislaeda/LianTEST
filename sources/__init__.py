import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import db_dir

lian = Flask(__name__)
lian.config.from_object('config')
db = SQLAlchemy(lian)
lm = LoginManager()
lm.init_app(lian)
lm.login_view = 'login'
openid = OpenID(lian, os.path.join(db_dir, 'oidTMP'))

from sources import display
from sources.models import users, posts

