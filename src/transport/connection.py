""" Connection object base class """
import asyncio
from enum import Flag, auto

class UnsupportedMethodException(Exception):
    """ When Connection type does not support a given method
    """

class ConnectionType(Flag):
    UNDEFINED = 0
    RECV = auto()
    SEND = auto()
    DUPLEX = RECV | SEND


class Connection:
    def __init__(self, flags=ConnectionType.UNDEFINED):
        self.flags = flags
        self.done = asyncio.Event()

    async def recv(self):
        raise UnsupportedMethodException

    async def send(self, msg: str):
        raise UnsupportedMethodException()

    async def wait(self):
        await self.done.wait()

    def can_send(self):
        return self.flags & ConnectionType.SEND

    def can_recv(self):
        return self.flags & ConnectionType.RECV

    def is_duplex(self):
        return self.flags & ConnectionType.DUPLEX

    def close(self):
        self.done.set()

    def upgrade(self):
        self.flags = ConnectionType.DUPLEX
