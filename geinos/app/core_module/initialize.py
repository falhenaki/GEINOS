from flask_restful import Api
from app import app
from app.core_module import api_plugs

def initialize_APIs():
    api = Api(app)
    api.add_resource(api_plugs.HelloWorld, '/abcde')
    api.add_resource(api_plugs.Login, '/login', '/')
    api.add_resource(api_plugs.Users, '/users')
    api.add_resource(api_plugs.Devices, '/devices')
    api.add_resource(api_plugs.Device_Groups, '/device_groups')
    api.add_resource(api_plugs.Parameters, '/parameters')