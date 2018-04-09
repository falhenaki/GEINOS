import os
from os.path import realpath, join, dirname
from flask import Flask, request, redirect, url_for, flash, send_from_directory, render_template, json
from werkzeug.utils import secure_filename
from app import app
from flask import Response
from app.core_module import xml_templates, genios_decorators

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/uploaded_files', methods=['POST'])
def upload_file():
	"""
	routing to upload a new file will overwite a file of the same name if it already exists
	:return:
	"""
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		filename = secure_filename(file.filename)
		xml_templates.store_file(filename, file)
		response = app.response_class(
			response=file,
			status=200,
			mimetype='application/json'
		)
		return response


@app.route('/uploaded_files/<filename>', methods=['GET'])
def uploaded_file(filename):
	"""
	routing to get a file previously uploaded
	:param filename: filename to get
	:return:
	"""
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
	"""
	route to render and apply a template to a device group
	:param filename: name of template to apply
	:param group_name: group to apply template to
	:return: status of operation
	"""
	template = xml_templates.render_template(filename)
	print(template)
	#TODO send this rendered template to devices
	return Response(status=201, mimetype='application/json')