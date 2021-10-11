from abc import ABCMeta
from datetime import datetime

from discord.types.snowflake import Snowflake


class DiscordObject(metaclass=ABCMeta):
    __slots__ = ('_id', '_created_at')

    _id: Snowflake
    _created_at: datetime

    @property
    def id(self) -> Snowflake:
        return self._id

    @property
    def created_at(self):
        return self._created_at

    def __eq__(self, other):
        return isinstance(other, DiscordObject) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id.id >> 22
