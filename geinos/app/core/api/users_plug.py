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
        if (request_parser.validateCreds(request)):
            all_users = user_connector.get_all_users()
            return jsonify(
                status=200,
                message="Sent all users.",
                data=all_users
            )
        else:
            return jsonify(
                status=400,
                message="Could not authenticate"
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
        if (request_parser.validateCreds(request)):
            POST_USERNAME = request.form['usr']
            POST_PASSWORD = request.form['password']
            POST_RETYPE_PASS = request.form['retypepassword']
            POST_EMAIL = request.form['email']
            POST_ROLE = str(request.form['role'])
            if POST_PASSWORD == POST_RETYPE_PASS:
                if auth.add_user(POST_USERNAME, POST_PASSWORD, POST_EMAIL, POST_ROLE):
                    auth.change_user_role(POST_USERNAME, POST_ROLE)
                    status=200
                    message = "User added"
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
        if (request_parser.validateCreds(request)):
            POST_USERNAME = request.form['rmusr']
            auth.remove_user(POST_USERNAME)
            return jsonify(
                status=200,
                message="Users Deleted"
            )
        #TODO handle failure message