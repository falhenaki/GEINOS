import os
import six
import types
import platform
import warnings

import socket
import datetime
import time
import sys
import json
import re

from lxml import etree
from ncclient import manager as netconf_ssh
import ncclient.transport.errors as NcErrors
from ncclient.transport.session import SessionListener
import ncclient.operations.errors as NcOpErrors
from ncclient.operations import RPCError
import paramiko

# local packages
from . import exception as OrbitErrors

class DeviceSessionListener(SessionListener):

    """
    Listens to Session class of Netconf Transport
    and detects errors in the transport.
    """
    def __init__(self, device):
        self._device = device

    def callback(self, root, raw):
        """Required by implementation but not used here."""
        pass

    def errback(self, ex):
        """Called when an error occurs.
        Set the device's connected status to False.
        :type ex: :exc:`Exception`
        """
        self._device.connected(False)


class Device(object):

    """
    Orbit Device class.
    """

    def __init__(self, *vargs, **kvargs):
        """
        Device object constructor.

        :param str vargs[0]: host-name or ipaddress.  This is an
                             alternative for **host**

        :param str host:
            **REQUIRED** host-name or ipaddress of target device

        :param str user:
            *OPTIONAL* login user-name, uses $USER if not provided

        :param str passwd:
            *OPTIONAL* if not provided, assumed ssh-keys are enforced

        :param int port:
            *OPTIONAL* NETCONF port (defaults to 830)

        :param str ssh_private_key_file:
            *OPTIONAL* The path to the SSH private key file.
            This can be used if you need to provide a private key rather than
            loading the key into the ssh-key-ring/environment.  if your
            ssh-key requires a password, then you must provide it via
            **passwd**

        :param str ssh_config:
            *OPTIONAL* The path to the SSH configuration file.
            This can be used to load SSH information from a configuration file.
            By default ~/.ssh/config is queried.

        """

        hostname = vargs[0] if len(vargs) else kvargs.get('host')
        if hostname is None:
            raise ValueError("You must provide the 'host' value")
        self._hostname = hostname

        self._port = kvargs.get('port', 830)

        self._auth_user = kvargs.get('username') or os.getenv('USER')
        self._auth_password = kvargs.get('password') or kvargs.get('admin')

        # initialize instance variables
        self._conn = None
        self._connected = False

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        if value in [True, False]:
            self._connected = value

    @property
    def hostname(self):
        """
        :returns: the host-name of the Orbit device.
        """
        return self._hostname

    def open(self, *vargs, **kvargs):
        """
        Opens a connection to the device using existing login/auth
        information.

        :returns Device: Device instance (*self*).

        :raises ConnectAuthError:
            When provided authentication credentials fail to login

        :raises ConnectRefusedError:
            When the device does not have NETCONF enabled

        :raises ConnectTimeoutError:
            When the the :meth:`Device.timeout` value is exceeded
            during the attempt to connect to the remote device

        :raises ConnectError:
            When an error, other than the above, occurs.  The
            originating ``Exception`` is assigned as ``err._orig``
            and re-raised to the caller.
        """

        try:
            ts_start = datetime.datetime.now()

            # we want to enable the ssh-agent if-and-only-if we are
            # not given a password or an ssh key file.
            # in this condition it means we want to query the agent
            # for available ssh keys

            allow_agent = bool((self._auth_password is None) and
                               (self._ssh_private_key_file is None))

            self._conn = netconf_ssh.connect(
                host=self._hostname,
                port=self._port,
                username=self._auth_user,
                password=self._auth_password,
                hostkey_verify=False,
                allow_agent=False,
                look_for_keys=False,
                device_params={'name': 'orbit', 'local': False})

            self._conn._session.add_listener(DeviceSessionListener(self))
        except NcErrors.AuthenticationError as err:
            # bad authentication credentials
            raise OrbitErrors.ConnectAuthError(self)

        except NcErrors.SSHError as err:
            # this is a bit of a hack for now, since we want to
            # know if the connection was refused or we simply could
            # not open a connection due to reachability.  so using
            # a timestamp to differentiate the two conditions for now
            # if the diff is < 3 sec, then assume the host is
            # reachable, but NETCONF connection is refushed.

            ts_err = datetime.datetime.now()
            diff_ts = ts_err - ts_start
            if diff_ts.seconds < 3:
                raise OrbitErrors.ConnectRefusedError(self)

            # at this point, we assume that the connection
            # has timeed out due to ip-reachability issues

            if str(err).find('not open') > 0:
                raise OrbitErrors.ConnectTimeoutError(self)
            else:
                # otherwise raise a generic connection
                # error for now.  tag the new exception
                # with the original for debug
                cnx = OrbitErrors.ConnectError(self)
                cnx._orig = err
                raise cnx

        except socket.gaierror:
            # invalid DNS name, so unreachable
            raise OrbitErrors.ConnectUnknownHostError(self)

        except Exception as err:
            # anything else, we will re-raise as a
            # generic ConnectError
            cnx_err = OrbitErrors.ConnectError(self)
            cnx_err._orig = err
            raise cnx_err

        self._connected = True

        return self

    def close(self):
        """
        Closes the connection to the device only if connected.
        """
        if self._connected is True:
            self._conn.close_session()
            self._connected = False

    def __repr__(self):
        return "Device(%s)" % self.hostname

    # -----------------------------------------------------------------------
    # Context Manager
    # -----------------------------------------------------------------------

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
