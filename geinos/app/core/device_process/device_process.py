from app.core.device import device_helpers
from app.core.device import device_connector
from app.core.device_process import tasks_connector
from app import app
import concurrent.futures

import time
from app.core.log import log_connector


def config_scep_thread(dev):
    for _ in range(2):
        device = device_connector.get_device(dev)
        tasks_connector.add_task(dev[0]['serial_number'], 'CERT')
        result = device_helpers.set_scep(device[0]['IP'],"admin","admin",device[0]['serial_number'])
        device_connector.set_device_access(dev, "FALSE")
        log_connector.add_log( "Get Cert Device {}".format(dev),'Cert Status:' + result,
                                      'System', 'None', 'None')
        if "Error" not in result:
            break
    tasks_connector.delete_task(dev[0]['serial_number'])


def config_device_thread(dev):
    for _ in range(2):
        device = device_connector.get_device(dev)
        #tasks_connector.add_task(dev[0]['serial_number'], 'CONFIG')
        result = device_helpers.apply_template(device[0]['serial_number'],device[0]['IP'],"admin","admin")
        device_connector.set_device_access(dev, "FALSE")
        if result is True:
            break
    tasks_connector.delete_task(dev[0]['serial_number'])


def config_process(device_queue):

    futures=[]
    pool = concurrent.futures.ProcessPoolExecutor(max_workers=app.config['DEVICE_PROCESS'])
    while True:
        if device_queue.empty():
            time.sleep(1)
        if device_queue.empty() is False:
            process = device_queue.get()
            if 'cert' in process['process']:
                log_connector.add_log("Device {}".format(process['sn']),'Cert Begin',
                                      'System', 'None', 'None')
                futures.append(pool.submit(config_scep_thread,process['sn'],))
            if 'config' in process['process']:
                log_connector.add_log("Device {}".format(process['sn']),'Config Begin',
                                      'System', 'None', 'None')
                futures.append(pool.submit(config_device_thread, process['sn'],))
        for future in futures:
            if future.done() is True:
                futures.remove(future)

