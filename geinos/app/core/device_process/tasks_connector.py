import os
from sqlalchemy.orm import sessionmaker
from app import engine, app
from app.core.exceptions.custom_exceptions import Conflict, MissingResource, GeneralError
from app.core.device_process import dev_queue
from app.core.device_process.tasks import Tasks
import datetime


def add_task(sn,status):
    Session = sessionmaker(bind=engine)
    s = Session()
    task = s.query(Tasks).filter(Tasks.serial_number == sn).first()
    if task is not None:
        delete_task(sn)
    task = Tasks(sn,status)
    s.add(task)
    s.commit()
    s.close()

def get_all_tasks():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Tasks).with_entities(Tasks.serial_number, Tasks.status)
    ret = []
    atts_returned = ['serial_number', 'status']
    for d in query:
        dictionary = {}
        for att in atts_returned:
            dictionary[att] = getattr(d, att)
        ret.append(dictionary)
    s.close()
    return ret

def delete_task(serial_number):
    Session = sessionmaker(bind=engine)
    s = Session()
    task = s.query(Tasks).filter(Tasks.serial_number == serial_number)
    task.delete()
    s.commit()
    s.close()

def update_task(serial_number, status):
    Session = sessionmaker(bind=engine)
    s = Session()
    task = s.query(Tasks).filter(Tasks.serial_number == serial_number).first()
    task.status = status
    s.commit()
    s.close()
