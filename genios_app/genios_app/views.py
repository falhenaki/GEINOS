from flask import Flask, render_template, session, request, g, redirect, url_for, abort, flash
from genios_app import app, models
from sqlalchemy.orm import sessionmaker
from tabledef import *
import datetime

@app.route('/')
def start_app():
	"""
	Initial route of the app renders a basic login template or connection test if the user is logged in
	:return: login template or connection test page
	"""
	if not session.get('logged_in'):
		return render_template('home.html')
	else:
		return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
	"""
	route to submit login requests to TODO add a database connection
	:return: returns to previous route with a potentially changed login status
	"""
	error = None
	if request.method == 'POST':
		POST_USERNAME = str(request.form['username'])
		POST_PASSWORD = str(request.form['password'])

	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.passwordhash.in_([POST_PASSWORD]))
	user = query.first()

		if user.check_password(POST_PASSWORD):
			print("Hashed: " + user.hashed_password)
			session['logged_in'] = True
			session['username'] = POST_USERNAME
		else:
			flash('Incorrect Username and/or Password')
		return start_app()

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return start_app()

@app.route('/ping_device', methods=['GET', 'POST'])
def simple_ping():
	r = models.simple_ping()
	flash(r)
	return start_app()

@app.route('/users', methods=['GET', 'POST'])
def users():
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
