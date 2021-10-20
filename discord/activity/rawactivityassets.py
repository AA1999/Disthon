from typing import TypedDict

from ..types.snowflake import Snowflake


class RawActivityAssets(TypedDict):
    largeimage: Snowflake
    largetext: str
    smallimage: Snowflake
    smalltext: str
