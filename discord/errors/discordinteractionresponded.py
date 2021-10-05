from discord.errors.discordclientexception import DiscordClientException


class DiscordInteractionResponded(DiscordClientException):

    _interaction: Interaction

    def __init__(self, interaction: Interaction):
        self._interaction = interaction
        super().__init__('This interaction has already been responded to before.')