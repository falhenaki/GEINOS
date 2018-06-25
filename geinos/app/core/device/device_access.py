from app.pyorbit import Device, ConnectError
from app.pyorbit.services import Config, Status, PKI
from app.core.scep import scep_config, scep_connector
import time

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


def generate_private_key(dev):
    try:
        dev.open()
        with PKI(dev) as pki:
            rsp = pki.get_priv_keys()
            print(rsp)
            # Generate private key
            print("GENERATING PRIVATE KEY...")
            # pki.cancel_priv_key_gen()
            pki.gen_priv_key(key_id="DEVKEY", key_size="2048")
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
        return


def get_ca_certs(dev, server_name, ca_name, cert_name):
    try:
        dev.open()
        with PKI(dev) as pki:
            rsp = pki.get_ca_certs()
            print(rsp)
            print("IMPORT CA CERTS...")
            pki.import_ca_cert_scep(cert_id= cert_name, cert_server_id=server_name, ca_server_id=ca_name)
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
        return


def get_client_cert(dev,server_name, ca_name, cert_name, cert_info):
    try:

        dev.open()
        with PKI(dev) as pki:
            rsp = pki.get_client_certs()
            print(rsp)
            print("IMPORT CLIENT CERTS...")
            pki.import_client_cert_scep(cert_id= cert_name, cert_server_id=server_name, ca_server_id=ca_name,
                                        cert_info_id=cert_info, cacert_id=ca_name, key_id="DEVKEY",
                                        otp="4B7AC2AFC101104F06C88A174C88CD52")
            done = False
            while not done:
                status = pki.get_client_cert_import_status()
                print(status)
                state = status['data']['pki']['client-certs']['import-status']['state']
                if state in ['inactive', 'complete', 'cancelled', 'failed']:
                    done = True
                else:
                    time.sleep(5)
            rsp = pki.get_client_certs()
            print(rsp)
    except ConnectError as err:
        print("Cannot connect to device: {0}".format(err))
        return


def set_scep(host, user, passwd, serial, server_name,ca_name, cert_name):
    dev = Device(host=host, username=user, password=passwd)
    scep_info = scep_connector.get_scep()
    scep_thumb = "12345"
    """server_name, cert_server, digest, encrypt"""
    cert_server = scep_config.format_config_cert_server(server_name, scep_info.server, scep_info.digestalgo, scep_info.encryptalgo)
    """ca_name,thumbprint"""
    ca_server = scep_config.format_config_ca_server(ca_name,scep_thumb)
    cert_info = scep_config.format_config_cert_info(cert_name, serial)
    set_config(host, user, passwd, cert_server)
    set_config(host, user, passwd, ca_server)
    set_config(host, user, passwd, cert_info)
    generate_private_key(dev)
    get_ca_certs(dev, server_name, ca_name, cert_name)
    get_client_cert(dev, server_name, ca_name, cert_name, cert_info)
