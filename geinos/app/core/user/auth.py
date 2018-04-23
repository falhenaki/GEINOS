from flask import session
from app.core.user import user_connector
from app.core.log import log_connector
from datetime import datetime



def login(username_or_token, password):
    """
    checks user login and if it is legal sets the required session tokens appropriately
    :param username: username to login
    :param password: password to check
    :return: true if user is logged in false otherwise
    """
    usr = user_connector.authenticate_token(username_or_token)
    if usr:
        return usr
    elif not usr and password:
        connector = user_connector.DB_User_Connection(username_or_token, password)
        print(0000)
        print(connector.is_legal())
        print(0000)
        if connector.is_legal():
            session['username'] = username_or_token
            session['user_role'] = connector.get_role()
            connector.update_last_login(datetime.now)
            return True
        else:
            return False
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
    if user_connector.check_username_availability(username):
        user_connector.add_user(username, password, email, role_type)
        log_connector.add_log(1,"User added", session['username'], session['user_role'])
        return True
    return False

def remove_user(username):
    """
    removes user from database
    :param username: username to remove
    :return:
    """
    user_connector.remove_user(username)

def change_user_role(username, new_role):
    """
    changes the role of the given user
    :param username: username to have privilages changed
    :param new_role: role to change user to
    :return:
    """
    user_connector.change_user_role(username, new_role)

def logout():
    """
    logs the user out of the current session
    :return:
    """
    session.pop('username', None)
    session.pop('user_role', None)

def check_username_availability(username):
    return user_connector.check_username_availability(username)

def get_user_role(username):
    return user_connector.get_user_role(username)

def update_user_login(username):
    user_connector.change_user_lastlogin(username)