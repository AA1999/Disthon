from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .types.snowflake import Snowflake

if TYPE_CHECKING:
    from .client import Client


class Message(BaseModel):
    id: Snowflake
    channel_id: Snowflake
    guild_id: Snowflake
    content: str

    _client: Client

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, client, data):
        super().__init__(_client=client, **data)

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"<Message id={self.id} Channel id ={self.channel_id} Content={self.content}>"

    @property
    def channel(self):
        return self._client.converter._get_channel(self.channel_id)


