from __future__ import annotations

from discord.activity.rawactivityassets import RawActivityAssets
from discord.types.snowflake import Snowflake
from discord.activity.activity import Activity


class PresenceAssets(dict[Snowflake, str]):
    largeimage: Snowflake
    largetext: str
    smallimage: Snowflake
    smalltext: str

    def __init__(self, activity: Activity, assets: RawActivityAssets):
        pass
