# Run a test server.
from app import app
from app.core.api import initialize
#import subprocess

#subprocess.call(['app/pyorbit/tst_scr.sh'])

initialize.initialize_APIs()

app.run(host='127.0.0.1', port=5000, debug=True)
