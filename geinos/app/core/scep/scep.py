from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.sqlalchemy_base.augmented_base import CustomMixin

Base = declarative_base()


class Scep(CustomMixin, Base):

    __tablename__ = "Scep"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    server = Column(String)
    #TODO make algo's enums instead of strings
    encryptalgo = Column(String)
    digestalgo = Column(String)
    cert_info_id = Column(String)
    ca_server_id = Column(String)
    country = Column(String)
    state = Column(String)
    locale = Column(String)
    organization = Column(String)
    org_unit = Column(String)
    cert_server_id  = Column(String)
    key_id = Column(String)
    ca_cert_id = Column(String)
    client_cert_id = Column(String)
    thumbprint = Column(String)
    sys_server = Column(String)



    #----------------------------------------------------------------------
    def __init__(self, server,username,password,digest,encrypt,cert_info_id,ca_server_id,country,state,locale,
                 organization,org_unit,cert_server_id,key_id,ca_cert_id,client_cert_id):
        """"""
        self.username = username
        self.password = password
        self.server = server
        self.encryptalgo = encrypt
        self.digestalgo = digest
        self.cert_info_id = cert_info_id
        self.ca_server_id = ca_server_id
        self.country = country
        self.state = state
        self.locale = locale
        self.organization = organization
        self.org_unit = org_unit
        self.cert_server_id = cert_server_id
        self.key_id = key_id
        self.ca_cert_id = ca_cert_id
        self.client_cert_id = client_cert_id
        self.sys_server = server

    def set_thumb(self,thumbprint):
        self.thumbprint = thumbprint