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
        if (request_parser.validateCreds(request)):
            prms = parameter_connector.get_all_parameters()
            return jsonify(
                status=200,
                message="Sent Parameters",
                data=prms
            )
        else:
            return jsonify(
                status=400,
                message="Could not send parameters"
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
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            name = request.form["name"]
            ptype = request.form["type"]
            #TODO value?
            val = request.form["value"]
            parameter_connector.add_parameter(name,ptype.upper(),val)
            status = 200
            message = "Parameter added"
        return jsonify(
            status=status,
            message=message
        )