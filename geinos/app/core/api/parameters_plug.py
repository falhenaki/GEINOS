from flask_restful import Resource
from flask import request, jsonify
from app.core.parameter import parameter_connector
from app.core.api import request_parser
import ipaddress

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
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            content = request.get_json()
            name = content["name"]
            ptype = content["type"]
            #TODO value?
            if 'DYNAMIC' in ptype.upper():
                val = content["value"]
                interface = content["interface"]
                if (parameter_connector.add_dynamic_parameter(name,ptype.upper(),val, logged_user.username, logged_user.role_type, request.remote_addr, interface)):
                    status = 200
                    message = "Parameter added"
                else:
                    status = 400
                    message = "Parameter already exists"
            else:
                val = content["value"]
                if 'RANGE' in ptype.upper():
                    try:
                        ip = ipaddress.ip_network(val)
                    except TypeError or ValueError:
                        return jsonify(
                            status=403,
                            message="Invalid address or mask"
                        )
                    val = ip
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
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            content = request.get_json()
            PARAMETER_NAMEs = content['param_names']
            deleted, not_deleted = parameter_connector.remove_parameters(PARAMETER_NAMEs, logged_user.username, logged_user.role_type, request.remote_addr)
            if len(not_deleted) == 0:
                return jsonify(
                    status=200,
                    message="Parameters deleted: {}".format(','.join(deleted))
                )
            else:
                status = 412,
                message = "Parameters not deleted : {}\nParameters deleted : {}".format(','.join(not_deleted), ','.join(deleted))

        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )