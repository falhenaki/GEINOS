from flask_restful import Resource, reqparse
from flask import request, jsonify
from app.core.template import xml_templates
from app.core.scep import scep_server
from app.core.api import request_parser
"""
 HTTP Method: PUT
 Authorization: Required
 Authorization type: (auth token) OR (username and password)
 Parameters (json): usr (String), password (String), server (String) ,digest (String), encrypt (String)
 Description : update scep.
 :return:
 Success: status= 200,
 Failure: status: 400,
 """
class Scep(Resource):

    def put(self):
        status = 400
        message = "SCEP Server not updated"
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            content = request.get_json(force=True)
            print(content)
            POST_USERNAME = content['usr']
            POST_PASSWORD = content['password']
            POST_SERVER = content['server']
            POST_DIGEST = content['digest']
            POST_ENCRYPT = content['encrypt']
            if scep_server.add_scep(POST_SERVER, POST_USERNAME, POST_PASSWORD, POST_DIGEST, POST_ENCRYPT):
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
