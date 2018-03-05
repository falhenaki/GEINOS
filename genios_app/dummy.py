import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
 
engine = create_engine('sqlite:///genios_db.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("admin","password", "email")
session.add(user)
 
user = User("python","python", "email")
session.add(user)
 
user = User("jumpiness","python", 'email')
session.add(user)
 
# commit the record the database
session.commit()
 
session.commit()