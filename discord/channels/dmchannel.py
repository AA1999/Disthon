from __future__ import annotations

from typing import List


from discord.abc.discordobject import DiscordObject
from discord.types.image import Image
from discord.user.user import User


class DMChannel(DiscordObject):
    type: int
    recipients: List[User]
    last_message_id: int


class GroupDMChannel(DMChannel):
    name: str
    icon: Image
    owner_id: int
