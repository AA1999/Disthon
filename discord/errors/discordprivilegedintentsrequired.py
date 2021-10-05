from typing import Optional

from discord.errors.discordclientexception import DiscordClientException


class DiscordPrivilegedIntentsRequired(DiscordClientException):

    _shard_id: Optional[int]

    def __init__(self, shard_id: Optional[int]):
        self._shard_id = shard_id
        msg = (
            'Shard %s is requesting privileged intents that have not been explicitly enabled in the '
            'developer portal. It is recommended to go to https://discord.com/developers/applications/ '
            'and explicitly enable the privileged intents within your application\'s page. If this is not '
            'possible, then consider disabling the privileged intents instead.'
        )
        super().__init__(msg % shard_id)

    @property
    def shard_id(self):
        return self._shard_id
