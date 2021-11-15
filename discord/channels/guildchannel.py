from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from ..message import Message
from .basechannel import BaseChannel

if TYPE_CHECKING:
    from ..embeds import Embed
    from ..interactions.components import View


class TextChannel(BaseChannel):
    __slots__ = ("name", "id", "guild", "nsfw", "category_id", "position", "topic")


class ThreadChannel(BaseChannel):
    __slots__ = (
        "name",
        "id",
        "guild",
        "nsfw",
        "category_id",
        "position",
        "topic",
        "parent",
    )


class VoiceChannel(BaseChannel):
    __slots__ = (
        "name",
        "id",
        "guild",
        "bitrate",
        "user_limit",
        "category_id",
        "position",
    )
