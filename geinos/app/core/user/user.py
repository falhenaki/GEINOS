from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app import db,app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import check_password_hash, generate_password_hash

Base = declarative_base()


class User(Base):
    """"""
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    passwordhash = Column(String)
    last_login = Column(DateTime(timezone=false))
    role_type = Column(Enum('ADMIN', 'OPERATOR'))

    #----------------------------------------------------------------------
    def __init__(self, username, password, email, role_type):
        """"""
        self.username = username
        self.hash_password(password)
        self.role_type = role_type

    def hash_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

    def update_last_login(self, login_date):
        self.last_login = login_date

    def change_role(self, role_type):
        self.role_type = role_type

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.get(User.id == data['id'])
        return user
