from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from genios_app import app

engine = create_engine('sqlite:///genios_db.db', echo=True)
Base = declarative_base()
db = SQLAlchemy(app)


class User(db.Model):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = db.Column(db.String(128))
    email = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, username, password, email):
        """"""
        self.username = username
        self.create_password_hash(password)
        self.email = email

    def create_password_hash(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

# create tables
db.Model.metadata.create_all(engine)