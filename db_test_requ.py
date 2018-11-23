from sources import db
from sources.models import users, posts
import datetime

u = posts.Posts.query.all()
db.session.commit()