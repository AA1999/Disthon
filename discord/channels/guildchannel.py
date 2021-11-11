from __future__ import annotations

from .basechannel import BaseChannel

class TextChannel(BaseChannel):
    __slots__ = (
        "name",
        "id",
        "guild",
        "nsfw",
        "category_id",
        "position",
        "topic"
    )

class ThreadChannel(BaseChannel):
    __slots__ = (
        "name",
        "id",
        "guild",
        "nsfw",
        "category_id",
        "position",
        "topic",
        "parent"
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