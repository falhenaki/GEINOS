from flask_restful import Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from flask import request, jsonify
from app.core.device import device_helpers, device_connector
from app.core.api import request_parser

parser = reqparse.RequestParser()
authen = HTTPBasicAuth()

class Register(Resource):
    """
    HTTP Method: POST
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters (form): serial-number (String), name (String), device_ip (String)
    Description : API for devices to request templates to be applied based on their device group.
    :return:
    Success: status= 200, message = 'Template has been applied,
    Failure:
        status: 401, message = 'Device does not currently exist'
        status: 402, message = "Device has not yet been assigned a template"

    """
    def post(self):
        """
        API for devices to request templates to be applied based on their device group
        :return: 402 if the device has not been added 401 if there is no template assigned to device group
        200 if assignment was sucessful
        """
       
        status = 400
        """
        TODO: Require authorization, needs to be changed in orbit device
        """
        if True:
            content = request.get_json()
            print(content)
            device_sn = content['serial-number']
            device_name = content['name']
            device_ip = content['ip-address']
            print(content)
            #device_usern = request.form['device_user']
            device_usern = "admin"
            #device_pass = request.form['device_pass']
            device_pass = "admin"
            '''
            device_exists, has_template = device_connector.device_exists_and_templated(device_sn, device_name)
            if not device_exists:
                    status=402
                    message="Device does not currently exist"
            if not has_template:
                    status=401,
                    message="Device has not yet been assigned a template"
            '''
            if device_helpers.apply_template(device_sn, device_name, device_ip,
                                             device_usern, device_pass):
                status = 200
                message = "Device Configured"

        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )
