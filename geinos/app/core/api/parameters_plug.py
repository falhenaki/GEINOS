from flask_restful import Resource
from flask import request, jsonify
from app.core.user import auth
from app.core.parameter import parameter_connector
from app.core.api import request_parser

class Parameters(Resource):
    """
    HTTP Method: GET
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Description : Retrieves all parameters
    :return:
    Success: status= 200, message= "Sent Parameters", data= parameters(json)
    Failure: status= 400, message= "Could not send Logs"
    """
    def get(self):
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            prms = parameter_connector.get_all_parameters()
            return jsonify(
                status=200,
                message="Sent Parameters",
                data=prms
            )
        else:
            return jsonify(
                status=401,
                message="Unauthorized"
            )
    """
    HTTP Method: PUT
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters (form): name (String), type (String), value (String)
    Description : Add a new parameter
    :return:
    Success: status= 200, message = 'Parameter Added'
    Failure:
        status: 400, message = 'Parameter not added'
    """
    def put(self):
        status = 400
        message = "Parameter not added"
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            content = request.get_json()
            name = content["name"]
            ptype = content["type"]
            #TODO value?
            val = content["value"]
            if (parameter_connector.add_parameter(name,ptype.upper(),val, logged_user.username, logged_user.role_type, request.remote_addr)):
                status = 200
                message = "Parameter added"
            else:
                status = 400
                message = "Parameter already exists"
        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )

    def delete(self):
        status=400
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            content = request.get_json()
            PARAMETER_NAME = content['param_name']
            if parameter_connector.remove_parameter(PARAMETER_NAME, logged_user.username, logged_user.role_type, request.remote_addr):
                return jsonify(
                    status=200,
                    message="Group Deleted"
                )
            else:
                status = 412,
                message = "Failed to delete parameter or parameter does not exist"

        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )