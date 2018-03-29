
# package modules
import Service

"""
Firmware Service
"""

class Firmware(Service):
    """
    Overview of Firmware Service.

    * :meth:`load`: load firmware in inactive image

    """

    def load(self, *vargs, **kvargs):
        """
        Loads firmware into inactive image

        :param str url:
          Specify the full pathname of the file that contains the configuration
          data to load. The value can be a local file path, an FTP location, or
          a Hypertext Transfer Protocol (HTTP).

          For example::

            fw.load(url="/tmp/mcr-bkrc-6.5.7.mpk")
            fw.load(url="ftp://username@ftp.hostname.net/filename")
            fw.load(url="http://username:password@hostname/path/filename")

        :returns:
            True

        :raises: FwLoadError: When firmware load fails.

        """
        pass

    def __init__(self, dev, **kwargs):
        """
        .. code-block:: python

           with Firmware(dev) as fw:
               fw.load(url="/tmp/mcr-bkrc-6.5.7.mpk")
        """
        Service.__init__(self, dev=dev)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
