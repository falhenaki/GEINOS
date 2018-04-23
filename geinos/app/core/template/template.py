from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Template(Base):
    """"""
    __tablename__ = "Templates"
    name = Column(String, primary_key=True)
    date_created = Column(DateTime(timezone=false))
    template_file = Column(String)
    # ----------------------------------------------------------------------
    def __init__(self, name, template_file, date_created):
        self.date_created = date_created
        self.template_file = template_file
        self.name = name