from app.core.template.template import Template
from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.exceptions.custom_exceptions import GeneralError, MissingResource, Conflict
import datetime

def add_file(path, filename):
    Session = sessionmaker(bind=engine)
    s = Session()
    template = Template(filename, path, datetime.datetime.now())
    s.add(template)
    s.commit()
    return True

def get_file(filename):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template).filter(Template.name == filename)
    file = query.first()
    if file:
        return file
    else:
        raise MissingResource("Could not get file location")

def template_exists(template_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template).filter(Template.name == template_name)
    if query is None:
        raise MissingResource("Template: {} could not be found", template_name)

def get_templates():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template)
    ret=[]
    for tm in query:
        ret.append(tm.as_dict())
    return ret
