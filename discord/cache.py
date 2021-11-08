from __future__ import annotations

from typing import TYPE_CHECKING, Any, OrderedDict

if TYPE_CHECKING:

    from .api.handler import Handler
    from .guild import Guild
    from .message import Message
    from .role import Role
    from .types.snowflake import Snowflake
    from .user.member import Member
    from .user.user import User


class LFUCache:

    capacity: int
    _cache: OrderedDict[Snowflake, Any]
    _frequency: dict[Snowflake, int]
    handler: Handler

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._frequency = {}

    @classmethod
    def _from_lfu(cls, lfu: LFUCache):
        self = cls.__new__(cls)
        self.capacity = lfu.capacity
        self._cache = lfu._cache
        self._frequency = lfu._frequency
        return self

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, LFUCache)
            and other._cache == self._cache
            and self.capacity == other.capacity
        )

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __setitem__(self, key: Snowflake, value: Any) -> None:
        self._cache[key] = value
        if self._frequency[key]:
            self._frequency[key] += 1
        else:
            self._frequency[key] = 0
        if len(self._cache) > self.capacity:
            snowflake: Snowflake
            min_freq = float("inf")
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
        super().__init__(100000)

    def __setitem__(self, key: Snowflake, value: User) -> None:
        return super().__setitem__(key, value)


class MemberCache(LFUCache):
    _cache: dict[Snowflake, Member]

    def __init__(self) -> None:
        super().__init__(100000)

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
