from flask import render_template, redirect, request, url_for
from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from apps.authentication.forms import LoginForm, SignupForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass
from apps.mail.mail import send_password_reset_email
# Setup URL serializer
serializer = URLSafeTimedSerializer('SECRET_KEY')

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        email = request.form['email']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(email=email).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/signup', methods=['GET', 'POST'])
def register():
    signup_form = SignupForm(request.form)
    if request.method == 'POST' and 'signup' in request.form:
        print(request)

        email = request.form['email']
        password = request.form['password']

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=signup_form)

        # else we can create the user
        new_user = Users.create_user(email=email, password=password, role='user')
        db.session.add(new_user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=signup_form)

    else:
        return render_template('accounts/register.html', form=signup_form)


@blueprint.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        print("current user", current_user)
        logout_user()
        return redirect(url_for('authentication_blueprint.login'))
    form = ForgotPasswordForm(request.form)
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        user = Users.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
        flash('Not Found User')
        print("User Not Found!!!!!!!!!!!!!!!!!!!!!!")
        return redirect(url_for('authentication_blueprint.login'))
    return render_template('accounts/forgot_password.html', form=form)


# @blueprint.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     try:
#         email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
#     except SignatureExpired:
#         flash('The password reset link is expired.', 'error')
#         return redirect(url_for('authentication_blueprint.forgot_password'))

#     form = ResetPasswordForm(request.form)
#     if request.method == 'POST' and 'password' in request.form:
#         user = Users.query.filter_by(email=email).first()
#         if user:
#             user.password = form.password.data  # Make sure to hash the password
#             db.session.commit()
#             flash('Your password has been updated!', 'success')
#             return redirect(url_for('authentication_blueprint.login'))
#     return render_template('accounts/reset_password.html', form=form)

@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash("The user is logged IN")
        return redirect(url_for('authentication_blueprint.login'))
    user = Users.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('authentication_blueprint.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('authentication_blueprint.login'))
    return render_template('accounts/reset_password.html', form=form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
