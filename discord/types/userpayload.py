from typing import Optional, TypedDict

from discord.types.avatar import Avatar
from discord.types.banner import Banner
from pydantic.main import BaseModel

from enums.locale import Locale
from enums.userflags import UserFlags
from snowflake import Snowflake


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
    
