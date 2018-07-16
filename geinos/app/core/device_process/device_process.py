from app.core.device import device_connector
from sqlalchemy.orm import sessionmaker
from app import engine, app
from app.core.device import device_helpers
from app.core.device import device_connector
from app.core.device.device import Device
from app import engine, app
from app.core.device_process import dev_queue
import os
import concurrent.futures
from sqlalchemy.orm import sessionmaker
from app.core.scep import scep_server
import time
from multiprocessing import Queue,Manager
from sqlalchemy import create_engine
from geinos.test_scripts import whatever
from app.core.scep.scep import Scep
from app import engine
from app.core.log import log_connector


def config_scep_thread(dev):
    #p_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    device = device_connector.get_device(dev)
    result = device_helpers.set_scep(device[0]['IP'],"admin","admin",device[0]['serial_number'])
    device_connector.set_device_access(dev, "FALSE")
    log_connector.add_log( "Get Cert Device {}".format(dev),'Cert Status:' + result,
                                      'System', 'None', 'None')
    if "Error" not in result:
        dev_queue.try_add_dev_queue(dev)
    #p_engine.dispose()
    return result


def config_device_thread(dev):

    device = device_connector.get_device(dev)
    result = device_helpers.apply_template(device[0]['serial_number'],device[0]['IP'],"admin","admin")
    device_connector.set_device_access(dev, "FALSE")
    return result



def config_process(device_queue):

    futures=[]
    pool = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    while True:
        if device_queue.empty():
            time.sleep(5)
        if device_queue.empty() is False:
            process = device_queue.get()
            if 'cert' in process['process']:
                print(process['sn'])
                log_connector.add_log("Device {}".format(process['sn']),'Cert Begin',
                                      'System', 'None', 'None')
                futures.append(pool.submit(config_scep_thread,process['sn'],))
            if 'config' in process['process']:
                log_connector.add_log("Device {}".format(process['sn']),'Config Begin',
                                      'System', 'None', 'None')
                futures.append(pool.submit(config_scep_thread, process['sn'],))
        for future in futures:
            if future.done() is True:
                print("TRUE")
                futures.remove(future)