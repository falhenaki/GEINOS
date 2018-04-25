from app.core import device

def add_list_of_devices(entries):
    for entry in entries:
        device.device_connector.add_device(int(entry[0]), int (entry[1]), int (entry[2]))
    return True