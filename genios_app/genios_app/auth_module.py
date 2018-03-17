from flask import session
from genios_app import db_connector
from datetime import datetime

def login(username, password):
    """
    checks user login and if it is legal sets the required session tokens appropriately
    :param username: username to login
    :param password: password to check
    :return: true if user is logged in false otherwise
    """
    connector = db_connector.DB_User_Connection(username, password)
    print(connector.is_legal())
    if connector.is_legal():
        session['username'] = username
        session['user_role'] = connector.get_role()
        connector.update_last_login(datetime.now)
        return True
    else:
        return False

def add_user(username, password, email, role_type):
    """
    adds user with given username password and email
    :param username: username to add
    :param password: user password
    :param email: user email
    :return: true if user is added false otherwise
    """
    if db_connector.check_username_availability(username):
        db_connector.add_user(username, password, email)
        return True
    return False

def remove_user(username):
    """
    removes user from databa
    se
    :param username: username to remove
    :return:
    """
    db_connector.remove_user(username)

def change_user_role(username, new_role):
    """
    changes the role of the given user
    :param username: username to have privilages changed
    :param new_role: role to change user to
    :return:
    """
    db_connector.change_user_role(username, new_role)

def logout():
    """
    logs the user out of the current session
    :return:
    """
    session.pop('username', None)
    session.pop('user_role', None)

def check_username_availability(username):
    return db_connector.check_username_availability(username)

def get_user_role(username):
    return db_connector.get_user_role(username)