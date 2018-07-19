from sqlalchemy.orm import sessionmaker
from app.core.user.user import User
from app import engine
import json
import datetime
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from math import floor
import time
authen = HTTPBasicAuth()

@authen.verify_password
def verify_password(username, password):
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.username == username).first()
    if not user or not user.verify_password(password):
        return False
    Flask.g.user = user
    s.close()
    return True

def authenticate_token(token):
    user = User.verify_auth_token(token)
    return user

def get_user_by_id(id):
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.id == id).first()
    s.close()
    return user

def get_user(username):
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.username == username).first()
    s.close()
    return user

def add_user(username, password, email, role_type):
    """
    adds user to the database
    :param username: username to add
    :param password: password to attach to username
    :param email: user email
    :param role_type: user role
    :return:
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    user = User(username, password, email, role_type)
    s.add(user)
    s.commit()
    s.close()


def remove_user(username):
    """
    removes specified user from the database
    :param username: user to remove
    :return:
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    s.query(User).filter(User.username == username).delete()
    s.commit()
    s.close()

def change_user_role(username, new_role):
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.username == username).first()
    if user.role_type == new_role:
        s.close()
        return False
    else:
        user.role_type = new_role
        s.commit()
        s.close()
    return True

def change_user_email(username, new_email):
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.username == username).first()
    try:
        if user.email == new_email:
            s.close()
            return False
        else:
            user.email = new_email
    except AttributeError:
        user.email = new_email
        s.commit()
    s.close()
    return True

def change_user_lastlogin(username):
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.username == username).first()
    user.last_login = datetime.datetime.now()
    s.commit()
    s.close()
    return True

def get_all_users():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).with_entities(User.role_type, User.username, User.email, User.last_login)
    ret = []
    atts_returned = ['role_type', 'username', 'email', 'last_login']
    for d in query:
        dictionary = {}
        for att in atts_returned:
            dictionary[att] = getattr(d, att)
        ret.append(dictionary)
    s.close()
    return ret


def get_user_role(username):
    """
    gets the user's current role
    :param username: user to check
    :return: user's current role
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username == username)
    user = query.first()
    s.close()
    return user.role_type

def check_username_availability(username):
    """
    checks to see if username is taken returns true if username is free false if it is taken
    :param username: username to check
    :return: true if username is free false if it is taken
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.username == username).first()
    if user:
        s.close()
        return False
    s.close()
    return True

def change_role_type(username, role_type):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_(username))
    user = query.first()
    if user:
        user.change_role(role_type)
    s.close()

class DB_User_Connection():
    """
    object that can be used to hold and get user information about a user in the database
    """
    legal_user = False
    def __init__(self, username, password):
        Session = sessionmaker(bind=engine)
        self.s = Session()
        self.check_legal(username, password)

    def is_legal(self):
        """
        getter for checking if login should be allowed
        :return: true if username and password were valid false otherwise
        """
        return self.legal_user

    def check_legal(self, username, password):
        """
        checks username and password with database to see if the login is valid
        :param username: username to check
        :param password: password to check
        :return:
        """
        query = self.s.query(User).filter(User.username == username)
        user = query.first()
        #if user exists
        if user:
            #check password
            if user.check_password(password):

                self.legal_user = True
                self.this_user = user

    def get_role(self):
        """
        getter for the user pulled from the database's role
        :return: user's role type
        """
        return self.this_user.role_type

    def update_last_login(self, login_datetime):
        self.this_user.update_last_login(login_datetime)

    def close_session(self):
        self.s.close()