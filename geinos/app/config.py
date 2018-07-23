# Statement for enabling the development environment
DEBUG = True
USE_DEBUGGER=False
USE_RELOADER=False
# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQL_USERNAME = 'admin'
SQL_PASSWORD = 'password'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' + SQL_USERNAME + ':' + SQL_PASSWORD + '@bitforcedev.se.rit.edu/se_project'
#SQLALCHEMY_DATABASE_URI = 'sqlite:////home/qasim/Desktop/se_project.db'
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' + SQL_USERNAME + ':' + SQL_PASSWORD + '@localhost/demo'
DATABASE_CONNECT_OPTIONS = {}
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# allowed file extensions
UPLOADS_FOLDER = os.path.join(BASE_DIR, 'app/core/upload_folder')
APPLIED_PARAMS_FOLDER = os.path.join(BASE_DIR, 'app/core/assigned_params')
ALLOWED_EXTENSIONS = set({'xml'})
DEVICE_PROCESS = 2
