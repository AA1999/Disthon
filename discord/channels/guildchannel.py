from __future__ import annotations

import ..abc

from .basechannel import BaseChannel

class TextChannel(BaseChannel):
    __slots__ = (
        "name",
        "id",
        "guild",
        "nsfw",
        "category_id",
        "position"
    )

class VoiceChannel(BaseChannel):
    __slots__ = (
        "name",
        "id",
        "guild",
        "bitrate",
        "user_limit",
        "category_id",
        "position"
    )