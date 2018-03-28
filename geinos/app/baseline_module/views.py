from flask import Blueprint
from flask import Flask, render_template, session, request, g, redirect, url_for, abort, flash
from app.baseline_module import __init__, models, auth_module, genios_decorators, user_routing,db_connector, device_helpers
import datetime
from app import app
from werkzeug.security import generate_password_hash, check_password_hash


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@app.route('/', methods=['GET'])
def start_app():
	"""
	Initial route of the app renders a basic login template or connection test if the user is logged in
	:return: login template or connection test page
	"""
	if not 'username' in session:
		return render_template('index.html')
	else:
		return render_template('index.html')

