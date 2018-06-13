from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length
from user.models import *


class PostForm(FlaskForm):
    title = StringField('title', validators=[Length(0, 128)])
    content = TextAreaField('content', validators=[DataRequired()])
    submit = SubmitField('submit')