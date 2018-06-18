from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.api import request_parser
from app.core.device_group import device_group_connector
authen = HTTPBasicAuth()

class Device_Groups(Resource):
    """
    HTTP Method: GET
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Description : Retrieves all device groups
    :return:
    Success: status= 200, message= "Sent Device Groups", data= devie_groups(json)
    Failure: status= 400, message= "Could not send device groups
    """
    def get(self):
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            dgs = device_group_connector.get_all_device_groups()
            return jsonify(
                status=200,
                message="Sent Device Groups",
                data=dgs
            )
        else:
            return jsonify(
                status=401,
                message="Unauthorized"
            )
    """
    HTTP Method: POST
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters (form): group_name (String), attribute (String), value -device model- (String)
    Description : Adds a new device to group.
    :return:
    Success: status= 201, message = "Device(s) added to group"",
    Failure: status: 400, message = "Device(s) not added to group"
    Failure: status: 402, message = "Device Group not created, group name or value already exists"
    """
    #TODO why are we using a post here but a put for all other "adds"
    def post(self):
        status = 400
        message = "Device(s) not added to group"
        logged_user = request_parser.validateCreds(request)
        if True:# (logged_user):
            content = request.get_json()
            group_name = content["group_name"] #TODO api failing here
            attribute = content["attribute"]
            value = content["value"]
            '''
            groups = device_group_connector.get_all_device_groups()
            #TODO allow cases in which value is not just model, also take this logic out of here
            for g in groups:
                if group_name in g or attribute in g:
                    return jsonify(
                        status=402,
                        message="Device Group not created, group name or value already exists"
                    )
            '''
            if device_group_connector.add_device_group(group_name):
                print("Device group added")
                if device_group_connector.add_devices_to_groups(group_name, attribute, value, 'doug', 'ADMIN', '1.1.1.1'):
                    status=201
                    message="Device(s) added to group"
            else:
                status = 402
                message = "Device Group not created, group name or value already exists, or device could belong to multiple groups"
        else:
            status= 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )


    def delete(self):
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            content = request.get_json()
            GROUP = content['group_name']
            if device_group_connector.remove_group(GROUP, logged_user.username, logged_user.role_type, request.remote_addr):
                return jsonify(
                    status=200,
                    message="Group Deleted"
                )