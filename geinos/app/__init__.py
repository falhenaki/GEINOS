# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# Define the WSGI application object
app = Flask(__name__)
#Database Login Credentials
import json
datafile = "data.json"

data_file_dir = os.path.join(app.root_path, 'static')
data_file_path = os.path.join(data_file_dir, datafile)
data = json.load(open(data_file_path))

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

engine = create_engine('mysql+mysqlconnector://' + str(data['login'][0]['user']) +':' + str(data['login'][0]['password']) +'@bitforcedev.se.rit.edu/se_project')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return #render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.core_module.views import mod_auth as auth_mod

# Register blueprint(s)
app.register_blueprint(auth_mod)
# app.register_blueprint(xyz_module)
# ..
# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()
