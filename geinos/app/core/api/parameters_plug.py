from flask_restful import Resource
from flask import request, jsonify, session
from flask_httpauth import HTTPBasicAuth
from app.core.user import auth
from app.core.parameter import parameter_connector
from  app.core.api import request_parser

authen = HTTPBasicAuth()
class Parameters(Resource):
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
    def put(self):
        status = 400
        message = "Parameter not added"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            name = request.form["name"]
            ptype = request.form["type"]
            val = request.form["value"]
            parameter_connector.add_parameter(name,ptype.upper(),val)
            status = 200
            message = "Parameter added"
        return jsonify(
            status=status,
            message=message
        )