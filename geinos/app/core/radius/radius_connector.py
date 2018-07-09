from app.core.parameter.parameter import Parameter
from app.core.parameter.list_parameter import ListParameter
from app.core.log import log_connector
from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.exceptions.custom_exceptions import Conflict, GeneralError, MissingResource, InvalidInput
import ipaddress
from app.core.device.device import Device
from app.core.device import device_access
from app.core.radius.radius import Radius
import radius

def authenticate_user(username, password):
    Session = sessionmaker(bind=engine)
    s = Session()
    result = s.query(Radius).first()
    if result is None:
        return True
    r = radius.Radius(result.secret, result.host, result.port)
    return r.authenticate(username, password)

def get_radius_settings():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Radius)
    ret = []
    atts_returned = ['host', 'port', 'secret']
    for d in query:
        dictionary = {}
        for att in atts_returned:
            dictionary[att] = getattr(d, att)
        ret.append(dictionary)
    return ret

def set_radius_settings(host, port, secret):
    Session = sessionmaker(bind=engine)
    s = Session()
    result = s.query(Radius).first()
    if result is None:
        newRadius = Radius(secret, host, port)
        s.add(newRadius)
    else:
        s.query(Radius).update(
            {'host': host,
             'port': port,
             'secret': secret})
    s.commit()
    return True