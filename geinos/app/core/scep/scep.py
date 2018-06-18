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
    password = Column(String)
    server = Column(String)
    encryptalgo = Column(String)
    digestalgo = Column(String)


    #----------------------------------------------------------------------
    def __init__(self, server,username,password,digest,encrypt):
        """"""
        self.username = username
        self.password = password
        self.server = server
        self.encryptalgo = encrypt
        self.digestalgo = digest
