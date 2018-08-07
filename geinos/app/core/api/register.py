from flask_restful import Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from flask import request, jsonify
from app.core.device import device_helpers, device_connector

from app.core.proto import ztp_pb2

parser = reqparse.RequestParser()
authen = HTTPBasicAuth()

class Register(Resource):
    """
    HTTP Method: POST
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters (form): serial-number (String), name (String), device_ip (String)
    Description : API for devices to request templates to be applied based on their device group.
    :return:
    Success: status= 200, message = 'Template has been applied,
    Failure:
        status: 401, message = 'Device does not currently exist'
        status: 402, message = "Device has not yet been assigned a template"

    """
    def post(self, dev_ip=None):
        """
        API for devices to request templates to be applied based on their device group
        :return: 402 if the device has not been added 401 if there is no template assigned to device group
        200 if assignment was sucessful
        """
       
        status = 400
        """
        TODO: Require authorization, needs to be changed in orbit device. See if IP address can be obtained.
        """
        print("Enter Register")
        if True:

            msg = ztp_pb2.registration()
            msg.ParseFromString(request.data)
            if dev_ip is not None:
                ip = dev_ip
                serial_number = device_connector.get_sn_from_ip(ip)
                if serial_number is False:
                    return jsonify(
                        status=402,
                        message="No Device with ip {}".format(dev_ip)
                    )
            else:
                ip = request.remote_addr
                serial_number = msg.serial_number
                print("Device IP: " + ip)
                print("Device Serial: " + serial_number)
            if device_connector.update_device(serial_number,"IP",ip) is not True:
                print("Failed to find device in database")
                return jsonify(
                    status=402,
                    message="Device could not be found"
                )

            else:
                print("Device Registered: " + serial_number)
                status=200
                message="Success"
        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )
