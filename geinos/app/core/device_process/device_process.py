from app.core.device import device_connector
from sqlalchemy.orm import sessionmaker
from app import engine, app
from app.core.device import device_helpers
from app.core.device import device_connector
from app.core.device.device import Device
from app import engine, app
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
m = Manager()
q = m.Queue()

def config_scep_thread(dev):
    '''
    p_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    device = device_connector.get_device(dev)
    result = device_helpers.set_scep(device[0]['IP'],"admin","admin",device[0]['serial_number'])
    device_connector.set_device_access(dev, "FALSE")
    p_engine.dispose()
    '''
    print(dev)
    time.sleep(3)
    result = 1
    return result


def config_device_thread(dev):
    '''
    p_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    engine = p_engine
    device = device_connector.get_device(dev)
    result = device_helpers.apply_template(device[0]['serial_number'],device[0]['IP'],"admin","admin")
    device_connector.set_device_access(dev, "FALSE")
    p_engine.dispose()
    '''

    time.sleep(10)
    result = 1
    return result



def config_process():
    futures=[]
    pool = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    while True:
        if q.empty() is False:
            process = q.get()
            if 'cert' in process['process']:
                futures.append(pool.submit(config_scep_thread,process['sn'],))
            if 'config' in process['process']:
                futures.append(pool.submit(config_scep_thread, process['sn'],))
        for future in futures:
            if future.done() is True:
                print("TRUE")
                futures.remove(future)



def sample(num):
    for x in range(5):
        print(num)
        time.sleep(1)


if __name__ == '__main__':
    '''
    Session = sessionmaker(bind=engine)
    s = Session()
    x = s.query(Device).first()
    config_process(x)
    '''
    for x in range(10):
        q.put({'sn':x,'process':'config'})
    config_process()


