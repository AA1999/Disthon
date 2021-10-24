from typing import (
    NamedTuple,
    Optional,
    List,
    MISSING
)

from discord.abc.discordobject import DiscordObject
from discord.channels.guildchannel import GuildChannel
from discord.member.member import Member
from discord.role.role import Role
from discord.types.guildpayload import GuildPayload
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
    __slots__ = (
        'region'
        'owner_id'
        'mfa.level'
        'name'
        'id'
        '_members'
        '_channels'
        '_vanity'
        '_banner'
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
    def remove_roles(self, role:Role) -> None:
        role = self._roles.pop(role.id)

        for p in self._roles.values:
            p.position -= p.position > role.position

        return role
    @property
    async def channels(self) -> List[GuildChannel]:
        return list(self._channels.values())
    @property
    async def roles(self) -> List[Role]:
        return sorted(self._roles.values())
    @property
    async def owner(self) -> Optional[Member]:
        return self.get_member(self.owner.id)
    @property
    async def members(self) -> List[Member]:
        return list(self._members.values())
    def get_member(self, member_id: int) -> Optional[Member]:
        return self._members.get(member_id)
    def get_channel(self, channel_id: int) -> Optional[GuildChannel]:
        return self._channels(channel_id)

    async def create_channel(
        self,
        *,
        name: str,
        type: str = None,
        reason: Optional[str] = None,
        category: Optional[CategoryChannel] = None,
        position: int = None,
        slowmode_delay: int = None
    ):
     return
        
    

