from pyorbit import Device, ConnectError
from pyorbit.services import Config, Status, PKI
from app.core.scep import scep_config, scep_connector,scep_server
import time
import json

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
            print(t_conf)
            rsp = cm.load(content=t_conf)
            rsp = cm.validate()
            print (rsp)
            rsp = cm.commit()
            print(rsp)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return False
    return True

def get_config(host, user, passwd):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Config(dev) as cm:
            out = cm.get(format='json')
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

def get_interface_address(host="192.168.1.1", username="admin", password="admin", ifname="LO1"):
    try:
        dev = Device(host="192.168.1.1", username="admin", password="admin")
        dev.open()
        with Status(dev) as st:
            ipv4 = """/interfaces-state/interface[name='{}']/ipv4/address""".format(ifname)
            # JSON
            out = st.get(filter=('xpath', ipv4), format='json')
            dt = json.loads(out)
            #print(out)
            ifip = dt['data']['interfaces-state']['interface']['ipv4']['address']['ip']
            return
    except:
        print("COULD NOT GET IF ADDRESS")

def generate_private_key(dev, key_name):
    try:
        dev.open()
        state = "Failed to open connection to device"
        with PKI(dev) as pki:
            rsp = pki.get_priv_keys()
            print(rsp)
            # Generate private key
            print("GENERATING PRIVATE KEY...")
            # pki.cancel_priv_key_gen()
            pki.gen_priv_key(key_id=key_name, key_size="2048")
            done = False
            while not done:
                status = pki.get_priv_key_gen_status()
                print(status)
                state = status['data']['pki']['private-keys']['generate-status']['state']
                if state in ['inactive', 'complete', 'cancelled', 'failed']:
                    done = True
                else:
                    time.sleep(5)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return False
    return state


def get_ca_certs(dev,cert_id,cert_server_id, ca_server_id):
    try:
        state = "failed to connect"
        dev.open()
        with PKI(dev) as pki:
            rsp = pki.get_ca_certs()
            pki.import_ca_cert_scep(cert_id= cert_id, cert_server_id=cert_server_id, ca_server_id=ca_server_id)
            done = False
            while not done:
                status = pki.get_ca_cert_import_status()
                print(status)
                state = status['data']['pki']['ca-certs']['import-status']['state']
                if state in ['inactive', 'complete', 'cancelled', 'failed']:
                    done = True
                else:
                    time.sleep(5)
            rsp = pki.get_ca_certs()
            print(rsp)
    except ConnectError as err:
        print("Cannot connect to device: {0}".format(err))
        return False
    return state


def get_client_cert(dev, cert_server_id, ca_server_id, cert_id, cert_info_id, ca_cert_id, key_id, otp):
    try:
        state = "failed to connect"
        dev.open()
        with PKI(dev) as pki:
            rsp = pki.get_client_certs()
            print(rsp)
            pki.import_client_cert_scep(cert_id= cert_id, cert_server_id=cert_server_id, ca_server_id=ca_server_id,
                                        cert_info_id=cert_info_id, cacert_id=ca_cert_id, key_id=key_id,
                                        otp=otp)
            done = False
            while not done:
                status = pki.get_client_cert_import_status()
                state = status['data']['pki']['client-certs']['import-status']['state']
                if state in ['inactive', 'complete', 'cancelled', 'failed']:
                    done = True
                else:
                    time.sleep(5)
            rsp = pki.get_client_certs()
    except ConnectError as err:
        print("Cannot connect to device: {0}".format(err))
        return False
    return state


def set_scep(host, user, passwd, serial):
    otp = scep_server.get_otp()
    if "Error" in otp:
        return otp
    dev = Device(host=host, username=user, password=passwd)
    scep_info = scep_connector.get_scep()
    if scep_info is None:
        return "Error: SCEP information not in database"
    scep_thumb = scep_info.thumbprint
    cert_server = scep_config.format_config_cert_server(scep_info.cert_server_id, scep_info.server,
                                                        scep_info.digestalgo, scep_info.encryptalgo)
    ca_server = scep_config.format_config_ca_server(scep_info.ca_server_id,scep_thumb)
    cert_info = scep_config.format_config_cert_info(scep_info.cert_info_id, serial,scep_info.country,scep_info.state,
                                                    scep_info.locale,scep_info.organization,scep_info.org_unit)
    cert_config = set_config(host, user, passwd, cert_server)
    ca_config = set_config(host, user, passwd, ca_server)
    cert_info_config = set_config(host, user, passwd, cert_info)
    if cert_config is False:
        return "Error: Failed to config Certificate server information"
    if ca_config is False:
        return "Error: Failed to config CA server information"
    if cert_info_config is False:
        return "Error: Failed to config Certificate Information"
    pk = generate_private_key(dev,scep_info.key_id)
    if pk is False:
        return "Error: Failed to generate private key"
    if pk is not "complete":
        return "Error: Device returned the following status of the private key" + pk
    ca_cert = get_ca_certs(dev, scep_info.ca_cert_id, scep_info.cert_server_id, scep_info.ca_server_id)
    if ca_cert is False:
        return "Error: Failed to get CA Cert"
    if ca_cert is not "complete":
        return "Error: Device returned the following when attempt to get a CA Cert:" + ca_cert
    client_cert = get_client_cert(dev, scep_info.cert_server_id, scep_info.ca_server_id, scep_info.client_cert_id,
                    scep_info.cert_info_id,scep_info.ca_cert_id,scep_info.key_id,otp)
    if client_cert is False:
        return "Error: Failed to get Client Cert"
    if client_cert is not "complete":
        return "Error: Device returned the following when attempt to get a Client Cert:" + client_cert
