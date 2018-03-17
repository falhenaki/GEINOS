from flask import session
from genios_app import db_connector
from datetime import datetime

def add_device(vendor_id, serial_number, model_number, ip):
    """
    adds device with a given vendorid, serial number, model number, ip

    """
    if db_connector.device_listed(vendor_id, serial_number, model_number):
        db_connector.add_device(vendor_id, serial_number, model_number, "UNAUTHORIZED", datetime.now(), ip)
        return True
    return False

def device_listed(vendor_id, serial_number, model_number):
    return db_connector.device_listed(vendor_id, serial_number,model_number)

def remove_device(vendor_id, serial_number,model_number):
    return db_connector.remove_device(vendor_id, serial_number,model_number)

def get_all_devices():
    return db_connector.get_all_devices()