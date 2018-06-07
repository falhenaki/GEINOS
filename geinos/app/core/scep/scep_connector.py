from sqlalchemy.orm import sessionmaker
from app.core.scep.scep import Scep
from app import engine
from flask_httpauth import HTTPBasicAuth
authen = HTTPBasicAuth()



def add_scep(server,username, password):
    """
    adds user to the database
    :param username: username to add
    :param password: password to attach to username
    :return:
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    scep = Scep(server,username, password)
    s.add(scep)
    s.commit()

def get_scep():
    Session = sessionmaker(bind=engine)
    s = Session()
    scep = s.query(Scep).first()
    return scep


