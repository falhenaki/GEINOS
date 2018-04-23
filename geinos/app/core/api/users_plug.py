from flask_restful import Resource
from flask import request, jsonify, session
from flask_httpauth import HTTPBasicAuth
from app.core.user import auth
from app.core.user import user_connector
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
def validateCreds(request):
    if request.authorization:
        if request.authorization["username"]:
            username = request.authorization["username"]
        if request.authorization["password"]:
            password = request.authorization["password"]
        else:
            password = ""
        return auth.login(username,password)

class Users(Resource):
    #@authen.login_required
    #@genios_decorators.requires_roles("ADMIN")
    def get(self):

        #if (auth.login(request.authorization["username"],request.authorization["password"])):


        if(validateCreds(request)):
            all_users = user_connector.get_all_users()
            return jsonify(
                status=200,
                message="Sent all users.",
                data=all_users
            )
        return jsonify(
            status=400,
            message="Could not authenticate"
        )
    def put(self):
        status = 400
        message = "Could not authenticate"
        if(validateCreds(request)):
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
        if(validateCreds(request)):
            POST_USERNAME = request.form['rmusr']
            auth.remove_user(POST_USERNAME)
            return jsonify(
                status=200,
                message="Users Deleted"
            )
        return jsonify(
            status=400,
            message="Could not authenticate"
        )