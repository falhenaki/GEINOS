from app.core.device.device import Device
from app.core.device import device_connector
from app.core.device_group import device_group_connector
from app.core.device_group.device_group import Device_Group
from app.core.device_group.device_in_group import Device_in_Group
from sqlalchemy.orm import sessionmaker
from app import engine
import unittest





class Test_Device_Group(unittest.TestCase):

    def setUp(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        s.query(Device_Group).delete()
        s.commit()
        s.query(Device_in_Group).delete()
        s.commit()
        s.query(Device).delete()
        s.commit()
        name = "Exists"
        device_group_connector.add_device_group(name)
        username = "Setup"
        vend = "Dev1"
        sn = "123"
        mn = "Orbit"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)

        username = "ToBeDeleted"
        vend = "Dev2"
        sn = "456"
        mn = "Orbit"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)

    def tearDown(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        s.query(Device_Group).delete()
        s.commit()
        s.query(Device).delete()
        s.commit()
        s.query(Device_in_Group).delete()
        s.commit()

    def test_add_group(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        name ="Test"
        add = device_group_connector.add_device_group(name)
        group = s.query(Device_Group).filter(Device_Group.device_group_name == name).first()
        self.assertTrue(add,msg="Failed to create group")
        self.assertIsNotNone(group, "Failed to add group to database")
        with self.assertRaises(Exception):
            device_group_connector.add_device_group(name)
    def test_group_exists(self):
        name = "Exists"
        no_name = "Does_Not_Exist"
        find = device_group_connector.device_group_exists(name)
        dont_find = device_group_connector.device_group_exists(no_name)
        self.assertTrue(find,msg="Cannot find existing group")
        self.assertFalse(dont_find, msg="Found group that does not exist")
    def test_get_all_groups(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        s.query(Device_Group).delete()
        s.commit()
        group0 = "Exists"
        group1 = "Test"
        device_group_connector.add_device_group(group0)
        device_group_connector.add_device_group(group1)
        group_0 = device_group_connector.get_all_device_groups()[0]['device_group_name']
        group_1 = device_group_connector.get_all_device_groups()[1]['device_group_name']
        self.assertEqual(group0 or group1,group_0, msg="First group not found")
        self.assertEqual(group1 or group0,group_1,msg="Group 2 not found")



class Test_Device_Group2(unittest.TestCase):

    def setUp(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        s.query(Device_Group).delete()
        s.commit()
        s.query(Device).delete()
        s.commit()
        s.query(Device_in_Group).delete()
        s.commit()
        name = "Exists"
        device_group_connector.add_device_group(name)
        username = "Setup"
        vend = "Dev1"
        sn = "123"
        mn = "Orbit"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)

        username = "ToBeDeleted"
        vend = "Dev2"
        sn = "456"
        mn = "Orbit"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)

    def tearDown(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        s.query(Device_Group).delete()
        s.commit()
        s.query(Device).delete()
        s.commit()
        s.query(Device_in_Group).delete()
        s.commit()

    def test_add_devices_to_group(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        s.query(Device_Group).delete()
        s.commit()
        group = "Test_Group"
        model ="Orbit"
        attr = "model"
        username = "blank"
        role_type = "Admin"
        remote_addr = "1.1.1.1"
        no_group = "DNE"
        bad_attr = "Fake_attr"
        bad_model = "Fake_model"
        device_group_connector.add_device_group(group)
        add = device_group_connector.add_devices_to_groups(group, attr, model, username, role_type, remote_addr)
        self.assertTrue(add)
        with self.assertRaises(Exception):
            device_group_connector.add_devices_to_groups(no_group, attr, model, username, role_type, remote_addr)
        with self.assertRaises(Exception):
            device_group_connector.add_devices_to_groups(group, bad_attr, model, username, role_type, remote_addr)