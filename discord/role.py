from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar

from .abc.discordobject import DiscordObject
from .color import Color

if TYPE_CHECKING:
    from .guild import Guild

__all__ = ("RoleTags", "Role")

from .cache import RoleCache
from .types.rolepayload import RolePayload, RoleTagsPayload
from .types.snowflake import Snowflake


class RoleTags:
    __slots__ = ("_bot_id", "_integration_id", "_premium_subscriber")
    _bot_id: Snowflake
    _integration_id: Snowflake
    _premium_subscriber: bool

    def __init__(self, payload: RoleTagsPayload):
        self._bot_id = payload["bot_id"]
        self._integration_id = payload["integration_id"]
        self._premium_subscriber = payload["premium_subscriber"]

    def is_bot_managed(self) -> bool:
        return self._bot_id is not None

    def is_premium_subscriber(self):
        return self._premium_subscriber is not None

    def is_integration(self):
        return self._integration_id is not None

    def __repr__(self):
        return f"bot id: {self._bot_id}, integration id: {self._integration_id} premium subscriber: {self.is_premium_subscriber()}"


class Role(DiscordObject):
    __slots__ = (
        "_guild",
        "_cache",
        "_id",
        "_name",
        "_color",
        "_hoist",
        "_position",
        "_permissions",
        "_managed",
        "_mentionable",
        "_tags",
    )

    _guild: Guild
    _cache: RoleCache
    _id: Snowflake
    _name: str
    _color: Color
    _hoist: bool
    _position: int
    _permissions: str
    _managed: bool
    _mentionable: bool
    _tags: Optional[RoleTags]

    def __init__(self, guild: Guild, cache: RoleCache, payload: RolePayload):
        self._guild = guild
        self._cache = cache
        self._id = payload["id"]
        self._name = payload["name"]
        self._color = payload["color"]
        self._hoist = payload["hoist"]
        self._position = payload["position"]
        self._permissions = payload["permissions"]
        self._managed = payload["managed"]
        self._mentionable = payload["mentionable"]
        self._tags = RoleTags(payload["tags"])

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"Role {self._name} with id {self._id}"

    def __eq__(self, other):
        return (
            isinstance(other, Role)
            and self.id == other.id
            and self.guild == other.guild
        )

    def __lt__(self, other):
        if not isinstance(other, Role):
            raise NotImplementedError

        if self.guild != other.guild:
            raise RuntimeError("Cannot compare roles from different guilds.")

        if self.id == self.guild.id:
            return other.id != self.guild.id

        if self.position != other.position:
            return self.position < other.position
        return self.id < other.id

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def is_everyone(self):
        return self.id == self.guild.id

    def is_bot_managed(self):
        return self.tags is not None and self.tags.is_bot_managed()

    def is_integration(self):
        return self.tags is not None and self.tags.is_integration()

    def is_premium_subscriber(self):
        return self.tags is not None and self.tags.is_premium_subscriber()

    def is_assignable(self):
        me = self.guild.me
        return (
            not self.is_everyone()
            and not self.managed
            and (me.top_role > self or me.id == self.guild.owner_id)
        )

    @property
    def id(self) -> Snowflake:
        return self._id

    @property
    def guild(self) -> Guild:
        return self._guild

    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> Color:
        return self._color

    @property
    def hoist(self) -> bool:
        return self._hoist

    @property
    def position(self) -> int:
        return self._position

    @property
    def permissions(self) -> str:
        return self._permissions

    @property
    def managed(self) -> bool:
        return self._managed

    @property
    def mentionable(self) -> bool:
        return self._mentionable

    @property
    def tags(self) -> RoleTags:
        return self._tags
