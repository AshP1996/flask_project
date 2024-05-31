from flask_mail import Message
from flask import current_app
from apps import mail

def send_email(to, subject, body):
    msg = Message(
        subject,
        recipients=[to],
        body=body,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
    print(f"Sent email to: {to}")  # Debug statement
