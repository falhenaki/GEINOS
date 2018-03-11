from sqlalchemy.orm import sessionmaker, session
from tabledef import *

def check_user():
    return True

def add_user(username, password, email):
    user = User(username, password, email)
    session.add(user)
    session.commit()

def remove_user():
    return True

def modify_user_role():
    return True

def get_user_role():
    return True

class DB_User_Connection():
    def __init__(self):
        return True
        Session = sessionmaker(bind=engine)
        self.s = Session()


    def legal_user(self, username, password):
        query = s.query(User).filter(User.username.in_(username))
        user = query.first()
        if user.check_password(password):
            self.this_user = user
            return True
        else:
            return False

    def get_role(self):
        ###TODO grab user role from database and return it here
        return True
