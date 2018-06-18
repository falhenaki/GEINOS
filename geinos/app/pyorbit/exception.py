import json
import xmltodict
import xml.etree.ElementTree as ET
from ncclient.operations.rpc import RPCError

# Device RPC exceptions

class RpcError(Exception):

    """
    Parent class for all RPC exceptions
    """

    def __init__(self, cmd=None, rsp=None, dev=None):
        """
          :cmd: is the rpc command
          :rsp: is the rpc response (after <rpc-reply>)
          :dev: is the device rpc was executed on
        """
        self.cmd = cmd
        self.rsp = rsp
        self.dev = dev
        self.rsp_json = json.dumps(xmltodict.parse(ET.tostring(rsp)))

    def __repr__(self):
        """
          pprints the RPC error response
        """
        if self.rsp_json is not None:
            return self.rsp_json
        else:
            return self.__class__.__name__

    __str__ = __repr__

class LockError(RpcError):

    """
    Generated in response to attempting to take an exclusive
    lock on the configuration database.
    """

    def __init__(self, rsp):
        RpcError.__init__(self, rsp=rsp)


class UnlockError(RpcError):

    """
    Generated in response to attempting to unlock the
    configuration database.
    """

    def __init__(self, rsp):
        RpcError.__init__(self, rsp=rsp)


class ConfigLoadError(RpcError):

    """
    Generated in response to a failure when loading a configuration.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)

class ConfigRollbackError(RpcError):

    """
    Generated in response to a failure when rollback configuration.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)


class ValidateError(RpcError):

    """
    Generated in response to a validate action.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)


class CommitError(RpcError):

    """
    Generated in response to a commit-check or a commit action.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)


class GetError(RpcError):

    """
    Generated in response to a Get operation.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)


class FwError(RpcError):

    """
    Generated in response to a Firmware operations.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)

class PkiError(RpcError):

    """
    Generated in response to a PKI operations.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)

# Device connection exceptions

class ConnectError(Exception):

    """
    Parent class for all connection related exceptions
    """

    def __init__(self, dev, msg=None):
        self.dev = dev
        self._orig = msg

    @property
    def user(self):
        """ login user-name """
        return self.dev.user

    @property
    def host(self):
        """ login host name/ipaddr """
        return self.dev.hostname

    @property
    def port(self):
        """ login SSH port """
        return self.dev._port

    @property
    def msg(self):
        """ login SSH port """
        return self._orig

    def __repr__(self):
        if self._orig:
            return "{}(host: {}, msg: {})".format(self.__class__.__name__,
                                                     self.dev.hostname,
                                                     self._orig)
        else:
            return "{}({})".format(self.__class__.__name__,
                                     self.dev.hostname)

    __str__ = __repr__


class ConnectAuthError(ConnectError):

    """
    Generated if the user-name, password is invalid
    """
    pass


class ConnectTimeoutError(ConnectError):

    """
    Generated if the NETCONF session fails to connect, could
    be due to the fact the device is not ip reachable; bad
    ipaddr or just due to routing
    """
    pass


class ConnectUnknownHostError(ConnectError):

    """
    Generated if the specific hostname does not DNS resolve
    """
    pass


class ConnectRefusedError(ConnectError):

    """
    Generated if the specified host denies the NETCONF; could
    be that the services is not enabled, or the host has
    too many connections already.
    """
    pass

class ConnectionClosedError(ConnectError):

    """
    Generated if connection unexpectedly closed
    """

    def __init__(self, dev):
        ConnectError.__init__(self, dev=dev)
        dev.connected = False

# Misc exception
class ArgError(Exception):

    """
    Generated if the specified arguments are invalid.
    """
    pass
