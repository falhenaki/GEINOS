import os
from flask import Flask, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from genios_app import app
from xml_templates import *

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
		if file and allowed_file(file.file):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploaded_files/<filename>', methods=['GET'])
def uploaded_file(filename):
	"""
	routing to get a file previously uploaded
	:param filename: filename to get
	:return:
	"""
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploaded_files/generate_jinja2/<filename>', methods=['PUT'])
def replace_jinja(filename):
	"""
	converts given file to jinja2 for now this will only replace the NCServer attribute but will be modified to use a
	set of parameters from a given device group
	:param filename: filename stored in server to have jinja templating applied to
	:return: jinja2 formatted xml file
	"""
	file = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
	if file == None:
		flash("Given file does not exist")
		return url_for('404')
	return xml_templates.generate_jinja(file, 'NCServer')