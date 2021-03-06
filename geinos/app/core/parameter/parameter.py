from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.sqlalchemy_base.augmented_base import CustomMixin
Base = declarative_base()

class Parameter(CustomMixin, Base):
    __tablename__ = "Parameters"
    param_name = Column(String, primary_key=True)
    start_value = Column(String)
    end_value = Column(String)
    current_offset = Column(String)
    param_type = Column(Enum('RANGE', 'SCALAR', 'LIST', 'DYNAMIC'))
    date_created = Column(DateTime(timezone=false))
    interface = Column(String)
    # ----------------------------------------------------------------------
    def __init__(self, name,start,ptype,end="", interface=None):
        self.param_name = name
        self.start_value = start
        self.end_value = end
        self.param_type = ptype
        self.current_offset = start
        self.interface = interface
