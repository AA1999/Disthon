from __future__ import annotations

from typing import Optional, TypedDict

from pydantic.main import BaseModel

from ..types.avatar import Avatar
from ..types.banner import Banner
from .enums.locale import Locale
from .enums.userflags import UserFlags
from .snowflake import Snowflake


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
