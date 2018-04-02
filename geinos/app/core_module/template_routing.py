import os
from os.path import realpath, join, dirname
from flask import Flask, request, redirect, url_for, flash, send_from_directory, render_template, json
from werkzeug.utils import secure_filename
from app import app
from app.core_module import xml_templates

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/uploaded_files', methods=['POST'])
def upload_file():
	"""
	routing to upload a new file
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
	file = xml_templates.get_file(filename)
	response = app.response_class(
		response=file,
		status=200,
		mimetype='application/json'
	)
	return response

@app.route('/uploaded_files/generate_jinja2/<filename>', methods=['PUT'])
def replace_jinja(filename):
	"""
	converts given file to jinja2 for now this will only replace the NCServer attribute but will be modified to use a
	set of parameters from a given device group
	:param filename: filename stored in server to have jinja templating applied to
	:return: jinja2 formatted xml file
	"""
	replacement_test = ['template_ntp-server']
	return xml_templates.generate_jinja(filename, replacement_test)