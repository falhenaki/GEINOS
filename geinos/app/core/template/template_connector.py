from app.core.template.template import Template
from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.exceptions.custom_exceptions import GeneralError, MissingResource, Conflict
import datetime
from app.core.template import xml_templates
from app.core.device_group.device_group import Device_Group

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
    query = s.query(Template).filter(Template.name == template_name)
    if not query is None:
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
    s.query(Template).filter(Template.name == name).delete()
    s.query(Device_Group).filter(Device_Group.template_name == name).update(
        {'template_name': None})
    s.commit()
    s.close()
    if xml_templates.delete_template(name, username, role_type, remote_addr):
        return True
    else:
        return False

def delete_templates(names, username, role_type, remote_addr):
    deleted = []
    not_deleted = []
    for name in names:
        if (delete_template(name, username, role_type, remote_addr)):
            deleted.append(name)
        else:
            not_deleted.append(name)
    return deleted, not_deleted