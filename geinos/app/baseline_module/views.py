from flask import Blueprint
from flask import Flask, render_template, session, request, g, redirect, url_for, abort, flash
from app.baseline_module import __init__, models, auth_module, genios_decorators, user_routing,db_connector
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
	print(generate_password_hash("password"))
	print(generate_password_hash("password"))
	if not 'username' in session:
		return render_template('login.html')
	else:
		return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
	'''
	route to submit login requests to TODO add a database connection
	:return: returns to previous route with a potentially changed login status
	'''
	error = None
	if request.method == 'POST':
		POST_USERNAME = str(request.form['username'])
		POST_PASSWORD = str(request.form['password'])
		auth_module.login(POST_USERNAME, POST_PASSWORD)
		return start_app()

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	auth_module.logout()
	return start_app()

@app.route('/ping_device', methods=['GET', 'POST'])
def simple_ping():
	r = models.simple_ping()
	flash(r)
	return start_app()

@app.route('/users', methods=['GET', 'POST'])
@genios_decorators.requires_roles('ADMIN')
def users():
	test = db_connector.get_all_users()

	return render_template('users.html', test=test)


@app.route('/createusers', methods=['POST'])
#@genios_decorators.login_required
def createusers():


	return render_template('users.html')

@app.route('/devices', methods=['GET', 'POST'])
def devices():
	return render_template('devices.html')

@app.route('/device_groups', methods=['GET', 'POST'])
def device_groups():
	return render_template('device_groups.html')

@app.route('/user_groups', methods=['GET', 'POST'])
def user_groups():
	return render_template('layout.html')

@app.route('/enrollment', methods=['GET', 'POST'])
def enrollment():
	return render_template('layout.html')

@app.route('/support', methods=['GET', 'POST'])
def support():
	return render_template('layout.html')

@app.route('/templates', methods=['GET', 'POST'])
def templates():
	return render_template('templates.html')

@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
	return render_template('assignments.html')

@app.route('/parameters', methods=['GET', 'POST'])
def parameters():
	return render_template('parameters.html')

@app.route('/deployments', methods=['GET', 'POST'])
def deployments():
	return render_template('layout.html')

@app.route('/events_alarms', methods=['GET', 'POST'])
def events_alarms():
	return render_template('layout.html')

@app.route('/authentication', methods=['GET', 'POST'])
def authentication():
	return render_template('layout.html')
