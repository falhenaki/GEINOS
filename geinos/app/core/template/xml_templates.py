from app.core.parameter import parameter_connector
from app.core.template import template_connector
from app import app
import os
from flask import send_from_directory
from werkzeug.utils import secure_filename
from jinja2 import Environment, meta, FileSystemLoader
from app.core.template import template_connector
from app.core.log import log_connector
from xml.etree import ElementTree as ET
from app.core.exceptions.custom_exceptions import MissingResource, Conflict

def save_with_jinja(xml_file, filename, username, user_role, request_ip):
    """
    method to replace the value of all attributes with a tag in replacements with jinja2 tags
    :param xml_file: file to perform replacements on
    :param replacements: xml tags that should have their values replaced with jinja2 tags
    :return: true if file is saved correctly
    """
    if (template_connector.template_exists(filename) or not valid_xml(xml_file)):
        log_connector.add_log('SAVE TEMPLATE FAIL', "Failed to save template: {}".format(filename), username, user_role, request_ip)
        return False
    all_params = []
    all_params.extend(parameter_connector.get_all_parameter_names())
    sec_filename = secure_filename(filename)
    path = os.path.join(app.config['UPLOADS_FOLDER'], sec_filename)
    xml_file.save(path)
    with open(path, 'r') as f:
        s = f.read()
    with open(path, 'w') as fout:
        fout.write(s)
        template_connector.add_file(sec_filename)
    log_connector.add_log('SAVE TEMPLATE', "Saved template: {}".format(filename), username, user_role, request_ip)
    return True

def delete_template(filename, username, user_role, request_ip):
    if (not template_connector.template_exists(filename)):
        log_connector.add_log('DELETE TEMPLATE FAIL', "Failed to delete template: {}".format(filename), username, user_role, request_ip)
        return False
    sec_filename = secure_filename(filename)
    path = os.path.join(app.config['UPLOADS_FOLDER'], sec_filename)
    if (os.path.isfile(path)):
        os.remove(path)
        log_connector.add_log('DELETED TEMPLATE', "Deleted template: {}".format(filename), username, user_role, request_ip)
        return True
    else:
        log_connector.add_log('DELETE TEMPLATE FAIL', "Failed to delete template: {}".format(filename), username, user_role, request_ip)
        return False

def valid_xml(xml_file):
    return True
    try:
        x = ET.fromstring(xml_file)
    except:
        raise Conflict("XML file to be added is not of valid XML form")

def get_template(xml_filename):
    """
    sends the xml template specified
    :param xml_filename: filename to get
    :return: specified filename
    """
    sec_filename = secure_filename(xml_filename)
    try:
        with open(os.path.join(app.config['UPLOADS_FOLDER'], sec_filename), 'r') as myfile:
            data = myfile.read()
            print(sec_filename)
    except FileNotFoundError:
        print("Attempted to get_template {} but file was not found".format(xml_filename))
        raise Conflict("File Not Found")
    return data

def get_templates():
    """
    stubbed out method to get all template names
    :return:
    """
    return template_connector.get_templates()

def apply_parameters(xml_filename, request_ip, sn):
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
    param_file = ''
    for var in all_vars:
        to_render[var] = parameter_connector.get_parameter_next_value(var, request_ip, sn)
    for rendered in to_render:
        param_file += (rendered) + '=' + to_render[rendered] + '\n'
    return param_file

def render_jinja(filename, context):
    env = Environment(loader=FileSystemLoader(app.config['UPLOADS_FOLDER']))
    template = env.get_template(filename)
    return template.render(context)

def parse_config_params(param_file, template_file, sn):
    to_render = {}
    with open(param_file, 'r') as fin:
        s = fin.read()
        for param_set in s.splitlines():
            pair = param_set.split('=')
            if pair[1] == '??dynamic??':
                to_render[pair[0]] = parameter_connector.get_dynamic_parameter(pair[0], sn)
            else:
                to_render[pair[0]] = pair[1]

    return render_jinja(template_file, to_render)