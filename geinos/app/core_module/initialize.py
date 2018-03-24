from flask_restful import Api
from app import app
from app.core_module import views

def initialize_APIs():
    api = Api(app)
    api.add_resource(views.HelloWorld, '/abcde')