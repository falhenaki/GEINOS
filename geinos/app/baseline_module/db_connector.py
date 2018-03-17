from sqlalchemy.orm import sessionmaker, session
from tabledef import *
import json
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

def get_all_users():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User)
    userList=[]
    for user in query:
        userList.append([user.username, user.role_type])
    return userList

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


    ######################################
        #Devices
def add_device(vendor_id, serial_number,model_number, device_status, last_modified, ip ):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = Device(vendor_id, serial_number, model_number, device_status, last_modified, ip)
    s.add(device)
    s.commit()

    return True

def device_listed(vendor_id, serial_number,model_number):
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.vendor_id == vendor_id).filter(Device.serial_number == serial_number).filter( Device.model_number == model_number ).first()
    if device:
        return True
    return False

def remove_device(vendor_id, serial_number,model_number):
    """
    removes specified device from the database
    :param device: vendor_id, serial_number,model_number
    :return:
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    device = s.query(Device).filter(Device.vendor_id == vendor_id).filter(Device.serial_number == serial_number).filter( Device.model_number == model_number ).delete()
    s.commit()
    return True

def get_all_devices():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device)
    deviceList=[]
    for device in query:
        deviceList.append([device])
    return deviceList

