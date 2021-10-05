from discord.errors.discordexception import DiscordException


class DiscordClientException(DiscordException):
    def __init__(self, message: str):
        super().__init__(message)
