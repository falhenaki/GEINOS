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

##### Devices
    def test_Devices_no_auth_get(self):
        response = self.app.get('/devices')
        data = json.loads(response.data)
        print(data)
        assert(data['status'] == 401)
        assert(data['message'] == "Unauthorized")

    def test_Devices_no_auth_put(self):
        response = self.app.put('/devices')
        data = json.loads(response.data)
        print(data)
        assert(data['status'] == 401)
        assert(data['message'] == "Unauthorized")
"""
# Device Groups
    def test_get_Device_Groups_no_auth_post(self):

        response = self.app.post('/device_groups')
        assert response == jsonify(
                status=400,
                message=failAuth
        )
    def test_get_Device_Groups_no_auth_put(self):

        response = self.app.put('/devices_groups')
        assert response == jsonify(
                status=400,
                message=failAuth
        )
    def test_get_Device_Groups_no_auth_post(self):

        response = self.app.put('/devices')
        assert response == jsonify(
                status=400,
                message=failAuth
        )

    def test_login_auth_post(self):
        username = "test"
        password = "password"
        response = self.app.post('/login', data=dict(
                username="fawaz",
                password="password"
            ), follow_redirects=True)
        data = json.loads(response.data)
        assert(data['status'] == 200)
        assert(data['message'] == 'User logged in')

    def test_users_auth_put(self):
        response = self.app.put('/users', data=dict(
                username="guy",
                password="hispassword",
                retyppassword = "hispassword",
                email = "guy@hotmail.com",
                role = "ADMIN"
            ))
        assert response == jsonify(
                status=200,
                message="User added"
        )
        assert db_connector.get_user("guy") != None

    def test_users_auth_delete(self):
        db_connector.add_user("man", "passwd11", "man@gmail.com", "OPERATOR")
        response = self.app.delete('/users', data=dict(
                rmusr="guy",
            ))
        assert response == jsonify(
                status=200,
                message="User Deleted"
        )
        assert db_connector.get_user("guy") == None

    #DEVICE AUTHED

    def test_get_Device_Groups_auth_get(self):

        response = self.app.get('/device_groups')
        assert response == jsonify(
                status=200,
                message="Sent Devices"
        )
        data = json.loads(response.data)
        assert(data['status'] == 400)
        assert(data['message'] == 'Sent Devices')
        assert(data['data'] != None)

    def test_get_Device_auth_put(self):

        response = self.app.put('/devices', data=dict(
                vendor_id="1",
                serial_num = "2",
                model_num = "3"

            ))
        assert response == jsonify(
                status=200,
                message="Device Added"
        )
        data = json.loads(response.data)
        assert(data['status'] == 200)
        assert(data['message'] == 'Sent Devices')
        assert(data['data'] != None)
        assert db_connector.get_all_devices() != None


    def test_get_Device_auth_get(self):
        db_connector.add_device("111", "2222", "3333")
        response = self.app.get('/devices')
        assert response == jsonify(
                status=200,
                message="Device Added"
        )
        data = json.loads(response.data)
        assert(data['status'] == 200)
        assert(data['message'] == 'Sent Devices')
        assert(data['data'] != None)
        assert db_connector.get_all_devices() != None


    def test_get_Device_auth_put(self):

        response = self.app.put('/devices', data=dict(
                vendor_id="1",
                serial_num = "2",
                model_num = "3"

            ))
        assert response == jsonify(
                status=200,
                message="Device Added"
        )
        data = json.loads(response.data)
        assert(data['status'] == 200)
        assert(data['message'] == 'Sent Devices')
        assert(data['data'] != None)
        assert db_connector.get_all_devices() != None

"""
####  Parameters

if __name__ == '__main__':
    unittest.main()
