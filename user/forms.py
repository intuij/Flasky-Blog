from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from user.models import *


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 16)])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(4, 16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 16),
                            EqualTo('password_confirm', message='Password must match')])
    password_confirm = PasswordField('Password Confirm', validators=[DataRequired(), Length(4, 16)])
    submit = SubmitField('Register')


    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email address has been used!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username has been used!')


class ProfileForm(FlaskForm):
    fullname = StringField('Fullname', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    desc = TextAreaField('About')
    submit = SubmitField('Submit')

