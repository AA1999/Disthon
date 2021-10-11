from __future__ import annotations

from datetime import datetime
from discord.abc.abstractuser import AbstractUser
from discord.color.color import Color
from discord.internal.cache import GuildCache, UserCache
from discord.message.message import Message
from discord.types.avatar import Avatar
from discord.types.banner import Banner
from discord.types.enums.defaultavatar import DefaultAvatar
from discord.types.enums.userflags import UserFlags
from discord.types.userpayload import UserPayload


class BaseUser(AbstractUser):
    __slots__ = ('_id', '_created_at', '_avatar', '_bot', '_username', '_discriminator', '_mention', '_cache',
                 '_banner', '_default_avatar', '_display_name', '_public_flags', '_cache', '_guilds', '_system')
    _banner: Banner
    _system: bool
    _default_avatar: Avatar
    _display_avatar: Avatar
    _display_name: str
    _public_flags: UserFlags
    _cache: UserCache
    _guilds: GuildCache

    def __init__(self, cache: UserCache, guilds: GuildCache, payload: UserPayload):
        self._cache = cache
        self._guilds = guilds
        self._id = payload['id']
        self._created_at = datetime.utcnow()
        self._avatar = Avatar(payload['avatar']) or None
        self._username = payload['username']
        self._discriminator = payload['discriminator']
        self._banner = Banner(payload['banner']) or None
        self._public_flags = payload['flags']
        self._system = payload['system'] or False
        self._bot = payload['bot'] or False
    
    @classmethod
    def _from_user(cls, user: BaseUser) -> BaseUser:
        self = cls.__new__(cls)
        self._avatar = user.avatar or user.default_avatar
        self._banner = user.banner
        self._cache = user._cache
        self._created_at = user.created_at
        self._discriminator = user.discriminator
        self._display_name = user.display_name
        self._id = user.id
        self._public_flags = user.public_flags
        self._system = user.system
        self._username = user.username
        return self

    async def create_dm(self):
        pass

    async def fetch_message(self):
        pass

    async def send(self, content: str = None, *, tts=None, embeds: list[Message] = None, files=None,
                   stickers=None, delete_after=None, nonce = None, allowed_mentions: bool = None, reference=None,
                   mention_author: bool = None, view=None, components=None):
        pass
    
    async def edit(self, *, username: str = None, avatar: bytes = None):
        pass

    async def typing(self):
        pass

    @property
    def banner(self):
        return self._banner

    @property
    def system(self):
        return self._system

    @property
    def default_avatar(self):
        return self.avatar._from_default_avatar(self._cache, int(self.discriminator) % len(DefaultAvatar))

    @property
    def display_avatar(self):
        return self._avatar

    @property
    def display_name(self):
        return self._display_name

    @property
    def public_flags(self):
        return self._public_flags
    
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
            "banner": self.banner
        }
