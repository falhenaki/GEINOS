from flask_restful import Resource
from flask import request, jsonify
from app.core.device.device_access import *
from  app.core.api import request_parser

class Device_Configs(Resource):
    """
    HTTP Method: GET
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters (Form): host (string), username (String), pass (String)
    Description : Retrieves a given device config
    :return:
    Success: status: 200, message: "ok", configs: tbd
    Failure: status: 400, message: "Configs not created"
    """
    def get(self):
        status=400
        message = "Configs not created"
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            hst = request.form["host"]
            usr = request.form["username"]
            passw = request.form["pass"]
            #TODO actually return configs, also, should device auth be passed in auth request?
            conf = get_config(hst,usr,passw)
            status=200
            message="ok"
        return jsonify(
            status=status,
            message=message
        )