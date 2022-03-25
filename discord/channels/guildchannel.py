from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from ..message import Message
from .basechannel import BaseChannel

if TYPE_CHECKING:
    from ..embeds import Embed
    from ..interactions.components import View


class TextChannel(BaseChannel):
    ...


class ThreadChannel(BaseChannel):
    ...


class VoiceChannel(BaseChannel):
    ...
