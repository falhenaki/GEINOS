import re
import xmltodict
import json
from jinja2 import Template
from lxml import etree

# package modules
from .service import Service
from pyorbit.exception import *

"""
Configuration Service
"""

class Config(Service):
    """
    Configuration Service.

    * :meth:`lock`: take an exclusive lock on the candidate config
    * :meth:`unlock`: release the exclusive lock
    * :meth:`get`: get config
    * :meth:`load`: load changes into the candidate config
    * :meth:`validate`: perform the validation on candidate config
    * :meth:`diff`: return the diff string between running and candidate config
    * :meth:`commit`: commit changes
    * :meth:`rollback`: rollback back config
    """

    def lock(self):
        """
        Attempts an exclusive lock on the candidate configuration.  This
        is a non-blocking call.

        :returns:
            ``True`` always when successful

        :raises LockError: When the lock cannot be obtained
        """
        try:
            self.dev._conn.lock()
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise LockError(rsp=err.xml)
            else:
                raise

        return True

    def unlock(self):
        """
        Unlocks the candidate configuration.

        :returns:
            ``True`` always when successful

        :raises UnlockError: If you attempt to unlock a configuration
                             when you do not own the lock
        """
        try:
            self.dev._conn.unlock()
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise UnlockError(rsp=err.xml)
            else:
                raise

        return True

    def get(self, **kvargs):
        """
        Get the configuration from target store.

        :returns:
            ``True`` always when successful

        :raises UnlockError: If you attempt to unlock a configuration
                             when you do not own the lock
        """
        source = 'running'
        rsp_format = 'xml'

        if 'source' in kvargs:
            source = kvargs['source']

        if 'format' in kvargs:
            rsp_format = kvargs['format']

        try:
            rsp = self.dev._conn.get_config(source=source).data_xml
            if rsp_format == 'odict':
                rsp = xmltodict.parse(out)
            if rsp_format == 'json':
                rsp = json.dumps(xmltodict.parse(rsp))
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetConfigError(rsp=err.xml)
            else:
                raise

        return rsp

    def load(self, **kvargs):
        """
        Loads changes into the candidate configuration.  Changes can be
        in the form of strings (xml), XML objects, and files.
        Files can be either static snippets of configuration or Jinja2
        templates.  When using Jinja2 Templates, this method will render
        variables into the templates and then load the resulting change.

        :param object content:
            The content to load.  If the content is a string, the framework
            will attempt to automatically determine the format.  If it is
            unable to determine the format then you must specify the
            **format** parameter.  If the content is an XML object, then
            this method assumes you've structured it correctly;
            and if not an Exception will be raised.

        :param str path:
            Path to configuratio file on a server.
            The path extension will be used to determine the format of
            the contents:

            * "xml"
            * "json"

            .. note:: The format can specifically be set using **format**.

        :param str format:
          Determines the format of the content. Refer to options
          from the **path** description.

        :param bool operation:
          Determines if the operation ('merge' or 'replace') applied to the
          candidate configuration.  Default is ``merge``.

        :param jinja2.Template template:
          A Jinja2 Template object or str.

        :param dict template_vars:
          Dictionary of variables to render into the template.

        :returns:
            RPC-reply as XML str.

        :raises: ConfigLoadError: When errors detected while loading candidate
                                  configuration. You can use the Exception
                                  errs variable  to identify the specific
                                  problems.
        """
        rpc_contents = None

        operation = 'merge'
        if 'operation' in kvargs:
            operation = kvargs['operation']

        # private helpers

        def _lformat_byext(path):
            """ determine the format style from the file extension """
            ext = os.path.splitext(path)[1]
            if ext == '.xml':
                return 'xml'
            elif ext == '.json':
                return 'json'
            raise ValueError("Unknown file contents from extension: %s" % ext)

        def _lset_fromfile(path):
            """ setup the format based on path """
            if 'format' not in kvargs:
                kvargs['format'] = _lformat_byext(path)


        def _lset_from_rexp(content):
            """ setup the format based on content """
            if re.search(r'^\s*<.*>$', content, re.MULTILINE):
                kvargs['format'] = 'xml'
            elif re.search(r'^\s*\{', content) and re.search(r'.*}\s*$', content):
                kvargs['format'] = 'json'
            elif re.search(r'^\s*(set|delete|rename)\s', content):
                kvargs['format'] = 'set'

        # if content is provided as argument
        if 'content' in kvargs:
            rpc_contents = kvargs['content']
            if isinstance(rpc_contents, str):
                if 'format' not in kvargs:
                    _lset_from_rexp(rpc_contents)

        # if path is provided, use the static-config file
        elif 'path' in kvargs:
            rpc_contents = open(kvargs['path'], 'rU').read()
            _lset_fromfile(kvargs['path'])

        elif 'template' in kvargs:
            template = kvargs['template']
            if isinstance(template, str):
                template = Template(template)
            rpc_contents = template.render(kvargs.get('template_vars', {}))
            _lset_from_rexp(rpc_contents)

        if rpc_contents is None:
            raise RuntimeError("contents not available")

        try:
            rsp = self.dev._conn.edit_config(config=rpc_contents, \
                default_operation=operation)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise ConfigLoadError(rsp=err.xml)
            else:
                raise
        return rsp

    def validate(self):
        """
        Validate canidate config validation.

        :returns: ``True`` if validation is successful (no errors)
        """
        try:
            self.dev._conn.validate()
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise LoadError(rsp=err.xml)
            else:
                raise

        return True

    def diff(self, rb_id=0):
        """
        Retrieve a diff report of the candidate config against
        either the current active config, or a different rollback.

        :param int rb_id: rollback id [0..49]

        :returns:
            * ``None`` if there is no difference
            * ascii-text (str) if there is a difference
        """

        if rb_id < 0 or rb_id > 49:
            raise ArgError("Invalid rollback #" + str(rb_id))

        try:
            pass
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise LoadError(rsp=err.xml)
            else:
                raise

        return None

    def commit(self, **kvargs):
        """
        Commit a configuration.

        :param bool confirmed: whether this is a confirmed commit
        :param int timeout: specifies the confirm timeout in seconds

          For example::

            cu.commit()

        :returns:
            * ``True`` when successful

        :raises CommitError: When errors detected in candidate configuration.

        """
        try:
            confirmed=False
            if 'confirmed' in kvargs:
                confirmed = kvargs['confirmed']

            timeout=None
            if 'timeout' in kvargs:
                timeout = kvargs['timeout']

            rsp = self.dev._conn.commit(confirmed=confirmed, timeout=timeout)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise CommitError(rsp=err.xml)
            else:
                raise

        return rsp

    def rollback(self, rb_id=0):
        """
        Rollback the candidate config to either the last active or
        a specific rollback number.

        :param int rb_id: The rollback id value [0-49], defaults to ``0``.

        :returns:
            ``True`` always when successful

        :raises ArgError: When invalid rollback id is given

        """

        if rb_id < 0 or rb_id > 49:
            raise ArgError("Invalid rollback #" + str(rb_id))

        try:
            pass
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise RollbackError(rsp=err.xml)
            else:
                raise

        return True

    def __init__(self, dev, **kwargs):
        """
        .. code-block:: python

           with Config(dev) as cm:
               cm.load('<config></config>')
               print cm.diff()
               cm.commit()
        """
        Service.__init__(self, dev=dev)

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unlock()
