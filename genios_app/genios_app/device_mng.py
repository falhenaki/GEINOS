from flask import session
from genios_app import db_connector
from datetime import datetime
import socket
def add_device(vendor_id, serial_number, model_number, ip):
    """
    adds device with a given vendorid, serial number, model number, ip

    """
    #if the ip is not a valid ip, return false
    if  not is_valid_ipv4_address(ip) and not is_valid_ipv6_address(ip):
        return False
        # if the device isn't listed already, add it
    if not db_connector.device_listed(vendor_id, serial_number, model_number):
        db_connector.add_device(vendor_id, serial_number, model_number, "UNAUTHORIZED", datetime.now(), ip)
        return True

    return False

def device_listed(vendor_id, serial_number, model_number):
    return db_connector.device_listed(vendor_id, serial_number,model_number)

def remove_device(vendor_id, serial_number,model_number):
    return db_connector.remove_device(vendor_id, serial_number,model_number)

def get_all_devices():
    return db_connector.get_all_devices()



#helper methods
#this methods checks if given address is a valid ipv4
def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True
#this methods checks if given address is a valid ipv6
def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True