from flask import Flask, render_template, session, request, g, redirect, url_for, abort, flash
from genios_app import app, models, genios_decorators
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tabledef import *

engine = create_engine('sqlite:///genios_db.db', echo=True)


@app.route('/')
def start_app():
	"""
	Initial route of the app renders a basic login template or connection test if the user is logged in
	:return: login template or connection test page
	"""
	if not 'username' in session:
		return render_template('login.html')
	else:
		return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
	"""
	route to submit login requests to
	:return: returns to previous route with a potentially changed login status
	"""
	error = None
	if request.method == 'POST':
		POST_USERNAME = str(request.form['username'])
		POST_PASSWORD = str(request.form['password'])

		Session = sessionmaker(bind=engine)
		s = Session()
		user = s.query(User).filter_by(username=POST_USERNAME).first()

		if user.check_password(POST_PASSWORD):
			print("Hashed: " + user.hashed_password)
			session['logged_in'] = True
			session['username'] = POST_USERNAME
		else:
			flash('Incorrect Username and/or Password')
		return start_app()

@app.route('/logout', methods=['GET', 'POST'])
@genios_decorators.login_required
def logout():
	session.pop('logged_in', None)
	session.pop('username')
	flash('You were logged out')
	return start_app()

@app.route('/ping_device', methods=['GET', 'POST'])
@genios_decorators.login_required
def simple_ping():
	r = models.simple_ping()
	flash(r)
	return start_app()

@app.route('/users', methods=['GET', 'POST'])
@genios_decorators.login_required
def users():
	if request.method == 'POST':
		POST_USERNAME = str(request.form['usr'])


	return render_template('users.html')
@app.route('/createusers', methods=['POST'])
@genios_decorators.login_required
def createusers():
	if request.method == 'POST':
		print('post')
		POST_USERNAME = str(request.form['usr'])
		POST_PASSWORD = str(request.form['password'])
		print(POST_PASSWORD)
		print(POST_USERNAME)
		Session = sessionmaker(bind=engine)
		s = Session()
		user = User(POST_USERNAME, POST_PASSWORD, "email")
		s.add(user)
		s.commit()
	return render_template('users.html')


@app.route('/devices', methods=['GET', 'POST'])
@genios_decorators.login_required
def devices():
	return render_template('devices.html')

@app.route('/device_groups', methods=['GET', 'POST'])
@genios_decorators.login_required
def device_groups():
	return render_template('device_groups.html')

@app.route('/user_groups', methods=['GET', 'POST'])
@genios_decorators.login_required
def user_groups():
	return render_template('layout.html')

@app.route('/enrollment', methods=['GET', 'POST'])
@genios_decorators.login_required
def enrollment():
	return render_template('layout.html')

@app.route('/support', methods=['GET', 'POST'])
@genios_decorators.login_required
def support():
	return render_template('layout.html')

@app.route('/templates', methods=['GET', 'POST'])
@genios_decorators.login_required
def templates():
	return render_template('templates.html')

@app.route('/assignments', methods=['GET', 'POST'])
@genios_decorators.login_required
def assignments():
	return render_template('assignments.html')

@app.route('/parameters', methods=['GET', 'POST'])
@genios_decorators.login_required
def parameters():
	return render_template('parameters.html')

@app.route('/deployments', methods=['GET', 'POST'])
@genios_decorators.login_required
def deployments():
	return render_template('layout.html')

@app.route('/events_alarms', methods=['GET', 'POST'])
@genios_decorators.login_required
def events_alarms():
	return render_template('layout.html')

@app.route('/authentication', methods=['GET', 'POST'])
@genios_decorators.login_required
def authentication():
	return render_template('layout.html')
