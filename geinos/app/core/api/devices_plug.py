from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.device import device_connector, device_helpers
from app.core.api import request_parser
from app.core.device_process import dev_queue
authen = HTTPBasicAuth()
import csv

class Devices(Resource):
    """
    HTTP Method: GET
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Description : Retrieves all devices
    :return:
    Success: status= 200, message= "Sent Devices", data= devices(json)
    Failure: status= 400, message= "Could not send devices
    """

    def get(self,device=None):
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            if device is not None:
                device_info = device_connector.get_device(device)
                return jsonify(
                    auth_token=auth_token,
                    status=200,
                    message="Sent Device",
                    data=device_info
                )

            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            devices = device_connector.get_all_devices()
            return jsonify(
                auth_token=auth_token,
                status=200,
                message="Sent Devices",
                data=devices
            )
        else:
            return jsonify(
                auth_token=auth_token,
                status=401,
                message="Unauthorized"
            )

    """
    HTTP Method: PUT
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters (form): vendor_id (String), serial_num (String), model_num (String)
    Description : Adds a new device to DB.
    :return:
    Success: status= 201, message = 'Device Added',
    Failure: status: 400, message = 'Device not added'
    Failure: status 401, message = 'Unauthorized'
    """
    def put(self):

        status = 400
        message = "Device not added"
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            if 'file' not in request.files:
                content = request.get_json(force=True)

                VENDOR_ID = content['vendor_id']
                SERIAL_NUMBER = content['serial_num']
                MODEL_NUMBER = content['model_num']
                LOCATION = content['location']
                cert_required = content['scep']
                if device_connector.add_device(VENDOR_ID, SERIAL_NUMBER, MODEL_NUMBER, LOCATION, logged_user.username, logged_user.role_type, request.remote_addr, cert_required.upper()):
                    status = 201
                    message = "Device Added"
                else:
                    status = 402
                    message = "Device not added. Device already exists"
            else:
                file = request.files['file']
                file_data = file.readlines()
                content = [str(x,'utf-8').strip().split(',') for x in file_data]
                #records = csv.DictReader(request.files['file'])
                header = content[0]
                #a = [dict(zip(header, map(int, row))) for row in file_data]
                # for row in records:
                a = [dict(zip(header, map(str, row))) for row in content[1:]]
                #     print(row)
                #print(a)
                if device_helpers.add_list_of_devices(a, file.filename, logged_user.username, logged_user.role_type, request.remote_addr):
                    status=201
                    message="Devices Added"
                else:
                    status = 402
                    message = "Failed to add devices"
        else:
            status = 401
            message = "Unauthorized"

        return jsonify(
            auth_token=auth_token,
            status=status,
            message=message
        )

    def delete(self):
        status=400
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            content = request.get_json()
            content = request.get_json(force=True)
            DEVICE_SNs = content['serial_nums']
            if device_connector.remove_device(DEVICE_SNs, logged_user.username, logged_user.role_type, request.remote_addr):
                return jsonify(
                    auth_token=auth_token,
                    status=200,
                    message="Device Deleted"
                )
            return jsonify(
                auth_token=auth_token,
                status=status,
                message="Failed to delete device or device does not exist"
            )
