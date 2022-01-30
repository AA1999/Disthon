from __future__ import annotations

from typing import Optional

from ..types.enums.locale import Locale
from ..types.enums.userflags import UserFlags
from ..types.userpayload import UserPayload
from ..user.baseuser import BaseUser


class ClientUser(BaseUser):
    async def edit(self, *, username: str = None, avatar: bytes = None):
        pass

    def __repr__(self) -> str:
        return f"{self.username}#{self.discriminator} ({self.id})"
