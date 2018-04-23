from flask_restful import Resource, reqparse
from flask import request, jsonify, session
from flask_httpauth import HTTPBasicAuth
from app.core.user import auth
from app.core.template import template_connector, xml_templates

authen = HTTPBasicAuth()

parser = reqparse.RequestParser()
parser.add_argument('template_name')

class Templates(Resource):
	def get(self):
		if (True): #auth.login(request.authorization["username"], request.authorization["password"])):
			args = parser.parse_args()
			tmp_name = args.get('template_name')
			if tmp_name != '':
				nms = xml_templates.get_template(tmp_name)
			else:
				nms = xml_templates.get_template_names()
			return jsonify(
				status=200,
				message="Sent Templates",
				data=nms
			)
		else:
			return jsonify(
				status=400,
				message="Could not send templates"
			)
	def post(self):
		status = 400
		message = "Parameter not added"
		if True: #(auth.login(request.authorization["username"], request.authorization["password"])):
			args = parser.parse_args()
			tmp_name = args.get('template_name')
			if 'file' in request.files:
				file = request.files['file']
				if xml_templates.save_with_jinja(file, tmp_name):
					status=200
					message="Template Added"

		return jsonify(
			status=status,
			message=message
		)