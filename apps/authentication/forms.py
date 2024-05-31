from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email',
                         id='email_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])

class SignupForm(FlaskForm):
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     id='pwd_confirm',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email',
                         id='email_forgot',
                         validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             id='pwd_reset',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     id='pwd_reset_confirm',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
