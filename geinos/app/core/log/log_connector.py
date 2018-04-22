from sqlalchemy.orm import sessionmaker
from app import engine
from app.core import Log
from flask_httpauth import HTTPBasicAuth

authen = HTTPBasicAuth()



def get_all_logs():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Log)
    logList=[]
    for log in query:
        logList.append([log.user, log.log_message])
    return logList