from flask_restful import Resource, reqparse
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.api import request_parser
from app.core.device import device_helpers, device_connector
from app.core.device_group import device_group_connector
from app.core.template import template_connector

authen = HTTPBasicAuth()

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
    Failure on missing group or template: 404
    TODO perform parameter assignment here
    """
    def post(self):
        status = 401
        message = "Unauthorized"
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            content = request.get_json()
            if content['temp_name'] and content['group_name']:
                templ_name = content['temp_name']
                group_name = content['group_name']
                if device_group_connector.assign_template(group_name, templ_name, logged_user.username, logged_user.role_type, request.remote_addr):
                    status = 200
                    message = templ_name + " Assigned to " + group_name
                else:
                    status = 400
                    message = "Could not process request"
        return jsonify(
                status=status,
                message= message
            )

