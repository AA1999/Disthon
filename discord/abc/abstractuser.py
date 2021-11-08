from __future__ import annotations

from typing import Optional

from ..message import Message
from ..types.avatar import Avatar

from discordobject import DiscordObject


class AbstractUser(DiscordObject):

    avatar: Optional[Avatar]
    bot: bool
    username: str
    discriminator: str

    @property
    def tag(self):
        return f"{self.username}#{self.discriminator}"

    @property
    def mention(self):
        return f"<@!{self.id}>"

    def mentioned_in(self, message: Message):
        if message.mention_everyone:
            return True
        return any(user.id == self.id for user in message.mentions)
