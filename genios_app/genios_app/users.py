from flask import Flask, render_template, session, request, g, redirect, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from genios_app import app, models
from sqlalchemy.orm import sessionmaker
from tabledef import *
from genios_decorations import login_required

engine = create_engine('sqlite:///genios_db.db', echo=True)

@app.route('/genios/users/login', methods='POST')
def login():
    return

@app.route('/genios/users/add_user', methods='POST')
@login_required
def add_User():
    POST_USERNAME = request.form['username']
    POST_PASSWORD = request.form['password']
    POST_RETYPE_PASS = request.form['retype_password']
    POST_EMAIL = request.form['email']
    return

@app.route('genios/user_groups/add_group', methods='POST')
@login_required
def add_user_group():
    return

@app.route('genios/user_groups/remove_group/<int:group_id>', methods='DELETE')
@login_required
def remove_user_group():
    return





