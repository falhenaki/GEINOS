from app.core.device.device import Device
from app.core.device_group.device_group import Device_Group
from app.core.device_group.device_in_group import Device_in_Group
from sqlalchemy.orm import sessionmaker, session
from app import engine
import datetime
from flask_httpauth import HTTPBasicAuth

authen = HTTPBasicAuth()


def add_device_group(name):
    Session = sessionmaker(bind=engine)
    s = Session()
    dg = Device_Group(name,datetime.datetime.now())
    s.add(dg)
    s.commit()

def get_all_device_groups():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_Group)
    dgs=[]
    for dg in query:
        dgs.append(dg.device_group_name)
    return dgs

def add_devices_to_groups(group_name, att, val):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_Group).filter(Device_Group.device_group_name == group_name).first()
    if query is None:
        add_device_group(group_name)
    if att == "model":
        q = s.query(Device).filter(Device.model_number == val).first()
        dig = Device_in_Group(group_name, q.vendor_id, q.serial_number, q.model_number)
        s.add(dig)
        s.commit()
    else:
        print("Work in progress")