from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.sqlalchemy_base.augmented_base import CustomMixin
Base = declarative_base()

class Log(CustomMixin, Base):
    """"""
    __tablename__ = "Logs"
    log_id = Column(Integer, primary_key=True)
    event_type = Column(Integer)
    log_message = Column(String)
    user = Column(String)
    role = Column(Enum('ADMIN', 'OPERATOR'))
    IP = Column(Integer)
    date_created = Column(DateTime(timezone=false))
    # ----------------------------------------------------------------------
    def __init__(self, log_id, event_type, log_message, user, role, ip, date_created):
        """"""
        self.log_id = log_id
        self.event_type = event_type
        self.log_message = log_message
        self.user = user
        self.role = role
        self.IP = ip
        self.date_created = date_created
