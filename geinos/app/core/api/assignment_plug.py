from flask_restful import Resource, reqparse
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.api import request_parser
from app.core.device import device_helpers, device_connector
from app.core.device_group import device_group_connector

authen = HTTPBasicAuth()

parser = reqparse.RequestParser()


class Assign(Resource):
    def post(self):
        """
        API to assign a template to a device group
        :return: 400 if failed 200 if sucessful
        """
        print("AFTER POST")
        status = 400
        if (request_parser.validateCreds(request)):
            print("AFTER AUTH")
            args = parser.parse_args()
            templ_name = request.form['temp_name']
            group_name = request.form['group_name']
            print(templ_name)
            print(group_name)
            device_group_connector.assign_template(group_name, templ_name)
            # set_config('192.168.1.1', 'admin', 'admin', template) default credentials for testing
            status = 200
            return jsonify(
                status=status,
                message='Template assigned'
            )

