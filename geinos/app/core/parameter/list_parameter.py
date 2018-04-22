from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class ListParameter(Base):
    __tablename__ = "ListParameters"
    param_name = Column(String, primary_key=True)
    param_value = Column(String, primary_key=True)
    # ----------------------------------------------------------------------
    def __init__(self,name,val):
        self.param_name = name
        self.param_value = val