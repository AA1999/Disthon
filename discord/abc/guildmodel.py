from typing import List

from ..types.snowflake import Snowflake

from .objectmodel import ObjectModel

class GuildModel(ObjectModel):
    owner: bool = False
    owner_id: Snowflake
    members: List[dict]
    roles: List[dict]
    emojis: List[dict]
    stickers: List[dict]