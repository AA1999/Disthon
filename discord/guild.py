from __future__ import annotations

from typing import NamedTuple, Optional

from .abc.discordobject import DiscordObject
from .channels.guildchannel import GuildChannel
from .role import Role
from .types.guildpayload import GuildPayload
from .types.snowflake import Snowflake
from .user.member import Member
from .user.user import User


class BanEntry(NamedTuple):
    user: User
    reason: Optional[str]


class GuildLimit(NamedTuple):
    filesize: int
    emoji: int
    channels: int
    roles: int
    categories: int
    bitrate: int
    stickers: int


class Guild(DiscordObject):
    __slots__ = (
        "region"
        "owner_id"
        "mfa.level"
        "name"
        "id"
        "_members"
        "_channels"
        "_vanity"
        "_banner"
    )

    _roles: set[Role]
    me: Member
    owner_id: Snowflake

    def __init__(self, data: GuildPayload):
        self._members: dict[Snowflake, Member] = {}
        self._channels: dict[Snowflake, GuildChannel] = {}
        self._roles = set()

    def _add_channel(self, channel: GuildChannel, /) -> None:
        self._channels[channel.id] = channel

    def _delete_channel(self, channel: DiscordObject) -> None:
        self._channels.pop(channel.id, None)

    def add_member(self, member: Member) -> None:
        self._members[member.id] = member

    def add_roles(self, role: Role) -> None:
        for p in self._roles.values:
            p.postion += not p.is_default()
            # checks if role is @everyone or not

            self._roles[role.id] = role
