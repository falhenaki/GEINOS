from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.api import request_parser
from app.core.device_process import tasks_connector
authen = HTTPBasicAuth()


class Tasks(Resource):

    def get(self):
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            dgs = tasks_connector.get_all_tasks()
            return jsonify(
                status=200,
                message="Sent Tasks",
                auth_token=auth_token,
                data=dgs
            )
        else:
            return jsonify(
                auth_token=auth_token,
                status=401,
                message="Unauthorized"
            )
