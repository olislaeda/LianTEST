from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, BooleanField
from wtforms.validators import DataRequired, Length
from sources.models.users import User


class EditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    about = TextAreaField('about', validators=[Length(min=0, max=180)])

    def __init__(self, original_username, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_username = original_username

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.username.data == self.original_username:
            return True
        user = User.query.filter_by(username=self.username.data).first()
        if user != None:
            return False
        return True
