from app.core.device.device import Device
from app.core.device_group.device_group import Device_Group
from app.core.device_group.device_in_group import Device_in_Group
from sqlalchemy.orm import sessionmaker
from app import engine
import datetime

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
    dgs={}
    for dg in query:
        dgs.append([dg.device_group_name, dg.last_modified, dg.template_name])
    return dgs

def get_devices_in_group(g_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_in_Group).filter(Device_in_Group.device_group_name == g_name)
    #ret = []
    #for x in query:
        #ret.append([x.vendor_id, x.serial_number, x.model_number])
    return query

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

def assign_template(group_name, template_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    dg = s.query(Device_Group).filter(Device_Group.device_group_name == group_name).first()
    if dg is None:
        return False
    dg.template_name = template_name
    dg.last_updated = datetime.datetime.now()
    s.commit()

def get_template_for_device(sn, vn):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_in_Group).filter(Device_in_Group.serial_number == sn, Device_in_Group.vendor_id == vn)
    device_in_group = query.first()
    device_group_name = device_in_group.device_group_name
    device_group = s.query(Device_Group).filter(Device_Group.device_group_name == device_group_name).first()
    return device_group.template_name