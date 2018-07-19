from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.device.device_access import *
from app.core.api import request_parser
from app.core.device import device_connector
from app.core.template import xml_templates

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
    def post(self):
        status=400
        message = "Configs not created"
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            content = request.parse_json()
            device_sn = content['device_sn']
            config_path, template_path = device_connector.get_device_template(device_sn)
            rendered_template = xml_templates.parse_config_params(config_path, template_path, device_sn)
        return jsonify(
            status=status,
            message=message,
            data=rendered_template
        )