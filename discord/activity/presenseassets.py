from __future__ import annotations
from typing import TYPE_CHECKING

from ..types.snowflake import Snowflake
if TYPE_CHECKING:
    from .activity import Activity
    from .rawactivityassets import RawActivityAssets


class PresenceAssets(dict[Snowflake, str]):
    largeimage: Snowflake
    largetext: str
    smallimage: Snowflake
    smalltext: str

    def __init__(self, activity: Activity, assets: RawActivityAssets):
        pass
