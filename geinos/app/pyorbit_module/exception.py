from ncclient.operations.rpc import RPCError

class RpcError(Exception):

    """
    Parent class for all pyorbit Exceptions
    """

    def __init__(self, cmd=None, rsp=None, errs=None, dev=None,
                 timeout=None):
        """
          :cmd: is the rpc command
          :rsp: is the rpc response (after <rpc-reply>)
          :errs: is a list of dictionaries of extracted <rpc-error> elements.
          :dev: is the device rpc was executed on
          :timeout: is the timeout value of the device
        """
        self.cmd = cmd
        self.rsp = rsp
        self.dev = dev
        self.timeout = timeout
        self.rpc_error = None
        self.xml = rsp
        pass

    def __repr__(self):
        """
          pprints the response XML attribute
        """
        if self.rpc_error is not None:
            return "{}(severity: {}, bad_element: {}, message: {})"\
                .format(self.__class__.__name__, self.rpc_error['severity'],
                        self.rpc_error['bad_element'], self.message)
        else:
            return self.__class__.__name__

    __str__ = __repr__

class GetError(RpcError):

    """
    Generated in response to a Get operation.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)

    def __repr__(self):
        return "{}(edit_path: {}, bad_element: {}, message: {})"\
            .format(self.__class__.__name__, self.rpc_error['edit_path'],
                    self.rpc_error['bad_element'], self.message)

    __str__ = __repr__

class CommitError(RpcError):

    """
    Generated in response to a commit-check or a commit action.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)

    def __repr__(self):
        return "{}(edit_path: {}, bad_element: {}, message: {})"\
            .format(self.__class__.__name__, self.rpc_error['edit_path'],
                    self.rpc_error['bad_element'], self.message)

    __str__ = __repr__


class ConfigLoadError(RpcError):

    """
    Generated in response to a failure when loading a configuration.
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd, rsp, errs)

    def __repr__(self):
        return "{}(severity: {}, bad_element: {}, message: {})"\
            .format(self.__class__.__name__, self.rpc_error['severity'],
                    self.rpc_error['bad_element'], self.message)

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


class PermissionError(RpcError):

    """
    Generated in response to invoking an RPC for which the
    auth user does not have user-class permissions.

    PermissionError.message gives you the specific RPC that cause
    the exceptions
    """

    def __init__(self, rsp, cmd=None, errs=None):
        RpcError.__init__(self, cmd=cmd, rsp=rsp, errs=errs)
        self.message = rsp.findtext('.//bad-element')


class RpcTimeoutError(RpcError):

    """
    Generated in response to a RPC execution timeout.
    """

    def __init__(self, dev, cmd, timeout):
        RpcError.__init__(self, dev=dev, cmd=cmd, timeout=timeout)

    def __repr__(self):
        return "{}(host: {}, cmd: {}, timeout: {})"\
            .format(self.__class__.__name__, self.dev.hostname,
                    self.cmd, self.timeout)

    __str__ = __repr__

# Connection exceptions

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
