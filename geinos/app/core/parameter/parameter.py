from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Parameter(Base):
    __tablename__ = "Parameters"
    param_name = Column(String, primary_key=True)
    start_value = Column(String)
    end_value = Column(String)
    current_offset = Column(String)
    param_type = Column(Enum('RANGE', 'SCALAR', 'LIST'))
    date_created = Column(DateTime(timezone=false))
    # ----------------------------------------------------------------------
    def __init__(self, name,start,ptype,end=""):
        self.param_name = name
        self.start_value = start
        self.end_value = end
        self.param_type = ptype
        self.current_offset = start
