__author__ = 'DevProfile'

import os
from flask import Flask, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from genios_app import app

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/uploaded_files', methods=['POST'])
def upload_file():
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
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)