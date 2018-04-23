from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.user import auth

from app.core.device_group import device_group_connector
authen = HTTPBasicAuth()

class Device_Groups(Resource):
    def get(self):
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            dgs = device_group_connector.get_all_device_groups()
            return jsonify(
                status=200,
                message="Sent Device Groups",
                data=dgs
            )
        else:
            return jsonify(
                status=400,
                message="Could not send device groups"
            )
    '''
    def put(self):
        status=400
        message="Device Group not added"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            group_name = request.form["group_name"]
            device_group_connector.add_device_group(group_name)
            status=200
            message="Device group added"
        return jsonify(
            status=status,
            message=message
        )
    '''
    def post(self):
        status = 400
        message = "Device(s) not added to group"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            group_name = request.form["group_name"]
            atrbute = request.form["attribute"]
            valu = request.form["value"]
            device_group_connector.add_devices_to_groups(group_name,atrbute, valu)
            status=200
            message="Device(s) added to group"
        return jsonify(
            status=status,
            message=message
        )