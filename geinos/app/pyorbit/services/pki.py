from urllib import parse
from lxml import etree

# package modules
from .service import Service
from app.pyorbit.exception import *

"""
PKI Service
"""

class PKI(Service):
    """
    Overview of PKI Service.

    * :meth:`restart`: Restart device to specified image.

    """

    #
    # PRIVATE KEYS API
    #
    def gen_priv_key(self, **kwargs):
        """
        Generates private key.

        :param str key_id:
          Specify the identifier/name for the key.

        :param str key_size:
            Specify the key_size (1024/1536/2048/3072/4096)

        For example::
            pki.gen_priv_key(key_id="DEVKEY", key_size="2048")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'key_id' in kwargs:
            key_id = kwargs['key_id']
        else:
            raise ArgError("key_id must be specified")

        if 'key_size' in kwargs:
            key_size = kwargs['key_size']
        else:
            raise ArgError("key_size must be specified")


        rpc = """
            <generate-private-key xmlns="com:gemds:mds-certmgr">
                <key-identity>{}</key-identity>
                <key-size>{}</key-size>
            </generate-private-key>
        """.format (key_id, key_size)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def del_priv_key(self, **kwargs):
        """
        Deletes private key.

        :param str key_id:
          Specify the name for the key.

        For example::
            pki.del_priv_key(key_id="DEVKEY")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'key_id' in kwargs:
            key_id = kwargs['key_id']
        else:
            raise ArgError("key_id must be specified")

        rpc = """
            <delete-private-key xmlns="com:gemds:mds-certmgr">
                <key-identity>{}</key-identity>
            </delete-private-key>
        """.format (key_id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def get_priv_key_gen_status(self, **kwargs):
        """
        Get private key generation status.

        :returns:
            Status as dict.

        :raises: GetError: When operation fails.

        """

        filter = """/pki/private-keys/generate-status"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    def cancel_priv_key_gen(self, **kwargs):
        """
        Cancel ongoing private key generation.

        For example::
            pki.cancel_priv_key_gen()

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = """
            <cancel-generate-private-key xmlns="com:gemds:mds-certmgr"/>
        """

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def get_priv_keys(self, **kwargs):
        """
        Retrieves list of private keys on the device.

        :returns:
            Status as dict.

        :raises: GetError: When operation fails.
        """

        filter = """/pki/private-keys/show-all"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    #
    # CA CERT API
    #
    def import_ca_cert_efile(self, **kwargs):
        """
        Imports CA cert from external file server.

        :param str cert_id:
          Specify the identifier/name for the CA cert.

        :param str url:
          Specify the identity configured in the device for the SCEP server.

        :param str username:
          File server username

        :param str password:
          File server password

        For example::
            pki.import_ca_cert_efile(cert_id="CACERT",url="sftp://<host>/tmp/mcr-bkrc-6.7.8.mpk", username="test", password="test")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'cert_id' in kwargs:
            cert_id = kwargs['cert_id']
        else:
            raise ArgError("cert_id must be specified")

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
            <import-ca-cert xmlns="com:gemds:mds-certmgr">
                <efile>
                    <filename>{}</filename>
                    <manual-file-server>
                        <sftp>
                            <address>{}</address>
                            <username>{}</username>
                            <password>{}</password>
                        </sftp>
                    </manual-file-server>
                </efile>
                <cert-identity>{}</cert-identity>
            </import-ca-cert>
        """.format (urlsplit.path, urlsplit.netloc, username, password, cert_id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def import_ca_cert_scep(self, **kwargs):
        """
        Imports CA cert via SCEP.

        :param str cert_id:
          Specify the identifier/name for the CA cert.

        :param str cert_server_id:
          Specify the identity configured in the device for the SCEP server.

        :param str ca_server_id:
          Specify the identity configured in the device for the CA server.

        For example::
            pki.import_ca_cert_scep(cert_id="CACERT",cert_server_id="CERT-SERVER", ca_server_id="CA-SERVER")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'cert_id' in kwargs:
            cert_id = kwargs['cert_id']
        else:
            raise ArgError("cert_id must be specified")

        if 'cert_server_id' in kwargs:
            cert_server_id = kwargs['cert_server_id']
        else:
            raise ArgError("cert_server_id must be specified")

        if 'ca_server_id' in kwargs:
            ca_server_id = kwargs['ca_server_id']
        else:
            raise ArgError("ca_server_id must be specified")

        rpc = """
            <import-ca-cert xmlns="com:gemds:mds-certmgr">
                <scep>
                    <cert-server-identity>{}</cert-server-identity>
                    <ca-issuer-identity>{}</ca-issuer-identity>
                </scep>
                <cert-identity>{}</cert-identity>
            </import-ca-cert>
        """.format (cert_server_id, ca_server_id, cert_id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def del_ca_cert(self, **kwargs):
        """
        Deletes CA cert on the device.

        :param str cert_id:
          Specify the name for the CA cert.

        For example::
            pki.del_ca_cert(cert_id="CACERT")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'cert_id' in kwargs:
            cert_id = kwargs['cert_id']
        else:
            raise ArgError("cert_id must be specified")

        rpc = """
            <delete-ca-cert xmlns="com:gemds:mds-certmgr">
                <cert-identity>{}</cert-identity>
            </delete-ca-cert>
        """.format (cert_id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def get_ca_cert_import_status(self, **kwargs):
        """
        Get CA certificate import status.

        :returns:
            Status as dict.

        :raises: GetError: When operation fails.

        """

        filter = """/pki/ca-certs/import-status"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    def get_ca_certs(self, **kwargs):
        """
        Retrieves list of CA certs on the device.

        :returns:
            Status as dict.

        :raises: GetError: When operation fails.
        """

        filter = """/pki/ca-certs/show-all"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    #
    # CLIENT CERT API
    #
    def import_client_cert_efile(self, **kwargs):
        """
        Imports client cert from external file server.

        :param str cert_id:
          Specify the identifier/name for the client cert.

        :param str url:
          Specify the identity configured in the device for the SCEP server.

        :param str username:
          File server username

        :param str password:
          File server password

        For example::
            pki.import_client_cert_efile(cert_id="DEVCERT",url="sftp://<host>/tmp/mcr-bkrc-6.7.8.mpk", username="test", password="test")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'cert_id' in kwargs:
            cert_id = kwargs['cert_id']
        else:
            raise ArgError("cert_id must be specified")

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
            <import-client-cert xmlns="com:gemds:mds-certmgr">
                <efile>
                    <filename>{}</filename>
                    <manual-file-server>
                        <sftp>
                            <address>{}</address>
                            <username>{}</username>
                            <password>{}</password>
                        </sftp>
                    </manual-file-server>
                </efile>
                <cert-identity>{}</cert-identity>
            </import-ca-cert>
        """.format (cert_id, urlsplit.path, urlsplit.netloc, username, password)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def import_client_cert_scep(self, **kwargs):
        """
        Imports client cert via SCEP.

        :param str cert_id:
          Specify the identifier/name for the client cert.

        :param str cert_server_id:
          Specify the identity configured in the device for the SCEP server.

        :param str ca_server_id:
          Specify the identity configured in the device for the CA server.

        :param str cert_info_id:
          Specify the identity of certificate info configured in the device. 

        :param str cacert_id:
          Specify the identity of CA certificate configured in the device. 

        :param str key_id:
          Specify the identity of private key configured in the device. 

        :param str otp:
          Specify the OTP/challenge obtained from SCEP server. 

        For example::
            pki.import_client_cert_scep(cert_id="DEVCERT",cert_server_id="CERT-SERVER", ca_server_id="CA-SERVER", cert_info_id="CERT-INFO", cacert_id="CACERT", key_id="DEVKEY",otp="36DE2A1E53BECF9AE5BB3E0B12D4C85E")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'cert_id' in kwargs:
            cert_id = kwargs['cert_id']
        else:
            raise ArgError("cert_id must be specified")

        if 'cert_server_id' in kwargs:
            cert_server_id = kwargs['cert_server_id']
        else:
            raise ArgError("cert_server_id must be specified")

        if 'ca_server_id' in kwargs:
            ca_server_id = kwargs['ca_server_id']
        else:
            raise ArgError("ca_server_id must be specified")

        if 'cert_info_id' in kwargs:
            cert_info_id = kwargs['cert_info_id']
        else:
            raise ArgError("cert_info_id must be specified")

        if 'cacert_id' in kwargs:
            cacert_id = kwargs['cacert_id']
        else:
            raise ArgError("cacert_id must be specified")

        if 'key_id' in kwargs:
            key_id = kwargs['key_id']
        else:
            raise ArgError("key_id must be specified")

        if 'otp' in kwargs:
            otp = kwargs['otp']
        else:
            raise ArgError("OTP/challenge must be specified")

        rpc = """
            <import-client-cert xmlns="com:gemds:mds-certmgr">
                <scep>
                    <cert-server-identity>{}</cert-server-identity>
                    <ca-issuer-identity>{}</ca-issuer-identity>
                    <cert-info-identity>{}</cert-info-identity>
                    <ca-cert-identity>{}</ca-cert-identity>
                    <private-key-identity>{}</private-key-identity>
                    <ca-challenge>{}</ca-challenge>
                </scep>
                <cert-identity>{}</cert-identity>
            </import-client-cert>
        """.format (cert_server_id, ca_server_id, cert_info_id, cacert_id, key_id, otp, cert_id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def renew_client_cert_scep(self, **kwargs):
        """
        Renews existing client cert via SCEP.

        :param str cert_id:
          Specify the identifier/name for the client cert.

        :param str cert_server_id:
          Specify the identity configured in the device for the SCEP server.

        :param str ca_server_id:
          Specify the identity configured in the device for the CA server.

        :param str cert_info_id:
          Specify the identity of certificate info configured in the device. 

        :param str cacert_id:
          Specify the identity of CA certificate configured in the device. 

        :param str key_id:
          Specify the identity of private key configured in the device. 

        :param str existing_cert_id:
          Specify the existing client certificate identity for renewal via  SCEP.

        :param str existing_key_id:
          Specify the existing client private identity for cert. renewal via SCEP.

        For example::
            pki.renew_client_cert_scep(cert_id="DEVCERT",cert_server_id="CERT-SERVER", ca_server_id="CA-SERVER", cert_info_id="CERT-INFO", cacert_ID="CACERT", key_id="DEVKEY", existing_cert_id="DEVCERT", existing_key_id="DEVKEY")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'cert_id' in kwargs:
            cert_id = kwargs['cert_id']
        else:
            raise ArgError("cert_id must be specified")

        if 'cert_server_id' in kwargs:
            cert_server_id = kwargs['cert_server_id']
        else:
            raise ArgError("cert_server_id must be specified")

        if 'ca_server_id' in kwargs:
            ca_server_id = kwargs['ca_server_id']
        else:
            raise ArgError("ca_server_id must be specified")

        if 'cert_info_id' in kwargs:
            cert_info_id = kwargs['cert_info_id']
        else:
            raise ArgError("cert_info_id must be specified")

        if 'cacert_id' in kwargs:
            cacert_id = kwargs['cacert_id']
        else:
            raise ArgError("cacert_id must be specified")

        if 'key_id' in kwargs:
            key_id = kwargs['key_id']
        else:
            raise ArgError("key_id must be specified")

        if 'existing_cert_id' in kwargs:
            existing_cert_id = kwargs['existing_cert_id']
        else:
            raise ArgError("Existing cert identity must be specified")

        if 'existing_key_id' in kwargs:
            existing_key_id = kwargs['existing_key_id']
        else:
            raise ArgError("Existing key identity must be specified")

        rpc = """
            <import-client-cert xmlns="com:gemds:mds-certmgr">
                <cert-identity>{}</cert-identity>
                <scep>
                    <cert-server-identity>{}</cert-server-identity>
                    <ca-issuer-identity>{}</ca-issuer-identity>
                    <cert-info-identity>{}</cert-info-identity>
                    <ca-cert-identity>{}</ca-cert-identity>
                    <private-key-identity>{}</private-key-identity>
                    <existing-cert-identity>{}</existing-cert-identity>
                    <existing-private-key-identity>{}</existing-private-key-identity>
                </scep>
            </import-client-cert>
        """.format (cert_id, cert_server_id, ca_server_id, cert_info_id, cacert_id, key_id, existing_cert_id, existing_key_id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def del_client_cert(self, **kwargs):
        """
        Deletes client cert on the device.

        :param str cert_id:
          Specify the name for the client cert.

        For example::
            pki.del_client_cert(cert_id="DEVCERT")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'cert_id' in kwargs:
            cert_id = kwargs['cert_id']
        else:
            raise ArgError("cert_id must be specified")

        rpc = """
            <delete-client-cert xmlns="com:gemds:mds-certmgr">
                <cert-identity>{}</cert-identity>
            </delete-client-cert>
        """.format (cert_id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def get_client_cert_import_status(self, **kwargs):
        """
        Get client certificate import status.

        :returns:
            Status as dict.

        :raises: GetError: When operation fails.

        """

        filter = """/pki/client-certs/import-status"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    def get_client_cert_import_scep_status(self, **kwargs):
        """
        Get client certificate import SCEP status.

        :returns:
            Status as dict.

        :raises: GetError: When operation fails.

        """

        filter = """/pki/client-certs/import-scep-status"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    def get_client_certs(self, **kwargs):
        """
        Retrieves list of client certs on the device.

        :returns:
            Status as dict.

        :raises: GetError: When operation fails.
        """

        filter = """/pki/client-certs/show-all"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    #
    # FIRMWARE CERT API
    #
    def import_fw_cert(self, **kwargs):
        """
        Imports firmware cert from external file server.

        :param str cert_id:
          Specify the identifier/name for the firmware cert.

        :param str url:
          Specify the identity configured in the device for the SCEP server.

        :param str username:
          File server username

        :param str password:
          File server password

        For example::
            pki.import_fw_cert(cert_id="GEMDS-FW",url="sftp://<host>/tmp/pkgsigner-cert.pem", username="test", password="test")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'cert_id' in kwargs:
            cert_id = kwargs['cert_id']
        else:
            raise ArgError("cert_id must be specified")

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
            <import-firmware-cert xmlns="com:gemds:mds-certmgr">
                <filename>{}</filename>
                <manual-file-server>
                    <sftp>
                        <address>{}</address>
                        <username>{}</username>
                        <password>{}</password>
                    </sftp>
                </manual-file-server>
                <cert-identity>{}</cert-identity>
            </import-firmware-cert>
        """.format (urlsplit.path, urlsplit.netloc, username, password, cert_id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def del_fw_cert(self, **kwargs):
        """
        Deletes firmware cert on the device.

        :param str cert_id:
          Specify the name for the firmware cert.

        For example::
            pki.del_client_cert(cert_id="GEMDS-FW")

        :returns:
            True

        :raises: PkiError: When operation fails.
        """

        rpc = None

        if 'cert_id' in kwargs:
            cert_id = kwargs['cert_id']
        else:
            raise ArgError("cert_id must be specified")

        rpc = """
            <delete-firmware-cert xmlns="com:gemds:mds-certmgr">
                <cert-identity>{}</cert-identity>
            </delete-firmware-cert>
        """.format (cert_id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise PkiError(rsp=err.xml)
            else:
                raise
        return True

    def get_fw_cert_import_status(self, **kwargs):
        """
        Get firmware certificate import status.

        :returns:
            Status as dict.

        :raises: GetError: When operation fails.

        """

        filter = """/pki/firmware-certs/import-status"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    def get_fw_certs(self, **kwargs):
        """
        Retrieves list of firmware certs on the device.

        :returns:
            Status as dict.

        :raises: GetError: When operation fails.
        """

        filter = """/pki/firmware-certs/show-all"""

        try:
            rsp = xmltodict.parse(self.dev._conn.get(filter=('xpath',filter)).data_xml)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    def __init__(self, dev, **kwargs):
        """
        .. code-block:: python

           with PKI(dev) as pki:
               sys.gen_priv_key(key_id="DEVKEY", key_size="2048")
               sys.del_priv_key(key_id="DEVKEY")
        """
        Service.__init__(self, dev=dev)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
