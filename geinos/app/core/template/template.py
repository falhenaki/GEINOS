from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.sqlalchemy_base.augmented_base import CustomMixin

Base = declarative_base()

class Template(CustomMixin, Base):
    """"""
    __tablename__ = "Templates"
    name = Column(String, primary_key=True)
    date_created = Column(DateTime(timezone=false))
    # ----------------------------------------------------------------------
    def __init__(self, name, date_created):
        self.date_created = date_created
        self.name = name