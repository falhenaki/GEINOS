from app.core.device import device_connector, device_access
from app.core.device_group import device_group_connector
from app.core.template import template_connector, xml_templates

def add_list_of_devices(entries):
    for entry in entries:
        device_connector.add_device(int(entry[0]), int (entry[1]), int (entry[2]))
    return True

def apply_template(sn, vn, ip, user, pw):
    template_name = device_group_connector.get_template_for_device(sn, vn)
    rendered_template, applied_params = xml_templates.apply_parameters(template_name, sn, vn)
    device_connector.set_rendered_params(sn, vn, applied_params)
    device_access.set_config(ip, user, pw, rendered_template)
    return True