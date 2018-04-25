from flask_restful import Resource
from flask import request, jsonify
from app.core.device.device_access import *
from  app.core.api import request_parser

class Device_Configs(Resource):
    def get(self):
        status=400
        message = "Configs not created"
        if (request_parser.validateCreds(request)):
            hst = request.form["host"]
            usr = request.form["username"]
            passw = request.form["pass"]
            conf = get_config(hst,usr,passw)
            status=200
            message="ok"
        return jsonify(
            status=status,
            message=message
        )