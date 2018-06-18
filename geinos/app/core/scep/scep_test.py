from app.core.scep import scep_connector
from sqlalchemy.orm import sessionmaker
from app.core.scep.scep import Scep
from app.core.scep import scep_server
from app.core.scep import scep_config
from app import engine
from flask_httpauth import HTTPBasicAuth
from app.core.device import device_access
authen = HTTPBasicAuth()
import unittest


def setUpModule():
    Session = sessionmaker(bind=engine)
    s = Session()
    s.query(Scep).delete()
    s.commit()


class TestScep(unittest.TestCase):

    def test_add_scep(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        server = "http://192.168.56.102/certsrv/mscep_admin/"
        password = "Password12"
        user_name = "Administrator"
        scep_server.add_scep(server, user_name, password)
        scep_test_server = s.query(Scep).filter\
            (Scep.server == server, Scep.username == user_name).first()
        s.commit()
        self.assertIsNotNone(scep_test_server)
    def test_get_scep_info(self):
        print(scep_server.get_thumbprint_and_otp())

    def test_config_cert(self):
        x =scep_config.format_config_cert_server("Test_CERT","192.1.2.3", "sha256", "3des_cbc")
        device_access.set_config("192.168.1.1", "admin","admin",x)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()