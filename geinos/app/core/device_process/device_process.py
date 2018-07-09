from app.core.device import device_connector
from app.core.device import device_helpers
from multiprocessing import Pool
import time

def device_config_process():
    while True:
        devices = device_connector.get_devices_exist_and_scep()
        if devices is not False:
            pool = Pool(processes=50)
            [pool.apply_async(config_scep_thread, args=(x,)) for x in devices]

        template_devices = device_connector.get_rdy_config()
        print(template_devices)
        if template_devices is not None:
            pool = Pool(processes=50)
            [pool.apply_async(config_device_thread(), args=(x,)) for x in template_devices]
        print("Next loop")
        time.sleep(10)

def config_scep_thread(device):
    if device_helpers.set_scep(device.IP,device.username,device.password,device.serial_number) is True:
        device_connector.update_device(device.serial_number, "cert_set", "TRUE")
    else:
        device_connector.update_device(device.serial_number, "cert_set", "FAIL")

def config_device_thread(device):
    device_helpers.apply_template(device.serial_number,device.IP,device.username,device.password)

if __name__ == '__main__':
    device_config_process()