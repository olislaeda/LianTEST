from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from sources.models.users import User


class EditProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    about = TextAreaField('about', validators=[Length(min=0, max=180)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    # def validate(self):
    #    if not FlaskForm.validate(self):
    #        return False
    #    if self.username.data == self.original_username:
    #        return True
    #    user = User.query.filter_by(username=self.username.data).first()
    #    if user != None:
    #        return False
    #    return True
