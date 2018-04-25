from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Device(Base):
    """"""
    __tablename__ = "Devices"
    vendor_id = Column(String, primary_key=True)
    serial_number = Column(String, primary_key=True)
    model_number = Column(String, primary_key=True)
    device_status = Column(Enum('UNAUTHORIZED', 'AUTHORIZED', 'PROVISIONED'))
    last_modified = Column(DateTime(timezone=false))
    username = Column(String)
    password = Column(String)
    IP = Column(String)
    config_file = Column(String)
    #----------------------------------------------------------------------
    def __init__(self, vendor_id, serial_number, model_number, device_status, IP, last_modified, username=None, password=None,
                 config_file=None):
        """"""
        self.vendor_id = vendor_id
        self.serial_number = serial_number
        self.model_number = model_number
        self.device_status = device_status
        self.last_modified = last_modified
        self.IP = IP
        self.username = username
        self.password = password
        self.config_file = config_file

    def set_config_file(self, config_file):
        self.config_file = config_file

