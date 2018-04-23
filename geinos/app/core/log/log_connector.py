from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.log.log import Log
from flask_httpauth import HTTPBasicAuth
import datetime

authen = HTTPBasicAuth()

def get_all_logs():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Log)
    logList=[]
    for log in query:
        logList.append([log.user, log.log_message])
    return logList

def add_log(event_type, log_message, user, role):
    Session = sessionmaker(bind=engine)
    s = Session()
    dv = Log(event_type, log_message, user, role, datetime.datetime.now())
    s.add(dv)
    s.commit()