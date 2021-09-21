from typing import Hashable
import unicodedata
import datetime
import copy

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

class Guild(Hashable):
    """Returns a discord Guild.
        
        
        Often referred to as a server, and is referred to as a server in the official Discord UI
        
        
        represents: x == y:
          Checks if two guilds are equal."""
    def __init__(self):
      "Guild Class"


    def _add_channel(self, channel: GuildChannel,/) -> None:
     self._channels[channel.id] = channel    






#properties
