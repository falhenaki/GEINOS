from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('mysql+mysqlconnector://admin:password@bitforcedev.se.rit.edu/se_project', echo=True)
Base = declarative_base()


class User(Base):
    """"""
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    passwordhash = Column(String)
    last_login = Column(DateTime(timezone=false))
    role_type = Column(Enum('ADMIN', 'OPERATOR'))

    #----------------------------------------------------------------------
    def __init__(self, username, passwordhash, last_login, role_type):
        """"""
        self.username = username
        self.passwordhash = passwordhash
        self.last_login = last_login
        self.role_type = role_type


class User_Group(Base):
    """"""
    __tablename__ = "User_Groups"
    role_type = Column(Enum('ADMIN', 'OPERATOR'))
    group_name = Column(String, primary_key=True)
    #----------------------------------------------------------------------
    def __init__(self, role_type, group_name):
        """"""
        self.role_type = role_type
        self.group_name = group_name


class User_in_Group(Base):
    """"""
    __tablename__ = "Users_in_Groups"
    group_name = Column(String, primary_key=True)
    user_id = Column(Integer, primary_key=True)
    #----------------------------------------------------------------------
    def __init__(self, group_name, user_id):
        """"""
        self.group_name = group_name
        self.user_id = user_id


class Device(Base):
    """"""
    __tablename__ = "Devices"
    vendor_id = Column(Integer, primary_key=True)
    serial_number = Column(Integer, primary_key=True)
    model_number = Column(Integer, primary_key=True)
    device_status = Column(Enum('UNAUTHORIZED', 'AUTHORIZED', 'PROVISIONED'))
    last_modified = Column(DateTime(timezone=false))
    IP = Column(String)
    #----------------------------------------------------------------------
    def __init__(self, vendor_id, serial_number, model_number, device_status, last_modified, IP):
        """"""
        self.vendor_id = vendor_id
        self.serial_number = serial_number
        self.model_number = model_number
        self.device_status = device_status
        self.last_modified = last_modified
        self.IP = IP

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

class Device_in_Group(Base):
    """"""
    __tablename__ = "Devices_in_Groups"
    device_group_name = Column(String, primary_key=True)
    vendor_id = Column(Integer, primary_key=True)
    serial_number = Column(Integer, primary_key=True)
    model_number = Column(Integer, primary_key=True)
    #----------------------------------------------------------------------
    def __init__(self, device_group_name, vendor_id, serial_number, model_number):
        """"""
        self.device_group_name = device_group_name
        self.vendor_id = vendor_id
        self.serial_number = serial_number
        self.model_number = model_number

# create tables
# Base.metadata.create_all(engine)