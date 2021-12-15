from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, Optional, List

from .abc.discordobject import DiscordObject
from .channels.guildchannel import TextChannel, VoiceChannel
from .types.guildpayload import GuildPayload
from .types.snowflake import Snowflake
from .user.member import Member
from .user.user import User


if TYPE_CHECKING:
    from .role import Role


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
    owner: bool = False
    owner_id: Snowflake
    members: List[dict]
    roles: List[dict]
    emojis: List[dict]
    stickers: List[dict]
