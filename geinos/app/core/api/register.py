from flask_restful import Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from flask import request, jsonify
from app.core.device import device_helpers, device_connector
from app.core.device_process import dev_queue
import threading

#import read_protobuf.tests.demo_pb2
#from google.protobuf.json_format import MessageToJson
#from protobuf_to_dict import protobuf_to_dict, TYPE_CALLABLE_MAP
#from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.message import Message
#from copy import copy

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
    def post(self):
        """
        API for devices to request templates to be applied based on their device group
        :return: 402 if the device has not been added 401 if there is no template assigned to device group
        200 if assignment was sucessful
        """
       
        status = 400
        """
        TODO: Require authorization, needs to be changed in orbit device. See if IP address can be obtained.
        """
        if True:
            #my_message = MyMessage()
            #my_message.ParseFromString(request.data)
            sn = ""
            idx = -1
            while (request.data.decode("utf-8")[idx].isdigit()):
                sn = request.data.decode("utf-8")[idx] + sn
                idx -= 1
            if device_connector.update_device(sn,"IP",request.remote_addr) is not True:
                return jsonify(
                    status=402,
                    message="Device could not be found"
                )

            else:
                status=200
                message="Success"
        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )
