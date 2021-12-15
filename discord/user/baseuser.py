from __future__ import annotations

from datetime import datetime
from typing import Optional

from ..abc.abstractuser import AbstractUser
from ..cache import LFUCache
from ..color import Color
from ..message import Message
from ..types.avatar import Avatar
from ..types.banner import Banner
from ..types.enums.defaultavatar import DefaultAvatar
from ..types.enums.userflags import UserFlags
from ..types.userpayload import UserPayload


class BaseUser(AbstractUser):
    class Config:
        arbitrary_types_allowed = True

    banner: Banner
    system: bool
    display_avatar: Avatar
    display_name: str
    public_flags: UserFlags

    async def create_dm(self):
        pass

    async def fetch_message(self):
        pass

    async def send(
        self,
        content: str = None,
        *,
        tts=None,
        embeds: list[Message] = None,
        files=None,
        stickers=None,
        delete_after=None,
        nonce=None,
        allowed_mentions: bool = None,
        reference=None,
        mention_author: bool = None,
        view=None,
        components=None
    ):
        pass

    async def edit(self, *, username: str = None, avatar: bytes = None):
        pass

    async def typing(self):
        pass

    @property
    def default_avatar(self):
        return self.avatar._from_default_avatar(
            self._cache, int(self.discriminator) % len(DefaultAvatar)
        )

    @property
    def color(self):
        return Color.default()

    @property
    def colour(self):
        return self.color

    def to_json(self):
        return {
            "username": self.username,
            "discriminator": self.discriminator,
            "tag": self.tag,
            "id": self.id,
            "created_at": self.created_at,
            "avatar": self.avatar,
            "default_avatar": self.default_avatar,
            "display_avatar": self.display_avatar,
            "bot": self.bot,
            "system": self.system,
            "public_flags": self.public_flags,
            "display_name": self.display_name,
            "banner": self.banner,
        }
