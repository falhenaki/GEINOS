import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('mysql+mysqlconnector://admin:password@bitforcedev.se.rit.edu/se_project', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin", "password", datetime.datetime.now(), 'ADMIN')
session.add(user)

user = User("python", "python", datetime.datetime.now(), 'OPERATOR')
session.add(user)

user = User("jumpiness", "python", datetime.datetime.now(), 'OPERATOR')
session.add(user)

# commit the record the database
session.commit()

session.commit()