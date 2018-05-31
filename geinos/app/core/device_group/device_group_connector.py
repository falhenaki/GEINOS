from app.core.device.device import Device
from app.core.device_group.device_group import Device_Group
from app.core.device_group.device_in_group import Device_in_Group
from app.core.log import log_connector
from app.core.template import template_connector
from sqlalchemy.orm import sessionmaker
from app import engine
import datetime

def add_device_group(name):
    Session = sessionmaker(bind=engine)
    s = Session()
    dg = Device_Group(name,datetime.datetime.now())
    s.add(dg)
    s.commit()

def device_group_exists(group_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_in_Group).filter(Device_in_Group.device_group_name == group_name).first()
    return (query is not None)

def get_all_device_groups():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_Group)
    dgs=[]
    for dg in query:
        dgs.append(dg.as_dict())
    return dgs

def get_devices_in_group(g_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_in_Group).filter(Device_in_Group.device_group_name == g_name)
    #ret = []
    #for x in query:
        #ret.append([x.vendor_id, x.serial_number, x.model_number])
    return query

def add_devices_to_groups(group_name, att, val, username, role_type, remote_addr):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_Group).filter(Device_Group.device_group_name == group_name).first()
    if query is None:
        add_device_group(group_name)
        log_connector.add_log(1, "Added {} device group (att: {}, value:{})".format(group_name, att, val), username, role_type, remote_addr)
    if att == "model":
        devices = s.query(Device).filter(Device.model_number == val)
        for q in devices:
            dig = Device_in_Group(group_name, q.vendor_id, q.serial_number, q.model_number)
            s.add(dig)
        s.commit()
        log_connector.add_log(1, "Added devices with {} = {} to {} device group".format(att, val, group_name), username,
                              role_type, remote_addr)
        return True
    else:
        print("Work in progress")
        log_connector.add_log(1, "Failed to add devics (with {} = {}) to {} device group".format(att, val, group_name), username,
                              role_type, remote_addr)
        return False

def assign_template(group_name, template_name, username, user_role, request_ip):
    if group_name is None or template_name is None or not device_group_exists(group_name) or not template_connector.template_exists(template_name):
        log_connector.add_log(1, "Failed to assign {} to {}".format(template_name, group_name), username, user_role, request_ip)
        return False
    Session = sessionmaker(bind=engine)
    s = Session()
    dg = s.query(Device_Group).filter(Device_Group.device_group_name == group_name).first()
    dg.template_name = template_name
    dg.last_updated = datetime.datetime.now()
    s.commit()
    log_connector.add_log(1, "Assigned {} to {}".format(template_name, group_name), username, user_role, request_ip)
    return True

def get_template_for_device(sn, vn):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_in_Group).filter(Device_in_Group.serial_number == sn, Device_in_Group.vendor_id == vn)
    device_in_group = query.first()
    device_group_name = device_in_group.device_group_name
    device_group = s.query(Device_Group).filter(Device_Group.device_group_name == device_group_name).first()
    return device_group.template_name

def remove_group(group_name, username, user_role, request_ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    device_group = s.query(Device_Group).filter(Device_Group.device_group_name == group_name).delete()
    if device_group is 0:
        log_connector.add_log(1, "Failed to remove {} device group".format(group_name), username, user_role, request_ip)
        return False
    s.commit()
    log_connector.add_log(1, "Removed {} device group".format(group_name), username, user_role, request_ip)
    return True
