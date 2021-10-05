from typing import TypedDict

from discord.types.snowflake import Snowflake


class RawPresenceAssets(TypedDict):
    largeimage: Snowflake
    largetext: str
    smallimage: Snowflake
    smalltext: str
