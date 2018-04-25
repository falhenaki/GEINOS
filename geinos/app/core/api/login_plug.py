from flask_restful import Resource
from flask import request, jsonify
from app.core.user import auth
from app.core.user import user_connector

class Login(Resource):
    def post(self):
        if request.authorization:
            POST_USERNAME = request.authorization["username"]
            POST_PASSWORD = request.authorization["password"]
            # we are making sure username and password both exist before logging in
            if POST_USERNAME and POST_PASSWORD and auth.login(POST_USERNAME, POST_PASSWORD):
                print(POST_USERNAME)
                print(POST_PASSWORD)
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