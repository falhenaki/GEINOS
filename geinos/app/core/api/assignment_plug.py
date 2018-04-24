from flask_restful import Resource, reqparse
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.core.template import xml_templates
from app.core.device.device_access import *
from  app.core.api import request_parser
from app.core.device_group import device_group_connector

authen = HTTPBasicAuth()

parser = reqparse.RequestParser()

class Assign(Resource):
	def post(self):
		print("AFTER POST")
		status = 400
		if (request_parser.validateCreds(request)):
			print("AFTER AUTH")
			args = parser.parse_args()
			templ_name = request.form['temp_name']
			group_name = request.form['group_name']
			print(templ_name)
			template = xml_templates.apply_parameters(templ_name)
			print(template)
			dvs = device_group_connector.get_devices_in_group(group_name)
			for dv in dvs:
				set_config(dv.IP, dv.username, dv.password, template)
			#set_config('192.168.1.1', 'admin', 'admin', template) default credentials for testing
			return jsonify(
				status=status,
				message='Template assigned'
			)