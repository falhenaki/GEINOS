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
    #TODO Get specific device group
    def get(self, device_group_name=None):
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            dgs = device_group_connector.get_all_device_groups(device_group_name)
            return jsonify(
                status=200,
                message="Sent Device Groups",
                auth_token=auth_token,
                data=dgs
            )
        else:
            return jsonify(
                auth_token=auth_token,
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
        print("Attempting to add group")
        status = 400
        message = "Device(s) not added to group"
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            content = request.get_json()
            group_name = content["group_name"]
            try:
                attribute = content["attribute"]
            except KeyError:
                attribute = "other"
            value = content["value"]
            print("Group Name: " + group_name)
            print("Group Value: " + str(value))
            print("Group Attribute: " + str(attribute))


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
            if device_group_connector.add_device_group(group_name, attribute, value, logged_user.username, logged_user.role_type, request.remote_addr):
                print("Device group: " + group_name + "added")
                status=201
                message="Device(s) added to group"
            else:
                print("Failed to add group: " + group_name + "to database")
                status = 402
                message = "Device Group not created, group name or value already exists, or device could belong to multiple groups"
        else:
            status= 401
            message = "Unauthorized"
        print(message)
        return jsonify(
            status=status,
            message=message,
            auth_token=auth_token
        )


    def delete(self):
        status = 401
        message = "Unauthorized"
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            content = request.get_json()
            GROUPs = content['group_names']
            deleted, not_deleted = device_group_connector.remove_groups(GROUPs, logged_user.username, logged_user.role_type, request.remote_addr)
            if len(not_deleted) == 0:
                status=200
                message="Groups deleted: {}".format(','.join(deleted))
            else:
                status=401
                message="Groups deleted: {}\nGroups not deleted: {}".format(','.join(deleted), ','.join(not_deleted))
        else:
            status= 401
            message = "Unauthorized"
        print(message)
        return jsonify(
            status=status,
            message=message,
            auth_token=auth_token
        )