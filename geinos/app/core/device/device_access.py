import sys, os, warnings
from app.pyorbit import Device, ConnectError
from app.pyorbit.services import Config, Status

config="""
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

ntp_template="""
<config>
    <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
        <ntp>
            <use-ntp>true</use-ntp>
            <ntp-server>
                <address>{{ ntp_server }}</address>
            </ntp-server>
        </ntp>
    </system>
</config>
"""

def set_config_with_template(host, user, passwd):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Config(dev) as cm:
            rsp = cm.load(template=ntp_template, template_vars={'ntp_server':'1.1.1.1'})
            print(rsp)
            rsp = cm.validate()
            print(rsp)
            rsp = cm.commit()
            print(rsp)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

def get_uptime(host, user, passwd):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Status(dev) as st:
            uptime="""/system/uptime/seconds"""

            # JSON
            out = st.get(filter=('xpath',uptime),format='json')
            print(out)

            # ODICT
            #out = st.get(filter=('xpath',uptime),format='odict')
            #print(out)

            # XML
            #out = st.get(filter=('xpath',uptime))
            #print(out)

    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

def set_config(host, user, passwd, t_conf):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Config(dev) as cm:
            rsp = cm.load(content=t_conf)
            print(rsp)
            rsp = cm.validate()
            print(rsp)
            rsp = cm.commit()
            print(rsp)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

def get_config(host, user, passwd):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Config(dev) as cm:
            out = cm.get(format='json')
            print(out)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return
