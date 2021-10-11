from typing import TypeVar

from discord.internal.cache import GuildCache, UserCache
from discord.types.userpayload import UserPayload
from discord.user.baseuser import BaseUser

BU = TypeVar('BU', bound='User')

class User(BaseUser):
    
    __slots__ = ('_stored',)
    
    
    _stored: bool
    
    def __init__(self, cache: UserCache, payload: UserPayload):
        super().__init__(cache, payload)
        self._stored = False
    
    @classmethod
    def _from_user(cls, user: BU) -> BU: 
        self = super()._from_user(user)
        self._stored = False
        return self
        
    
    def __repr__(self) -> str:
        return f'{self.tag} ({self.id})'
    
    
    def __str__(self) -> str:
        return self.tag
    
        
    def __del__(self):
        if self._stored:
            del self._cache[self.id]
        else:
            raise KeyError
    
    @property
    def dm_channel(self):
        return self._cache.get_user_dms(self)
    
    @property
    def mutual_guilds(self):
        
    
