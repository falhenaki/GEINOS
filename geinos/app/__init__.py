# Import flask and template operators
from flask import Flask, render_template
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# Define the WSGI application object
app = Flask(__name__, static_folder='react/static', template_folder='react')
CORS(app)
#Database Login Credentials
from app import app
import os
datafile = "data.json"

data_file_dir = os.path.join(app.root_path, 'react/static')
data_file_path = os.path.join(data_file_dir, datafile)
#data = json.load(open(data_file_path))

#print(data)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
username = "admin"
password = "password"

'''
if username == "MYSQLUSERHERE" or password == "YOUR PASSWORD here":
    print("Please update mysql credentials in the static/data.json")
    sys.exit()
'''

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
#engine = create_engine('mysql+mysqlconnector://' + username +':' + password +'@localhost/test')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return #render_template('404.html'), 404

@app.route('/')
def hello_world():
    return render_template('index.html')

# Import a module / component using its blueprint handler variable (mod_auth)
#from app.core.views import mod_auth as auth_mod

# Register blueprint(s)
#app.register_blueprint(auth_mod)
# app.register_blueprint(xyz_module)
# ..
# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()

def init_db():
    Session = sessionmaker(bind=engine)
    s = Session()
    s.commit()
