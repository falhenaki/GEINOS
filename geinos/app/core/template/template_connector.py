from app.core.template.template import Template
from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.exceptions.custom_exceptions import GeneralError, MissingResource, Conflict
import datetime
import app
from app import app
from app.core.template import xml_templates
from app.core.device_group.device_group import Device_Group
from app.core.device.device import Device
import os

def add_file(filename):
    Session = sessionmaker(bind=engine)
    s = Session()
    template = Template(filename, datetime.datetime.now())
    s.add(template)
    s.commit()
    s.close()
    return True

def template_exists(template_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template).filter(Template.name == template_name).count()
    if query == 0:
        s.close()
        return False
    s.close()
    return True

def get_templates():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template)
    ret=[]
    for tm in query:
        ret.append(tm.as_dict())
    s.close()
    return ret

def delete_template(name, username, role_type, remote_addr):
    print("delete_template from database start: " + str(name) + " " + username + " " +role_type + " " + remote_addr)
    Session = sessionmaker(bind=engine)
    s = Session()
    xml_templates.delete_template(name, username, role_type, remote_addr)
    tmp = s.query(Template).filter(Template.name == name).first()
    template_path = os.path.join(app.config["UPLOADS_FOLDER"], tmp.name)
    if os.path.exists(template_path):
        os.remove(template_path)
    s.delete(tmp)
    s.commit()
    grps = s.query(Device_Group).filter(Device_Group.template_name == name)
    for grp in grps:
        cur = s.query(Device_Group).filter(Device_Group.device_group_name == grp.device_group_name).first()
        cur.template_name = None
        s.commit()
    dvs = s.query(Device).filter(str(Device.config_file).split('-')[0] == name)
    for dv in dvs:
        cur = s.query(Device).filter(Device.serial_number == dv.serial_number).first()
        cur.config_file = None
        s.commit()
    s.commit()
    print("Commited deletion of template: {}".format(name))
    s.close()
    return True


def delete_templates(names, username, role_type, remote_addr):
    print("delete_templates start: " + str(names) + " " + username + " " +role_type + " " + remote_addr)
    deleted = []
    not_deleted = []
    for name in names:
        print("Template from list to be deleted:" + name)
        if (delete_template(name, username, role_type, remote_addr)):
            deleted.append(name)
        else:
            not_deleted.append(name)
    return deleted, not_deleted