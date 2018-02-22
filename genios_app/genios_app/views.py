from flask import Flask, render_template, session, request, g, redirect, url_for, abort, flash
from genios_app import app

@app.route('/')
def start_app():
	"""
	Initial route of the app renders a basic login template or connection test if the user is logged in
	:return: login template or connection test page
	"""
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('connection_test.html')

@app.route('/login', methods=['POST'])
def login():
	"""
	route to submit login requests to TODO add a database connection
	:return: returns to previous route with a potentially changed login status
	"""
	error = None
	if request.form['password'] == 'password' and request.form['username'] == 'admin':
		session['logged_in'] = True
	else:
		flash('Incorrect Username and/or Password')
	return start_app()

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return start_app()

if __name__ == "__main__":
	app.run()
