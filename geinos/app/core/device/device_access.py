from app.pyorbit import Device, ConnectError
from app.pyorbit.services import Config, Status

def get_uptime(host, user, passwd):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Status(dev) as st:
            uptime="""/system/uptime/seconds"""

            # JSON
            out = st.get(filter=('xpath',uptime),format='json')

    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

def set_config(host, user, passwd, t_conf):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Config(dev) as cm:
            rsp = cm.load(content=t_conf)
            rsp = cm.validate()
            rsp = cm.commit()
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

def get_config(host, user, passwd):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Config(dev) as cm:
            out = cm.get(format='json')
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return
