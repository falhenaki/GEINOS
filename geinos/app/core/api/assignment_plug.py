from flask_restful import Resource, reqparse
from flask import request, jsonify, session
from flask_httpauth import HTTPBasicAuth
from app.core.template import xml_templates
from app.core.device.device_access import *

authen = HTTPBasicAuth()

parser = reqparse.RequestParser()
parser.add_argument('temp_name')
parser.add_argument('group_name')

class Assign(Resource):
	def post(self):
		status = 400
		if (auth.login(request.authorization["username"], request.authorization["password"])):
			args = parser.parse_args()
			templ_name = args.get('temp_name')
			group_name = args.get('group_name')
			template = xml_templates.render_template(templ_name)
			print(template)
			set_config('192.168.1.1', 'admin', 'admin', template)
			return jsonify(
				status=status,
				message='Template assigned'
			)