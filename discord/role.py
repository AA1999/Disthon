from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any

from .abc.discordobject import DiscordObject
from .asset import Asset
from .color import Color

if TYPE_CHECKING:
    from .guild import Guild

__all__ = ("RoleTags", "Role")

from .cache import LFUCache
from .types.rolepayload import RolePayload, RoleTagsPayload
from .types.snowflake import Snowflake


class RoleTags:
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
    id: Snowflake
    guild: Any
    name: str
    color: Color
    hoist: bool
    icon: Optional[str] = None
    unicode_emoji: Optional[str] = None
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: Optional[RoleTags] = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Role {self.name} with id {self.id}"

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
