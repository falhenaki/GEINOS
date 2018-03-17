from flask import Flask
import os
import json
from pprint import pprint
app = Flask(__name__, template_folder='templates')
app.config.from_object(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
datafile = "data.json"

data_file_dir = os.path.join(app.root_path, 'static')
data_file_path = os.path.join(data_file_dir, datafile)
data = json.load(open(data_file_path))

app.config.update(dict(
    SECRET_KEY='something_secret',
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://' + str(data['login'][0]['user']) +':' + str(data['login'][0]['password']) +'@bitforcedev.se.rit.edu/se_project',
))
from genios_app import views
if __name__ == '__main__':
   app.run()

