import os
from geinos.app import create_app, engine
from geinos.app.core_module import initialize, auth, db_connector
import geinos.app
import unittest
import tempfile
from geinos.app import core_module
from flask import jsonify, json
failAuth = "Could not authenticate."

class FlaskrTestCase(unittest.TestCase):


    def create_app(self):

        # pass in test configuration
        return create_app(self)

    setup_done = False
    def setUp(self):
        self.db_fd, geinos.app.app.config['DATABASE'] = tempfile.mkstemp()
        geinos.app.app.testing = True
        self.app = geinos.app.app.test_client()
        with geinos.app.app.app_context():
            geinos.app.init_db()
       # print("setup")
        if not FlaskrTestCase.setup_done:
            geinos.app.core_module.initialize.initialize_APIs()
            FlaskrTestCase.setup_done = True

        ## adding users

        auth.add_user("fawaz", "password","test@mail.edu", "ADMIN")

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(geinos.app.app.config['DATABASE'])

    def test_Dalive(self):
        with geinos.app.app.test_client() as c:
            rv = c.get('/')
            data = json.loads(rv.data)

        assert(data['status'] == 200)
        assert(str(data['message']) == str("You are at the homepage"))

    def test_login_noauth_post(self):
        username = "test"
        password = "password"
        print("55555555555")
        response = self.app.post('/login', auth=('fawaz', 'test'), follow_redirects=True)
        data = json.loads(response.data)
        assert(data['status'] == 400)
        assert(data['message'] == 'User not logged in.')

    def test_get_users_no_auth_get(self):
        response = self.app.get('/users')
        assert response == jsonify(
                status=400,
                message=failAuth
        )
    def test_users_no_auth_put(self):
        response = self.app.put('/users')
        assert response == jsonify(
                status=400,
                message=failAuth
        )

    def test_users_auth_delete(self):
        response = self.app.delete('/users')
        assert response == jsonify(
                status=400,
                message=failAuth
        )

    def test_users_no_auth_delete(self):
        response = self.app.delete('/users')
        assert response == jsonify(
                status=400,
                message=failAuth
        )

##### Devices
    def test_Devices_no_auth_get(self):
        response = self.app.get('/devices')
        assert response == jsonify(
                status=400,
                message=failAuth
        )
    def test_Devices_no_auth_put(self):
        response = self.app.put('/devices')
        assert response == jsonify(
                status=400,
                message=failAuth
        )

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


####  Parameters

if __name__ == '__main__':
    unittest.main()