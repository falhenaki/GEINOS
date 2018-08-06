from app.core.template.template import Template
from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.exceptions.custom_exceptions import GeneralError, MissingResource, Conflict
import datetime
import app
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
    Session = sessionmaker(bind=engine)
    s = Session()
    if not xml_templates.delete_template(name, username, role_type, remote_addr):
        return False
    tmp = s.query(Template).filter(Template.name == name).first()
    template_path = os.path.join(app.config["UPLOADS_FOLDER"], tmp.name)
    if os.path.exists(template_path):
        os.remove(template_path)
    s.delete(tmp)
    s.query(Device_Group).filter(Device_Group.template_name == name).update(
        {'template_name': None})
    s.query(Device).filter(name in Device.config_file).update({'config_file': None})
    s.commit()
    s.close()
    return True


def delete_templates(names, username, role_type, remote_addr):
    deleted = []
    not_deleted = []
    for name in names:
        if (delete_template(name, username, role_type, remote_addr)):
            deleted.append(name)
        else:
            not_deleted.append(name)
    return deleted, not_deleted