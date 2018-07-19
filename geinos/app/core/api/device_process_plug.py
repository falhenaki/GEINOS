from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.api import request_parser
from app.core.device_process import tasks_connector
authen = HTTPBasicAuth()


class Tasks(Resource):

    def get(self):
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            dgs = tasks_connector.get_all_tasks()
            return jsonify(
                status=200,
                message="Sent Tasks",
                data=dgs
            )
        else:
            return jsonify(
                status=401,
                message="Unauthorized"
            )