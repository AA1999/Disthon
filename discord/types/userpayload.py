from __future__ import annotations

from typing import Optional, TypedDict

from .enums.locale import Locale
from .enums.userflags import UserFlags
from pydantic.main import BaseModel
from .snowflake import Snowflake

from ..types.avatar import Avatar
from ..types.banner import Banner


class UserPayload(BaseModel):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Avatar
    banner: Banner
    bot: bool
    system: bool
    two_factor_enabled: bool
    local: str
    email: Optional[str]
    flags: UserFlags
    verified: bool
    locale: Locale
