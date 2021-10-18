from __future__ import annotations

from discord.guild.guild import Guild
from discord.role.role import Role
from discord.user.user import User


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

