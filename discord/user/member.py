from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Any

from pydantic import validator

from .user import User
from ..asset import Asset
from ..types.image import Image
from ..types.snowflake import Snowflake


def validate_dt(val):
    if val is None:
        return val

    return datetime.fromisoformat(str(val))


class Member(User):
    nick: Optional[str] = None
    guild_avatar: Optional[Asset] = None
    roles: List[Snowflake]
    guild: Any
    joined_at: datetime
    premium_since: Optional[datetime] = None
    deaf: Optional[bool]
    mute: Optional[bool]
    pending: Optional[bool]
    permissions: Optional[str] = None
    communication_disabled_until: Optional[datetime] = None

    @validator("joined_at")
    def validate_joined_at(cls, val):
        return validate_dt(val)

    @validator("premium_since")
    def validate_premium_since(cls, val):
        return validate_dt(val)

    @validator("communication_disabled_until")
    def validate_communication_disabled_until(cls, val):
        return validate_dt(val)
