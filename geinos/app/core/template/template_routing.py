from flask import request, redirect, flash
from werkzeug.utils import secure_filename

from flask import Response

from app import app
from app.core.template import xml_templates
from app.core.device.device_access import *


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/uploaded_files', methods=['POST'])
def upload_file():
	"""
	routing to upload a new file will overwite a file of the same name if it already exists
	:return:
	"""
	status = 400
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		filename = app.config["UPLOADS_FOLDER"] + secure_filename(file.filename)
		with open(filename) as f:
			f.write(file)
		status = 201
	response = app.response_class(
		response=file,
		status=status,
		mimetype='application/json'
	)
	return response


@app.route('/uploaded_files/<filename>', methods=['GET'])
def uploaded_file(filename):
	if filename == None:
		return True  # add all templates here
	return xml_templates.get_file(filename)


@app.route('/uploaded_files/generate_jinja2/<filename>', methods=['PUT'])
def replace_jinja(filename):
	"""
	converts given file to jinja2 for now this will only replace the NCServer attribute but will be modified to use a
	set of parameters from a given device group
	:param filename: filename stored in server to have jinja templating applied to
	:return: jinja2 formatted xml file
	"""
	return xml_templates.generate_jinja(filename)


@app.route('/uploaded_files/<filenams>', methods=['DELETE'])
def delete_file(filename):
	if xml_templates.delete_file(filename):
		return Response(status=201, mimetype='application/json')


@app.route('/assign/<filename>/<group_name>', methods=['POST', 'PUT'])
def assign_template(filename, group_name):
	template = xml_templates.render_template(filename)
	print(template)
	set_config('192.168.1.1', 'admin', 'admin', template)
	return Response(status=201, mimetype='application/json')
