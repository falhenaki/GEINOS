__author__ = 'Fawaz'
import os
from sqlalchemy.orm import sessionmaker
from app.core.device_group.device_in_group import Device_in_Group
from app.core.device_group import device_group_connector
from app.core.device.device import Device
from app import engine, app
from app.core.log import log_connector
from app.core.template import xml_templates
from app.core.exceptions.custom_exceptions import Conflict, MissingResource, GeneralError
import datetime

#TODO Log update
def update_device(sn, attribute, value):
    Session = sessionmaker(bind=engine)
    s = Session()
    #TODO what contitutes existing?
    device = s.query(Device).filter(Device.serial_number == sn).first()
    try:
        getattr(device,attribute)
    except AttributeError:
        return False
    device.__setattr__(attribute, value)
    s.commit()
    return True

def add_device(vend, sn, mn, location, username, user_role, request_ip, cert):
    Session = sessionmaker(bind=engine)
    s = Session()
    #TODO what contitutes existing?
    query = s.query(Device).filter(Device.serial_number == sn).first()
    if query is None:
        dv = Device(vend, sn, mn, 'UNAUTHORIZED', datetime.datetime.now(), added_date=datetime.datetime.now(), location=location, cert_required=cert)
        s.add(dv)
        s.commit()
        log_connector.add_log('ADD DEVICE', "Added device (vend={}, sn={}, mn={})".format(vend, sn, mn), username, user_role, request_ip)
        return True
    else:
        log_connector.add_log('ADD DEVICE FAIL', "Failed to add device (vend={}, sn={}, mn={})".format(vend, sn, mn), username, user_role, request_ip)
        raise Conflict("Device already exists in system")

def get_all_devices():
    ret = []
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).with_entities(Device.vendor_id, Device.model_number, Device.serial_number)
    ret = []
    atts_returned = ['vendor_id', 'model_number', 'serial_number']
    for d in query:
        dictionary = {}
        for att in atts_returned:
            dictionary[att] = getattr(d, att)
        ret.append(dictionary)
    return ret

def get_device(device):
    ret = []
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.serial_number == device)
    for d in query:
        ret.append(d.as_dict())
    return ret

def device_exists_and_templated(sn):
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

def get_templated_devices():
    Session = sessionmaker(bind=engine)
    s = Session()
    devices = s.query(Device)
    templated_devices =[]
    for d in devices:
        if device_exists_and_templated(d.serial_number) is True:
            templated_devices.append(d)
    return templated_devices

def get_devices_exist_and_scep():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.IP.like("%.%.%"),Device.cert_required == "TRUE",Device.cert_set == "FALSE")
    if query is None:
        return False
    return query

#TODO Can this be moved to templates?
def set_rendered_template(sn, name, template_name): #TODO add back in functionality to save params to a file
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.vendor_id == name, Device.serial_number == sn)
    device = query.first()
    if device is None:
        raise MissingResource()
    filename = device.vendor_id + device.serial_number + device.model_number
    print(filename)
    rendered_template = xml_templates.apply_parameters(template_name, '1.1.1.1', sn)
    save_path = os.path.join(app.config['APPLIED_PARAMS_FOLDER'], filename)
    with open(save_path, 'w') as fout:
        fout.write(rendered_template)
    device.set_config_file(save_path)
    s.commit()
    return True

def remove_device(device_sn, username, user_role, request_ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.serial_number == device_sn)
    if device.count() is 0:
        log_connector.add_log('DELETE DEVICE FAIL', "Failed to remove device (sn={})".format(device_sn), username, user_role, request_ip)
        raise MissingResource("Device to be removed did not previously exist")
    device.delete()
    log_connector.add_log('DELETE DEVICE', "Removed device (sn={})".format(device_sn), username, user_role, request_ip)
    s.commit()
    return True

def get_device_template(device_sn):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.serial_number == device_sn)
    return device.config_file, device_group_connector.get_template_for_device(device_sn)

