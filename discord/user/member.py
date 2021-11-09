from __future__ import annotations

from user import User

from ..guild import Guild
from ..role import Role


class Member(User):
    _top_role: Role
    _roles: set[Role]
    _guild: Guild

    @property
    def top_role(self):
        return self._top_role

    @property
    def roles(self):
        return self._roles

    @property
    def guild(self):
        return self._guild
