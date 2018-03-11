from flask import session
from db_connector import *

def login(username, password):
    connector = DB_USER_Connection()
    if connector.legal_user(username, password):
        session['username'] = username
        session['user_role'] = connector.get_role()
        session['logged_in'] = True
        return True
    else:
        return False

def add_user(username, password, email):
    db_connector.add_user(username, password, email)

def remove_user():
    return True

def change_user_role():
    return True

def logout():
    session.pop('username', None)
    session.pop('user_role', None)
    return True