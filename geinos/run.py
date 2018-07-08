import os
import sys

# Run a test server.
from app import app
from app.core.api import initialize

#import subprocess

#subprocess.call(['app/pyorbit/tst_scr.sh'])

if not os.path.exists(app.config['UPLOADS_FOLDER']):
    os.makedirs(app.config['UPLOADS_FOLDER'])

if not os.path.exists(app.config['APPLIED_PARAMS_FOLDER']):
    os.makedirs(app.config['APPLIED_PARAMS_FOLDER'])

initialize.initialize_APIs()

app.run(host='0.0.0.0', port=5000, debug=True)
