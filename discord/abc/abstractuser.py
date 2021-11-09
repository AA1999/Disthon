from __future__ import annotations

from typing import Optional

from discordobject import DiscordObject

from ..message import Message
from ..types.avatar import Avatar


class AbstractUser(DiscordObject):

    avatar: Optional[Avatar]
    bot: bool
    username: str
    discriminator: str
    id: int

    @property
    def tag(self):
        return f"{self.username}#{self.discriminator}"
    
    @property
    def discriminator(self):
        return self.discriminator

    @property
    def mention(self):
        return f"<@!{self.id}>"
    
    @propery
    def name(self):
        return self.username
    
    @property
    def id(self):
        return self.id

    def mentioned_in(self, message: Message):
        if message.mention_everyone:
            return True
        return any(user.id == self.id for user in message.mentions)
