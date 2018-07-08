from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.sqlalchemy_base.augmented_base import CustomMixin

Base = declarative_base()

class Device_Group(CustomMixin, Base):
    """"""
    __tablename__ = "Device_Groups"
    device_group_name = Column(String,primary_key=True)
    last_modified = Column(DateTime(timezone=false))
    template_name = Column(String)
    attribute_value = Column(String)
    num_attributes = Column(Integer)
    #----------------------------------------------------------------------
    def __init__(self, device_group_name, last_modified, attribute_value, template_name=None, num_atts=None):
        """"""
        self.device_group_name = device_group_name
        self.last_modified = last_modified
        self.template_name = template_name
        self.attribute_value = attribute_value
        self.num_attributes = num_atts

