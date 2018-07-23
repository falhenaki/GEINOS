import os
import concurrent.futures
# Run a test server.
from app import app
from app.core.api import initialize
from app.core.device_process import device_process,dev_queue
from multiprocessing import Manager

from flask import render_template

import time
#import subprocess

#subprocess.call(['app/pyorbit/tst_scr.sh'])

if not os.path.exists(app.config['UPLOADS_FOLDER']):
    os.makedirs(app.config['UPLOADS_FOLDER'])

if not os.path.exists(app.config['APPLIED_PARAMS_FOLDER']):
    os.makedirs(app.config['APPLIED_PARAMS_FOLDER'])

from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher


'''cherrypy.config.update({
        'engine.autoreload_on': True,
        'log.screen': True,
        'server.socket_port': 5000,
        'server.socket_host': '0.0.0.0'
    })*/
'''




if __name__ == '__main__':
    initialize.initialize_APIs()


    d = PathInfoDispatcher({'/': app})
    server = WSGIServer(('0.0.0.0', 5000), d)
    m = Manager()
    device_queue = m.Queue()
    dev_queue.device_queue = device_queue
    pool = concurrent.futures.ProcessPoolExecutor(max_workers=1)
    pool.submit(device_process.config_process,device_queue)


    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

#cherrypy.engine.start()
#cherrypy.engine.block()
#app.run(host='0.0.0.0', port=5000, debug=True)
