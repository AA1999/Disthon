from __future__ import annotations

from .rawactivityassets import RawActivityAssets
from ..types.snowflake import Snowflake
from .activity import Activity


class PresenceAssets(dict[Snowflake, str]):
    largeimage: Snowflake
    largetext: str
    smallimage: Snowflake
    smalltext: str

    def __init__(self, activity: Activity, assets: RawActivityAssets):
        pass
