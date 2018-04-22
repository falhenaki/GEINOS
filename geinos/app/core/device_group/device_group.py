from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Device_Group(Base):
    """"""
    __tablename__ = "Device_Groups"
    device_group_name = Column(String,primary_key=True)
    last_modified = Column(DateTime(timezone=false))
    #----------------------------------------------------------------------
    def __init__(self, device_group_name, last_modified):
        """"""
        self.device_group_name = device_group_name
        self.last_modified = last_modified

