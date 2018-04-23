from flask_restful import Api

from app import app
from app.core.api import configs_plug, devices_plug, login_plug, parameters_plug, device_groups, users_plug, templates_plug, assignment_plug, logs_plugs

def initialize_APIs():
    api = Api(app)
    api.add_resource(login_plug.Login, '/login', '/')
    api.add_resource(users_plug.Users, '/users')
    api.add_resource(devices_plug.Devices, '/devices')
    api.add_resource(device_groups.Device_Groups, '/device_groups')
    api.add_resource(parameters_plug.Parameters, '/parameters')
    api.add_resource(configs_plug.Device_Configs, '/configs')
    api.add_resource(templates_plug.Templates, '/templates')
    api.add_resource(assignment_plug.Assign, '/assign')
    api.add_resource(logs_plugs.Logs, '/logs')