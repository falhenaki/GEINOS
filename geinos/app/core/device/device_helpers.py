from app.core.device import device_connector, device_access
from pyorbit import Device, ConnectError
from app.core.device_group import device_group_connector
from app.core.template import template_connector, xml_templates
from app.core.device import device_connector
from app.core.log import log_connector
from app.core.exceptions.custom_exceptions import MissingResource
from app.core.scep import scep_config,scep_connector,scep_server
import datetime
import csv

#TODO should be moved to device connector
def add_list_of_devices(entries, filename, username, user_role, request_ip):
    for entry in entries:
        device_connector.add_device(entry["vendor_id"], entry["serial_num"], entry["model_num"], entry["location"], username, user_role, request_ip, entry["cert_required"].upper())
    log_connector.add_log('ADD DEVICES', "Added all devices from {} file".format(filename), username, user_role, request_ip)
    return True


def apply_template(sn, ip, user, pw):
    if device_connector.device_exists_and_templated(sn):
        config_path, template_path = device_connector.get_device_template(sn)
        rendered_template = xml_templates.parse_config_params(config_path, template_path, sn)

        if (rendered_template) == (None):
            #TODO Make this log message more meaningful
            log_connector.add_log('APPLY TEMPLATE FAIL', "Failed to provision device (sn:{}, ip:{}, user:{}). Missing param(s)".format(sn, ip, user), None, None, None)
            return False

        device_access.set_config(ip, user, pw, rendered_template)
        device_connector.update_device(sn, 'date_provisioned', datetime.datetime.now())
        #TODO: check if all devices are provisioned, log it
        log_connector.add_log('APPLY TEMPLATE', "Provisioned device (sn:{}, ip:{}, user:{})".format(sn, ip, user), None, None, None)
        return True
    else:
        log_connector.add_log('APPLY TEMPLATE FAIL', "Failed to provision device (sn:{}, ip:{}, user:{})".format(sn, ip, user), None, None, None)
        return False

#TODO add logging and update device modified field
def set_scep(host, user, passwd, serial):
    otp = scep_server.get_otp()
    if "Error" in otp:
        return otp
    dev = Device(host=host, username=user, password=passwd)
    scep_info = scep_connector.get_scep()
    if scep_info is None:
        return 'Error: SCEP information not in database'
        
    scep_thumb = scep_info.thumbprint
    cert_server = scep_config.format_config_cert_server(scep_info.cert_server_id,
                                                        scep_info.server,
                                                        scep_info.digestalgo, scep_info.encryptalgo)
    ca_server = scep_config.format_config_ca_server(scep_info.ca_server_id,scep_thumb)
    cert_info = scep_config.format_config_cert_info(scep_info.cert_info_id, serial,scep_info.country,scep_info.state,
                                                    scep_info.locale,scep_info.organization,scep_info.org_unit)
    cert_config = device_access.set_config(host, user, passwd, cert_server)
    ca_config = device_access.set_config(host, user, passwd, ca_server)
    cert_info_config = device_access.set_config(host, user, passwd, cert_info)
    if cert_config is False:
        return "Error: Failed to config Certificate server information"
        
    if ca_config is False:
        return "Error: Failed to config CA server information"
        
    if cert_info_config is False:
        return "Error: Failed to config Certificate Information"
        
    pk = device_access.generate_private_key(dev,scep_info.key_id)
    if pk is False:
        return "Error: Failed to generate private key"
        
    if "complete" not in pk:
       return "Error: Failed to config Certificate server information"
       
    ca_cert = device_access.get_ca_certs(dev, scep_info.ca_cert_id, scep_info.cert_server_id, scep_info.ca_server_id)
    if ca_cert is False:
        return "Error: Failed to get CA Cert"
        
    if "complete" not in ca_cert:
        return "Error: Device return ed the following when attempt to get a CA Cert:" + ca_cert
        
    client_cert = device_access.get_client_cert(dev, scep_info.cert_server_id, scep_info.ca_server_id, scep_info.client_cert_id,
                    scep_info.cert_info_id,scep_info.ca_cert_id,scep_info.key_id,otp)
    if client_cert is False:
        return "Error: Failed to get Client Cert"
        
    if "complete" not in client_cert:
        return  \
               "Error: Device return ed the following when attempt to get a Client Cert:" + client_cert
    return "Device (sn:{})".format(serial) + "Client Certificate Obtained"

def do_it_all(host,user,passwd,serial):
    #set_scep(host,user,passwd,serial)
    apply_template(serial, host,
                   user, passwd)
