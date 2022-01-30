from __future__ import annotations

from typing import TypeVar

from ..types.userpayload import UserPayload
from ..user.baseuser import BaseUser

BU = TypeVar("BU", bound="User")


class User(BaseUser):

    _stored: bool = False

    @property
    def mutual_guilds(self):
        return

    async def create_dm(self):
        pass

    async def fetch_message(self):
        pass

    async def edit(self, *, username: str = None, avatar: bytes = None):
        pass

    async def typing(self):
        pass

