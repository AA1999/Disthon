from __future__ import annotations

from ..types.snowflake import Snowflake
from .activity import Activity
from .rawactivityassets import RawActivityAssets


class PresenceAssets(dict[Snowflake, str]):
    largeimage: Snowflake
    largetext: str
    smallimage: Snowflake
    smalltext: str

    def __init__(self, activity: Activity, assets: RawActivityAssets):
        pass
