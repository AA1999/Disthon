from __future__ import annotations

from ..abc.discordobject import DiscordObject
from ..abc.messageable import Messageable
from ..types.snowflake import Snowflake


class BaseChannel(DiscordObject, Messageable):
    name: str

    def _get_channel(self):
        return self

    @property
    def mention(self):
        return f"<#{self.id}>"

    @property
    def created_at(self):
        return
