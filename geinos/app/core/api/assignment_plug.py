from flask_restful import Resource, reqparse
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.api import request_parser
from app.core.device import device_helpers, device_connector
from app.core.device_group import device_group_connector
from app.core.template import template_connector

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
        status = 401
        message = "Unauthorized"
        if (request_parser.validateCreds(request)):
            args = parser.parse_args()
            if request.form['temp_name'] and request.form['group_name']:
                templ_name = request.form['temp_name']
                group_name = request.form['group_name']
                groups = device_group_connector.get_all_device_groups()
                templates = template_connector.get_template_names()
                if templ_name in templates and group_name in groups:
                    device_group_connector.assign_template(group_name, templ_name)
                    status = 200
                    message = templ_name + " Assigned to " + group_name
                else:
                    status = 402
                    message = "Template or Group does not exist"
        return jsonify(
                status=status,
                message= message
            )

