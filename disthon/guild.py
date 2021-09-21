from typing import Hashable
import unicodedata
import datetime
import copy

class Guild(Hashable):
    """Returns a discord Guild.
        
        
        Often referred to as a server, and is referred to as a server in the official Discord UI
        
        
        represents: x == y:
          Checks if two guilds are equal."""
    

__slots__(
    'region'
    'owner_id'
    'mfa.level'
    'name'
    'id'
    '_members'
    '_channels'
    '_vanity'
    '_banner'
)




#properties
def __init__(self):
    "Guild Class"


def _add.channel(self, channel: GuildChannel,/) -> None:
self._channels[channel.id] = channel