from flask_restful import Resource, reqparse
from flask import request, jsonify, session
from flask_httpauth import HTTPBasicAuth
from app.core.template import xml_templates
from app.core.device.device_access import *
from  app.core.api import request_parser
from app.core.device_group import device_group_connector

authen = HTTPBasicAuth()

parser = reqparse.RequestParser()
parser.add_argument('temp_name')
parser.add_argument('group_name')

class Assign(Resource):
	def post(self):
		status = 400
		if (request_parser.validateCreds(request)):
			args = parser.parse_args()
			templ_name = args.get('temp_name')
			group_name = args.get('group_name')
			template = xml_templates.render_template(templ_name)
			print(template)
			dvs = device_group_connector.get_devices_in_group(group_name)
			for dv in dvs:
				set_config(dv.IP, dv.username, dv.password, template)
			#set_config('192.168.1.1', 'admin', 'admin', template)
			return jsonify(
				status=status,
				message='Template assigned'
			)