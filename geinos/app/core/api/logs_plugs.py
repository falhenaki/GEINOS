from flask_restful import Resource
from flask import request, jsonify, session
from flask_httpauth import HTTPBasicAuth
from app.core.user import auth
from app.core.log import log_connector
authen = HTTPBasicAuth()
class Logs(Resource):
    def get(self):
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            lgs = log_connector.get_all_logs()
            return jsonify(
                status=200,
                message="Sent Logs",
                data=lgs
            )
        else:
            return jsonify(
                status=400,
                message="Could not send Logs"
            )