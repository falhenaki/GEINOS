from flask_restful import Api

from app import app
from flask import jsonify
from app.core.api import configs_plug, devices_plug, login_plug, parameters_plug, device_groups, users_plug, templates_plug, \
    assignment_plug, logs_plugs, register, scep_plug, radius_plug
from app.core.exceptions.custom_exceptions import Conflict, MissingResource, GeneralError, InvalidInput
"""
API END POINTS
"""
def initialize_APIs():
    api = Api(app)
    api.add_resource(login_plug.Login, '/login', '/')
    api.add_resource(users_plug.Users, '/users')
    api.add_resource(devices_plug.Devices, '/devices/<device>','/devices')
    api.add_resource(device_groups.Device_Groups, '/device_groups')
    api.add_resource(parameters_plug.Parameters, '/parameters')
    api.add_resource(configs_plug.Device_Configs, '/configs')
    api.add_resource(templates_plug.Templates, '/templates')
    api.add_resource(assignment_plug.Assign, '/assign')
    api.add_resource(logs_plugs.Logs, '/logs')
    api.add_resource(register.Register, '/register')
    api.add_resource(login_plug.Login_Helper, '/verify_token')
    api.add_resource(scep_plug.Scep, '/scep')
    api.add_resource(radius_plug.Radius, '/radius')

    """
    Exception responses
    """
    #TODO also log the errors into the logging system here
    @app.errorhandler(Conflict)
    def handle_device_conflict(error):
        """
        Error handler for the case where a device can belong to multiple groups
        :param error: error information
        :return: json of error for response
        """
        return form_response(error)

    @app.errorhandler(MissingResource)
    def handle_missing_resource(error):
        """
        Error for when a resource could not be found
        :param error: error information
        :return: json of error for response
        """
        return form_response(error)

    @app.errorhandler(GeneralError)
    def handle_general_error(error):
        """
        Error for when the system fails in an unexpected way
        :param error: error information
        :return: json of error for response
        """
        return form_response(error)

    @app.errorhandler(InvalidInput)
    def handle_invalid_input(error):
        """
        Error when user input is passed to the backend in an invalid format
        :param error: error information
        :return: json of error for response
        """
        return form_response(error)


def form_response(error):
    """
    method to convert error into json
    :param error: error containing a message, status code, and possible payload
    :return: jsonified response to return to frontend
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response