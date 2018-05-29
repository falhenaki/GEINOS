from app.core.parameter import parameter_connector
from app.core.template import template_connector
from app import app
import os
from flask import send_from_directory
from werkzeug.utils import secure_filename
from jinja2 import Environment, meta, FileSystemLoader
from app.core.template import template_connector
from app.core.log import log_connector

def save_with_jinja(xml_file, filename, username, user_role, request_ip):
    """
    method to replace the value of all attributes with a tag in replacements with jinja2 tags
    :param xml_file: file to perform replacements on
    :param replacements: xml tags that should have their values replaced with jinja2 tags
    :return: true if file is saved correctly
    """
    if (template_connector.template_exists(filename)):
        log_connector.add_log(1, "Failed to save template: ".format(filename), username, user_role, request_ip)
        return False
    all_params = []
    all_params.extend(parameter_connector.get_all_parameter_names())
    sec_filename = secure_filename(filename)
    path = os.path.join(app.config['UPLOADS_FOLDER'], sec_filename)
    xml_file.save(path)
    print(path)
    with open(path, 'r') as f:
        s = f.read()
    with open(path, 'w') as fout:
        fout.write(s)
        template_connector.add_file(path, sec_filename)
    log_connector.add_log(1, "Saved template: ".format(filename), username, user_role, request_ip)
    return True

def get_template(xml_filename):
    """
    sends the xml template specified
    :param xml_filename: filename to get
    :return: specified filename
    """
    sec_filename = secure_filename(xml_filename)
    return send_from_directory(app.config['UPLOADS_FOLDER'], sec_filename)

def get_template_names():
    """
    stubbed out method to get all template names
    :return:
    """
    return template_connector.get_template_names()

def apply_parameters(xml_filename, device_sn, device_name, request_ip):
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
        if not parameter_connector.parameter_exists(var):
            return None, None

    for var in all_vars:
        to_render[var] = parameter_connector.get_parameter_next_value(var, request_ip)
    return render_jinja(xml_filename, to_render), to_render

def render_jinja(filename, context):
    env = Environment(loader=FileSystemLoader(app.config['UPLOADS_FOLDER']))
    template = env.get_template(filename)
    return template.render(context)