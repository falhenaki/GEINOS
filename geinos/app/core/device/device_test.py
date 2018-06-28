from app.core.scep import scep_config
from app.pyorbit import Device
from app.core.device import device_access,device_connector
from app.core.device.device import Device
from sqlalchemy.orm import sessionmaker
from app import engine
import unittest

"""
These tests require a device to be connected, and assume a host address
of 192.168.1.1, and the user name and password is admin. The scep tests
require a scep server running, and the details must be filled in, such as
OTP, thumbprint, and server address.
"""




class TesttDevice(unittest.TestCase):

    def setUpModule(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        s.query(Device).delete()
        s.commit()
        username = "Setup"
        vend = "Setup"
        sn = "123456"
        mn = "Orbit"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)

        username = "ToBeDeleted"
        vend = "ToBeDeleted"
        sn = "0987"
        mn = "Orbit"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)

    def tearDown(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        s.query(Device).delete()
        s.commit()


    @unittest.skip
    def test_set_private_key(self):
        dev = Device(host="192.168.1.1", username="admin", password="admin")
        x = device_access.generate_private_key(dev, "test")
        self.assertEqual("complete", x)

    @unittest.skip
    def test_set_cert_info(self):
        host = "192.168.1.1"
        username = "admin"
        password = "admin"
        cert_info_cfg = scep_config.format_config_cert_info("test","12345","US","NY","Roch","organization","org_unit")
        x = device_access.set_config(host,username,password,cert_info_cfg)
        print (x)
        self.assertIsNot(x,False)

    @unittest.skip
    def test_set_ca_server(self):
        host = "192.168.1.1"
        username = "admin"
        password = "admin"
        ca_server = scep_config.format_config_ca_server("ca_server_name_test","12345thumbprint")
        x = device_access.set_config(host,username,password,ca_server)
        print (x)
        self.assertIsNot(x,False)
    @unittest.skip
    def test_set_cert_server(self):
        host = "192.168.1.1"
        username = "admin"
        password = "admin"
        cert_server = scep_config.format_config_cert_server("server_name",cert_server,"sha256","3des_cbc")
        x = device_access.set_config(host,username,password,cert_server)
        self.assertIsNot(x, False)


    @unittest.skip
    def test_get_ca_cert(self):
        cert_id = "test_cert_id"
        cert_server_id = "cer_server_id"
        ca_server_id = "ca_server_id"
        dev = Device(host="192.168.1.1", username="admin", password="admin")
        x = device_access.get_ca_certs(dev,cert_id,cert_server_id,ca_server_id)
        self.assertEqual(x,"complete")

    @unittest.skip
    def test_get_client_cert(self):
        challenpassword = "64BFE8E79D7A5406"
        cert_server_id = "cer_server_id"
        ca_server_id = "ca_server_id"
        cert_info_id = "cert_info_id"
        cert_id = "test_cert"
        key_id = "DEVKEY"
        ca_cert_id = "sdgg"
        dev = Device(host="192.168.1.1", username="admin", password="admin")
        x = device_access.get_client_cert(dev,cert_server_id,ca_server_id,cert_id,cert_info_id,ca_cert_id,key_id,challenpassword)
        self.assertEqual(x, "complete")

    def test_add_device(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        s.commit()
        username = "TestName"
        vend = "AutoTest"
        sn = "12345"
        mn = "Orbit"
        location = "Roch"
        user_role = "Admin"
        request_ip = "1.1.2.3"
        add_result = device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)
        device = s.query(Device).filter(Device.serial_number == sn).first()
        '''
        Test device was added
        '''
        self.assertTrue(add_result, msg="Device could not be added")
        '''
        Verify device is in the database
        '''
        self.assertEqual(sn,device.serial_number, msg="Failed to find device in database from add_device")
        with self.assertRaises(Exception):
            device_connector.add_device(vend, sn, mn, location, username, user_role, request_ip)

    def test_update_device(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        sn = "123456"
        mn = "Orbit ECR"
        update = device_connector.update_device(sn,"model_number", mn)
        update_fail = device_connector.update_device(sn, "model_naumber", mn)
        device = s.query(Device).filter(Device.serial_number == sn).first()
        self.assertTrue(update, msg="Failed to update a device")
        self.assertEqual(mn,device.model_number, msg="Update to device cannot be found in database ")
        self.assertFalse(update_fail, msg="Failed to identify attribute does not exist")

    def test_remove_device(self):
        Session = sessionmaker(bind=engine)
        s = Session()
        sn = "0987"
        fake_sn = "0000"
        remove_device = device_connector.remove_device(sn,"","ADMIN","")
        device = s.query(Device).filter(Device.serial_number == sn).first()
        self.assertTrue(remove_device, msg="Device was not removed from databse")
        self.assertIsNone(device, msg="Device still in database after removal")
        with self.assertRaises(Exception):
            device_connector.remove_device(sn, "", "ADMIN", "")
        with self.assertRaises(Exception):
            device_connector.remove_device(sn, "", "ADMIN", "")

if __name__ == '__main__':
    unittest.main()