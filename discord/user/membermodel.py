from typing import Any, Optional, List

from ..types.snowflake import Snowflake

from ..asset import Asset

from .usermodel import UserModel

from datetime import datetime

class MemberModel(UserModel):
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