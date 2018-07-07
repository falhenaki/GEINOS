from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.sqlalchemy_base.augmented_base import CustomMixin
Base = declarative_base()

class Device_Group_Filter(CustomMixin, Base):
    """"""
    __tablename__ = "Device_Group_Filter"
    device_group_name = Column(String, primary_key=True)
    filter = Column(String, primary_key=True)
    filter_value = Column(String)
    #----------------------------------------------------------------------
    def __init__(self, device_group_name, filter, filter_value):
        """"""
        self.device_group_name = device_group_name
        self.filter = filter
        self.filter_value = filter_value

