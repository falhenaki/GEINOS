"""
Orbit Python Service Base Class
"""

class Service(object):
    """
    Base class for all Service classes
    """

    def __init__(self, dev):
        self._dev = dev

    def __repr__(self):
        return "Services.%s(%s)" % (
            self.__class__.__name__, self._dev.hostname)

    @property
    def dev(self):
        """
        :returns: the Device object
        """
        return self._dev

    @dev.setter
    def dev(self, value):
        """ read-only property """
        raise RuntimeError("read-only: dev")

    @property
    def rpc(self):
        """
        :returns: Device RPC meta object
        """
        return self._dev.rpc

    @rpc.setter
    def rpc(self, value):
        """ read-only property """
        raise RuntimeError("read-only: rpc")
