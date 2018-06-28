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
        mn = "Orbit ECR"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)

        username = "ToBeDeleted"
        vend = "Dev2"
        sn = "456"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)

        username = "ToBeDeleted"
        vend = "Dev3"
        sn = "789"
        mn = "Orbit MDS"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)
        sn = "11111"
        mn = "Cisco"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)
        sn = "22222"
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
        group2 = "Test_Group2"
        model ="Orbit ECR"
        attr = "model"
        username = "blank"
        role_type = "Admin"
        remote_addr = "1.1.1.1"
        no_group = "DNE"
        bad_attr = "Fake_attr"
        dev1 = "123"
        dev2 = "456"
        dev3 = "789"
        '''
        Add two different groups. The test will attempt to add the same devices to both groups
        '''
        device_group_connector.add_device_group(group)
        device_group_connector.add_device_group(group2)
        '''
        Add devices to a group. The expected result is the method add_devices_to_group will return true
        '''
        add = device_group_connector.add_devices_to_groups(group, attr, model, username, role_type, remote_addr)
        '''
        Check that the two devices of the same model are associated with the same group name, and the third device
        of a different model is NOT associated with the same group.
        '''
        dev1_is_assigned = s.query(Device_in_Group).filter(Device_in_Group.device_group_name == group,
                                                           Device_in_Group.serial_number == dev1).first()
        dev2_is_assigned = s.query(Device_in_Group).filter(Device_in_Group.device_group_name == group,
                                                           Device_in_Group.serial_number == dev2).first()
        dev3_not_assigned = s.query(Device_in_Group).filter(Device_in_Group.device_group_name == group,
                                                           Device_in_Group.serial_number == dev3).first()
        '''
        Check that 2 of the devices only belong to one group, and device 3 does not belong to any groups
        '''
        dev1_num_groups = s.query(Device_in_Group).filter(Device_in_Group.serial_number == dev1).count()
        dev2_num_groups = s.query(Device_in_Group).filter(Device_in_Group.serial_number == dev2).count()
        dev3_num_groups = s.query(Device_in_Group).filter(Device_in_Group.serial_number == dev3).count()

        self.assertTrue(add, msg="Failed to add devices")
        self.assertIsNotNone(dev1_is_assigned, msg="Device 1 did not get assigned to the group")
        self.assertIsNotNone(dev2_is_assigned, msg="Device 2 did not get assigned to the group")
        self.assertIsNone(dev3_not_assigned, msg="Device 3 was incorrectly assigned to the group")
        self.assertEqual(1,dev1_num_groups, msg="dev1 does not exist in only 1 group")
        self.assertEqual(1,dev2_num_groups, msg="dev2 does not exist in only 1 group")
        self.assertEqual(0, dev3_num_groups, msg="dev3 should not be in any groups")
        with self.assertRaises(Exception):
            device_group_connector.add_devices_to_groups(no_group, attr, model, username, role_type, remote_addr)
        with self.assertRaises(Exception):
            device_group_connector.add_devices_to_groups(group, bad_attr, model, username, role_type, remote_addr)
        with self.assertRaises(Exception):
                device_group_connector.add_devices_to_groups(group2, bad_attr, model, username, role_type, remote_addr)


    def test_remove_group(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        name = "Remove"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        username = "ADV"
        fake_group = "Fake_remove"
        model = "Cisco"
        attr = "model"
        role_type = "Admin"
        device_group_connector.add_device_group(name)
        device_group_connector.add_devices_to_groups(name, attr, model, username, role_type, request_ip)
        remove = device_group_connector.remove_group(name,username,user_role,request_ip)
        is_removed = s.query(Device_Group).filter(Device_Group.device_group_name == name).first()
        devices_removed = s.query(Device_in_Group).filter(Device_in_Group.device_group_name == name).count()
        self.assertTrue(remove, msg="Failed to remove group")
        self.assertIsNone(is_removed, msg="Group was not removed from database")
        self.assertEqual(0,devices_removed,msg="Devices not removed")
        with self.assertRaises(Exception):
            device_group_connector.remove_group(fake_group, username, user_role, request_ip)
        with self.assertRaises(Exception):
            device_group_connector.remove_group(name, username, user_role, request_ip)