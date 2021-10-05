from typing import Dict

from discord.activity.rawactivityassets import RawPresenceAssets
from discord.types.snowflake import Snowflake
from discord.activity.activity import Activity

class PresenceAssets(Dict[Snowflake, str]):
    largeimage: Snowflake
    largetext: str
    smallimage: Snowflake
    smalltext: str
    
    def __init__(self, activity: Activity, assets: RawPresenceAssets):
        
        
    
    