import xmltodict
import json
from lxml import etree

# package modules
from .service import Service
from pyorbit.exception import *

"""
Operational Status Service
"""

class Status(Service):
    """
    Opererational Status Service.

    * :meth:`get`: Retrieve running configuration and device state information.
    """

    def get(self, **kvargs):
        """
        Retrieve running configuration and device state information.

        :param object filter:
            A Filter object that is used to limit the data being retrieved.
            For details, see: https://ncclient.readthedocs.io/en/latest/manager.html#filter-parameters

        :param str format:
            Select what format that retrieved data should be set to, either odict or json.

        :returns:
            ``True`` always when successful

        """
        source = 'running'
        rsp_format = 'xml'

        if 'filter' in kvargs:
            filter = kvargs['filter']

        if 'format' in kvargs:
            rsp_format = kvargs['format']

        try:
            rsp = self.dev._conn.get(filter=filter).data_xml
            if rsp_format == 'odict':
                rsp = xmltodict.parse(rsp)
            elif rsp_format == 'json':
                rsp = json.dumps(xmltodict.parse(rsp))
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise GetError(rsp=err.xml)
            else:
                raise

        return rsp

    def __init__(self, dev, **kwargs):
        """
        .. code-block:: python

           with Status(dev) as st:
              rsp = st.get(filter=('xpath','/system/uptime/seconds'), \
                format='json')
        """
        Service.__init__(self, dev=dev)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
