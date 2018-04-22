from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Device_in_Group(Base):
    """"""
    __tablename__ = "Devices_in_Groups"
    device_group_name = Column(String, primary_key=True)
    vendor_id = Column(String, primary_key=True)
    serial_number = Column(String, primary_key=True)
    model_number = Column(String, primary_key=True)
    #----------------------------------------------------------------------
    def __init__(self, device_group_name, vendor_id, serial_number, model_number):
        """"""
        self.device_group_name = device_group_name
        self.vendor_id = vendor_id
        self.serial_number = serial_number
        self.model_number = model_number