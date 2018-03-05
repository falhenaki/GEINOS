from flask import Flask
import os
app = Flask(__name__, template_folder='templates')
app.config.from_object(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(dict(
    SECRET_KEY='something_secret',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'data.sqlite')
))
from genios_app import views
if __name__ == '__main__':
   app.run()

