from sqlalchemy.orm import sessionmaker
from app.core.device_group.device_group import Device_Group
from app.core.device.device import Device
from app import engine

def get_assignments():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device_Group).filter(Device_Group.template_name != None)
    dgs=[]
    for dg in query:
        dgs.append(dg.as_dict())

    for dg in dgs:
        devices = s.query(Device).filter(Device.device_group == dg['device_group_name'])
        dg['Added'] = 0
        dg['Authorized'] = 0
        dg['Configured'] = 0
        dg['Connected']= 0
        dg['Added'] = devices.count()
        dg['Authorized'] = devices.filter(Device.cert_required == 'FALSE').count() + devices.filter(Device.cert_set == 'TRUE').count()
        dg['Connected'] = devices.filter(Device.IP != '').count()
        dg['Configured'] = devices.filter(Device.date_provisioned != None).filter(Device.config_file != None).count()

    s.close()
    return dgs
