from app.pyorbit import Device
from app.pyorbit.services import Config

t_config="""
<config>
    <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
        <ntp>
            <use-ntp>true</use-ntp>
            <ntp-server>
                <address>1.1.1.1</address>
            </ntp-server>
        </ntp>
    </system>
</config>
"""

def get_config(hst,usr,passw):
    dev = Device(host=hst,username=usr,password=passw)
    print("00000000000000000000000000000000000000000000000")
    dev.open()
    print("111111111111111111111111111111111111111111111111111111")
    with Config(dev) as cm:
        out = cm.get(format='json')
        return out

def set_config(hst,usr,passw,conf):
    dev = Device(host=hst,username=usr,password=passw)
    print("00000000000000000000000000000000000000000000000")
    dev.open()
    print("111111111111111111111111111111111111111111111111111111")
    with Config(dev) as cm:
        rsp = cm.load(content=conf)
        print(rsp)
        rsp = cm.validate()
        print(rsp)
        rsp = cm.commit()
        print(rsp)
