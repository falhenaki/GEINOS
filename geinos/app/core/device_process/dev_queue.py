from app.core.device import device_connector
from app.core.device_group import device_group_connector
from app.core.log import log_connector
from app.core.device_process import tasks_connector

device_queue = []



def try_add_dev_queue(serial_number):
    if device_connector.get_dev_exist(serial_number) is False:
        return False
    status = device_connector.get_cert_or_config(serial_number)
    if status is False:
        return False
    access = device_connector.get_device_access(serial_number)
    if access is True:
        return False
    if "TRUE" in status['config']:
        if device_connector.get_rdy_config(serial_number):
            tasks_connector.add_task(serial_number,'WAITING_CONFIG')
            log_connector.add_log( "Queue Device {}".format(serial_number),'In queue for config',
                                   'System', 'None', 'None')
            device_connector.set_device_access(serial_number,"TRUE")
            device_queue.put({'sn':serial_number,'process':'config'})
            return True
    if "TRUE" in status['cert_req'] and "TRUE" not in status['cert_obt']:
        device_connector.set_device_access(serial_number, "TRUE")
        tasks_connector.add_task(serial_number, 'WAITING_CERT')
        log_connector.add_log("Queue Device {}".format(serial_number),'In queue for certification',
                              'System', 'None', 'None')
        device_queue.put({'sn': serial_number, 'process': 'cert'})
        return True
    return False

def try_add_group_queue(group_name):
    try:
        devices = device_group_connector.get_all_devices_in_group(group_name)
    except:
        return False
    for device in devices:
        try_add_dev_queue(device['serial_number'])

if __name__ == '__main__':
    print("Running")
