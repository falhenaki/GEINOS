from app.core.scep import scep_config
from pyorbit import Device
from app.core.device import device_access
import unittest

"""
These tests require a device to be connected, and assume a host address
of 192.168.1.1, and the user name and password is admin. The scep tests
require a scep server running, and the details must be filled in, such as
OTP, thumbprint, and server address.
"""
host = "192.168.1.1"
username = "admin"
password = "admin"

otp = ""
thumbprint = "thumb"
cert_server = "192.168.1.6/certsrv/mscep/mscep.dll"

class TesttDevice(unittest.TestCase):
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



if __name__ == '__main__':
    unittest.main()