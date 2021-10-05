from typing import Any, Dict, OrderedDict, TypeVar
from discord.types.snowflake import Snowflake
from discord.user.user import User
from discord.member.member import Member
from discord.message.message import Message
from discord.role.role import Role
from discord.guild.guild import Guild
from discord.api.handler import Handler

LFU = TypeVar('LFU', bound='LFUCache')

class LFUCache:
    __slots__ = ('_max_size', '_cache', '_frequence')

    _max_size: int
    _cache: OrderedDict[Snowflake, Any]
    _frequence: Dict[Snowflake, int]
    _handler: Hand

    def __init__(self, capacity: int) -> None:
        self._max_size = capacity
        self._frequence = {}

    @classmethod
    def _from_lfu(cls, lfu: LFU):
        self = cls.__new__(cls)
        self._max_size = lfu._max_size
        self._cache = lfu._cache
        self._frequence = lfu._frequence
        return self
    
    def __eq__(self, o: object) -> bool:
        return isinstance(o, LFUCache) and o._cache == self._cache and self.capacity == o.capacity

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    @property
    def capacity(self):
        return self._max_size
    
    def __setitem__(self, key: Snowflake, value: Any) -> None:
        self._cache[key] = value
        if self._frequence[key]:
            self._frequence[key] += 1
        else:
            self._frequence[key] = 0
        if len(self._cache) > self.capacity:
            snowflake: Snowflake
            min_freq = 100000000000000000000000000
            for k in self._frequence.keys():
                if self._frequence[k] < min_freq:
                    min_freq = self._frequence[k]
                    snowflake = k
            del self._cache[snowflake]


    def __getitem__(self, key: Snowflake):
        if self._cache[key]:
            self._frequence[key] += 1
            return self._cache[key]
        raise KeyError

    def __delitem__(self, key: Snowflake):
        del self._cache[key]
        del self._frequence[key]
    

class UserCache(LFUCache):
    _cache: Dict[Snowflake, User]
    
    def __init__(self) -> None:
        super().__init__(10000)

    def __setitem__(self, key: Snowflake, value: User) -> None:
        return super().__setitem__(key, value)


class MemberCache(LFUCache):
    _cache: Dict[Snowflake, Member]

    def __init__(self) -> None:
        super().__init__(10000)

    def __setitem__(self, key: Snowflake, value: Member) -> None:
        return super().__setitem__(key, value)

class MessageCache(LFUCache):
    _cache: Dict[Snowflake, Message]

    def __init__(self) -> None:
        super().__init__(2000)

    def __setitem__(self, key: Snowflake, value: Message) -> None:
        return super().__setitem__(key, value)

class RoleCache(LFUCache):
    _cache: Dict[Snowflake, Role]

    def __init__(self) -> None:
        super().__init__(250)

    def __setitem__(self, key: Snowflake, value: Role) -> None:
        return super().__setitem__(key, value)

class GuildCache(LFUCache):
    _cache: Dict[Snowflake, Guild]

    def __init__(self) -> None:
        super().__init__(20000)

    def __setitem__(self, key: Snowflake, value: Guild) -> None:
        return super().__setitem__(key, value)
