from app.core_module import db_connector
from app import app
import os
from flask import send_from_directory
from jinja2 import Environment, meta, FileSystemLoader


def generate_jinja(xml_filename):
	"""
	method to replace the value of all attributes with a tag in replacements with jinja2 tags
	:param xml_file: file to perform replacements on
	:param replacements: xml tags that should have their values replaced with jinja2 tags
	:return: xml file with desired replacements converted to jinja2 tags
	"""
	all_params = db_connector.get_all_parameters()
	xml_file = os.path.join(app.config['UPLOADS_FOLDER'], xml_filename)
	with open(xml_file, 'r') as f:
		s = f.read()
	with open(xml_file, 'w') as fout:
		for param in all_params:
			s = s.replace(param, '{{' + param + '}}')
		fout.write(s)
	return send_from_directory(app.config['UPLOADS_FOLDER'], xml_filename)

def store_file(xml_filename, file):
	file.save(os.path.join(app.config['UPLOADS_FOLDER'], xml_filename))

def get_file(xml_filename):
	return send_from_directory(app.config['UPLOADS_FOLDER'], xml_filename)

def render_template(xml_filename):
	"""
	method to pull all jinja variables from file and replace them with the appropriate values
	:param xml_filename: file to replace jinja variables
	:return: template containing replaced variables
	"""
	xml_file = os.path.join(app.config['UPLOADS_FOLDER'], xml_filename)
	all_vars = []
	with open(xml_file, 'r') as f:
		env = Environment()
		s = f.read()
		ast = env.parse(s)
		all_vars.extend(meta.find_undeclared_variables(ast))
	to_render = {}
	for var in all_vars:
		to_render[var] = db_connector.get_parameter_next_value(var)
	return render(xml_filename, to_render)

def render(filename, context):
	env = Environment(loader=FileSystemLoader(app.config['UPLOADS_FOLDER']))
	template = env.get_template(filename)
	return template.render(context)