from app.core_module import db_connector
from app import app
import os
from flask import send_from_directory


def generate_jinja(xml_filename, replacements):
	"""
	method to replace the value of all attributes with a tag in replacements with jinja2 tags
	:param xml_file: file to perform replacements on
	:param replacements: xml tags that should have their values replaced with jinja2 tags
	:return: xml file with desired replacements converted to jinja2 tags
	"""
	xml_file = os.path.join(app.config['UPLOADS_FOLDER'], xml_filename)
	with open(xml_file, 'r') as f:
		s = f.read()
	with open(xml_file, 'w') as fout:
		for replacement in replacements:
			s = s.replace(replacement, '{{' + replacement + '}}')
		fout.write(s)
	return send_from_directory(app.config['UPLOADS_FOLDER'], xml_filename)

def store_file(xml_filename, file):
	file.save(os.path.join(app.config['UPLOADS_FOLDER'], xml_filename))

def get_file(xml_filename):
	return send_from_directory(app.config['UPLOADS_FOLDER'], xml_filename)