from sqlalchemy.orm import sessionmaker
from app.core.device_group.device_group import Device_Group
from app import engine

def get_assignments():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_Group).filter(Device_Group.template_name is not None)
    dgs=[]
    for dg in query:
        dgs.append(dg.as_dict())
    return dgs