from __future__ import annotations

from ..abc.discordobject import DiscordObject
from ..types.snowflake import Snowflake


class BaseChannel(DiscordObject):
    __slots__ = ('_id', '_name')

    _id: Snowflake
    _name: str

    @property
    def id(self) -> Snowflake:
        return self._id

    @property
    def name(self):
        return self._name

