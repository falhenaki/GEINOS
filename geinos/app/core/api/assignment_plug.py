from flask_restful import Resource, reqparse
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.api import request_parser
from app.core.device import device_helpers, device_connector
from app.core.device_group import device_group_connector

authen = HTTPBasicAuth()

parser = reqparse.RequestParser()


class Assign(Resource):
    """
    HTTP Method: POST
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters(Form): temp_name (String), group_name (String)
    Description : Assign a template with a given temp_name to a device group with group_name
    :return:
    Success: status: 200, message: "Template assigned"
    Failure: status: 400
    """
    def post(self):
        print("AFTER POST")
        status = 400
        if (request_parser.validateCreds(request)):
            print("AFTER AUTH")
            args = parser.parse_args()
            if request.form['temp_name'] and request.form['group_name']:
                templ_name = request.form['temp_name']
                group_name = request.form['group_name']
                device_group_connector.assign_template(group_name, templ_name)
            # set_config('192.168.1.1', 'admin', 'admin', template) default credentials for testing
            status = 200
            #TODO Failure status
            return jsonify(
                status=status,
                message='Template assigned'
            )
        else:
            return jsonify(
                status=401,
                message="Unauthorized"
            )

