from __future__ import annotations

from ..guild.guild import GuildChannel
import ..abc

from .basechannel import BaseChannel

class TextChannel(GuildChannel):
    __slots__ = (
        "name",
        "id",
        "guild",
        "nsfw",
        "category_id",
        "position"
    )
    