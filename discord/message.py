from __future__ import annotations

from .abc.discordobject import DiscordObject
from .types.snowflake import Snowflake


class Message(DiscordObject):
    channel_id: Snowflake
    guild_id: Snowflake
    content: str

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"<Message id={self.id} content={self.content} channel_id ={self.channel_id} guild_id={self.guild_id}>"

    @property
    def guild(self):
        return self._client.ws.guild_cache.get(self.guild_id)

    @property
    def channel(self):
        return self._client.ws.channel_cache.get(self.channel_id)
