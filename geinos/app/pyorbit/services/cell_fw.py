from urllib import parse
from lxml import etree

# package modules
from .service import Service
from app.pyorbit.exception import *

"""
Cellular Modem Firmware Service
"""

class CellFirmware(Service):
    """
    Overview of Cellular Modem Firmware Service.

    * :meth:`get_versions`: Get firmware versions on the modem.
    * :meth:`load`: load and activate firmware on the modem.
    * :meth:`status`: Get firmware load status.
    * :meth:`cancel`: Cancel firmware image load.
    * :meth:`delete`: Delete firmware image on the modem.
    * :meth:`restart`: Restart modem to specified firmware image.

    """

    def get_versions(self, **kwargs):
        """
        Get firmware versions on the modem.

        :returns:
            dict with requested info.

        :raises: GetError: When operation fails.

        """

        ifname = None
        if 'ifname' in kwargs:
            ifname = kwargs['ifname']
        else:
            raise ArgError('ifname not specified')

        filter =  """/interfaces-state/interface[name='{}']/firmware/versions""".format(ifname)

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
        Loads and activates firmware on the cellular modem.

        :param str url:
          Specify the full pathname of the firmware file. The value can be a
          local file path, an FTP location, or a Hypertext Transfer Protocol (HTTP).

          For example::
            fw.load(ifname='Cell', url="sftp://<host>/tmp/cell-4Gy-verizon-1.0.0.mpk", username="test", password="test")

        :returns:
            True on success

        :raises: FwError: When operation fails.
        """

        ifname = None
        if 'ifname' in kwargs:
            ifname = kwargs['ifname']
        else:
            raise ArgError('ifname not specified')

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
                <reprogram xmlns="com:gemds:mds-if-cell">
                    <interface>{}</interface>
                    <filename>{}</filename>
                    <manual-file-server>
                        <sftp>
                            <address>{}</address>
                            <username>{}</username>
                            <password>{}</password>
                        </sftp>
                    </manual-file-server>
                </reprogram>
            """.format (ifname, urlsplit.path, urlsplit.netloc, username, password)
        else:
            raise ArgError("only sftp file transfer supported")

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise FwError(rsp=err.xml)
            else:
                raise
        return True

    def status(self, **kwargs):
        """"
        Get firmware load status.

        :returns:
            dict with requested info.

        :raises: GetError: When operation fails.

        """

        ifname = None
        if 'ifname' in kwargs:
            ifname = kwargs['ifname']
        else:
            raise ArgError('ifname not specified')

        filter =  """/interfaces-state/interface[name='{}']/firmware/reprogram-status""".format(ifname)

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
        Cancel firmware load.

        :returns:
            True on success

        :raises: FwError: When operation fails.

        """

        ifname = None
        if 'ifname' in kwargs:
            ifname = kwargs['ifname']
        else:
            raise ArgError('ifname not specified')

        rpc = """
           <cancel-reprogram xmlns="com:gemds:mds-if-cell">
               <interface>{}</interface>
           </cancel-reprogram>
        """.format(ifname)

        try:
           self.dev._conn.rpc(rpc)
        except Exception as err:
           if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
               raise FwError(rsp=err.xml)
           else:
               raise

        return True

    def delete(self, **kwargs):
        """
        Delete firmware image from the modem.

        :returns:
            True on success

        :raises: FwError: When operation fails.

        """

        ifname = None
        if 'ifname' in kwargs:
            ifname = kwargs['ifname']
        else:
            raise ArgError('ifname not specified')

        id = None
        if 'id' in kwargs:
            id = kwargs['id']
        else:
            raise ArgError('image id not specified')

        rpc = """
           <delete-image xmlns="com:gemds:mds-if-cell">
               <interface>{}</interface>
               <id>{}</id>
           </delete-image>
        """.format(ifname, id)

        try:
           self.dev._conn.rpc(rpc)
        except Exception as err:
           if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
               raise FwError(rsp=err.xml)
           else:
               raise

        return True

    def restart(self, **kwargs):
        """
        Restart modem to specified firmware image.

        :returns:
            True on succes

        :raises: FwError: When operation fails.

        """

        ifname = None
        if 'ifname' in kwargs:
            ifname = kwargs['ifname']
        else:
            raise ArgError('ifname not specified')

        id = None
        if 'id' in kwargs:
            id = kwargs['id']
        else:
            raise ArgError('image id not specified')

        rpc = """
           <restart xmlns="com:gemds:mds-if-cell">
               <interface>{}</interface>
               <id>{}</id>
           </restart>
        """.format(ifname, id)

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

           with CellFirmware(dev) as fw:
               versions = fw.get_versions(ifname="Cell")
               fw.load(ifname="Cell", url="sftp://<host>/tmp/cell-4Gy-verizon-1.0.0.mpk", username="test", password="test")
               status = fw.status(ifname="Cell")
        """
        Service.__init__(self, dev=dev)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
