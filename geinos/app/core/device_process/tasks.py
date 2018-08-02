from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.sqlalchemy_base.augmented_base import CustomMixin
Base = declarative_base()

class Tasks(CustomMixin, Base):
    """"""
    __tablename__ = "Tasks"
    serial_number = Column(String, primary_key=True)
    status = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, serial,status):
        """"""
        self.serial_number = serial
        self.status = status
