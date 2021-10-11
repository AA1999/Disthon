from __future__ import annotations

from typing import Any, OrderedDict
from discord.types.snowflake import Snowflake
from discord.user.user import User
from discord.member.member import Member
from discord.message.message import Message
from discord.role.role import Role
from discord.guild.guild import Guild
from discord.api.handler import Handler


class LFUCache:
    __slots__ = ('_max_size', '_cache', '_frequency')

    _max_size: int
    _cache: OrderedDict[Snowflake, Any]
    _frequency: dict[Snowflake, int]
    _handler: Handler

    def __init__(self, capacity: int) -> None:
        self._max_size = capacity
        self._frequency = {}

    @classmethod
    def _from_lfu(cls, lfu: LFUCache):
        self = cls.__new__(cls)
        self._max_size = lfu._max_size
        self._cache = lfu._cache
        self._frequency = lfu._frequency
        return self

    def __eq__(self, other) -> bool:
        return isinstance(other, LFUCache) and other._cache == self._cache and self.capacity == other.capacity

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    @property
    def capacity(self):
        return self._max_size

    def __setitem__(self, key: Snowflake, value: Any) -> None:
        self._cache[key] = value
        if self._frequency[key]:
            self._frequency[key] += 1
        else:
            self._frequency[key] = 0
        if len(self._cache) > self.capacity:
            snowflake: Snowflake
            min_freq = 1000000000000000000000000000000000000000000000000
            for k in self._frequency.keys():
                if self._frequency[k] < min_freq:
                    min_freq = self._frequency[k]
                    snowflake = k
            del self._cache[snowflake]

    def __getitem__(self, key: Snowflake):
        if self._cache[key]:
            self._frequency[key] += 1
            return self._cache[key]
        raise KeyError

    def __delitem__(self, key: Snowflake):
        del self._cache[key]
        del self._frequency[key]


class UserCache(LFUCache):
    _cache: dict[Snowflake, User]

    def __init__(self) -> None:
        super().__init__(10000)

    def __setitem__(self, key: Snowflake, value: User) -> None:
        return super().__setitem__(key, value)


class MemberCache(LFUCache):
    _cache: dict[Snowflake, Member]

    def __init__(self) -> None:
        super().__init__(10000)

    def __setitem__(self, key: Snowflake, value: Member) -> None:
        return super().__setitem__(key, value)


class MessageCache(LFUCache):
    _cache: dict[Snowflake, Message]

    def __init__(self) -> None:
        super().__init__(2000)

    def __setitem__(self, key: Snowflake, value: Message) -> None:
        return super().__setitem__(key, value)


class RoleCache(LFUCache):
    _cache: dict[Snowflake, Role]

    def __init__(self) -> None:
        super().__init__(250)

    def __setitem__(self, key: Snowflake, value: Role) -> None:
        return super().__setitem__(key, value)


class GuildCache(LFUCache):
    _cache: dict[Snowflake, Guild]

    def __init__(self) -> None:
        super().__init__(20000)

    def __setitem__(self, key: Snowflake, value: Guild) -> None:
        return super().__setitem__(key, value)
