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
            POST_CERT_INFO_ID = content['cert_info_id']
            POST_CA_SERVER_ID = content['ca_server_id']
            POST_COUNTRY = content['country']
            POST_STATE = content['state']
            POST_LOCALE = content['locale']
            POST_ORGANIZATION = content ['organization']
            POST_ORG_UNIT = content['org_unit']
            POST_CERT_SERVER_ID = content['cert_server_idd']
            POST_KEY_ID = content['key_id']
            POST_CA_CERT_ID = content['ca_cert_id']
            POST_CLIENT_CERT_ID = content['client_cert_id']
            if scep_server.add_scep(POST_SERVER, POST_USERNAME, POST_PASSWORD, POST_DIGEST, POST_ENCRYPT,
                                    POST_CERT_INFO_ID,POST_CA_SERVER_ID,POST_COUNTRY,POST_STATE,POST_LOCALE,
                                    POST_ORGANIZATION,POST_ORG_UNIT,POST_CERT_SERVER_ID,POST_KEY_ID,POST_CA_CERT_ID,
                                    POST_CLIENT_CERT_ID):
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
