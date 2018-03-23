from flask import Flask, render_template, session, request, g, redirect, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.core_module import __init__, models, auth, db_connector
from sqlalchemy.orm import sessionmaker
from app.core_module.models import *
from app.core_module import genios_decorators
from app import app

#engine = create_engine('sqlite:///genios_db.db', echo=True)
'''
@app.route('/genios/users/login', methods=['POST'])
def login():
    return
'''
@app.route('/genios/add_user', methods=['POST'])
@genios_decorators.requires_roles("ADMIN")
def add_User():

    POST_USERNAME = request.form['usr']
    POST_PASSWORD = request.form['password']
    POST_RETYPE_PASS = request.form['retypepassword']
    POST_EMAIL = request.form['email']
    POST_ROLE = str(request.form['role'])
    test = db_connector.get_all_users()
    if POST_PASSWORD != POST_RETYPE_PASS:

        print('Passwords did not match')
        return render_template('users.html',test=test)
    else:
        if auth.add_user(POST_USERNAME, POST_PASSWORD, POST_EMAIL, POST_ROLE):
            auth.change_user_role(POST_USERNAME, POST_ROLE)
            print("User added sucessfully")
        else:
            print("Username already taken")

    return render_template("users.html",test=test)
