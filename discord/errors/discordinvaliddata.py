from discord.errors.discordclientexception import DiscordClientException


class DiscordInvalidData(DiscordClientException):

    def __init__(self, message: str):
        super().__init__(message)
