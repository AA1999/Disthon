from discord.errors.discordexception import DiscordException


class DiscordNoMoreItems(DiscordException):
    def __init__(self, message: str, code: int):
        super().__init__(message, code)

