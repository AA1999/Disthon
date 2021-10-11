from discord.types.enums.locale import Locale
from typing import Optional

from discord.internal.cache import UserCache
from discord.types.enums.userflags import UserFlags
from discord.types.userpayload import UserPayload
from discord.user.baseuser import BaseUser


class ClientUser(BaseUser):
    __slots__ = ('_id', '_created_at', '_avatar', '_bot', '_username', '_discriminator', '_mention', '_cache',
                 '_banner', '_default_avatar', '_display_name', '_public_flags', '_cache', '_system', '_verified',
                 '_locale', '_two_factor_enabled', '_flags')
    _verified: bool
    _locale: Optional[Locale]
    _two_factor_enabled: bool
    _flags: UserFlags

    def __init__(self, cache: UserCache, payload: UserPayload):
        self._verified = payload['verified']
        self._two_factor_enabled = payload['two_factor_enabled']
        self._locale = payload['locale']
        self._flags = payload['flags']
        super().__init__(cache, payload)

    async def edit(self, *, username: str = None, avatar: bytes = None):
        pass

    def __repr__(self) -> str:
        return f'{self.username}#{self.discriminator} ({self.id})'

    @property
    def verified(self):
        return self._verified

    @property
    def locale(self):
        return self._locale

    @property
    def two_factor_enabled(self):
        return self._two_factor_enabled

    @property
    def flags(self):
        return self._flags
