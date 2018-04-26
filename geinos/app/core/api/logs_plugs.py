from flask_restful import Resource
from flask import request, jsonify
from app.core.log import log_connector
from  app.core.api import request_parser

class Logs(Resource):
    """
    HTTP Method: GET
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Description : Retrieves all logs
    :return:
    Success: status= 200, message= "Sent Logs", data= logs(json)
    Failure: status= 400, message= "Could not send Logs"
    """
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