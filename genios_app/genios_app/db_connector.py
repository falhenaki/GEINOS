from sqlalchemy.orm import sessionmaker, session
from tabledef import *

def add_user(username, password, email):
    """
    adds user to the database
    :param username: username to add
    :param password: password to attach to username
    :param email: user email
    :return:
    """
    user = User(username, password, email)
    session.add(user)
    session.commit()

def remove_user(username):
    """
    removes specified user from the database
    :param username: user to remove
    :return:
    """
    User.query.filter_by(username=username).delete()

def modify_user_role(username, new_role):
    return True

def get_user_role(username):
    """
    gets the user's current role
    :param username: user to check
    :return: user's current role
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_(username))
    user = query.first()
    return user.role_type

def check_username_availability(username):
    """
    checks to see if username is taken returns true if username is free false if it is taken
    :param username: username to check
    :return: true if username is free false if it is taken
    """
    query = s.query(User).filter(User.username.in_(username))
    user = query.first()
    if user:
        return False
    return True

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
        print("ran islegal")
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
