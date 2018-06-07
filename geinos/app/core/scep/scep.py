from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app import db,app
from app.core.user import user_connector
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import check_password_hash, generate_password_hash
from app.core.sqlalchemy_base.augmented_base import CustomMixin

Base = declarative_base()


class Scep(CustomMixin, Base):
    """"""
    __tablename__ = "Scep"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    passwordhash = Column(String)
    server = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, server,username,password):
        """"""
        self.username = username
        self.hash_password(password)
        self.server = server
    """
    For Now do not salt password.    
    """
    def hash_password(self, password):
        self.passwordhash = password

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)