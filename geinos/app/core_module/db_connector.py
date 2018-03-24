from sqlalchemy.orm import sessionmaker, session
from app.core_module.models import *
from app import db, engine
import json
import datetime
from math import floor
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

def change_user_role(username, new_role):
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.username == username).first()
    if user.role_type == new_role:
        return False
    else:
        user.role_type = new_role
        s.commit()
    return True

def change_user_email(username, new_email):
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.username == username).first()
    try:
        if user.email == new_email:
            return False
        else:
            user.email = new_email
    except AttributeError:
        user.email = new_email
        s.commit()
    return True

def change_user_lastlogin(username):
    Session = sessionmaker(bind=engine)
    s = Session()
    user = s.query(User).filter(User.username == username).first()
    user.last_login = datetime.datetime.now()
    s.commit()
    return True

def get_all_users():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User)
    userList=[]
    for user in query:
            last_login_time = 'min ago'
            #change_user_email(user.username, 'none@noemail')
            if user.last_login is None:
                final_login = "Never"
            else:
                last_login = (datetime.datetime.now() - user.last_login).seconds
                print(last_login)
                last_login = floor(last_login/60)
                if last_login < 1 :
                    last_login = 1
                    last_login_time = ' <  min ago'
                if last_login < 60 and last_login > 1 :

                    last_login_time = ' minutes ago'
                if last_login > 60:
                    last_login = floor(last_login/60)
                    if last_login < 24 :
                        last_login_time = ' hours ago'
                    else:
                        last_login = floor(last_login/24)
                        last_login = ' days ago'
                        if last_login > 7 :
                            last_login = 7
                            last_login_time = ' > days ago'

                final_login = str(last_login) + last_login_time
            userList.append([user.username, user.role_type, final_login])

    return userList

def get_all_logs():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Log)
    logList=[]
    for log in query:
        logList.append(log.user, log.log_message)
    return logList

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
    print(user)
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
        return False
    return True

def change_role_type(username, role_type):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_(username))
    user = query.first()
    if user:
        user.change_role(role_type)

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
        print(self.legal_user)
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
        if user.check_password(password):

            self.legal_user = True
            self.this_user = user

    def get_role(self):
        """
        getter for the user pulled from the database's role
        :return: user's role type
        """
        print("tried getting role")
        print(self.this_user.role_type)
        return self.this_user.role_type

    def update_last_login(self, login_datetime):
        self.this_user.update_last_login(login_datetime)

