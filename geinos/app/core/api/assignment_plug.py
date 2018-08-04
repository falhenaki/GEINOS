from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.api import request_parser
from app.core.device import device_connector
from app.core.device_group import device_group_connector
from app.core.assignment import assignment_connector

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
    """
    def get(self):
        status = 401
        message = "Unauthorized"
        data = None
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            asgns = assignment_connector.get_assignments()
            status=200
            message="Sent Assignments"
            data=asgns
        return jsonify(
            status=status,
            message=message,
            auth_token=auth_token,
            data=data
        )

    def post(self):
        status = 401
        message = "Unauthorized"
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            content = request.get_json(force=True)
            if content['temp_name'] and content['group_name']:
                templ_name = content['temp_name']
                group_name = content['group_name']
                if device_group_connector.assign_template(group_name, templ_name, logged_user.username, logged_user.role_type, request.remote_addr):
                    for dev in device_group_connector.get_all_devices_in_group(group_name):
                        device_connector.set_rendered_template(dev['serial_number'], dev['vendor_id'], templ_name)
                    status = 200
                    message = templ_name + " Assigned to " + group_name
                else:
                    status = 400
                    message = "Could not process request"
        return jsonify(
                status=status,
                message= message,
                auth_token=auth_token,
            )

    def delete(self):
        status = 401
        message = "Unauthorized"
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            content = request.get_json(force=True)
            if content['temp_name'] and content['group_name']:
                templ_name = content['temp_name']
                group_name = content['group_name']
                if device_group_connector.remove_assignment(group_name, templ_name, logged_user.username, logged_user.role_type, request.remote_addr):
                    status = 200
                    message = templ_name + " Unassigned to " + group_name
                else:
                    status = 400
                    message = "Could not process request"
        return jsonify(
                status=status,
                message= message,
                auth_token=auth_token,
            )
