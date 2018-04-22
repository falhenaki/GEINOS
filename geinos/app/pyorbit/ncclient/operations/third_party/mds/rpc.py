from ncclient.xml_ import *

from ncclient.operations.rpc import RPC
from ncclient.operations.rpc import RPCReply
from ncclient.operations.rpc import RPCError
from ncclient import NCClientError

class ExecuteRpc(RPC):
    def request(self, rpc):
        if isinstance(rpc, str):
            rpc = to_ele(rpc)
        return self._request(rpc)
