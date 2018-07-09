from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.sqlalchemy_base.augmented_base import CustomMixin
Base = declarative_base()

class Radius(CustomMixin, Base):
    __tablename__ = "Radius"
    host = Column(String, primary_key=True)
    port = Column(Integer)
    secret = Column(String)
    # ----------------------------------------------------------------------
    def __init__(self, secret, host, port):
        self.secret = secret
        self.host = host
        self.port = port
