from app.core_module import db_connector

def add_list_of_devices(entries):
    for entry in entries:
        #entry.split(",")
        db_connector.add_device(int(entry[0]), int (entry[1]), int (entry[2]))
    return True