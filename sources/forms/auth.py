from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    open_id = StringField('openid', validators=[DataRequired()])  # Or another validator
    id_key = BooleanField('id_key', default=False)
