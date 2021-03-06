from flask_restful import Resource
from flask import request, jsonify
from app.core.scep import scep_server
from app.core.api import request_parser
from app.core.device_process import dev_queue
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
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            content = request.get_json(force=True)
            POST_USERNAME = content['usr']
            POST_PASSWORD = content['password']
            POST_SERVER = content['server']
            POST_DIGEST = content['digest']
            POST_ENCRYPT = content['encrypt']
            POST_CERT_INFO_ID = "GEINOS_CERT_ID"
            POST_CA_SERVER_ID = "GEINOS_SERVER_ID"
            POST_COUNTRY = content['country']
            POST_STATE = content['state']
            POST_LOCALE = content['locale']
            POST_ORGANIZATION = content ['organization']
            POST_ORG_UNIT = content['org_unit']
            POST_CERT_SERVER_ID = "GEINOS_CERT_SERVER"
            POST_KEY_ID = "GEINOS_KEY"
            POST_CA_CERT_ID = "GEINOS_CA_CERT "
            POST_CLIENT_CERT_ID = "GEINOS_CLIENT_CERT"
            POST_SYS_SERVER = content ['sys_server']
            POST_THUMB_ONLY = content['thumb_only']
            if 'TRUE' in POST_THUMB_ONLY:
                thumb = scep_server.get_thumbprint()
                if thumb is False:
                    status = 405
                    message = "Failed to obtain scep thumbprint"
                elif "Error" in thumb:
                    status = 406
                    message = thumb
                else:
                    scep_server.update_thumbprint(thumb)
                    status = 200
                    message = "SCEP server added"
            elif scep_server.add_scep(POST_SERVER, POST_USERNAME, POST_PASSWORD, POST_DIGEST, POST_ENCRYPT,
                                    POST_CERT_INFO_ID,POST_CA_SERVER_ID,POST_COUNTRY,POST_STATE,POST_LOCALE,
                                    POST_ORGANIZATION,POST_ORG_UNIT,POST_CERT_SERVER_ID,POST_KEY_ID,POST_CA_CERT_ID,
                                    POST_CLIENT_CERT_ID,POST_SYS_SERVER):
                thumb = scep_server.get_thumbprint()
                if thumb is False:
                    status = 405
                    message = "Failed to obtain scep thumbprint"
                elif "Error" in thumb:
                    status = 406
                    message = thumb
                else:
                    scep_server.update_thumbprint(thumb)
                    dev_queue.retry_failed_cert()
                    status = 200
                    message = "Thumb Print Obtained"
            else:
                status = 403
                message = "Error adding SCEP server to database"
        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            auth_token=auth_token,
            status=status,
            message=message
        )

    def get(self):
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            scep = scep_server.scep_connector.get_scep_info()
            return jsonify(
                auth_token=auth_token,
                status=200,
                message="SCEP settings sent",
                data=scep
            )
        else:
            return jsonify(
                auth_token=auth_token,
                status=401,
                message="Unauthorized"
            )
