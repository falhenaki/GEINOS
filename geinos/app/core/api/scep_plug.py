from flask_restful import Resource, reqparse
from flask import request, jsonify
from app.core.template import xml_templates
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
    message = "scep Server not updated"
    logged_user = request_parser.validateCreds(request)
    if (logged_user):
        content = request.get_json()
        POST_USERNAME = content['usr']
        POST_PASSWORD = content['password']
        POST_RETYPE_PASS = content['retypepassword']
        POST_EMAIL = content['email']
        POST_ROLE = str(content['role'])
        '''
        users = user_connector.get_all_users()
        for u in users:
            if POST_USERNAME in u:
                return jsonify(
                    status=402,
                    message= "Cannot create user. User already exists"
                )
        if POST_PASSWORD == POST_RETYPE_PASS:
        '''
        if auth.add_user(POST_USERNAME, POST_PASSWORD, POST_EMAIL, POST_ROLE, logged_user.username,
                         logged_user.role_type, request.remote_addr):
            auth.change_user_role(POST_USERNAME, POST_ROLE)
            status = 200
            message = "User added"
    else:
        status = 401
        message = "Unauthorized"
    return jsonify(
        status=status,
        message=message
    )