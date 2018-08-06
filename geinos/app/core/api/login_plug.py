from flask_restful import Resource
from flask import request, jsonify
from app.core.user import auth
from app.core.user import user_connector
from app.core.log import log_connector
from app.core.api import request_parser

import time

class Login(Resource):
    """
    HTTP Method: POST
    Authorization: Required
    Authorization type: (username and password)
    Description : Login for user and privde authtoken
    :return:
    Success: status= 200, message= "User logged in.", auth_token= (generated token):unused
    Failure: status: 400, "User not logged in."
    """
    def post(self):
        print("Log in attempt")
        if request.authorization:
            POST_USERNAME = request.authorization["username"]
            POST_PASSWORD = request.authorization["password"]
            print(POST_USERNAME + " attempting to login")
            # we are making sure username and password both exist before logging in
            if POST_USERNAME and POST_PASSWORD and auth.login(POST_USERNAME, POST_PASSWORD):
                auth.update_user_login(POST_USERNAME)
                usr = user_connector.get_user(POST_USERNAME)
                print(POST_USERNAME + " Logged in")
                log_connector.add_log('LOGIN', "Logged in successfully", usr.username, usr.role_type, request.remote_addr)
                return jsonify(
                    status=200,
                    message="User logged in.",
                    auth_token=usr.generate_auth_token().decode('ascii') + ":unused"
                )
            else:
                log_connector.add_log('LOGIN FAIL', "Failed login attempt (username: {})".format(POST_USERNAME), None, None, request.remote_addr)
        else:
            log_connector.add_log('LOGIN FAIL', "Failed login attempt", None, None, request.remote_addr)
        return jsonify(
            status=400,
            message="Incorrect Password"
        )

class Login_Helper(Resource):
    def get(self):
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if logged_user:
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            return jsonify(
                auth_token=auth_token,
                status=200,
                message="User logged in."
            )
        return jsonify(
                auth_token=auth_token,
                status=403,
                message="Incorrect Password."
            )
