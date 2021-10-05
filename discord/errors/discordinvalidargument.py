from discord.errors.discordclientexception import DiscordClientException


class DiscordInvalidArgument(DiscordClientException):

    def __init__(self, message: str):
        super().__init__(message)
