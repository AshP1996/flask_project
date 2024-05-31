from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from flask import current_app
from apps import db, login_manager

from apps.authentication.util import hash_pass

from time import time
import jwt


class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    role = db.Column(db.String(10), CheckConstraint("role IN ('admin', 'user')"), nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            if property == 'role' and value not in ['admin', 'user']:
                raise ValueError("Role must be either 'admin' or 'user'")

            setattr(self, property, value)

    @classmethod
    def create_user(cls, email, password, role='user'):
        return cls(email=email, password=password, role=role)
    def __repr__(self):
        return str(self.email)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
    

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(Users, id)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    # email = request.form.get('email')
    # user = Users.query.filter_by(email=email).first()
    # return user if user else None
    None
