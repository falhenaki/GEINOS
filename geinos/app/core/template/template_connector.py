from app.core import Template
from sqlalchemy.orm import sessionmaker
from app import engine
import datetime
from flask_httpauth import HTTPBasicAuth

authen = HTTPBasicAuth()

def add_file(file, filename):
    Session = sessionmaker(bind=engine)
    s = Session()
    template = Template(filename, file, datetime.datetime.now())
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

def replace_template(filename, file):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Template).filter(Template.name == filename)
    xml_file = query.first()
    xml_file.file = file
    s.commit()

