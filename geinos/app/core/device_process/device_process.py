from app.core.device import device_connector
from app.core.device import device_helpers
import threading
#TODO Need to check if device requires cert and has cert before configuring.
def device_config_process():
    while True:
        devices = device_connector.get_devices_exist_and_scep()
        if devices is not False:
            for device in devices:
                t = threading.Thread(target=config_scep_thread,
                                    args=(device.IP, device.username, device.password, device.serial_number,))

        template_devices = device_connector.get_templated_devices()
        #TODO Figure out why we need to send the vendor_name or user name, and ip.
        if len(template_devices) > 0:
            for device in template_devices:
                t = threading.Thread(target=config_device_thread,
                                     args=(device.serial_number,'name',device.username,device.password, '1.1.1.1',))

def config_scep_thread(ip,username,password,serial_number):
    if device_helpers.set_scep(ip,username,password,serial_number) is True:
        device_connector.update_device(serial_number, "cert_set", "TRUE")
    else:
        device_connector.update_device(serial_number, "cert_set", "FAIL")

def config_device_thread(sn,vn,ip,usr,passwd,request_ip):
    device_helpers.apply_template(sn,vn,ip,usr,passwd,request_ip)