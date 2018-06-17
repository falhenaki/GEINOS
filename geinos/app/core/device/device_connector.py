__author__ = 'Fawaz'
import os
from sqlalchemy.orm import sessionmaker
from app.core.device_group.device_in_group import Device_in_Group
from app.core.device.device import Device
from app import engine, app
from app.core.log import log_connector
from app.core.exceptions.custom_exceptions import Conflict, MissingResource, GeneralError
import datetime

def update_device(sn, attribute, value):
    Session = sessionmaker(bind=engine)
    s = Session()
    #TODO what contitutes existing?
    device = s.query(Device).filter(Device.serial_number == sn).first()
    device.__setattr__(attribute, value)
    s.commit()

def add_device(vend, sn, mn, location, username, user_role, request_ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    #TODO what contitutes existing?
    query = s.query(Device).filter(Device.serial_number == sn).first()
    if query is None:
        dv = Device(vend, sn, mn, 'UNAUTHORIZED','1.1.1.1', datetime.datetime.now(), added_date=datetime.datetime.now(), location=location)
        s.add(dv)
        s.commit()
        log_connector.add_log(1, "Added device (vend={}, sn={}, mn={})".format(vend, sn, mn), username, user_role, request_ip)
        return True
    else:
        log_connector.add_log(1, "Failed to add device (vend={}, sn={}, mn={})".format(vend, sn, mn), username, user_role, request_ip)
        raise Conflict("Device already exists in system")
        return False

def get_all_devices():
    ret = []
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device)
    for d in query:
        ret.append(d.as_dict())
    return ret

def device_exists_and_templated(sn, name, do_both_exist=False):
    Session = sessionmaker(bind=engine)
    exists = False
    has_template = False
    s = Session()
    query = s.query(Device).filter(Device.vendor_id == name, Device.serial_number == sn)
    device = query.first()
    if device is None:
        raise MissingResource("Device has not been added")
    query = s.query(Device_in_Group).filter(Device.vendor_id == name, Device.serial_number == sn)
    device_in_group = query.first()
    if device_in_group is None: #TODO check if device group has a template assigned
        raise MissingResource("Device is not assigned to a group")
    return True

def set_rendered_params(sn, name, rendered_params): #TODO add back in functionality to save params to a file
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.vendor_id == name, Device.serial_number == sn)
    device = query.first()
    if device is None:
        raise MissingResource()
    write_string = ''
    for param in rendered_params:
        write_string += param + ':' + rendered_params[param] + '\n'
    filename = device.vendor_id + device.serial_number +  device.model_number
    print(filename)
    save_path = os.path.join(app.config['APPLIED_PARAMS_FOLDER'], filename)
    with open(save_path, 'w') as fout:
        fout.write(write_string)
    device.set_config_file(save_path)
    return True

def remove_device(device_sn, username, user_role, request_ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.serial_number == device_sn)
    if device is None:
        raise MissingResource("Device to be removed did not previously exist")
    device.delete()
    if device is 0:
        log_connector.add_log(1, "Failed to delete device (sn={})".format(device_sn), username, user_role, request_ip)
        raise GeneralError("Device could not be removed")
    log_connector.add_log(1, "Added device (sn={})".format(device_sn), username, user_role, request_ip)
    s.commit()
    return True

def get_device_template(device_sn):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.serial_number == device_sn)
    return device.config_file