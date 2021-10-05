from typing import Optional

from discord.errors.discordclientexception import DiscordClientException
from aiohttp import ClientWebSocketResponse


class DiscordConnectionClosed(DiscordClientException):
    _code: Optional[int]
    reason = ''
    _shard_id: Optional[int]

    def __init__(self, socket: ClientWebSocketResponse, *, shard_id: Optional[int], code: Optional[int] = None):
        self._code = code or socket.close_code or -1
        self._shard_id = shard_id
        super().__init__(f'Shard {shard_id} closed with code {code}.')

    @property
    def code(self):
        return self._code

    @property
    def shard_id(self):
        return self._shard_id
