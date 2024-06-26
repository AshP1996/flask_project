from flask import render_template, current_app
from flask_mail import Message

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail = current_app.extensions['mail']
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender="admin@hello.com",
               recipients=[user.email],
               text_body=render_template('mail/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('mail/reset_password.html',
                                         user=user, token=token))