from flask import Blueprint

from flask import render_template, current_app
from flask_mail import Message

blueprint = Blueprint(
    'mail_blueprint',
    __name__,
    url_prefix='/mail'
)