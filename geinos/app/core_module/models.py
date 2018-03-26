from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from app import db,app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash

#engine = create_engine('mysql+mysqlconnector://admin:password@bitforcedev.se.rit.edu/se_project', echo=True)
#db = SQLAlchemy(__init__)

import requests, os
from werkzeug.security import check_password_hash, generate_password_hash
def simple_ping():
  """
  Basic test ping to check if the Orbit device can be reached
  :return: response from device
  """
  APP_ROUTE = os.path.dirname(os.path.abspath(__file__))
  APP_STATIC = os.path.join(APP_ROUTE, 'static')
  filepath = 'body.txt'

  with open(os.path.join(APP_STATIC, filepath)) as fh:
    data = fh.read()

  headers = {'Accept':'application/xml', 'Content-Type' : 'application/xml'}
  r = requests.put('http://localhost:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/new-netconf-device', headers = headers, data = data, auth=('admin', 'admin'))


  return r

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
    def __init__(self, username, password, email, role_type):
        """"""
        self.username = username
        self.hash_password(password)
        self.role_type = role_type

    def hash_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

    def update_last_login(self, login_date):
        self.last_login = login_date

    def change_role(self, role_type):
        self.role_type = role_type

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

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
    def __init__(self, vendor_id, serial_number, model_number, device_status, IP, last_modified=null):
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

class Log(Base):
    """"""
    __tablename__ = "Logs"
    log_id = Column(Integer, primary_key=True)
    event_type = Column(Integer)
    log_message = Column(String)
    user = Column(String)
    role = Column(Enum('ADMIN', 'OPERATOR'))
    date_created = Column(DateTime(timezone=false))
    # ----------------------------------------------------------------------
    def __init__(self, log_id, event_type, log_message, user, role, date_created):
        """"""
        self.log_id = log_id
        self.event_type = event_type
        self.log_message = log_message
        self.user = user
        self.role = role
        self.date_created = date_created

# create tables
# Base.metadata.create_all(engine)