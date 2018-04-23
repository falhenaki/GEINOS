from app.core.template.template import Template
from sqlalchemy.orm import sessionmaker
from app import engine
import datetime
from flask_httpauth import HTTPBasicAuth

authen = HTTPBasicAuth()

def add_file(path, filename):
    Session = sessionmaker(bind=engine)
    s = Session()
    template = Template(filename, path, datetime.datetime.now())
    s.add(template)
    s.commit()

def get_file(filename):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template).filter(Template.name == filename)
    file = query.first()
    if file:
        return file
    return None

def get_template_names():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template)
    ret=[]
    for tm in query:
        ret.append([tm.name])
    return ret
