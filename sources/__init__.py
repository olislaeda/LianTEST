import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import Config

lian = Flask(__name__)
lian.config.from_object(Config)
db = SQLAlchemy(lian)
lm = LoginManager()
lm.init_app(lian)
lm.login_view = 'login'
openid = OpenID(lian, os.path.join(Config.db_dir, 'oidTMP'))

from sources import display
from sources.models import users, posts

if not lian.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler

    # MAIL HANDLER
    credentials = None
    if Config.MAIL_USERNAME or Config.MAIL_PASSWORD:
        credentials = (Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
    mail_handler = SMTPHandler((Config.MAIL_SERVER, Config.MAIL_PORT), 'no-reply@' + Config.MAIL_SERVER,
                               Config.ADMINS, 'Lian failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    lian.logger.addHandler(mail_handler)

    # LOG FILE HANDLER
    file_handler = RotatingFileHandler('log.log', 'a', 1 * 1024 * 1024)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    lian.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    lian.logger.addHandler(file_handler)
    lian.logger.info('Lian started')
