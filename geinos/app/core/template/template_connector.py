from app.core.template.template import Template
from sqlalchemy.orm import sessionmaker
from app import engine
import datetime

def add_file(path, filename):
    Session = sessionmaker(bind=engine)
    s = Session()
    template = Template(filename, path, datetime.datetime.now())
    print('adding to db')
    s.add(template)
    print(path)
    print(template.name)
    print(template.template_file)
    s.commit()
    print('commit')
    return True

def get_file(filename):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template).filter(Template.name == filename)
    file = query.first()
    if file:
        return file
    return None

def template_exists(template_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template).filter(Template.name == template_name)
    return (query is not None)

def get_template_names():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template)
    ret=[]
    for tm in query:
        ret.append([tm.name])
    return ret
