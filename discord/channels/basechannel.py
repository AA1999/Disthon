from __future__ import annotations

from ..abc.discordobject import DiscordObject
from ..types.snowflake import Snowflake


class BaseChannel(DiscordObject):
    name: str

    @property
    def mention(self):
        return f"<#{self.id}>"

    @property
    def created_at(self):
        return
