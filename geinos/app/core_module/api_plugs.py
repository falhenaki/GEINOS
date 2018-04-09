from flask_restful import Resource
from flask import request, jsonify, session, render_template
from app.core_module import auth,db_connector,device_helpers
from app import app
from flask_httpauth import HTTPBasicAuth
from app.pyorbit_module import Device
from app.pyorbit_module.services import Config

authen = HTTPBasicAuth()
def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

def user_logged_in():
    if not 'username' in session:
        return False
    else:
        return True

class Login(Resource):
    #@app.route('/', methods=['POST'])
    def post(self):
        POST_USERNAME = request.authorization["username"]
        POST_PASSWORD = request.authorization["password"]
        if auth.login(POST_USERNAME, POST_PASSWORD):
            auth.update_user_login(POST_USERNAME)
            usr = db_connector.get_user(POST_USERNAME)

            return jsonify(
                status=200,
                message="User logged in.",
                auth_token=usr.generate_auth_token().decode('ascii') + ":unused"
            )
        else:

            return jsonify(
                status=400,
                message="User not logged in."
            )
    def get(self):
        return jsonify(
            status=200,
            message="You are at the homepage"
        )

class Users(Resource):
    #@authen.login_required
    def get(self):
        if (auth.login(request.authorization["username"],request.authorization["password"])):
            all_users = db_connector.get_all_users()
            return jsonify(
                status=200,
                message="Sent all users.",
                data=all_users
            )
        else:
            return jsonify(
                status=400,
                message="Could not authenticate"
            )
    def put(self):
        user_added = True
        status = 400
        message = "User not added"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            POST_USERNAME = request.form['usr']
            POST_PASSWORD = request.form['password']
            POST_RETYPE_PASS = request.form['retypepassword']
            POST_EMAIL = request.form['email']
            POST_ROLE = str(request.form['role'])
            if POST_PASSWORD == POST_RETYPE_PASS:
                if auth.add_user(POST_USERNAME, POST_PASSWORD, POST_EMAIL, POST_ROLE):
                    auth.change_user_role(POST_USERNAME, POST_ROLE)
                    status=200
                    message = "User added"
        return jsonify(
            status=status,
            message=message
        )
    def delete(self):
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            POST_USERNAME = request.form['rmusr']
            auth.remove_user(POST_USERNAME)
            return jsonify(
                status=200,
                message="Users Deleted"
            )

class Devices(Resource):
    def get(self):
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            devices = db_connector.get_all_devices()
            return jsonify(
                status=200,
                message="Sent Devices",
                data=devices
            )
        else:
            return jsonify(
                status=400,
                message="Could not send devices"
            )
    def put(self):
        status = 400
        message = "Device not added"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            if 'file' not in request.files:
                VENDOR_ID = request.form['vendor_id']
                SERIAL_NUMBER = request.form['serial_num']
                MODEL_NUMBER = request.form['model_num']
                db_connector.add_device(VENDOR_ID, SERIAL_NUMBER, MODEL_NUMBER)
                status=200
                message="Device Added"
            else:
                file = request.files['file']
                file_data = file.readlines()
                content = [str(x,'utf-8').strip().split(',') for x in file_data]
                if device_helpers.add_list_of_devices(content):
                    status=200
                    message="Devices Added"
        return jsonify(
            status=status,
            message=message
        )

class Device_Groups(Resource):
    def get(self):
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            dgs = db_connector.get_all_device_groups()
            return jsonify(
                status=200,
                message="Sent Device Groups",
                data=dgs
            )
        else:
            return jsonify(
                status=400,
                message="Could not send device groups"
            )
    def put(self):
        status=400
        message="Device Group not added"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            group_name = request.form["group_name"]
            db_connector.add_device_group(group_name)
            status=200
            message="Device group added"
        return jsonify(
            status=status,
            message=message
        )
    def post(self):
        status = 400
        message = "Device(s) not added to group"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            group_name = request.form["group_name"]
            atrbute = request.form["attribute"]
            db_connector.add_devices_to_groups(group_name,atrbute)
            status=200
            message="Device(s) added to group"
        return jsonify(
            status=status,
            message=message
        )

class Parameters(Resource):
    def get(self):
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            prms = db_connector.get_all_parameters()
            return jsonify(
                status=200,
                message="Sent Parameters",
                data=prms
            )
        else:
            return jsonify(
                status=400,
                message="Could not send parameters"
            )
    def put(self):
        status = 400
        message = "Parameter not added"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            name = request.form["name"]
            ptype = request.form["type"]
            val = request.form["value"]
            db_connector.add_parameter(name,ptype.upper(),val)
            status = 200
            message = "Parameter added"
        return jsonify(
            status=status,
            message=message
        )

class Device_Configs(Resource):
    def put(self):
        status=400
        message = "Configs not created"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            hst = request.form["host"]
            usr = request.form["username"]
            passw = request.form["pass"]
            dev = Device(host=hst,username=usr,password=passw)
            dev.open()
            with Config(dev) as cm:
                out = cm.get(format='json')
                print(out)