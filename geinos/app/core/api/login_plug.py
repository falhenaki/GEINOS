from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.user import auth
from app.core.user import user_connector
from  app.core.api import request_parser

authen = HTTPBasicAuth()

class Login(Resource):
    #@app.route('/', methods=['POST'])
    def post(self):
        if request.authorization:
            POST_USERNAME = request.authorization["username"]
            POST_PASSWORD = request.authorization["password"]
            if auth.login(POST_USERNAME, POST_PASSWORD):
                auth.update_user_login(POST_USERNAME)
                usr = user_connector.get_user(POST_USERNAME)

                return jsonify(
                    status=200,
                    message="User logged in.",
                    auth_token=usr.generate_auth_token().decode('ascii') + ":unused"
                )

        return jsonify(
            status=400,
            message="User not logged in."
        )
    def get(self):
        return jsonify(
            status=200,
            message="You are at the homepage"
        )
