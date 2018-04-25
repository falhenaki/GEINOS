from flask_restful import Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from flask import request, jsonify
from app.core.device import device_helpers, device_connector
from app.core.api import request_parser

parser = reqparse.RequestParser()
authen = HTTPBasicAuth()

class Register(Resource):
    def post(self):
        """
        API for devices to request templates to be applied based on their device group
        :return: 402 if the device has not been added 401 if there is no template assigned to device group
        200 if assignment was sucessful
        """
        status = 400
        if (request_parser.validateCreds(request)):
            device_sn = request.form['serial-number']
            device_name = request.form['name']
            device_ip = request.form['device_ip']
            #device_usern = request.form['device_user']
            device_usern = "admin"
            #device_pass = request.form['device_pass']
            device_pass = "admin"
            device_exists, has_template = device_connector.device_exists_and_templated(device_sn, device_name)
            if not device_exists:
                return jsonify(
                    status=402,
                    message="Device does not currently exist"
                )
            if not has_template:
                return jsonify(
                    status=401,
                    message="Device has not yet been assigned a template"
                )
            if device_helpers.apply_template(device_sn, device_name, device_ip,
                                             device_usern, device_pass):
                status = 200
            return jsonify(
                status=status,
                message='Template has been applied'
            )