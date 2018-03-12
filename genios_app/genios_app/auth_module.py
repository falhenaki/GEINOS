from flask import session
from genios_app import db_connector

def login(username, password):
    """
    checks user login and if it is legal sets the required session tokens appropriately
    :param username: username to login
    :param password: password to check
    :return: true if user is logged in false otherwise
    """
    connector = db_connector.DB_User_Connection(username, password)
    if connector.is_legal():
        session['username'] = username
        print("set username")
        session['user_role'] = connector.get_role()
        print("tried setting user_role")
        return True
    else:
        return False

def add_user(username, password, email):
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
    removes user from database
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
    db_connector.modify_user_role(username, new_role)

def logout():
    """
    logs the user out of the current session
    :return:
    """
    session.pop('username', None)
    session.pop('user_role', None)