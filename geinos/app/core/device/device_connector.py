__author__ = 'Fawaz'
import os
from sqlalchemy.orm import sessionmaker
from app.core.device_group.device_in_group import Device_in_Group
from app.core.device.device import Device
from app import engine, app
import datetime

def add_device(vend, sn, mn):
    Session = sessionmaker(bind=engine)
    s = Session()
    dv = Device(vend, sn, mn, 'UNAUTHORIZED','1.1.1.1', datetime.datetime.now())
    s.add(dv)
    s.commit()

def get_all_devices():
    ret = []
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device)
    for d in query:
        ret.append([d.vendor_id, d.serial_number, d.model_number])
    return ret

def device_exists_and_templated(sn, name):
    Session = sessionmaker(bind=engine)
    exists = False
    has_template = False
    s = Session()
    query = s.query(Device).filter(Device.vendor_id == name, Device.serial_number == sn)
    device = query.first()
    if device != None:
        exists = True
        query = s.query(Device_in_Group).filter(Device.vendor_id == name, Device.serial_number == sn)
        device_in_group = query.first()
        if device_in_group != None:
            has_template = True
    return exists, has_template

def set_rendered_params(sn, name, rendered_params):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.vendor_id == name, Device.serial_number == sn)
    device = query.first()
    #write_string = ''
    #for param in rendered_params:
    #    write_string += param + ':' + rendered_params[param] + '\n'
    #filename = device.vendor_id + device.serial_number +  device.model_number
   # print(filename)
    #save_path = os.path.join(app.config['APPLIED_PARAMS_FOLDER'], filename)
   # with open(save_path, 'w') as fout:
    #    fout.write(write_string)
    #device.set_config_file(save_path)
    return True

def remove_device(device_sn):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.serial_number == device_sn).delete()
    if device is 0:
        return False
    s.commit()
    return True
