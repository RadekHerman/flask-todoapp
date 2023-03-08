from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flasktodo.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[Optional(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Optional(), Email()])
   
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken.')
            
class ChangePasswordForm(FlaskForm):
    
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Send New Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Invalid email. You are not registered.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    subject = StringField('Subject',validators=[DataRequired()])
    content = TextAreaField('Details', validators=[DataRequired()])
    date_todo = DateField('Date', validators=[DataRequired()])
    hour_todo = TimeField('Time', validators=[Optional()])
    submit = SubmitField('Add')