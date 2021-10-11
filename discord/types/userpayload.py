from discord.types.enums.locale import Locale
from typing import TypedDict, Optional

from discord.types.enums.userflags import UserFlags
from discord.types.snowflake import Snowflake


class UserPayload(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]
    banner: Optional[str]
    bot: bool
    system: bool
    two_factor_enabled: bool
    local: str
    email: Optional[str]
    flags: UserFlags
    verified: bool
    locale: Locale
    
