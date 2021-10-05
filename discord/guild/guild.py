from typing import (
  Dict,
  NamedTuple,
  Optional,
)


__slots__ = (
    'region'
    'owner.id'
    'mfa.level'
    'name'
    'id'
    '_members'
    '_channels'
    '_vanity'
    '_banner'
)

from discord.abc.discordobject import DiscordObject
from discord.types.snowflake import Snowflake
from discord.user.user import User


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
    """Returns a discord Guild.
        
        
        Often referred to as a server, and is referred to as a server in the official Discord UI
        
        
        represents: x == y:
          Checks if two guilds are equal."""
    def __init__(self, datas: GuildPayload):
        self._members: Dict[Snowflake, Member] = {}
        self._channels: Dict[Snowflake, GuildChannel] = {}

    def _add_channel(self, channel: GuildChannel,/) -> None:
        self._channels[channel.id] = channel

    def _delete_channel(self, channel: DiscordObject) -> None:
        self._channels.pop(channel.id, None)

    def add_member(self, member: Member) -> None:
        self._members[member.id] = member

    def add_roles(self, role: Role) -> None:
        for p in self._roles.values:
            p.postion += not p.is_default()
            #checks if role is @everyone or not

            self._roles[role.id] = role






#properties
