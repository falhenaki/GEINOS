from flask import Flask
app = Flask(__name__, template_folder='templates')
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='something_secret'
))

import genios_app.views