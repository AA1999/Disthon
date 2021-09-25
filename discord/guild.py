from typing import (
  Hashable,
  Dict,
  NamedTuple,
  Optional,
  Snowflake
  )


__slots__(
    'region'
    'owner.id'
    'mfa.level'
    'name'
    'id'
    '_members'
    '_channels'
    '_vanity'
    '_banner'
)


class BanEntry(NamedTuple):
  user: User
  reason: Optional[str]


class GuildLimit(NamedTuple):
  filesize: int
  emoji: int
  channels: int
  roles: int
  categories: int
  bitrate: int
  stickers: int



class Guild(Hashable):
    """Returns a discord Guild.


        Often referred to as a server, and is referred to as a server in the official Discord UI


        represents: x == y:
          Checks if two guilds are equal."""
    def __init__(self, datas: GuildPayload):
      self._members: Dict[int, Member] = {}
      self._channels: Dict[int, GuildChannel] = {}




    def _add_channel(self, channel: GuildChannel,/) -> None:
     self._channels[channel.id] = channel


    def _delete_channel(self, channel: Snowflake) -> None:
      self._channels.pop(channel.id, None)

    def add_member(self, member: Member) -> None:
      self._members[member.id] = member

    def add_roles(self, role: Role) -> None:
      for p in self._roles.values:
        p.postion += not p.is_default()
        #checks if role is @everyone or not

      self._roles[role.id] = role






#properties
