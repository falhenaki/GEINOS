from pyorbit import Device, ConnectError
from pyorbit.services import Config, Status, PKI
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


def set_config(host, user, passwd, t_conf,device=None):
    try:
        if device is None:
            dev = Device(host=host,username=user,password=passwd)
            dev.open()
        else:
            dev = device
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
    finally:
        dev.close()

def get_interface_address(host="192.168.1.1", username="admin", password="admin", ifname="Bridge"):
    try:
        dev = Device(host=host, username="admin", password="admin")
        dev.open()
        with Status(dev) as st:
            ipv4 = """/interfaces-state/interface[name='{}']/ipv4/address""".format(ifname)
            # JSON
            out = st.get(filter=('xpath', ipv4), format='json')
            dt = json.loads(out)
            ifip = dt['data']['interfaces-state']['interface']['ipv4']['address']['ip']
            return ifip
    except Exception as ex:
        print("COULD NOT GET IF ADDRESS: " + str(ex))
    finally:
        dev.close()

def generate_private_key(dev, key_name):
    try:
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
    except Exception as ex:
        print("Exception in Generatre Private Key: " + str(ex))

    return state


def get_ca_certs(dev,cert_id,cert_server_id, ca_server_id):
    try:
        state = "failed to connect"
        with PKI(dev) as pki:
            rsp = pki.get_ca_certs()
            pki.import_ca_cert_scep(cert_id= cert_id, cert_server_id=cert_server_id, ca_server_id=ca_server_id)
            done = False
            while not done:
                print("get_ca_cert \n")
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
        with PKI(dev) as pki:
            rsp = pki.get_client_certs()
            print(rsp)
            pki.import_client_cert_scep(cert_id= cert_id, cert_server_id=cert_server_id, ca_server_id=ca_server_id,
                                        cert_info_id=cert_info_id, cacert_id=ca_cert_id, key_id=key_id,
                                        otp=otp)
            done = False
            while not done:
                print("Get Client cert \n")
                print("OTP:" + otp)
                status = pki.get_client_cert_import_status()
                state = status['data']['pki']['client-certs']['import-status']['state']
                print(state)
                if state in ['inactive', 'complete', 'cancelled', 'failure']:
                    done = True
                else:
                    time.sleep(5)
            rsp = pki.get_client_certs()
    except ConnectError as err:
        print("Cannot connect to device: {0}".format(err))
        return False
    return state


