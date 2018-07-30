from flask_restful import Resource
from flask import request, jsonify
from app.core.radius import radius_connector
from app.core.api import request_parser
"""
 HTTP Method: PUT
 Authorization: Required
 Authorization type: (auth token) OR (username and password)
 Parameters (json): usr (String), password (String), server (String) ,digest (String), encrypt (String)
 Description : update radius.
 :return:
 Success: status= 200,
 Failure: status: 400,
 """


class Radius(Resource):
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
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            data = radius_connector.get_radius_settings()
            return jsonify(
                auth_token=auth_token,
                status=200,
                message="Sent Radius Settings",
                data=data
            )
        else:
            return jsonify(
                auth_token=auth_token,
                status=401,
                message="Unauthorized"
            )


    def put(self):
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            content = request.get_json(force=True)
            HOST = content['host']
            PORT = content['port']
            SECRET = content['secret']
            if radius_connector.set_radius_settings(HOST,PORT,SECRET):
                    status = 200
                    message = "Radius settings saved"
            else:
                status = 403
                message = "Error adding RADIUS server to database"
        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            auth_token=auth_token,
            status=status,
            message=message
        )
