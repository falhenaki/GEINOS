from flask_restful import Resource
from flask import request, jsonify
from app.core.user import auth
from app.core.user import user_connector
from  app.core.api import request_parser

class Users(Resource):
    """
    HTTP Method: GET
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Description : Retrieves all users
    :return:
    Success: status= 200, message= "Sent all users.", data= all users(json)
    Failure: status= 400, message= "Could not authenticate"
    """
    def get(self):
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            all_users = user_connector.get_all_users()
            status=200,
            message="Sent all users.",
            data=all_users

        else:
            status = 401
            message = "Unathorized"
            data = []
        return jsonify(
            status=400,
            message= message,
            data = data
        )


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
        message = "User not added"
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
            if auth.add_user(POST_USERNAME, POST_PASSWORD, POST_EMAIL, POST_ROLE, logged_user.username, logged_user.role_type, request.remote_addr):
                auth.change_user_role(POST_USERNAME, POST_ROLE)
                status=200
                message = "User added"
        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )
    """
    HTTP Method: DELETE
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters (form): rmusr -username- (String)
    Description : Deletes a user.
    :return:
    Success: status= 200, message = 'Users Deleted',
    """
    def delete(self):
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            content = request.get_json()
            POST_USERNAME = content['rmusr']
            auth.remove_user(POST_USERNAME, logged_user.username, logged_user.role_type, request.remote_addr)
            status=200,
            message="Users Deleted"
        else:
            status=401
            message="Unauthorized"
        return jsonify(
            status=status,
            message=message
        )

        #TODO handle failure message