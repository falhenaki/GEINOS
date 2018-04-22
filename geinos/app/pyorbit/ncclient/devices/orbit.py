"""
Handler for MDS Orbit device specific information.

Note that for proper import, the classname has to be:

    "<Devicename>DeviceHandler"

...where <Devicename> is something like "Default", "Orbit", etc.

All device-specific handlers derive from the DefaultDeviceHandler, which implements the
generic information needed for interaction with a Netconf server.

"""

import re
from lxml import etree
from .default import DefaultDeviceHandler
from ncclient.operations.third_party.mds.rpc import ExecuteRpc
from ncclient.operations.rpc import RPCError
from ncclient.xml_ import to_ele

class OrbitDeviceHandler(DefaultDeviceHandler):
    """
    MDS handler for device specific information.

    """
    def __init__(self, device_params):
        super(OrbitDeviceHandler, self).__init__(device_params)

    def add_additional_operations(self):
        dict = {}
        dict["rpc"] = ExecuteRpc
        return dict
