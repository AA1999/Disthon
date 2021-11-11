from __future__ import annotations
from typing import Optional, Union, List, TYPE_CHECKING

from .basechannel import BaseChannel
from ..message import Message

if TYPE_CHECKING:
    from ..embeds import Embed
    from ..interactions.components import View

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