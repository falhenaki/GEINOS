from flask_restful import Resource, reqparse
from flask import request, jsonify
from app.core.template import xml_templates
from  app.core.api import request_parser

parser = reqparse.RequestParser()
#parser.add_argument('template_name')

class Templates(Resource):
	def get(self):
		if True :
			args = parser.parse_args()
			tmp_name = args.get('template_name')
			if tmp_name is not None:
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
		if (request_parser.validateCreds(request)):
			#args = parser.parse_args()

			if 'file' in request.files:
				file = request.files['file']
				if xml_templates.save_with_jinja(file, file.filename):
					status=200
					message="Template Added"

		return jsonify(
			status=status,
			message=message
		)