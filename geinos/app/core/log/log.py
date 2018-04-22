from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Log(Base):
    """"""
    __tablename__ = "Logs"
    log_id = Column(Integer, primary_key=True)
    event_type = Column(Integer)
    log_message = Column(String)
    user = Column(String)
    role = Column(Enum('ADMIN', 'OPERATOR'))
    date_created = Column(DateTime(timezone=false))
    # ----------------------------------------------------------------------
    def __init__(self, log_id, event_type, log_message, user, role, date_created):
        """"""
        self.log_id = log_id
        self.event_type = event_type
        self.log_message = log_message
        self.user = user
        self.role = role
        self.date_created = date_created