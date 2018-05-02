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
        if (request_parser.validateCreds(request)):
            devices = device_connector.get_all_devices()
            return jsonify(
                status=200,
                message="Sent Devices",
                data=devices
            )
        else:
            return jsonify(
                status=400,
                message="Could not send devices"
            )
    """
    HTTP Method: PUT
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters (form): vendor_id (String), serial_num (String), model_num (String)
    Description : Adds a new device to DB.
    :return:
    Success: status= 200, message = 'Device Added',
    Failure: status: 400, message = 'Device not added'
    """
    def put(self):
        status = 400
        message = "Device not added"
        if (request_parser.validateCreds(request)):
            if 'file' not in request.files:
                VENDOR_ID = request.form['vendor_id']
                SERIAL_NUMBER = request.form['serial_num']
                MODEL_NUMBER = request.form['model_num']
                device_connector.add_device(VENDOR_ID, SERIAL_NUMBER, MODEL_NUMBER)
                status=200
                message="Device Added"
            else:
                file = request.files['file']
                file_data = file.readlines()
                content = [str(x,'utf-8').strip().split(',') for x in file_data]
                if device_helpers.add_list_of_devices(content):
                    status=200
                    message="Devices Added"
        return jsonify(
            status=status,
            message=message
        )

    def delete(self):
        status=400
        if (request_parser.validateCreds(request)):
            DEVICE_SN = request.form['serial_num']
            if device_connector.remove_device(DEVICE_SN):
                return jsonify(
                    status=200,
                    message="Device Deleted"
                )
            return jsonify(
                status=status,
                message="Failed to delete device or device does not exist"
            )