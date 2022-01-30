from __future__ import annotations

from pydantic import BaseModel

from .types.snowflake import Snowflake


class Message(BaseModel):
    id: Snowflake
    channel_id: Snowflake
    guild_id: Snowflake
    content: str

    def __init__(self, client, data):
        super().__init__(_client=client, **data)

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"<Message id={self.id} content={self.content} channel_id ={self.channel_id} guild_id={self.guild_id}>"

    @property
    def channel(self):
        return self._client.converter._get_channel(self.channel_id)
