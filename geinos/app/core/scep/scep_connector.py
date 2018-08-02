from sqlalchemy.orm import sessionmaker
from app.core.scep.scep import Scep
from app import engine
from flask_httpauth import HTTPBasicAuth
authen = HTTPBasicAuth()



def add_scep(server,username,password,digest,encrypt,cert_info_id,ca_server_id,country,state,locale,
                 organization,org_unit,cert_server_id,key_id,ca_cert_id,client_cert_id,sys_server):
    """
    adds scep server to database. delete any existing servers first
    :param username: username to add
    :param password: password to attach to username
    :return:
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    s.query(Scep).delete()
    scep = Scep(server,username,password,digest,encrypt,cert_info_id,ca_server_id,country,state,locale,
                 organization,org_unit,cert_server_id,key_id,ca_cert_id,client_cert_id,sys_server)
    s.add(scep)
    s.commit()
    s.close()
    return True

def get_scep():
    Session = sessionmaker(bind=engine)
    s = Session()
    scep = s.query(Scep).first()
    s.close()
    return scep

def get_scep_info():
    ret = []
    Session = sessionmaker(bind=engine)
    s = Session()
    scep = s.query(Scep).first()
    atts_returned = ['username', 'password', 'server','encryptalgo','digestalgo','country','state','locale','organization','org_unit','sys_server']
    dictionary = {}
    for att in atts_returned:
        dictionary[att] = getattr(scep, att)
    ret.append(dictionary)
    s.close()
    return ret
"""
Add thumprint to server. input is a Scep object, and a string

"""


def add_thumbprint(server,thumb):
    Session = sessionmaker(bind=engine)
    s = Session.object_session(server)
    scep = server
    scep.set_thumb(thumb)
    s.add(scep)
    s.commit()
    s.close()
    return True