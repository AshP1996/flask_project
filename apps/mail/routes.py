from apps.mail import blueprint
from flask import current_app
from flask_mail import Message

@blueprint.route('/send-mail')
def send_mail():
    msg = Message('Hello', sender='your-email@example.com', recipients=['recipient@example.com'])
    msg.body = 'Hello, this is a test email!'
    mail = current_app.extensions['mail']
    mail.send(msg)
    return 'Email sent!'
