from flask_restful import Resource
from flask import request, jsonify,send_file,make_response,send_from_directory
from flask_httpauth import HTTPBasicAuth
from app.core.device.device_access import *
from app.core.api import request_parser
from app.core.device import device_connector
from app.core.template import xml_templates
import xml.etree.ElementTree as ET
import io



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
    def POST(self,device=None):
        print("dsakjfsdkjlhadskfhsdkj")
        status=400
        message = "Configs not created"
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            if device is None:
                return jsonify(
                    status=status,
                    message=message,
                )

            config_path, template_path = device_connector.get_device_template(device)
            rendered_template = xml_templates.parse_config_params(config_path, template_path, device)
            return jsonify(
                status=status,
                message=message,
                data=rendered_template,

            )
        else:
            return jsonify(
                status=401,
                message="Unauthorized"
            )
