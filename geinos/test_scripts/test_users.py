import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from app import create_app, engine
#from app.core.api import initialize
#from app.core.user import auth, user_connector
import unittest
import tempfile
import app
import base64
from app.core.api import initialize
from flask import jsonify, json
from app.core.device import device_connector
from werkzeug.datastructures import Headers
failAuth = "Could not authenticate."
from requests.auth import HTTPBasicAuth

class FlaskrTestCase(unittest.TestCase):


    def create_app(self):

        # pass in test configuration
        return app.create_app(self)

    setup_done = False
    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.testing = True
        self.app = app.app.test_client()
        with app.app.app_context():
            app.init_db()
        if not FlaskrTestCase.setup_done:
            initialize.initialize_APIs()
            FlaskrTestCase.setup_done = True

        ## adding users

        app.core.user.auth.add_user("fawaz", "password","test@mail.edu", "ADMIN", "test", "ADMIN", "192.168.1.1")

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_Dalive(self):

        rv = self.app.get('/users')
        data = json.loads(rv.data)
        print(data)
        assert(data['status'] == 401)
        assert(str(data['message']) == str("Unauthorized"))

    def open_with_auth(self, url, method, username, password):
        return self.app.open(url,
            method=method,
            headers={
                'Authorization': b'Basic ' + base64.b64encode((username + b":" + password))
            }
        )
    def test_login_noauth_post(self):
        username = "test"
        password = "password"
        response = self.open_with_auth('/login', 'POST', b'test',
                                  b'password')
        data = json.loads(response.data)
        assert(data['status'] == 200)
        assert(data['message'] == 'User logged in.')
    def test_login_noauthentication_post(self):
        username = b"ss"
        password = b"passworssddasd"
        response = self.open_with_auth('/login', 'POST', username,
                                  password)
        data = json.loads(response.data)
        print(data)
        assert(data['status'] == 400)
        assert(data['message'] == 'User not logged in.')


    def test_get_users_auth_get(self):
        username = "test"
        password = "password"
        response = self.open_with_auth('/login', 'POST', b'test',
                                  b'password')
        data = json.loads(response.data)
        print(data["auth_token"])
        headers={
            'Authorization': b'Basic ' + base64.b64encode(str.encode(data["auth_token"]))
        }
        response = self.app.get('/users',headers = headers)
        data = json.loads(response.data)
        assert(data['status'] == 200)
        assert(data['message'] == 'Sent all users.')

    def test_users_no_auth_put(self):
        response = self.app.put('/users')
        data = json.loads(response.data)
        print(data)
        assert(data['status'] == 401)
        assert(data['message'] == 'Unauthorized')

    def test_users_auth_delete(self):
        response = self.app.delete('/users')
        data = json.loads(response.data)
        print(data)
        assert(data['status'] == 401)
        assert(data['message'] == 'Unauthorized')

    def test_users_no_auth_delete(self):
        response = self.app.delete('/users')
        data = json.loads(response.data)
        print(data)
        assert(data['status'] == 401)
        assert(data['message'] == 'Unauthorized')

if __name__ == '__main__':
    unittest.main()
