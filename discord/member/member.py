from __future__ import annotations

from discord.role.role import Role
from discord.user.user import User


class Member(User):
    top_role: Role
    roles: set[Role]
    