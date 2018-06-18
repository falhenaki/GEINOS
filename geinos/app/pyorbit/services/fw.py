from urllib import parse
from lxml import etree

# package modules
from .service import Service
from app.pyorbit.exception import *

"""
Firmware Service
"""

class Firmware(Service):
    """
    Overview of Firmware Service.

    * :meth:`get_versions`: Get firmware versions on device.
    * :meth:`load`: load firmware in inactive image.
    * :meth:`status`: Get firmware upgrade status.
    * :meth:`cancel`: Cancel firmware upgrade.

    """

    def get_versions(self):
        """
        Get firmware versions on the device.

        :returns:
            versions

        :raises: GetError: When operation fails.

        """

        filter =  """/system/firmware/versions"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    def load(self, **kwargs):
        """
        Loads firmware in the inactive image.

        :param str url:
          Specify the full pathname of the firmware file. The value can be a
          local file path, an FTP location, or a Hypertext Transfer Protocol (HTTP).

          For example::
            fw.load(url="sftp://<host>/tmp/mcr-bkrc-6.7.8.mpk", username="test", password="test")

        :returns:
            True

        :raises: FwLoadError: When firmware load fails.
        """

        url = None
        if 'url' in kwargs:
            url = kwargs['url']

        username = None
        if 'username' in kwargs:
            username = kwargs['username']

        password = None
        if 'password' in kwargs:
            password = kwargs['password']

        if url is None:
            raise ArgError("firmware file url not specified")

        urlsplit = parse.urlsplit(url)

        if urlsplit.scheme == 'sftp':
            if username is None or password is None:
                raise ArgError("username/password not specified for sftp server")

            rpc = """
                <reprogram-inactive-image xmlns="com:gemds:mds-system">
                    <filename>{}</filename>
                    <manual-file-server>
                        <sftp>
                            <address>{}</address>
                            <username>{}</username>
                            <password>{}</password>
                        </sftp>
                    </manual-file-server>
                </reprogram-inactive-image>
            """.format (urlsplit.path, urlsplit.netloc, username, password)
        else:
            raise ArgError("only sftp file transfer supported")

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise FwLoadError(rsp=err.xml)
            else:
                raise

        return True

    def status(self, **kwargs):
        """
        Get firmware upgrade status.

        :returns:
            Status as dict.

        :raises: FwLoadError: When firmware load fails.

        """

        filter = """/system/firmware/reprogram-status"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    def cancel(self, **kwargs):
        """
        Cancel firmware upgrade.

        :returns:
            Status in requested format.

        :raises: FwLoadCancelError: When firmware load fails.

        """

        rpc = """
            <cancel-reprogram-inactive-image xmlns="com:gemds:mds-system"/>
        """

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise FwError(rsp=err.xml)
            else:
                raise

        return True

    def __init__(self, dev, **kwargs):
        """
        .. code-block:: python

           with Firmware(dev) as fw:
               fw.load(url="/tmp/mcr-bkrc-6.5.7.mpk")
               status = fw.status()
        """
        Service.__init__(self, dev=dev)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
