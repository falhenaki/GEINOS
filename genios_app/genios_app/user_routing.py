from flask import Flask, render_template, session, request, g, redirect, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from genios_app import app, models, auth_module
from sqlalchemy.orm import sessionmaker
from tabledef import *
from genios_app import genios_decorators

engine = create_engine('sqlite:///genios_db.db', echo=True)

@app.route('/genios/users/login', methods='POST')
def login():
    return

@app.route('/genios/users/add_user', methods='POST')
@genios_decorators.roles_required("ADMIN")
def add_User():
    POST_USERNAME = request.form['username']
    POST_PASSWORD = request.form['password']
    POST_RETYPE_PASS = request.form['retype_password']
    POST_EMAIL = request.form['email']

    if POST_PASSWORD != POST_RETYPE_PASS:
        flash('Passwords did not match')
        return render_template('users.html')
    else:
        if auth_module.add_user(POST_USERNAME, POST_PASSWORD, POST_EMAIL):
            flash("User added sucessfully")
        else:
            flash("Username already taken")
    return render_template("users.html")






