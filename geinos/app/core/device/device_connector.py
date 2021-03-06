__author__ = 'Fawaz'
import os
from sqlalchemy.orm import sessionmaker
from app.core.device_group import device_group_connector
from app.core.device.device import Device
from app import engine, app
from app.core.log import log_connector
from app.core.template import xml_templates
from app.core.exceptions.custom_exceptions import Conflict, MissingResource, GeneralError
from app.core.scep.scep import Scep
from app.core.device_process import dev_queue
from werkzeug.utils import secure_filename
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
    if "IP" in attribute or "serial_number" in attribute:
        dev_queue.try_add_dev_queue(sn)
    s.close()
    return True

def add_device(vend, sn, mn, location, username, user_role, request_ip, cert):
    Session = sessionmaker(bind=engine)
    s = Session()
    #TODO what contitutes existing?
    query = s.query(Device).filter(Device.serial_number == sn).first()
    if query is None:
        dv = Device(vend, sn, mn, 'UNAUTHORIZED', datetime.datetime.now(), added_date=datetime.datetime.now(), location=location, cert_required=cert)
        dv.device_group = device_group_connector.get_group_of_device(dv)
        s.add(dv)
        s.commit()
        log_connector.add_log('ADD DEVICE', "Added device (vend={}, sn={}, mn={})".format(vend, sn, mn), username, user_role, request_ip)
        dev_queue.try_add_dev_queue(sn)
        s.close()
        return True
    else:
        log_connector.add_log('ADD DEVICE FAIL', "Failed to add device (vend={}, sn={}, mn={})".format(vend, sn, mn), username, user_role, request_ip)
        s.close()
        raise Conflict("Device already exists in system")

def get_all_devices():
    ret = []
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).with_entities(Device.vendor_id, Device.model_number, Device.serial_number, Device.IP)
    ret = []
    atts_returned = ['vendor_id', 'model_number', 'serial_number','IP']
    for d in query:
        dictionary = {}
        for att in atts_returned:
            dictionary[att] = getattr(d, att)
        ret.append(dictionary)
    s.close()
    return ret

def get_device(device):
    ret = []
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.serial_number == device)
    for d in query:
        ret.append(d.as_dict())
    s.close()
    return ret

def get_sn_from_ip(ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.IP == ip).first()
    s.close()
    if query is None:
        return False
    dev_ip = query.serial_number
    return dev_ip

#TODO fix device.config part
def device_exists_and_templated(sn):
    Session = sessionmaker(bind=engine)
    exists = False
    has_template = False
    s = Session()
    query = s.query(Device).filter(Device.serial_number == sn)
    device = query.first()
    if not device is None:
        exists = True
    if not device.config_file is None:
        has_template = True
    s.close()
    return exists and has_template

def get_templated_devices():
    Session = sessionmaker(bind=engine)
    s = Session()
    devices = s.query(Device)
    templated_devices =[]
    for d in devices:
        if device_exists_and_templated(d.serial_number) is True:
            templated_devices.append(d)
    s.close()
    return templated_devices

def get_rdy_config(dev):
    Session = sessionmaker(bind=engine)
    s = Session()
    d = s.query(Device).filter(Device.serial_number == dev).first()
    if ("TRUE" in d.cert_set or "FALSE" in d.cert_required) and "TRUE" in d.config_available and "." in d.IP:
        return True
    s.close()
    return False

def get_cert_or_config(dev):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.serial_number == dev).first()
    if device is None:
        return False
    cert = device.cert_required
    config = device.config_available
    cert_obt = device.cert_set
    result_dict = {'cert_req':cert,'config':config, 'cert_obt':cert_obt}
    s.close()
    return result_dict


def get_rdy_scep(device):
    Session = sessionmaker(bind=engine)
    s = Session()
    devices = s.query(Scep).first()
    if devices.thumbprint is None:
        s.close()
        return False
    if "TRUE" in device.cert_required and "." in device.IP:
        s.close()
        return True
    s.close()
    return False

def get_dev_exist(device):
    Session = sessionmaker(bind=engine)
    s = Session()
    dev = s.query(Device).filter(Device.serial_number == device).first()
    if dev is None:
        s.close()
        return False
    if '.' not in dev.IP:
        s.close()
        return False
    s.close()
    return True




#TODO Can this be moved to templates?
def set_rendered_template(sn, name, template_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.vendor_id == name, Device.serial_number == sn)
    device = query.first()
    if device is None:
        s.close()
        raise MissingResource()
    filename = secure_filename(template_name + "-" + device.vendor_id + device.serial_number + device.model_number)
    rendered_template = xml_templates.apply_parameters(template_name, '1.1.1.1', sn)
    save_path = os.path.join(app.config['APPLIED_PARAMS_FOLDER'], filename)
    with open(save_path, 'w') as fout:
        fout.write(rendered_template)
    device.set_config_file(save_path)
    device.set_config_status('TRUE')
    s.commit()
    s.close()
    return True

def remove_device(device_sns, username, user_role, request_ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    #device = s.query(Device).filter(Device.serial_number == device_sn)
    for x in device_sns:
        s.query(Device).filter(Device.serial_number == x).delete()
    #TODO move logic below to exception handling
    #if device.count() is 0:
        #log_connector.add_log('DELETE DEVICE FAIL', "Failed to remove device (sn={})".format(device_sn), username, user_role, request_ip)
        #s.close()
        #raise MissingResource("Device to be removed did not previously exist")
    #device.delete()
    log_connector.add_log('DELETE DEVICE', "Removed device (#={})".format(len(device_sns)), username, user_role, request_ip)
    s.commit()
    s.close()
    return True

def get_device_template(device_sn):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.serial_number == device_sn).first()
    s.close()
    return device.config_file, device_group_connector.get_template_for_device(device_sn)
'''
get_device_access: device access is true if device is in queue. it is false if it is not in queue or being processed.

'''
def get_device_access(device_sn):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.serial_number == device_sn).first()
    if "TRUE" in query.device_access is True:
        s.close()
        return True
    s.close()
    return False
def get_scep_fail():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device)
    result = []
    for d in query:
        if get_rdy_scep(d):
            result.append(d.serial_number)
    s.close()
    return result

def set_device_access(device_sn,state):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.serial_number == device_sn).first()
    device.device_access = state.upper()
    s.commit()
    s.close()