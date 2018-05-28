from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.device import device_connector, device_helpers
from  app.core.api import request_parser

authen = HTTPBasicAuth()
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
    def get(self):
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            devices = device_connector.get_all_devices()
            return jsonify(
                status=200,
                message="Sent Devices",
                data=devices
            )
        else:
            return jsonify(
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
        if (logged_user):
            if 'file' not in request.files:
                VENDOR_ID = request.form['vendor_id']
                SERIAL_NUMBER = request.form['serial_num']
                MODEL_NUMBER = request.form['model_num']
                '''
                devices = device_connector.get_all_devices()
                for d in devices:
                    if SERIAL_NUMBER in d:
                        status = 402
                        message = "Device not added. Device already exists"
                if status is not 402:
                    device_connector.add_device(VENDOR_ID, SERIAL_NUMBER, MODEL_NUMBER)
                    status=201
                    message="Device Added"
                '''
                if device_connector.add_device(VENDOR_ID, SERIAL_NUMBER, MODEL_NUMBER, logged_user.username, logged_user.role_type, request.remote_addr):
                    status = 201
                    message = "Device Added"
                else:
                    status = 402
                    message = "Device not added. Device already exists"
            else:
                file = request.files['file']
                file_data = file.readlines()
                content = [str(x,'utf-8').strip().split(',') for x in file_data]
                if device_helpers.add_list_of_devices(content, file.filename, logged_user.username, logged_user.role_type, request.remote_addr):
                    status=201
                    message="Devices Added"
                else:
                    status = 402
                    message = "Failed to add devices"
        else:
            status = 401
            message = "Unauthorized"
        return jsonify(
            status=status,
            message=message
        )

    def delete(self):
        status=400
        logged_user = request_parser.validateCreds(request)
        if (logged_user):
            DEVICE_SN = request.form['serial_num']
            if device_connector.remove_device(DEVICE_SN, logged_user.username, logged_user.role_type, request.remote_addr):
                return jsonify(
                    status=200,
                    message="Device Deleted"
                )
            return jsonify(
                status=status,
                message="Failed to delete device or device does not exist"
            )