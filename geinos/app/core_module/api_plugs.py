from flask_restful import Resource
from flask import request, jsonify, session, render_template
from app.core_module import auth,db_connector,device_helpers
from app import app
from flask_httpauth import HTTPBasicAuth
authen = HTTPBasicAuth()

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

class HelloWorld(Resource):
    def get(self):
        dic = {"frst" : "Qasim", "last" : "Ali"}
        dd = [["a","e"],["b"],"c","d"]
        return jsonify(
            hello = dd,
            status = "success",
            message = "nothin",
        )
        #return {'hello': 'world'}

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
            if POST_PASSWORD != POST_RETYPE_PASS:
                user_added = False
            else:
                if auth.add_user(POST_USERNAME, POST_PASSWORD, POST_EMAIL, POST_ROLE):
                    auth.change_user_role(POST_USERNAME, POST_ROLE)
                else:
                    user_added = False
        else:
            user_added = False

        if (user_added):
            status=200,
            message="User added"
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
            file = request.files['file']
            if not file:
                VENDOR_ID = request.form['vendor_id']
                SERIAL_NUMBER = request.form['serial_num']
                MODEL_NUMBER = request.form['model_num']
                db_connector.add_device(VENDOR_ID, SERIAL_NUMBER, MODEL_NUMBER)
                status=200
                message="Device Added"
            else:
                file_data = file.readlines()
                content = [x.strip() for x in file_data]
                device_helpers.add_list_of_devices(content)
                status=200
                message="Devices Added"
        return jsonify(
            status=status,
            message=message
        )


