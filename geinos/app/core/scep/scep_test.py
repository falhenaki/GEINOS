from app.core.scep import scep_connector
from sqlalchemy.orm import sessionmaker
from app.core.scep.scep import Scep
from app.core.scep import scep_server
from app.core.scep import scep_config
from app import engine
from flask_httpauth import HTTPBasicAuth
from queue import Queue
import threading
from app.core.device import device_access
authen = HTTPBasicAuth()
import unittest


def setUpModule():
    Session = sessionmaker(bind=engine)
    s = Session()
    s.query(Scep).delete()
    s.commit()
    s.close()

class TestScep(unittest.TestCase):

    def test_add_scep(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        server = "http://192.168.56.102/certsrv/mscep_admin/"

        password = "Password12"
        user_name = "Administrator"
        digest = "a"
        encrypt = "b"
        cert_info_id = "c"
        ca_server = "d"
        country = "e"
        state = "f"
        locale = "g"
        organization = "h"
        org_unit = "i"
        cert_server_id = "j"
        key_id = "k"
        ca_cert_id = "l"
        client_cert_id = "m"

        scep_server.add_scep(server, user_name, password, digest,encrypt,cert_info_id,ca_server,country,state,locale,
                             organization,org_unit,cert_server_id,key_id,ca_cert_id,client_cert_id)
        scep_test_server = s.query(Scep).filter\
            (Scep.server == server, Scep.username == user_name).first()
        s.commit()
        self.assertIsNotNone(scep_test_server)
        self.assertIs(scep_test_server.digestalgo,digest)
        self.assertIs(scep_test_server.encryptalgo, encrypt)
        self.assertIs(scep_test_server.cert_info_id, cert_info_id)
        self.assertIs(scep_test_server.ca_server_id, ca_server)
        self.assertIs(scep_test_server.country, country)
        self.assertIs(scep_test_server.state,state)
        self.assertIs(scep_test_server.locale,locale)
        self.assertIs(scep_test_server.organization,organization)
        self.assertIs(scep_test_server.org_unit,org_unit)
        self.assertIs(scep_test_server.cert_server_id,cert_server_id)
        self.assertIs(scep_test_server.key_id,key_id)
        self.assertIs(scep_test_server.ca_cert_id,ca_cert_id)
        self.assertIs(scep_test_server.client_cert_id,client_cert_id)
    def test_get_otp(self):
        x = scep_server.get_otp()
        print("\nOTP: " + x)
        self.assertNotIn("Error",x)

    def test_get_thumbprint(self):
        x = scep_server.get_thumbprint()
        print("Thumbprint: " + x)
        self.assertNotIn("Error", x)
    def test_add_thumbprint(self):
        x = scep_connector.get_scep()
        y = scep_connector.add_thumbprint(x,"abcd")
        z = x.thumbprint
        self.assertEqual('abcd', z)


if __name__ == '__main__':
    unittest.main()