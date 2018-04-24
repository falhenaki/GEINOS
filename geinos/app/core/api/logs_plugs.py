from flask_restful import Resource
from flask import request, jsonify
from app.core.log import log_connector
from  app.core.api import request_parser

class Logs(Resource):
    def get(self):
        if (request_parser.validateCreds(request)):
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