from sqlalchemy import *
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.sqlalchemy_base.augmented_base import CustomMixin
Base = declarative_base()

class Device(CustomMixin, Base):
    """"""
    __tablename__ = "Devices"
    vendor_id = Column(String, primary_key=True)
    serial_number = Column(String, primary_key=True)
    model_number = Column(String, primary_key=True)
    device_status = Column(Enum('UNAUTHORIZED', 'AUTHORIZED', 'PROVISIONED'))
    last_modified = Column(DateTime(timezone=false))
    username = Column(String)
    password = Column(String)
    IP = Column(String) # 3
    config_file = Column(String)
    date_added = Column(DateTime(timezone=false))
    date_authorized = Column(DateTime(timezone=false))
    date_provisioned = Column(DateTime(timezone=false))
    location = Column(String)
    cert_required = Column(Enum('TRUE','FALSE')) # 2
    device_group = Column(String)
    cert_set = Column(Enum('TRUE','FALSE','FAIL'))
    device_group_filters = Column(Integer)
    device_access = Column(Enum('TRUE','FALSE'))
    config_available = Column(Enum('TRUE', 'FALSE')) #available 1

    #----------------------------------------------------------------------
    def __init__(self, vendor_id, serial_number, model_number, device_status, last_modified, username="admin", password="admin",
                 config_file=None, added_date=None, location=None, cert_required = 'FALSE', group_name=None, num_filters=0):
        """"""
        self.vendor_id = vendor_id
        self.serial_number = serial_number
        self.model_number = model_number
        self.device_status = device_status
        self.last_modified = last_modified
        self.username = username
        self.password = password
        self.config_file = config_file
        self.date_added = added_date
        self.location = location
        self.IP = ""
        self.cert_required = cert_required
        self.device_group = group_name
        self.device_group_filters = num_filters
        self.cert_set = "FALSE"
        self.device_access = 'FALSE'
        self.config_available = 'FALSE' #Change this to config available

    def set_config_file(self, config_file):
        self.config_file = config_file

    def set_add_date(self, added):
        self.date_added = added

    def set_authorized_date(self, authorized):
        self.date_authorized = authorized

    def set_provisioned_date(self, provisioned):
        self.date_provisioned = provisioned

    def set_ip(self,ip):
        self.IP = ip
    def set_cert_req(self,required):
        self.cert_required = required
    def set_cert_set(self,status):
        self.cert_set = status
    def set_config_status(self,status):
        self.config_available = status
