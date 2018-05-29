from app.core.device import device_connector, device_access
from app.core.device_group import device_group_connector
from app.core.template import template_connector, xml_templates
from app.core.device import device_connector
from app.core.log import log_connector
import datetime

def add_list_of_devices(entries, filename, username, user_role, request_ip):
    for entry in entries:
        device_connector.add_device(int(entry[0]), int (entry[1]), int (entry[2]))
    log_connector.add_log(1, "Added all devices from {} file".format(filename), username, user_role, request_ip)
    return True

def apply_template(sn, vn, ip, user, pw, request_ip):
    if device_connector.device_exists_and_templated(sn,vn, True):
        template_name = device_group_connector.get_template_for_device(sn, vn)
        rendered_template, applied_params = xml_templates.apply_parameters(template_name, sn, vn, request_ip)

        if (rendered_template, applied_params) == (None, None):
            log_connector.add_log(1, "Failed to provision device (sn:{}, vn:{}, ip:{}, user:{}). Missing param(s)".format(sn, vn, ip, user), None, None, request_ip)
            return False

        device_connector.set_rendered_params(sn, vn, applied_params)
        device_access.set_config(ip, user, pw, rendered_template)
        device_connector.update_device(sn, 'date_provisioned', datetime.datetime.now())
        #TODO: check if all devices are provisioned, log it
        log_connector.add_log(1, "Provisioned device (sn:{}, vn:{}, ip:{}, user:{})".format(sn, vn, ip, user), None, None, request_ip)
        return True
    else:
        log_connector.add_log(1, "Failed to provision device (sn:{}, vn:{}, ip:{}, user:{})".format(sn, vn, ip, user), None, None, request_ip)
        return False