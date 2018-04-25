__author__ = 'Fawaz'
from sqlalchemy.orm import sessionmaker
from app.core.device.device import Device
from app import engine
import datetime

def add_device(vend, sn, mn):
    Session = sessionmaker(bind=engine)
    s = Session()
    dv = Device(vend, sn, mn, 'UNAUTHORIZED','1.1.1.1', datetime.datetime.now())
    s.add(dv)
    s.commit()

def get_all_devices():
    ret = []
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device)
    for d in query:
        ret.append([d.vendor_id, d.serial_number, d.model_number])
    return ret
