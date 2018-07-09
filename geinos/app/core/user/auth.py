from flask import session
from app.core.user import user_connector
from app.core.log import log_connector
from datetime import datetime
from app.core.radius import radius_connector

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
        if (radius_connector.authenticate_user(username_or_token, password)):
            connector = user_connector.DB_User_Connection(username_or_token, password)
            if connector.is_legal():
                connector.update_last_login(datetime.now)
                return connector.this_user
            else:
                return None
        else:
            return None
    else:
        return None

def add_user(username, password, email, role_type, curr_username, user_role, request_ip):
    """
    adds user with given username password and email
    :param username: username to add
    :param password: user password
    :param email: user email
    :return: true if user is added false otherwise
    """
    if user_connector.check_username_availability(username):
        user_connector.add_user(username, password, email, role_type)
        log_connector.add_log('ADD USER', "Added new user: {}".format(username), curr_username, user_role, request_ip)
        return True
    log_connector.add_log('ADD USER FAIL', "Failed to add user: {}".format(username), curr_username, user_role, request_ip)
    return False

def remove_user(username, curr_username, user_role, request_ip):
    """
    removes user from database
    :param username: username to remove
    :return:
    """
    #TODO: error checking
    log_connector.add_log('DELETE USER', "Removed user: {}".format(username), curr_username, user_role, request_ip)
    user_connector.remove_user(username)

def change_user_role(username, new_role):
    """
    changes the role of the given user
    :param username: username to have privilages changed
    :param new_role: role to change user to
    :return:
    """
    user_connector.change_user_role(username, new_role)

def check_username_availability(username):
    return user_connector.check_username_availability(username)

def get_user_role(username):
    return user_connector.get_user_role(username)

def update_user_login(username):
    user_connector.change_user_lastlogin(username)