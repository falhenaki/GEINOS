from flask_restful import Resource, reqparse
from flask import request, jsonify
from app.core.template import xml_templates
from app.core.scep import scep_server
from app.core.api import request_parser
"""
 HTTP Method: PUT
 Authorization: Required
 Authorization type: (auth token) OR (username and password)
 Parameters (form): usr (String), password (String), retypepassword (Email) ,retypepassword (String), role (String)
 Description : Adds a new user.
 :return:
 Success: status= 200, message = 'User added',
 Failure: status: 400, message = 'User not added'
 """


def put(self):
    status = 400
    message = "SCEP Server not updated"
    logged_user = request_parser.validateCreds(request)
    if (logged_user):
        content = request.get_json()
        POST_USERNAME = content['usr']
        POST_PASSWORD = content['password']
        POST_SERVER = content['server']
        if scep_server.add_scep(POST_SERVER, POST_USERNAME, POST_PASSWORD):
            status = 200
            message = "SCEP server added"
        else:
            status = 403
            message = "Error adding SCEP server to database"
    else:
        status = 401
        message = "Unauthorized"
    return jsonify(
        status=status,
        message=message
    )