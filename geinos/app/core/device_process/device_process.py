from app.core.device import device_helpers
from app.core.device import device_connector
from app.core.device_process import tasks_connector
from app import app
import concurrent.futures

import time
from app.core.log import log_connector


def config_scep_thread(dev):
    result = "SCEP configuration exception"
    try:
        for _ in range(2):
            device = device_connector.get_device(dev)
            tasks_connector.add_task(dev, 'Obtaining Certificate')
            result = device_helpers.set_scep(device[0]['IP'],"admin","admin",device[0]['serial_number'])
            if "Error" or "failure" not in result:
                break
    except Exception as ex:
        print('SCEP PROCESS FAILED: ' + str(ex))
    finally:
        print("SCEP Process Result: " + result)
        device_connector.set_device_access(dev, "FALSE")
        tasks_connector.delete_task(dev)
        log_connector.add_log("Get Cert Device {}".format(dev), 'Cert Status:' + result,
                              'System', 'None', 'None')
    config_device_thread(dev)


def config_device_thread(dev):
    result = "Configuration exception"
    device = device_connector.get_device(dev)
    try:
        for _ in range(2):
            tasks_connector.add_task(dev, 'Configuring Device')
            result = device_helpers.apply_template(device[0]['serial_number'], device[0]['IP'], "admin", "admin")
            if result is True:
                break
    except Exception as ex:
        print("Configuration process failed: " + str(ex))
    finally:
        print("Config Process Result: " + result)
        log_connector.add_log("Configure device {}".format(dev), 'Config Status:' + result,
                              'System', 'None', 'None')
        device_connector.set_device_access(dev, "FALSE")
        tasks_connector.delete_task(dev)


def config_process(device_queue):

    device_futures=[]
    pool = concurrent.futures.ProcessPoolExecutor(max_workers=app.config['DEVICE_PROCESS'])
    while True:
        if device_queue.empty():
            time.sleep(1)
        if device_queue.empty() is False:
            process = device_queue.get()
            if 'cert' in process['process']:
                log_connector.add_log("Device {}".format(process['sn']),'Cert Begin',
                                      'System', 'None', 'None')
                device_futures.append(pool.submit(config_scep_thread,process['sn'],))
            if 'config' in process['process']:
                log_connector.add_log("Device {}".format(process['sn']),'Config Begin',
                                      'System', 'None', 'None')
                device_futures.append(pool.submit(config_device_thread, process['sn'],))
        for future in device_futures:
            if future.done() is True:
                device_futures.remove(future)

