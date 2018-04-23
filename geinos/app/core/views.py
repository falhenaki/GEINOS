from flask import Blueprint
from flask import render_template, request, flash

#from app.core import models, auth, db_connector
from app.core.device import device_helpers
from app import app



# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

"""@app.route('/', methods=['GET'])
def start_app():
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
		auth.login(POST_USERNAME, POST_PASSWORD)
		auth.update_user_login(POST_USERNAME)
		return start_app()
"""
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	auth.logout()
	#return start_app()

@app.route('/ping_device', methods=['GET', 'POST'])
def simple_ping():
	r = models.simple_ping()
	flash(r)
	#return start_app()
"""
@app.route('/users', methods=['GET', 'POST'])
#@genios_decorators.requires_roles('ADMIN')
def users():
	test = db_connector.get_all_users()

	return render_template('users.html', test=test)
"""

@app.route('/createusers', methods=['POST'])
#@genios_decorators.login_required
def createusers():


	return render_template('users.html')
'''
@app.route('/devices', methods=['GET', 'POST'])
def devices():
	devices=db_connector.get_all_devices()
	print(devices)
	return render_template('devices.html', devices=devices)
'''

#@app.route('/device_groups', methods=['GET', 'POST'])
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

#@app.route('/templates', methods=['GET', 'POST'])
def templates():
	return render_template('templates.html')

@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
	return render_template('assignments.html')

#@app.route('/parameters', methods=['GET', 'POST'])
def parameters():
	return render_template('parameters.html')

@app.route('/deployments', methods=['GET', 'POST'])
def deployments():
	return render_template('layout.html')

@app.route('/events_alarms', methods=['GET', 'POST'])
def events_alarms():
    logs = db_connector.get_all_logs()
    return render_template('events_alarms.html', logs=logs)

@app.route('/authentication', methods=['GET', 'POST'])
def authentication():
	return render_template('layout.html')

@app.route('/add_devices_from_list', methods=['POST'])
def add_devices_from_list():
    file = request.files['import_file']
    if file:
        #a = file.read()
        file_data = file.readlines()
        content = [x.strip() for x in file_data]
        device_helpers.add_list_of_devices(content)
        flash("File was read")
    return render_template('devices.html')
