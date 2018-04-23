from flask_restful import Resource, reqparse
from flask import request, jsonify, session
from flask_httpauth import HTTPBasicAuth
from app.core.user import auth
from app.core.template import template_connector

authen = HTTPBasicAuth()

parser = reqparse.RequestParser()
#parser.add_argument('template_name')

class Templates(Resource):
    def get(self):
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            args = parser.parse_args()
            #tmp_name = args.get('template_name')
            nms = template_connector.get_template_names()
            return jsonify(
                status=200,
                message="Sent Templates",
                data=nms
            )
        else:
            return jsonify(
                status=400,
                message="Could not send templates"
            )
    def put(self):
        status = 400
        message = "Parameter not added"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            name = request.form["name"]
            ptype = request.form["type"]
            val = request.form["value"]
            #parameter_connector.add_parameter(name,ptype.upper(),val)
            status = 200
            message = "Parameter added"
        return jsonify(
            status=status,
            message=message
        )