from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.log.log import Log
import datetime

def get_all_logs():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Log).with_entities(Log.user, Log.IP, Log.event_type, Log.log_message, Log.date_created)
    ret = []
    atts_returned = ['user', 'IP', 'event_type', 'log_message', 'date_created']
    for d in query:
        dictionary = {}
        for att in atts_returned:
            dictionary[att] = getattr(d, att)
        ret.append(dictionary)
    s.close()
    return ret

def add_log(event_type, log_message, user, role, ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    dv = Log(None, event_type, log_message, user, role, ip, datetime.datetime.now())
    s.add(dv)
    s.commit()
    s.close()
    engine.dispose()
