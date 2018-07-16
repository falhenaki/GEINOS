from app.core.device.device import Device
from app.core.device import device_connector
from app.core.device_group.device_group import Device_Group
from app.core.device_group.device_in_group import Device_in_Group
from app.core.exceptions.custom_exceptions import Conflict, MissingResource
from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.device_process import dev_queue
import datetime
from app.core.parameter import parameter_connector
from app import app
import os
from jinja2 import Environment, meta
from app.core.log import log_connector
import ast

def add_device_group(name, att, val, username, role_type, remote_addr):
    Session = sessionmaker(bind=engine)
    s = Session()
    existence_check = s.query(Device_Group).filter(Device_Group.device_group_name == name).first()
    if existence_check is not None:
        s.close()
        raise Conflict("Device Group already exists")
    '''existence_check = s.query(Device_Group).filter(Device_Group.attribute_value == att+val).first()
    if existence_check is not None:
        raise Conflict("Device Group already exists")'''
    if att == "other":
        dict = {}
        val = val.split(',')
        for ele in val:
            item = ele.split('=')
            dict[item[0].strip()] = item[1].strip()
        att_val = str(dict)
        num_atts = len(val)
    else:
        num_atts = 1
        att_val = str({att : val})

    dg = Device_Group(name,datetime.datetime.now(), att_val, num_atts=num_atts)
    log_connector.add_log('ADD DEVICE GROUP', "Added {} device group (att: {})".format(name, att), username, role_type, remote_addr)
    update_groups_of_devices(dg)
    s.add(dg)
    s.commit()
    s.close()
    return True

def devices_in_group(new_group):
    Session = sessionmaker(bind=engine)
    s = Session()
    att_vals = ast.literal_eval(new_group.attribute_value)
    devices = list(s.query(Device))
    ret = []
    for i, device in enumerate(devices):
        in_group = True
        for key in att_vals:
            if (getattr(device, key) != att_vals[key]):
                in_group = False
                break
        if in_group:
            ret.append(devices[i])
    s.close()
    return ret

def devices_in_group_objects(group_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    devices = s.query(Device).filter(Device.device_group == group_name)
    return devices


def update_groups_of_devices(new_group):
    Session = sessionmaker(bind=engine)
    s = Session()
    devices = devices_in_group(new_group)
    for device in devices:
        if new_group.num_attributes >= device.device_group_filters:
            s.query(Device).filter(Device.serial_number == device.serial_number).update(
                {'device_group_filters': new_group.num_attributes, 'device_group': new_group.device_group_name})
    dev_queue.try_add_group_queue(new_group)
    s.commit()
    s.close()

def device_group_exists(group_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_Group).filter(Device_Group.device_group_name == group_name).first()
    s.close()
    return (query is not None)

def get_all_device_groups():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_Group).with_entities(Device_Group.device_group_name, Device_Group.template_name, Device_Group.last_modified)
    ret = []
    atts_returned = ['device_group_name', 'template_name', 'last_modified']
    for d in query:
        dictionary = {}
        for att in atts_returned:
            dictionary[att] = getattr(d, att)
        ret.append(dictionary)
    s.close()
    return ret

def get_all_devices_in_group(g_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    dict_string = s.query(Device_Group).filter(Device_Group.device_group_name == g_name).with_entities(Device_Group.attribute_value).first()
    if dict_string is None:
        s.close()
        raise MissingResource("Device Group does not exist")
    devices = s.query(Device).filter(Device.device_group == g_name)
    ret = []
    for x in devices:
        ret.append(x.as_dict())
    s.close()
    return ret

#TODO Check groups and templates exist
def assign_template(group_name, template_name, username, user_role, request_ip):
    if group_name is None or template_name is None: # or not device_group_exists(group_name) or not template_connector.template_exists(template_name):
        log_connector.add_log('ASSIGN FAIL', "Failed to assign {} to {}".format(template_name, group_name), username, user_role, request_ip)
        raise MissingResource("Template or device group does not exist")

    xml_file = os.path.join(app.config['UPLOADS_FOLDER'], template_name)
    all_vars = []
    with open(xml_file, 'r') as f:
        env = Environment()
        s = f.read()
        ast = env.parse(s)
        all_vars.extend(meta.find_undeclared_variables(ast))
    devs_in_groups = number_of_devices_in_group(group_name)
    for var in all_vars:
        if not (parameter_connector.parameter_exists(var) or (parameter_connector.number_of_parameter(var) != 1 and parameter_connector.number_of_parameter(var) < devs_in_groups)):
            return False
    Session = sessionmaker(bind=engine)
    s = Session()
    dg = s.query(Device_Group).filter(Device_Group.device_group_name == group_name).first()
    dg.template_name = template_name
    dg.last_updated = datetime.datetime.now()
    devices = devices_in_group_objects(group_name)
    #todo actually set config status correctly
    for d in devices:
        print(d)
        d.set_config_status("TRUE")
    s.commit()
    dev_queue.try_add_group_queue(group_name)
    log_connector.add_log('ASSIGN', "Assigned {} to {}".format(template_name, group_name), username, user_role, request_ip)
    s.close()
    return True

def number_of_devices_in_group(group_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    count = s.query(Device).filter(Device.device_group == group_name).count()
    s.close()
    return

def get_template_for_device(sn):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.serial_number == sn).first()
    device_group_name = device.device_group
    device_group = s.query(Device_Group).filter(Device_Group.device_group_name == device_group_name).first()
    if device_group is None:
        s.close()
        raise MissingResource("Device Group does not exist")
    if device_group.template_name == None:
        s.close()
        raise MissingResource("Device group does not have an assigned template")
    s.close()
    return device_group.template_name

def remove_group(group_name, username, user_role, request_ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    device_group = s.query(Device_Group).filter(Device_Group.device_group_name == group_name)
    if device_group.first() is None:
        log_connector.add_log('DELETE DEVICE GROUP FAIL', "Tried to remove {} device group which does not exist".format(group_name), username, user_role, request_ip)
        s.close()
        raise MissingResource("Device group being removed does not exist")
    device_group.delete()
    if device_group is 0:
        log_connector.add_log('DELETE DEVICE GROUP FAIL', "Failed to remove {} device group".format(group_name), username, user_role, request_ip)
        s.close()
        return False

    no_group_devices = s.query(Device).filter(Device.device_group == group_name)
    dgs = s.query(Device_Group).orderby(Device_Group.num_attributes.desc(), Device_Group.last_modified.desc())

    for dg in dgs:
        if (no_group_devices.count() == 0):
            break
        digs = devices_in_group(dg.device_group_name)
        overlap = list(set(digs) & set(no_group_devices))
        if (len(overlap) > 0):
            serials = [x.serial_number for x in overlap]
            s.query(Device).filter(Device.serial_number == serials).update({'group_name' : dg.device_group_name, 'device_group_filters' : dg.num_attributes})
            no_group_devices = list(set(no_group_devices) - set(overlap))

    remaining_serials = [x.serial_number for x in no_group_devices]
    s.query(Device).filter(Device.serial_number == remaining_serials).update({'group_name': None, 'device_group_filters': 0})
    s.commit()
    s.close()
    log_connector.add_log('DELETE DEVICE GROUP', "Removed {} device group".format(group_name), username, user_role, request_ip)
    return True
