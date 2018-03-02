from flask import Flask, render_template, session, request, g, redirect, url_for, abort, flash
from genios_app import app, models
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///tutorial.db', echo=True)


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

	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])

	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
	result = query.first()

	if result:
		session['logged_in'] = True
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

