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
        if (request_parser.validateCreds(request)):
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
    """
    #TODO why are we using a post here but a put for all other "adds"
    def post(self):
        status = 400
        message = "Device(s) not added to group"
        if (request_parser.validateCreds(request)):
            group_name = request.form["group_name"]
            atrbute = request.form["attribute"]
            valu = request.form["value"]
            #TODO allow cases in which value is not just model
            device_group_connector.add_devices_to_groups(group_name,atrbute, valu)
            status=201
            message="Device(s) added to group"
        else:
            status= 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )

    def delete(self):
        status=400
        if (request_parser.validateCreds(request)):
            GROUP = request.form['group_name']
            if device_group_connector.remove_group(GROUP):
                return jsonify(
                    status=200,
                    message="Group Deleted"
                )
            return jsonify(
                status=status,
                message="Failed to delete device group or device group does not exist"
            )