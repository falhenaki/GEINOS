from app.core.scep import scep_connector
from sqlalchemy.orm import sessionmaker
from app.core.scep.scep import Scep
from app.core.scep import scep_server
from app import engine
from flask_httpauth import HTTPBasicAuth
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
        server = "1.1.1.1"
        password = "testPassword"
        user_name = "test"
        scep_server.add_scep(server, user_name, password)
        scep_test_server = s.query(Scep).filter\
            (Scep.server == server, Scep.username == user_name).first()
        s.commit()
        self.assertIsNotNone(scep_test_server)




if __name__ == '__main__':
    unittest.main()